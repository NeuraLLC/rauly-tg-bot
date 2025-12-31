FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create sessions and logs directories for persistence
RUN mkdir -p /app/sessions /app/logs

# Set environment variable for Telethon session path
ENV SESSION_PATH=/app/sessions/rauly_session

# Command to run the application (Background worker mode)
# In production, we typically run a script that keeps the bot alive
CMD ["python", "main.py", "report"]
