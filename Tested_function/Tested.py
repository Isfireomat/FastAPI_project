from PIL import Image
import io

# Функция для преобразования изображения в байты
def image_to_bytes(image_path):
    with Image.open(image_path) as img:
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')
        return img_byte_arr.getvalue()

# Функция для преобразования байтов обратно в изображение
def bytes_to_image(image_bytes):
    img_byte_arr = io.BytesIO(image_bytes)
    return Image.open(img_byte_arr)

# Функция для сравнения двух изображений
def compare_images(img1, img2):
    # Убедимся, что изображения одного размера
    
    width, height = img1.size
    img1_pixels = img1.load()  # Получаем пиксели первого изображения
    img2_pixels = img2.load()  # Получаем пиксели второго изображения
    
    total_pixels = width * height
    matching_pixels = 0

    # Сравниваем каждый пиксель
    for x in range(width):
        for y in range(height):
            try:
                if img1_pixels[x, y] == img2_pixels[x, y]:
                    matching_pixels += 1
            except: pass
            
    # Рассчитываем процент схожести
    similarity_percentage = (matching_pixels / total_pixels) * 100
    return similarity_percentage

image_path1 = 'Tested_function\\Test1.jpg'  # Путь к первому изображению
image_path2 = 'Tested_function\\Test4.jpg'  # Путь ко второму изображению

image_bytes1 = image_to_bytes(image_path1)
image_bytes2 = image_to_bytes(image_path2)

image1 = bytes_to_image(image_bytes1)
image2 = bytes_to_image(image_bytes2)

similarity = compare_images(image1, image2)
print(f'Схожесть изображений: {similarity:.2f}%')
