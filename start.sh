#!/bin/bash
echo "Waiting for Database to wake up..."
sleep 15
# Start the Brain (Port 8000) in the background (&)
python -m uvicorn apps.brain:app --host 0.0.0.0 --port 8000 &

# Start the Surface (Port 8001) in the foreground
python -m uvicorn apps.surface:app --host 0.0.0.0 --port 8001