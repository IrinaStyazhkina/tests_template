FROM python:3.12
WORKDIR /app
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r /app/requirements.txt

CMD ["python", "ml_main.py"]