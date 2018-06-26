import os

import windows.pathVariables


# Initializing path variable file
pathvariable = windows.pathVariables.PathVarriables;
# Process ends


class Regression:
    def startRegresstion(self, need):
        # Working fine
        # regressionTask = pathvariable.windowsCmd + ' /c ' + '""' + pathvariable.vsCommandPrompt64 + '" & cd ' + pathvariable.pgsqlCode + '\\' + need + '\\src\\postgresql-' + need + '\\src\\tools\\msvc' ' &  ' + pathvariable.regression + '"'
        # os.system(regressionTask)

        regressionTask = pathvariable.windowsCmd + ' /c ' + '"   cd /d '+pathvariable.vsCommandPrompt64+' && vcvarsall amd64 && cd /d '+pathvariable.pgsqlCode+'\\'+need+'\\src\\postgresql-'+need+'\\src\\tools\\msvc && vcregress check > '+pathvariable.pgsqlCode+'\\'+need+'\\logs\\regression.log 2>&1"'

        result = os.system(regressionTask)
        os.system("exit")
        return result
        #print(regressionTask)