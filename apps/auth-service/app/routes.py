import logging
import secrets
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.metrics import USER_LOGIN_FAILURES, USER_LOGINS, USER_LOOKUPS, USER_REGISTRATIONS
from app.models import User
from app.redis_client import RedisError, get_redis
from app.schemas import LoginRequest, LoginResponse, RegisterRequest, UserResponse
from app.security import hash_password, verify_password

logger = logging.getLogger(__name__)
router = APIRouter()

DbSession = Annotated[Session, Depends(get_db)]
RedisClient = Annotated[Any, Depends(get_redis)]


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(payload: RegisterRequest, db: DbSession) -> User:
    """Create a user with a hashed password."""
    email = str(payload.email).lower()

    try:
        existing = db.query(User).filter(User.email == email).first()
        if existing:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")

        user = User(email=email, password_hash=hash_password(payload.password))
        db.add(user)
        db.commit()
        db.refresh(user)
    except HTTPException:
        raise
    except IntegrityError as exc:
        db.rollback()
        logger.info("duplicate_registration_attempt", extra={"email": email})
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered") from exc
    except SQLAlchemyError as exc:
        db.rollback()
        logger.exception("registration_database_error", extra={"email": email})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not register user",
        ) from exc

    USER_REGISTRATIONS.inc()
    logger.info("user_registered", extra={"user_id": user.id})
    return user


@router.post("/login", response_model=LoginResponse)
def login(payload: LoginRequest, db: DbSession, redis_client: RedisClient) -> LoginResponse:
    """Validate credentials and create a fake Redis-backed session."""
    email = str(payload.email).lower()

    try:
        user = db.query(User).filter(User.email == email).first()
    except SQLAlchemyError as exc:
        logger.exception("login_database_error", extra={"email": email})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not log in",
        ) from exc

    if not user or not verify_password(payload.password, user.password_hash):
        USER_LOGIN_FAILURES.inc()
        logger.info("login_failed", extra={"email": email})
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = secrets.token_urlsafe(32)
    try:
        redis_client.setex(f"session:{token}", settings.session_ttl_seconds, str(user.id))
    except RedisError as exc:
        logger.exception("session_store_error", extra={"user_id": user.id})
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Session storage unavailable",
        ) from exc

    USER_LOGINS.inc()
    logger.info("user_logged_in", extra={"user_id": user.id})
    return LoginResponse(token=token, user_id=user.id)


@router.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: DbSession) -> User:
    """Return public user information by id."""
    USER_LOOKUPS.inc()
    try:
        user = db.get(User, user_id)
    except SQLAlchemyError as exc:
        logger.exception("user_lookup_database_error", extra={"user_id": user_id})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not retrieve user",
        ) from exc

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user
