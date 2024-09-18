import requests
import time
import os

BASE_URL = "http://localhost:8000"

def test_valid_image():
    try:
        image_path = "test_image.jpg"  # Path to your test image
        
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Error: {image_path} not found.")
        
        with open(image_path, "rb") as image_file:
            files = {"file": ("test_image.jpg", image_file, "image/jpeg")}
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
        print("Valid image test passed")
    except FileNotFoundError as e:
        print(str(e))
    except AssertionError as e:
        print(f"Assertion Error: {str(e)}")
    except Exception as e:
        print(f"Error occurred: {str(e)}")

def test_invalid_file():
    try:
        with open("test_file.txt", "w") as text_file:
            text_file.write("This is not an image file")
        
        with open("test_file.txt", "rb") as text_file:
            files = {"file": ("test_file.txt", text_file, "text/plain")}
            response = requests.post(f"{BASE_URL}/detect_objects", files=files)
        
        assert response.status_code == 400, f"Expected status code 400, but got {response.status_code}"
        print("Invalid file test passed")
    except AssertionError as e:
        print(f"Assertion Error: {str(e)}")
    except Exception as e:
        print(f"Error occurred: {str(e)}")
    finally:
        if os.path.exists("test_file.txt"):
            os.remove("test_file.txt")

if __name__ == "__main__":
    test_valid_image()
    test_invalid_file()