import os
import paths

paths = paths.Path()

class Configuration:
    def runConfiguration(self, version, majorVersion):
        configPath = paths.currentProject+"/"+version+"/src/postgresql-"+version
        configCommand = "./configure  --with-openssl --with-python --with-zlib --prefix="+paths.currentProject+"/"+version+"/build/"+majorVersion+" > "+paths.currentProject+"/"+version+"/logs/configure.log 2>&1"
        os.system("cd "+configPath+" && "+configCommand+"")