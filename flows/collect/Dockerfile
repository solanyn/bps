FROM ghcr.io/astral-sh/uv:0.6.5
WORKDIR /app
COPY . .
RUN uv venv && uv pip install -r requirements.txt
ENV PATH="/app/.venv/bin:$PATH"
CMD ["uv", "run", "python", "collect.py"]
