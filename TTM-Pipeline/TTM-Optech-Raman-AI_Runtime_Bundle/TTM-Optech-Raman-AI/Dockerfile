# Minimal CPU image for Optech Raman AI pipeline
FROM python:3.12-slim

# System deps (parquet/native libs often need build tools)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    MPLBACKEND=Agg

WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy project
COPY . /app

# Default command prints help; override with `docker run ... python -m raman_ai.cli ...`
CMD ["python", "-m", "raman_ai.cli", "--help"]
