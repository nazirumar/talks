FROM python:3.12-slim


# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /code

# Install Python dependencies
COPY requirements.txt /code/
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . /code/

# Expose port 8000
EXPOSE 8000

# Run uWSGI
CMD ["uwsgi", "--ini", "config/uwsgi/uwsgi.ini"]
