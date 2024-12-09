```bash
kubectl create namespace diplom
sudo helm install  diplom-hadoop $(./calc_resources.sh 50) \
  --set persistence.nameNode.enabled=true \
  --set persistence.nameNode.storageClass=standard \
  --set persistence.dataNode.enabled=true \
  --set persistence.dataNode.storageClass=standard \
  stable/hadoop
```