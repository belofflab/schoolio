# Use the official Python image as the base image
FROM python:3.10

# Set the working directory
WORKDIR /opt/bot

# Copy the requirements file into the container
COPY requirements.txt .

RUN python3 -m pip install virtualenv 
RUN python3 -m virtualenv /opt/bot/venv

RUN /opt/bot/venv/bin/pip install -r requirements.txt

COPY . .

# Start the bot
CMD ["/opt/bot/venv/bin/python", "bot.py"]
