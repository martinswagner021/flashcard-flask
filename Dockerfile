FROM python

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY ./app .

# Install any needed packages specified in requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

# Run main.py when the container launches
CMD ["python", "main.py"]