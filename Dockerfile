FROM python:3.8

RUN mkdir /app
WORKDIR /app

COPY c3000z_enum.py /app/
RUN chmod +x c3000z_enum.py
COPY requirements.txt /app/

RUN pip3 install -r requirements.txt

CMD ["python3", "./c3000z_enum.py", "--file", "/app/config.xml"]

