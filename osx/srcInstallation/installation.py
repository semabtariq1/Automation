import os
import paths

path = paths.Path()

class Install:
    def unzipPostgresql(self, version):
        result = os.system("tar -xf postgresql-"+version+".tar.gz --directory "+path.currentProject +"/"+version +"/src")
        return result


    def unzipPostgis(self, version, ver):
        result = os.system(
        "tar -xf postgis-" + ver + ".tar.gz --directory " + path.currentProject + "/" + version + "/src")
        return result