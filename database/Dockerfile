FROM mysql:8.0

# ENV MYSQL_DATABASE=google_play_store
# ENV MYSQL_ROOT_PASSWORD=rootpassword

COPY ./init.sql /docker-entrypoint-initdb.d/

EXPOSE 3306