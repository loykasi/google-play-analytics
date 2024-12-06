FROM python:3.11-alpine

COPY requirements.txt .

RUN pip install -r requirements.txt

WORKDIR /app

COPY . .

CMD uvicorn app.main:app --host=0.0.0.0

# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

# RUN pip install --no-cache-dir --upgrade -r requirements.txt
# CMD ["python", "main.py"]
# CMD ["fastapi", "run", "app/main.py", "--port", "80"]

# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]