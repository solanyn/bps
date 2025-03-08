FROM ghcr.io/astral-sh/uv:debian
WORKDIR /app
COPY . .
RUN curl https://sh.rustup.rs -sSf | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"

RUN uv python install \
    && uv venv \
    && uv pip install -r requirements.txt
ENV PATH="/app/.venv/bin:${PATH}"
CMD ["uv", "run", "python", "collect.py"]
