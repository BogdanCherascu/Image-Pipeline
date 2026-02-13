import os
import time
from celery import Celery
from PIL import Image, ImageFilter

celery_app = Celery(
    "image_tasks",
    broker="redis://redis_mq:6379/0",
    backend="redis://redis_mq:6379/0"
)


@celery_app.task(name="process_image")
def process_image_task(filename: str):
    print(f"Bucătarul a primit comanda pentru: {filename}")

    time.sleep(5)

    input_path = os.path.join("/app/data", filename)
    output_filename = f"processed_{filename}"
    output_path = os.path.join("/app/data", output_filename)

    try:
        with Image.open(input_path) as img:
            gray_img = img.convert("L")
            final_img = gray_img.filter(ImageFilter.BoxBlur(2))
            final_img.save(output_path)

        print(f"Gata! Poza a fost salvată ca: {output_filename}")
        return {"status": "success", "file": output_filename}

    except Exception as e:
        print(f"Eroare la procesare: {e}")
        return {"status": "error", "message": str(e)}