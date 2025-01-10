from io import BytesIO

import requests
from PIL import Image

# Ссылка на изображение из датасета
image_url = "https://v5.airtableusercontent.com/v1/15/15/1677362400000/8XYHyC6BhcQlWERUddmqrA/JZOkhAQzNtgvDZ8hseUzcdYEmiNjyU45p1RqJsh5UNa2VTS3IiFzsP5G2ny0bC2s6PfcGuqSvExO1iop9lLICF6cvU2Atw5YpyI2cjVBaHRRQIsQYteV7johQrYiA75fT3xIgvKzQlomWmjDQoCQfQ/5wAawPq-9QC8UJDRwfWM3UvsM1bddJuFOqCFc6uBFlM"

# Загрузить изображение
response = requests.get(image_url)

if response.status_code == 200:
    # Чтение изображения в байтовый поток
    img = Image.open(BytesIO(response.content))

    # Сохранить изображение в файл
    img.save("downloaded_image.jpg")

    print("Изображение успешно загружено и сохранено как 'downloaded_image.jpg'.")
else:
    print(f"Не удалось загрузить изображение. Код состояния: {response.status_code}")
