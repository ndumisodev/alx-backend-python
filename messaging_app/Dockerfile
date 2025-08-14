# 1. Use Python 3.10 as the base image
FROM python:3.10

# 2. Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Set working directory
WORKDIR /app

# 4. Install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# 5. Copy project files
COPY . /app/

# 6. Expose the Django port
EXPOSE 8000

# 7. Command to run the app
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
