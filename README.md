# C3000Z
Script to decode the passwords from the ZYXEL C3000Z router config file

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
