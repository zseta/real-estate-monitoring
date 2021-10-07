#!/bin/bash
set -e

psql -v --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    \copy es_real_estate FROM 'real_estate_hun.csv' CSV HEADER;
EOSQL
