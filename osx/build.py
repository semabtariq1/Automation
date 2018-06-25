import os
import paths

paths = paths.Path()

class Build:
    def runBuild(self, version):
        buildPath = paths.currentProject + "/" + version + "/src/postgresql-" + version
        command = " make > "+paths.currentProject+"/"+version+"/logs/build.log 2>&1"

        os.system("cd "+buildPath+" && "+command+"")