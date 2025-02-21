FROM postgres:15-alpine

# Copy initialization scripts
COPY init.sql /docker-entrypoint-initdb.d/

# Add any additional PostgreSQL configurations if needed
# COPY postgresql.conf /etc/postgresql/postgresql.conf

# The official postgres image already includes necessary configurations and entrypoint scripts
# Environment variables POSTGRES_USER, POSTGRES_PASSWORD, and POSTGRES_DB will be set via docker-compose
