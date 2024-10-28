from PIL import Image
import io

def image_to_bytes(image_path):
    with Image.open(image_path) as img:
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')
        return img_byte_arr.getvalue()

def bytes_to_image(image_bytes):
    img_byte_arr = io.BytesIO(image_bytes)
    return Image.open(img_byte_arr)

def compare_images(img1: bytes, img2: bytes) -> float:    
    img1 = bytes_to_image(img1)
    img2 = bytes_to_image(img2)
    
    width_1, height_1 = img1.size
    width_2, height_2 = img2.size
    
    width, height = max(width_1,width_2), max(height_1, height_2)

    img1_pixels = img1.load()  
    img2_pixels = img2.load()  
    
    total_pixels = width * height
    matching_pixels = 0

    for x in range(width):
        for y in range(height):
            try:
                if img1_pixels[x, y] == img2_pixels[x, y]:
                    matching_pixels += 1
            except IndexError:
                pass
            
    similarity_percentage = (matching_pixels / total_pixels) * 100
    return similarity_percentage