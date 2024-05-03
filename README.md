# opencv-camera-capture

## 1. Description

Simple script to record video from camera in avi file

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
docker-compose exec -it app bash -c './main.py --image ./input/1.png --langs en,ru --gpu 1'
docker-compose down
```

## 5. Example

```bash
./test.sh
```

When image pops up, do not close it - it will cause console to freeze.
You just need to press any key to properly close the image. 
