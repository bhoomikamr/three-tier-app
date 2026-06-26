FROM python:3.14-alpine
WORKDIR /app
#Installing the tools needed to build database drivers
RUN apk add --no-cache gcc musl-dev postgresql-dev
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python","app.py"]