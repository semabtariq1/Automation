# 1 for needed 0 for not needed
import json

class ConfigFile:

    postgresql = 1
    # change v to something understandable
    pgVersions = '{"v": [{"fullVersion": "10.4", "majorVersion": "10", "minerVersion" : "4",' \
                 ' "url" : "https://ftp.postgresql.org/pub/source/v10.4/postgresql-10.4.tar.gz"} ] }'
    decoded = json.loads(pgVersions)

    postgis = '{"postgisV": [{"fullVersion": "2.4.4", "majorVersion": "4", "minerVersion" : "4",' \
              ' "url" : "https://download.osgeo.org/postgis/source/postgis-2.4.4.tar.gz"} ] }'
    decodedPostgis = json.loads(postgis)