import config

section = 'StackspotAI'

config.conf.spec[section] = {
    "client_id": "",
    "client_secret": "",
    "realm": "",
    "slug": ""
}


def getPref(key: str):
    return config.conf[section].get(key, "")


def setPref(key: str, value: str):
    config.conf[section][key] = value
    config.conf.save()
