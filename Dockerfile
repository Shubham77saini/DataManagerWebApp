FROM public.ecr.aws/koireader/base-images:builder.ubuntu22.python39 as poetry

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN poetry install --without dev --no-root && \
    rm -rf $POETRY_CACHE_DIR


FROM public.ecr.aws/koireader/base-images:release.ubuntu22.python39 as release

WORKDIR /app

ENV VENV_PATH=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

# RUN apt-get -y update \
#   && apt-get clean \
#   && rm -rf /var/lib/apt/lists/*

COPY --chown=koireader:koireader --from=poetry $VENV_PATH $VENV_PATH
COPY --chown=koireader:koireader ./src ./src
COPY --chown=koireader:koireader ./.streamlit ./.streamlit
COPY --chown=koireader:koireader main.py pyproject.toml poetry.lock ./
# COPY --chown=koireader:koireader --from=poetry /app/static ./static

USER root

RUN chown -R koireader:koireader /app

USER koireader

EXPOSE 8501

ENTRYPOINT [ "/tini", "--" ]
CMD [ "streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0" ]
