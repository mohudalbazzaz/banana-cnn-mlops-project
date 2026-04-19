# STAGE 1 - BUILDER
FROM python:3.13-slim as builder
WORKDIR /app

RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"

RUN pip install --no-cache-dir streamlit requests dotenv

# STAGE 2 - RUNTIME
FROM python:3.13-slim
WORKDIR /app

COPY --from=builder /venv /venv
ENV PATH="/venv/bin:$PATH"

COPY src/frontend/streamlit_app.py .

# streamlit blocks requests when its run behind a reverse proxy
# (using azure application gateway) so last flags prevent that
CMD ["streamlit", "run", "streamlit_app.py", \
     "--server.address=0.0.0.0", \
     "--server.port=8501", \
     "--server.enableCORS=false", \
     "--server.enableXsrfProtection=false", \
     "--server.enableWebsocketCompression=false"]