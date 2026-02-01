-- docker/postgres/initdb/init.sql
CREATE ROLE IF NOT EXISTS POSTGRES_USER WITH LOGIN PASSWORD POSTGRES_PASSWORD;
ALTER ROLE POSTGRES_USER WITH SUPERUSER; -- ou ajuste permissões conforme necessário
CREATE DATABASE IF NOT EXISTS queijaria OWNER pedro;
-- Se você tiver DDL, inclua aqui ou em arquivos separados
