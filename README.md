# 🖼️ Object Detection API

## 📚 Table of Contents
- [Overview](#overview)
- [Features](#features)
- [System Architecture](#system-architecture)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Testing](#testing)
- [Scalability](#scalability)

## 🔍 Overview

This Python-based API performs object detection on images using a pre-trained YOLOv8 model. The system is designed to handle multiple concurrent requests efficiently, utilizing Redis Queue (RQ) for request management. The API is built with vertical scalability in mind, making it suitable for high-load environments.

## ✨ Features

- 🚀 Fast object detection using YOLOv8
- 🔄 Asynchronous processing with Redis Queue
- 🌐 RESTful API built with FastAPI
- 🔧 Easily scalable architecture
- 🧪 Comprehensive testing suite

## 🏗️ System Architecture

The application consists of three main components:

1. **API Server** (`api.py`): Handles incoming HTTP requests, validates images, and enqueues tasks.
2. **Worker** (`RQ_Worker.py`): Processes queued tasks, performing object detection on images.
3. **Image Processor** (`image_processor.py`): Contains the core logic for object detection using YOLOv8.

## 🛠️ Installation

You have two options for installation: using Docker (recommended) or manual installation.

### Option 1: Docker Installation (Recommended)

1. Clone the repository:
   ```
   git clone https://github.com/Hasnain1997-ai/Scalable_Image_Inference_API.git
   cd Scalable_Image_Inference_API
   ```

2. Install Docker Compose (if not already installed):
   ```
   sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
   sudo chmod +x /usr/local/bin/docker-compose
   ```

3. Ensure that your local Redis server is stopped:
   ```
   sudo systemctl stop redis-server
   ```

4. Build and run the Docker containers:
   ```
   docker-compose up --build
   ```

This will set up the entire application, including the API server, Redis, and the worker.

### Option 2: Manual Installation

If you prefer not to use Docker, follow these steps:

1. Clone the repository:
   ```
   git clone https://github.com/Hasnain1997-ai/Scalable_Image_Inference_API.git
   cd object-detection-api
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Install Redis:
   - On Ubuntu: `sudo apt-get install redis-server`
   - On macOS: `brew install redis`
   - On Windows: Download from [Redis website](https://redis.io/download)


4. Start the Redis server:
   ```
   redis-server
   ```

## 🚀 Usage

If you're using Docker, the application should be up and running after `docker-compose up --build`.

For manual installation:

1. Start the Redis server (if not already running):
   ```
   redis-server
   ```

2. Start the RQ worker:
   ```
   python RQ_Worker.py
   ```

3. Run the API server:
   ```
   python api.py
   ```

The API will be available at `http://localhost:8000`.

## 🧪 Testing

The repository includes two test files:

1. `test_api.py`: Contains unit tests for the API endpoints.
2. `concurrent_test.py`: Assesses the API’s ability to handle multiple concurrent requests.

### Running API Tests

To test the API using a single image, execute the following command:

```bash
python3 test_api.py
```

This script will test the application by passing a valid image located in the test_files folder. If the tests run successfully, you should see the following output:

- Valid image test passed
- Invalid file test passed

### Running Concurrent Requests Test
To stress test the API with concurrent requests, run the following command:
```
sh ./test_concurrent_calls.sh
```
This script will send 10 concurrent requests to the application, with each request being processed in a queue. The results will be displayed in the terminal after execution.

## 🌐 API Endpoints

### POST /detect_objects

Upload an image for object detection.

- **Request**: Multipart form data with a file field named 'file'
- **Response**: JSON object with a `job_id`

Example:
```bash
curl -X POST -F "file=@path/to/your/image.jpg" http://localhost:8000/detect_objects
```

### GET /result/{job_id}

Retrieve the results of a detection job.

- **Response**: JSON object with detection results or processing status

Example:
```bash
curl http://localhost:8000/result/your-job-id-here
```


## 📈 Scalability

The application is designed with vertical scalability in mind:

- Redis Queue allows for easy addition of more worker processes.
- FastAPI provides high performance for the API layer.
- The YOLOv8 model can utilize GPU acceleration when available.

To scale the application:

1. Increase the number of worker processes by running multiple instances of `RQ_Worker.py`.
2. Deploy the API on more powerful hardware or cloud instances.
3. Utilize load balancing for distributing incoming requests across multiple API instances.