FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python -m pytest -v

EXPOSE 5000

CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]