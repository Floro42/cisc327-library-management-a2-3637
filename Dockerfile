FROM python:3.10-slim

WORKDIR /app

COPY . .

EXPOSE 5000

RUN pip install -r requirements.txt

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]