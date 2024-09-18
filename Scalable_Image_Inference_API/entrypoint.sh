#!/bin/bash

# Start the main application
./start_main.sh &

# Wait for a bit to ensure the main application has started
echo "##############################################################"
echo "            Waiting for 5 seconds, worker will start..."
echo "##############################################################"
sleep 5

# Start the worker
./start_worker.sh