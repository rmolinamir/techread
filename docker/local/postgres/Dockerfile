FROM postgres:15-bullseye
  # Copy the maintenance scripts into the container.
  COPY ./docker/local/postgres/maintenance /usr/local/bin/maintenance

  # Make sure the scripts in the maintenance directory are executable.
  RUN chmod +x /usr/local/bin/maintenance/*

  # Move the scripts out of the maintenance directory.
  RUN mv /usr/local/bin/maintenance/* /usr/local/bin/ \
    && rmdir /usr/local/bin/maintenance
