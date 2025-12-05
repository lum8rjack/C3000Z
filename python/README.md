## Install
This script uses Python3 and you will need to make sure the additional dependicies are installed using pip3

```python
pip3 install -r requirements.txt
```

### Docker
A dockerfile has also been created that can be used instead. Run the build.sh command to build the image. Once built, you can run the following command to supply the config file to docker for it to parse.

```
docker run --rm -v $(pwd)/<your config file>.xml:/app/config.xml c3000z
```

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
