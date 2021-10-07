FROM timescale/timescaledb:latest-pg12
ENV POSTGRES_USER docker
ENV POSTGRES_PASSWORD password
ENV POSTGRES_DB real_estate
COPY scripts/* /docker-entrypoint-initdb.d/
COPY data/real_estate_hun.csv .