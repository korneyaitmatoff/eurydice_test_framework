DASHBOARD_YAML = """apiVersion: 1

providers:
  - name: '{project}_dashboard'
    orgId: 1
    folder: ''
    type: file
    disableDeletion: false
    updateIntervalSeconds: 10
    options:
      path: /var/lib/grafana/dashboards"""