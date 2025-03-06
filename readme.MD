Para implementar esta configuración en Kubernetes:
Asegúrate de tener un cluster de Kubernetes funcionando y kubectl configurado.
Crea un directorio k8s y coloca todos los archivos YAML anteriores en él.

2. Construir la imagen Docker con el módulo


docker build -t orquidea/odoo-uber:17.0 .

# Subir la imagen a tu registro
docker push tu-registro/odoo-uber:17.0

3. Desplegar en Kubernetes


# Crear namespace
kubectl create namespace odoo

# Aplicar los manifiestos en orden
kubectl apply -f k8s/odoo-configmap.yaml -n odoo
kubectl apply -f k8s/persistent-volume-claims.yaml -n odoo
kubectl apply -f k8s/postgres-deployment.yaml -n odoo
kubectl apply -f k8s/odoo-deployment.yaml -n odoo
kubectl apply -f k8s/services.yaml -n odoo

Verificar el despliegue

# Verificar pods
kubectl get pods -n odoo

# Verificar servicios
kubectl get svc -n odoo

# Verificar PVCs
kubectl get pvc -n odoo


Acceder a Odoo
kubectl get svc odoo -n odoo


Verificar logs

# Logs de Odoo
kubectl logs -f deployment/odoo -n odoo

# Logs de PostgreSQL
kubectl logs -f deployment/odoo-db -n odoo

Para eliminar todo
kubectl delete namespace odoo



uber_delivery_integration/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   ├── delivery_carrier.py
│   ├── res_config_settings.py
│   ├── sale_order.py
│   ├── stock_picking.py
│   └── uber_delivery_request.py
├── security/
│   ├── ir.model.access.csv
│   └── security_rules.xml
├── data/
│   └── uber_delivery_data.xml
├── views/
│   ├── delivery_carrier_views.xml
│   ├── res_config_settings_views.xml
│   ├── sale_order_views.xml
│   ├── stock_picking_views.xml
│   └── uber_delivery_request_views.xml
└── static/
    └── description/
        └── icon.png