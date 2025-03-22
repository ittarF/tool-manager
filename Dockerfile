FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose the port that the application will run on
EXPOSE 8000

# Command to run the application
CMD ["python", "run.py"] 