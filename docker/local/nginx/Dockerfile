FROM nginx:1.23.3-alpine 
    # Delete the default nginx.conf.
    RUN rm /etc/nginx/conf.d/default.conf

    # Copying the custom nginx.conf.
    COPY ./docker/local/nginx/default.conf /etc/nginx/conf.d/default.conf
