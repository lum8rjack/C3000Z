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

# Copy your provider config file
COPY providers.cnf /app/

# Insert contents of providers.cnf after [openssl_init] in /etc/ssl/openssl.cnf
RUN awk '/^\[openssl_init\]/{print; system("cat /app/providers.cnf"); next} 1' \
    /etc/ssl/openssl.cnf > /etc/ssl/openssl.cnf.new && \
    mv /etc/ssl/openssl.cnf.new /etc/ssl/openssl.cnf

RUN apt update && apt install -y vim bsdmainutils

CMD ["python3", "./c3000z_enum.py", "--file", "/app/config.xml"]

