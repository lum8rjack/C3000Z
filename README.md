# C3000Z
Script to decode the passwords from the ZYXEL C3000Z router config file. If you are interested in how I discovered how to decode the passwords you can view the details here: https://lum8rjack.github.io/posts/c3000z/

## Overview

The Zyxel C3000Z modem/WiFi router is widely used by CenturyLink. The router allows the owner to download and backup the current router configurations. This backup config file not only has the WiFi details and passwords but it has the login credentials to login to the router and the PPP credentials for the router to connect to the Internet vie PPoE. The login and PPP passwords are encoded. This script will read in the config file and decode the passwords based on the default key CenturyLink used.

## Tested
This script was tested on a configuration file that was pulled from a router with firmware version: CZD005-4.16.011.0

You can download the firmware version here: http://internethelp.centurylink.com/internethelp/modems/c3000z/firmware/CZD005-4.16.011.0.bin

## Install
This script uses Python3 and you will need to make sure the additional dependicies are installed using pip3

~~~
pip3 install -r requirements.txt
~~~

### Docker
A dockerfile has also been created that can be used instead. Run the build.sh command to build the image. Once built, you can run the following command to supply the config file to docker for it to parse.

~~~
docker run --rm -v $(pwd)/<your config file>.xml:/app/config.xml c3000z
~~~

## Download Config
Downloading the configuration file can be done by:

1. Browse to the login page (Default is: 192.168.0.1)
2. Login using your admin credentials
3. Click on "Utilities"
4. Click "Upgrade Firmware"
5. Click "Download"

Depending on your version, there may be a "Save Configuration" section of "Utilities" instead of in the firmware update section.

## Openssl
Newer versions of openssl may have errors running the decrypt command. You can change the config file `/etc/ssl/openssl.cnf` or provide your own config or programmatic settings to openssl and make sure these sections have these values. The legacy providers are disabled by default for good reason (https://github.com/openssl/openssl/blob/master/README-PROVIDERS.md).

```bash
openssl_conf = openssl_init

[openssl_init]
providers = provider_sect

[provider_sect]
default = default_sect
legacy = legacy_sect

[default_sect]
activate = 1

[legacy_sect]
activate = 1
```

Original command:
```bash
openssl des -in <config file> -d -k C1000Z_1234 -a -md md5
```

Updated command:
```bash
openssl des -provider legacy -in <config file> -d -k C1000Z_1234 -a -md md5
```

## Credits
Thanks to the people below who have helped identify bugs and recommend fixes!

- [@zenfish](https://github.com/zenfish)
- [@micahjon](https://github.com/micahjon)
- [@surewould](https://github.com/surewould)
- [@jludwig75](https://github.com/jludwig75)
