FROM python:3.11.3

# Set the working directory to /app
WORKDIR /app

COPY ./requirements.txt /app

RUN pip install -U pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

CMD ["uvicorn", "apartment_scraper.api:app", "--host", "0.0.0.0", "--port", "80"]