# Use official slim Python 3.11 image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies for building Python packages, OpenCV, etc.
RUN apt-get update && apt-get install -y \
    build-essential \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements that rarely change for caching (PyTorch + numpy + OpenCV)
COPY requirements-base.txt .

# Upgrade pip, setuptools, wheel
RUN python -m pip install --upgrade pip setuptools wheel

# Install base dependencies (PyTorch + numpy + OpenCV)
RUN pip install --no-cache-dir -r requirements-base.txt -f https://download.pytorch.org/whl/cpu/torch_stable.html

# Copy remaining requirements that may change more frequently
COPY requirements.txt .

# Install remaining Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application source code
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Start FastAPI app
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
