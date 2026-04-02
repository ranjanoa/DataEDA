FROM python:3.11-slim

WORKDIR /app

# Install Node.js for Tailwind CSS build
RUN apt-get update && apt-get install -y nodejs npm && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Node dependencies and build CSS
COPY package.json package-lock.json ./
RUN npm ci

COPY . .
RUN npm run build:tailwind

# Expose HuggingFace default port
EXPOSE 7860

CMD ["uvicorn", "api.index:app", "--host", "0.0.0.0", "--port", "7860"]
