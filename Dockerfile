FROM python:3.11-slim

WORKDIR

COPY

RUN pip install --no-cache 

COPY . .

CMD ["python", "src/main.py"]