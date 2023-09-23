FROM python:3.11.3

# Set the working directory to /app
WORKDIR /app

COPY pyproject.toml /app

RUN pip install -U pip
RUN pip install poetry
RUN poetry export -f requirements.txt --output requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app