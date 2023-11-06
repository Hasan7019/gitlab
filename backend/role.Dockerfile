FROM python:3-slim
WORKDIR /app
COPY requirements.txt ./
RUN python -m pip install --no-cache-dir -r ./requirements.txt
COPY ./role.py .env ./classes.py .
CMD ["python", "./role.py", "./.env"]