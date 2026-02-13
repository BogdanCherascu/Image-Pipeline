from fastapi import FastAPI, UploadFile, File
from celery.result import AsyncResult
from celery import Celery
import shutil
import os

app = FastAPI()

celery_app = Celery(
    "image_tasks",
    broker="redis://redis_mq:6379/0",
    backend="redis://redis_mq:6379/0"
)

os.makedirs("/app/data", exist_ok=True)

@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    """ Endpoint to upload an image and dispatch a background processing task. """
    
    file_location = f"/app/data/{file.filename}"
    with open(file_location, "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)
    
    task = celery_app.send_task("process_image", args=[file.filename])
    
    return {
        "message": "Image uploaded successfully. Background processing initiated.",
        "task_id": task.id,
        "filename": file.filename
    }

@app.get("/status/{task_id}")
def check_task_status(task_id: str):
    """ Endpoint to check the status of an asynchronous task. """
    
    task = AsyncResult(task_id, app=celery_app)
    
    if task.ready():
        return {
            "task_id": task_id,
            "status": "COMPLETED",
            "result": task.result
        }
    else:
        return {
            "task_id": task_id,
            "status": "PROCESSING"
        }