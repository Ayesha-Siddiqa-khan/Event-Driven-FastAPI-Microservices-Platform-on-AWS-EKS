# Monitoring

Install Prometheus and Grafana with kube-prometheus-stack:

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm upgrade --install monitoring prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --create-namespace \
  -f k8s/monitoring/kube-prometheus-stack-values.yaml
```

Each FastAPI service exposes `/metrics`. Add `ServiceMonitor` objects after standardizing service labels across charts, or configure Prometheus additional scrape jobs for the service DNS names.
