FROM python:3.10.6

WORKDIR /usr/src/application

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8050

CMD ["python", "app/index.py", "--host", "0.0.0.0", "--port", "8050"]