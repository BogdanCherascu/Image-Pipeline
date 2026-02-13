# Asynchronous Image Processing Pipeline (Event-Driven Microservices)

A production-ready, decoupled microservices architecture designed to handle heavy background processing tasks without blocking the main web API. 

This project demonstrates a classic **Event-Driven Architecture** using a Message Broker and distributed workers, completely containerized for seamless deployment.

## Architecture & Flow

1. **API Gateway (FastAPI):** Receives user file uploads, saves them to a shared volume, and instantly dispatches a processing task to the message broker. Returns a `task_id` for status tracking (non-blocking).
2. **Message Broker (Redis):** Acts as the queue/broker, holding tasks in memory until a worker is free to pick them up.
3. **Background Worker (Celery/Python):** Listens to the Redis queue, picks up tasks, processes images (applies Grayscale and Blur filters via Pillow), and saves the results back to the shared volume.
4. **Shared Storage (Docker Volumes):** Ensures data persistence and allows isolated containers to access the same physical files securely.

## Tech Stack

* **Backend:** Python 3.11, FastAPI, Uvicorn
* **Task Queue / Message Broker:** Celery, Redis
* **Image Processing:** Pillow (PIL)
* **DevOps / Infrastructure:** Docker, Docker Compose, Docker Volumes

## How to Run

1. Clone this repository and navigate to the project folder.
2. Build and start the container orchestration:
   ```bash
   docker compose up --build
   ```
3. Access the auto-generated Swagger UI to interact with the API:
    **`http://localhost:8000/docs`**

## 📖 Usage Example

**1. Upload an Image:**
* Use the `POST /upload` endpoint via Swagger UI to upload any image.
* The API will respond in milliseconds with a `task_id`:
  ```json
  {
    "message": "Image uploaded successfully. Background processing initiated.",
    "task_id": "a1b2c3d4-...",
    "filename": "my_photo.jpg"
  }
  ```

**2. Check Processing Status:**
* Use the `GET /status/{task_id}` endpoint.
* If the Celery worker is still processing the image, you will get:
  ```json
  {
    "task_id": "a1b2c3d4-...",
    "status": "PROCESSING"
  }
  ```
* Once the background worker finishes, the status updates to:
  ```json
  {
    "task_id": "a1b2c3d4-...",
    "status": "COMPLETED",
    "result": {
      "status": "success",
      "file": "processed_my_photo.jpg",
      "message": "Filters applied successfully."
    }
  }
  ```
* Check your local `data/` folder to view the newly generated image.

## Cleanup
To safely stop the services and remove the isolated networks, press `Ctrl+C` in your terminal and run:
```bash
docker compose down
```
