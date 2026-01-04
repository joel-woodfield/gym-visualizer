# --- Stage 1: Build the Frontend ---
FROM node:22-slim AS build-frontend
WORKDIR /app

COPY frontend .

RUN npm install
RUN npm run build

# --- Stage 2: Final Python Image ---
FROM python:3.13-slim
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libgl1 \
    libglx0 \
    libegl1 \
    libosmesa6 \
    freeglut3-dev \
    libasound2t64 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

COPY --from=build-frontend /app/dist frontend/dist

COPY backend backend

WORKDIR /app/backend
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8765
ENV PYOPENGL_PLATFORM=osmesa
ENV SDL_VIDEODRIVER=dummy

CMD ["python", "src/server.py"]
