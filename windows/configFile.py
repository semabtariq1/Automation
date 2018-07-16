# 1 for needed 0 for not needed
import json

class ConfigFile:

    pgSql = 1
    # change v to something understandable
    pgVersions = '{"v": [{"fullVersion": "9.5.13", "majorVersion": "9.5", "minerVersion" : "13"} ] }'
    decoded = json.loads(pgVersions)

    diff = ["0", "https://excellmedia.dl.sourceforge.net/project/gnuwin32/diffutils/2.8.7-1/diffutils-2.8.7-1.exe",
              "diffutils-2.8.7-1.exe"]

    python = ["0", "https://www.python.org/ftp/python/3.3.0/python-3.3.0.amd64.msi",
              "python-3.3.0.amd64.msi"]
