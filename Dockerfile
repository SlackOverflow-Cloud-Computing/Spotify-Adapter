# The base image for python. There are countless official images.
# Alpine just sounded cool.
#
FROM python:3.9-slim

# The directory in the container where the app will run.
#
WORKDIR /app

# Copy the requirements.txt file from the project directory into the working
# directory and install the requirements.
#
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy over the files.
#
COPY . /app/.

# Expose/publish port 5002 for the container.
#
EXPOSE 8005

# Look in the code. This is an environment variable
# passed to the application.
#
ENV WHEREAMI=DOCKER

# Run the app.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8005"]

