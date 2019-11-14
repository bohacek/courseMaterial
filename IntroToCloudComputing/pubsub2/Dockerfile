# Use an official Python runtime as a parent image
FROM python:3.7

# Set the working directory to /app
WORKDIR /MyApp

# Copy the current directory contents into the container at /app
ADD . /MyApp

# copy gcp creds
COPY mycreds.json  mycreds.json

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt


# Define environment variable
ENV NAME World

# Run the app when the container launches
CMD ["python", "translator.py"]
