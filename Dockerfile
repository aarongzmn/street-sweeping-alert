# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.8-slim
RUN apt-get update && apt-get install -y apt-transport-https
RUN apt-get install git-core -y

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

# Install production dependencies.
RUN pip install Flask gunicorn
RUN pip install requests

# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 app:app