FROM python:3.8.0-buster

#Make directory
WORKDIR /src

#Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

#Copy code
COPY . /app

#Run
CMD ["python", "/app/main.py"]
