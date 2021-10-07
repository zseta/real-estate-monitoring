#!/bin/bash
set -e

psql -v --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    \copy es_real_estate FROM 'real_estate_hun1.csv' CSV HEADER;
    \copy es_real_estate FROM 'real_estate_hun2.csv' CSV HEADER;
EOSQL
