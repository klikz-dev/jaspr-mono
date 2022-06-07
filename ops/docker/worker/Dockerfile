FROM jaspr/base-server

COPY ./scripts/start-worker /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start
RUN chown django /start

USER django

WORKDIR /app

ENTRYPOINT ["/usr/bin/dumb-init", "--"]
CMD /start
