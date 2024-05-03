# opencv-camera-capture

## 1. Description

Simple script to record video from camera in avi file.

## 2. Requirements

- Windows 10/11 + WSL (Docker Compose configuration set up for it);
- Docker Desktop;

## 3. Build

```bash
docker-compose build
```

## 4. Usage

```bash
docker-compose up -d
docker-compose exec -it app bash -c './main.py'
docker-compose down
```

- The camera output will be displayed and recording will start immediately;
- The saved file will be `./output/result.avi`;
- You can adjust brightness with trackbar.
