# C3000Z
Script to decode the passwords from the ZYXEL C3000Z router config file. If you are interested in how I discovered how to decode the passwords you can view the details here: https://lum8rjack.github.io/posts/c3000z/

## Overview

The Zyxel C3000Z modem/WiFi router is widely used by CenturyLink. The router allows the owner to download and backup the current router configurations. This backup config file not only has the WiFi details and passwords but it has the login credentials to login to the router and the PPP credentials for the router to connect to the Internet vie PPoE. The login and PPP passwords are encoded. This code will take the key and password to decrypt the password.

## Download Router Config

Downloading the configuration file can be done by:

1. Browse to the login page (Default is: 192.168.0.1)
2. Login using your admin credentials
3. Click on "Utilities"
4. Click "Upgrade Firmware"
5. Click "Download"

Depending on your version, there may be a "Save Configuration" section of "Utilities" instead of in the firmware update section.

## Tested

This script was tested on a configuration file that was pulled from a router with firmware version: CZD005-4.16.011.0

You can download the firmware version here: http://internethelp.centurylink.com/internethelp/modems/c3000z/firmware/CZD005-4.16.011.0.bin

## Previous Script

The initial script was created in Python and used an older version of OpenSSL with Docker to decrypt the password. I have since switched to using Go and don't need to use OpenSSL. The original code can be found in the `python` directory

## Build

Make sure you have Go installed and you can run `make` or the following command to build the binary.

```go
go build -o c3000z .
```

## Run

The program takes takes the data, key, and mode.

```bash
./c3000z -h            
Usage of ./c3000z:
  -data string
        data to encrypt/decrypt
  -key string
        encryption key (default "C1000Z_1234")
  -mode string
        encrypt or decrypt the data (default "decrypt")
```

Example encrypting the password `password123`

```bash
./c3000z -data password123 -mode encrypt                                                 
Encrypted: U2FsdGVkX1+BHNw4Gmt5UnZZiz4t0E1yXgOwGdR3w/U=
```

Example decrypting the output from before

```bash
./c3000z -data U2FsdGVkX1+BHNw4Gmt5UnZZiz4t0E1yXgOwGdR3w/U= -mode decrypt
Decrypted: password123
```
