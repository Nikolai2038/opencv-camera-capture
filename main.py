#!/usr/bin/env python3

import argparse
import easyocr
import cv2
import torch

# Настройка аргументов скрипта
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Путь к изображению")
ap.add_argument("-l", "--langs", type=str, default="en", help="Список языков (сокращения), указанных через запятую (например: en,ru)")
ap.add_argument("-g", "--gpu", type=bool, default=False, help="Использовать ли GPU (иначе - будет использоваться CPU)")
args = vars(ap.parse_args())

# Для исправления "CUDNN_STATUS_NOT_SUPPORTED" (при "paragraph=True")
torch.backends.cudnn.enabled = False

# Получаем список языков
langs = args["langs"].split(",")
print("[INFO] Будет произведено распознавание следующих языков: {}".format(langs))

# Загрузка изображения
image = cv2.imread(args["image"])

print("[INFO] Распознавание...")
# Применение OCR - Optical Character Recognition
reader = easyocr.Reader(langs, gpu=args["gpu"])
results = reader.readtext(image, detail=1, paragraph=False)
print("[INFO] Распознавание успешно!")

# Весь распознанный текст одной строкой
all_text = ""

# loop over the results
for (bbox, text, prob) in results:
    all_text += text + " "

    # Пишем в лог распознанный текст, и его вероятность
    print("[INFO] {:.4f}: {}".format(prob, text))

    # Получаем координаты углов прямоугольника с распознанным текстом
    (top_left, top_right, bottom_right, bottom_left) = bbox
    top_left = (int(top_left[0]), int(top_left[1]))
    top_right = (int(top_right[0]), int(top_right[1]))
    bottom_right = (int(bottom_right[0]), int(bottom_right[1]))
    bottom_left = (int(bottom_left[0]), int(bottom_left[1]))

    # Цвет выделения и текста
    color = (255, 0, 255)

    # Толщина выделения и текста
    thickness = 1

    # Рисуем прямоугольник вокруг распознанного текста
    cv2.rectangle(image, top_left, bottom_right, color, thickness)

    # Рисуем сам текст
    cv2.putText(image, text, (top_left[0], top_left[1] - 10), cv2.FONT_HERSHEY_COMPLEX, 0.5, color, thickness)

print("[INFO] Распознанный текст целиком: " + all_text)

# show the output image
cv2.imshow("Image", image)
cv2.waitKey(0)
