#!/bin/sh

# Configuration
API_URL="http://localhost:8000"
IMAGE_PATH="/media/ai-dev/7ddb5cde-9928-4de6-abaa-cbbf9343b4df/home/hasnain-dev/work-space_HDD/Scalable_Image_Inference_API/test_image.jpg"
NUM_REQUESTS=10

# Function to send a request and store the job ID
send_request() {
    response=$(curl -s -X POST "${API_URL}/detect_objects" \
         -H "accept: application/json" \
         -H "Content-Type: multipart/form-data" \
         -F "file=@${IMAGE_PATH}")
    job_id=$(echo "$response" | sed -n 's/.*"job_id":"\([^"]*\)".*/\1/p')
    if [ -z "$job_id" ]; then
        echo "Error: $response" >&2
        return 1
    fi
    echo "$job_id"
}

# Function to check the result of a job
check_result() {
    job_id=$1
    curl -s -X GET "${API_URL}/result/${job_id}" \
         -H "accept: application/json"
}

# Send multiple requests concurrently
echo "Sending $NUM_REQUESTS concurrent requests..."
job_ids=""
for i in $(seq 1 $NUM_REQUESTS); do
    job_id=$(send_request)
    if [ $? -eq 0 ]; then
        job_ids="$job_ids $job_id"
    fi
done

echo "All requests sent. Job IDs:$job_ids"

# Check results
echo "Checking results..."
for job_id in $job_ids; do
    while true; do
        result=$(check_result $job_id)
        case $result in
            *"processing"*) sleep 1 ;;
            *"error"*) 
                echo "Job $job_id failed: $result"
                break
                ;;
            *)
                echo "Job $job_id completed: $result"
                break
                ;;
        esac
    done
done

echo "All jobs completed."