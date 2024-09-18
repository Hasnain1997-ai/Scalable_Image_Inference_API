import requests
import time
import os
import concurrent.futures
import uuid

BASE_URL = "http://localhost:8000"

def test_valid_image(image_path):
    try:
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Error: {image_path} not found.")
        
        with open(image_path, "rb") as image_file:
            files = {"file": (f"test_image_{uuid.uuid4().hex[:8]}.jpg", image_file, "image/jpeg")}
            response = requests.post(f"{BASE_URL}/detect_objects", files=files)
        
        assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
        job_id = response.json()["job_id"]
        
        max_retries = 30
        retry_count = 0
        while retry_count < max_retries:
            result_response = requests.get(f"{BASE_URL}/result/{job_id}")
            if result_response.json().get("status") != "processing":
                break
            time.sleep(1)
            retry_count += 1
        
        assert "detections" in result_response.json(), f"Expected 'detections' in response, but got: {result_response.json()}"
        return True
    except Exception as e:
        print(f"Error in test_valid_image: {str(e)}")
        return False

def test_invalid_file():
    try:
        with open("test_file.txt", "w") as text_file:
            text_file.write("This is not an image file")
        
        with open("test_file.txt", "rb") as text_file:
            files = {"file": ("test_file.txt", text_file, "text/plain")}
            response = requests.post(f"{BASE_URL}/detect_objects", files=files)
        
        assert response.status_code == 400, f"Expected status code 400, but got {response.status_code}"
        print("Invalid file test passed")
        return True
    except AssertionError as e:
        print(f"Assertion Error: {str(e)}")
        return False
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return False
    finally:
        if os.path.exists("test_file.txt"):
            os.remove("test_file.txt")

def test_concurrent_requests(num_requests=5):
    image_path = "test_image.jpg"  # Ensure this image exists
    if not os.path.exists(image_path):
        print(f"Error: {image_path} not found. Please provide a valid test image.")
        return False

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_requests) as executor:
        futures = [executor.submit(test_valid_image, image_path) for _ in range(num_requests)]
        results = [future.result() for future in concurrent.futures.as_completed(futures)]

    success_rate = sum(results) / len(results) * 100
    print(f"Concurrent requests test: {success_rate:.2f}% successful ({sum(results)}/{len(results)})")
    return success_rate == 100

if __name__ == "__main__":
    print("Running single valid image test...")
    test_valid_image("test_image.jpg")
    
    print("\nRunning invalid file test...")
    test_invalid_file()
    
    print("\nRunning concurrent requests test...")
    test_concurrent_requests()