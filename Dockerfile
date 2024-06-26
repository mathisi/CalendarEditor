# Use an official Python runtime as a parent image
FROM python:3

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip3 install --no-cache-dir --progress-bar off -r requirements.txt

# Make port 9013 available to the world outside this container
EXPOSE 9014

# Run app.py when the container launches
CMD ["python", "raplaeditor.py"]
