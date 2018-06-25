import os
import paths

paths = paths.Path()

class Install:
    def runInstall(self, version):
        buildPath = paths.currentProject + "/" + version + "/src/postgresql-" + version
        command = " make install > "+paths.currentProject+"/"+version+"/logs/install.log 2>&1"

        os.system("cd "+buildPath+" && "+command+"")