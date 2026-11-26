cat > scripts/k8s-up.sh <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

minikube status >/dev/null 2>&1 || minikube start --driver=docker --memory=2048

eval "$(minikube docker-env)"
docker build -t gerenciador-financeiro:latest .

G=monitoring/grafana
cm() { kubectl create configmap "$@" --dry-run=client -o yaml | kubectl apply -f -; }
cm grafana-datasources         --from-file="$G/provisioning/datasources"
cm grafana-dashboards-provider --from-file="$G/provisioning/dashboards"
cm grafana-alerting            --from-file="$G/provisioning/alerting"
cm grafana-dashboard-json      --from-file="$G/dashboards"
kubectl create secret generic grafana-secret \
  --from-literal=GF_SECURITY_ADMIN_PASSWORD="${GRAFANA_PASSWORD:-admin}" \
  --from-literal=GF_SMTP_ENABLED=true \
  --from-literal=GF_SMTP_HOST="${SMTP_HOST:-smtp.gmail.com:587}" \
  --from-literal=GF_SMTP_USER="${SMTP_USER:-}" \
  --from-literal=GF_SMTP_PASSWORD="${SMTP_PASSWORD:-}" \
  --from-literal=GF_SMTP_FROM_ADDRESS="${SMTP_USER:-grafana@example.com}" \
  --from-literal=ALERT_EMAIL_TO="${ALERT_EMAIL_TO:-alerta@example.com}" \
  --dry-run=client -o yaml | kubectl apply -f -

kubectl delete job financeiro-migrate --ignore-not-found
kubectl apply -f k8s/
kubectl rollout status deployment/mariadb --timeout=180s
kubectl wait --for=condition=complete job/financeiro-migrate --timeout=180s
for d in financeiro-app prometheus grafana; do
  kubectl rollout status deployment/$d --timeout=180s
done
kubectl get pods,svc
echo
echo "Acesso (Codespaces):"
echo "  kubectl port-forward svc/financeiro-service 8080:80"
echo "  kubectl port-forward svc/grafana 3000:3000"
echo "  kubectl port-forward svc/prometheus 9090:9090"
EOF
chmod +x scripts/k8s-up.sh