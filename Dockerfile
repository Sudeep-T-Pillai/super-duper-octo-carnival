# Use Python 3.13
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all your code
COPY . .

# We need a script to run BOTH Brain and Surface at the same time
COPY start.sh .
RUN chmod +x start.sh

# The command to run when container starts
CMD ["./start.sh"]