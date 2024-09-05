DC_YAML = """version: "3.8"
services:
  postgresql:
    image: postgres:latest
    restart: always
    volumes:
      - db-data:/var/lib/postgresql/data
    environment:
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_DB: ${POSTGRES_DB}
    ports:
      - "5432:5432"
volumes:
  db-data:"""