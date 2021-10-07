FROM apache/superset
USER root
COPY superset_start.sh .
COPY source.yaml .
COPY dashboard.yaml .
RUN pip install psycopg2-binary && \
    chmod +x superset_start.sh
USER superset

ENTRYPOINT ["./superset_start.sh"]