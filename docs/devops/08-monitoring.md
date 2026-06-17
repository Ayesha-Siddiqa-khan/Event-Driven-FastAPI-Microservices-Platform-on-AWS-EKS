# Monitoring

Install kube-prometheus-stack for Prometheus and Grafana:

```bash
helm upgrade --install monitoring prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --create-namespace \
  -f k8s/monitoring/kube-prometheus-stack-values.yaml
```

Each FastAPI service exposes `/metrics`.

Recommended next steps:

- Add ServiceMonitor resources for each service
- Add dashboards for request latency, error rate, queue depth, and worker processing failures
- Add alerts for failed readiness checks and DLQ growth
