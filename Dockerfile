# Base image
FROM stackbrew/debian:jessie

#prequisites
RUN apt-get update && apt-get -qy install python3 python3-pip

# Set the application directory
WORKDIR /app

# Install from requirements.txt
ADD requirements.txt /app/requirements.txt
RUN pip3 install -r requirements.txt

# Copy our code from the current folder to /app inside the container
ADD . /app

# Make port 5000 available for links and/or publish
EXPOSE 5000

# Define our command to be run when launching the container
CMD ["python", "run.py"]
