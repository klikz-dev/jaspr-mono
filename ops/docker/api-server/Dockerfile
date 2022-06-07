FROM jaspr/base-server:latest

# Setup Startup Script
COPY ./scripts/start-api-server /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start
RUN chown django /start

USER django

WORKDIR /app

EXPOSE 5000

ENTRYPOINT ["/usr/bin/dumb-init", "--"]
CMD /start
