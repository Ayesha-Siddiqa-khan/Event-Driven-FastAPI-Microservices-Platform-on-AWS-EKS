# KEDA Autoscaling

The notification worker scales from SQS queue depth.

The Helm chart creates:

- `TriggerAuthentication`
- `ScaledObject`

Dev default:

- min replicas: 1
- max replicas: 3

Staging default:

- max replicas: 5

Prod default:

- max replicas: 10

KEDA needs IAM permission to read queue attributes. Terraform creates a KEDA IRSA role for that purpose.

SQS permissions are split by workload:

- `order-service`: can send to the order events queue
- `payment-service`: can send to the notification events queue
- `notification-worker`: can receive, change visibility, and delete from the notification events queue
- `keda-operator`: can read queue attributes for scaling

These permissions are assigned with IAM roles for service accounts. No AWS keys are stored in pods.
