#!/bin/bash

echo "Starting the main application..."
exec uvicorn api:app --host 0.0.0.0 --port 8000