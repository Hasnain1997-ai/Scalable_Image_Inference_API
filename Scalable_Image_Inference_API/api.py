import os
import imghdr
from fastapi import FastAPI, HTTPException, UploadFile, File
from redis import Redis
from rq import Queue
from pydantic import BaseModel

from image_processor import process_image

app = FastAPI()


redis_host = os.getenv('REDIS_HOST', 'localhost')
redis_conn = Redis(host='localhost', port=6379)
queue = Queue(connection=redis_conn)

class DetectionResult(BaseModel):
    job_id: str

def is_valid_image(file_contents: bytes) -> bool:
    image_type = imghdr.what(None, file_contents)
    return image_type is not None

@app.post("/detect_objects", response_model=DetectionResult)
async def detect_objects(file: UploadFile = File(...)):
    """
    Endpoint to upload an image file for object detection.
    This endpoint accepts image uploads from any source.
    The image file should be sent as form-data with the key 'file'.
    """
    try:
        contents = await file.read()
        if not contents:
            raise HTTPException(status_code=400, detail="Empty file")
        
        if not is_valid_image(contents):
            raise HTTPException(status_code=400, detail="Invalid image file")
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing file: {str(e)}")
    
    # Enqueue the task
    job = queue.enqueue(process_image, contents)
    
    # Return the job ID
    return DetectionResult(job_id=job.id)

@app.get("/result/{job_id}")
async def get_result(job_id: str):
    job = queue.fetch_job(job_id)
    
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    
    if not job.is_finished:
        return {"status": "processing"}
    
    result = job.result
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))