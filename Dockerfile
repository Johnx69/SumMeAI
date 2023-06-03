# Use the official Python 3.10 base image
FROM python:3.10

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file first for better caching
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY . .

# Expose the port that FastAPI will run on
EXPOSE 8000

# Start the FastAPI application using uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
