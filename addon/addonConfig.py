import config

section = 'Stackspot AI'

if section not in config.conf.spec:
    config.conf.spec[section] = {
        "client_id": "",
        "client_secret": ""
    }


def getPref(key: str):
    try:
        return config.conf[section][key]
    except KeyError:
        return ""


def setPref(key: str, value: str):
    config.conf[section][key] = value
    config.conf.save()
