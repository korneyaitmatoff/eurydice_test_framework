DATASOURCE_YAML = """apiVersion: 1

datasources:
  - name: tests_runs
    uuid: {project}_ds
    type: postgres
    url: postgres:5432
    database: {project}_database
    user: {login}
    secureJsonData:
      password: {password}
    isDefault: true
    jsonData:
      sslmode: disable"""
