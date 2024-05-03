#!/usr/bin/env python3

import cv2

# ========================================
# Названия (должны быть английскими буквами)
# ========================================
# Заголовок окна
window_name = 'Camera capture'
# Название ползунка
trackbar_name = 'Brightness'
# ========================================

# Получаем объект веб-камеры
video_capture = cv2.VideoCapture(0)

# Формат для чтения
fourcc_for_read = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
video_capture.set(cv2.CAP_PROP_FOURCC, fourcc_for_read)

# Получаем параметры камеры
width = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(video_capture.get(cv2.CAP_PROP_FPS))

# Формат для записи
fourcc_for_write = cv2.VideoWriter_fourcc(*'XVID')
# Создаём объект для записи видео
video_writer = cv2.VideoWriter('./output/result.avi', fourcc_for_write, fps, (width, height))

# Задаём имя окну
cv2.namedWindow(window_name)

# Создаём ползунок
cv2.createTrackbar(trackbar_name, window_name, 50, 100, lambda x: None)

return_code = 0
# Будем захватывать изображение, пока пользователь не выйдет
while video_capture.isOpened():
    # Захватываем кадр
    is_frame_captured, frame = video_capture.read()

    if is_frame_captured:
        # Записываем кадр в видео
        video_writer.write(frame)
        cv2.imshow(window_name, frame)
    else:
        print("Не удалось захватить кадр!")
        return_code = 1
        break

    # Устанавливаем яркость согласно положению ползунка
    video_capture.set(10, cv2.getTrackbarPos(trackbar_name, window_name))  # brightness

    # Обработка нажатия клавиш
    key_pressed = cv2.waitKey(1)
    # Если нажато Q, ESC или SPACE - выходим из цикла
    if (key_pressed == ord('q')) or (key_pressed % 256 == 27) or (key_pressed % 256 == 32):
        break

# Освобождение памяти
video_capture.release()
video_writer.release()
# Закрытие окна
cv2.destroyAllWindows()

exit(return_code)
