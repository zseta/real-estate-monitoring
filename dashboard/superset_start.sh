#!/bin/bash 
superset fab create-admin \
            --username admin \
            --firstname Superset \
            --lastname Admin \
            --email admin@email.com \
            --password admin      
superset db upgrade
superset init
superset import_datasources -p source.yaml
superset import_dashboards -p dashboard.yaml
echo '****************Superset is starting up****************'
echo '****************Go to http://0.0.0.0:8088/ to login****************'
superset run -p 8088 --host 0.0.0.0