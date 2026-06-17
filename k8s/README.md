# Kubernetes Manifests

This folder contains cluster-level resources that are not owned by a single app chart:

- namespaces for dev, staging, and prod
- External Secrets Operator setup notes
- KEDA setup notes
- ingress controller notes
- monitoring installation notes

Application workloads are deployed through Helm charts in `helm/`.
