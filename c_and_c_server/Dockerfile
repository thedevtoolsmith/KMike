FROM python:3.8.3-buster
LABEL author="ksurya328@gmail.com"

COPY . /c_and_c_server
WORKDIR /c_and_c_server
EXPOSE 5000:5000
RUN pip3 install --no-cache-dir -r requirements.txt

CMD ["python3", "server.py"]