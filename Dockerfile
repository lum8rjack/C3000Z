FROM python:3.9

RUN mkdir /app
WORKDIR /app

# Copy requirements first so making changes to the python file
# doesn't have to install the requirements every time
COPY requirements.txt /app/
RUN pip3 install -r requirements.txt

# Copy decryption script
COPY c3000z_enum.py /app/
RUN chmod +x c3000z_enum.py

CMD ["python3", "./c3000z_enum.py", "--file", "/app/config.xml"]

