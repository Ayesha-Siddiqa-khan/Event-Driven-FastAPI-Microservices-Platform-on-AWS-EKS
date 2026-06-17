# 07 - ElastiCache Redis

Redis is used for session storage and order caching.

## Redis name

```text
edfp-dev-redis-main
```

## Which services use Redis?

| Service | Redis usage |
|---|---|
| auth-service | fake session token storage |
| order-service | order cache |

## Recommended beginner settings

```text
engine: Redis / Valkey-compatible Redis option depending on your AWS choice
subnets: private app or private data subnets
public access: no
security group: edfp-dev-sg-redis
replicas: 0 or 1 for dev
```

## Security group rule

Allow inbound only from EKS app security group:

```text
source: edfp-dev-sg-eks-apps
port: 6379
protocol: TCP
```

## Secret names

```text
/edfp/dev/auth-service/redis-url
/edfp/dev/order-service/redis-url
```

Example value:

```text
redis://<redis-endpoint>:6379/0
```

## How the app uses Redis

Auth service:

```text
session:<token> -> user_id
```

Order service:

```text
order:<order_id> -> JSON order data
```

## Readiness checks

The services using Redis should fail readiness if Redis is unavailable:

```text
/ready checks Redis PING
```

This teaches you the difference between liveness and readiness.

## Verification checklist

- Redis endpoint exists
- Redis is private
- only EKS workloads can access Redis
- auth-service `/ready` checks Redis
- order-service `/ready` checks Redis
- Redis failure causes readiness failure but not immediate pod crash
