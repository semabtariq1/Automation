import os
import paths

paths = paths.Path()

class Regression:
    def runRegression(self, version):
        regressionPath = paths.currentProject + "/" + version + "/src/postgresql-" + version
        command = " make check > "+paths.currentProject+"/"+version+"/logs/regression.log 2>&1"

        os.system("cd "+regressionPath+" && "+command+"")