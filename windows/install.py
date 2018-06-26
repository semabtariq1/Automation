import os

import windows.pathVariables


# Initializing path variable file
pathvariable = windows.pathVariables.PathVarriables
# Process ends


class Installation:
    def startInstation(self, need, majorVersion):
        #Works fine without hiding anything
        #installationTaskok = pathvariable.windowsCmd + ' /c ' + '""' + pathvariable.vsCommandPrompt64 + '" & cd ' + pathvariable.pgsqlCode + '\\' + need + '\\src\\postgresql-' + need + '\\src\\tools\\msvc' ' &  ' + pathvariable.install + '\\' + need + '\\build\\'+ majorVersion+ '"'
        # os.system(installationTask)

        # installationTask = pathvariable.windowsCmd + ' /c ' + '""' + pathvariable.vsCommandPrompt64 + '" & cd ' + pathvariable.pgsqlCode + '\\' + need + '\\src\\postgresql-' + need + '\\src\\tools\\msvc' ' &  ' + pathvariable.install + '\\' + need + '\\build\\' +\
        #                    majorVersion + '" > "'+pathvariable.pgsqlCode+"\\"+need+'\\logs\install.log""'


        installationTask = pathvariable.windowsCmd + ' /c ' + '"   cd /d '+pathvariable.vsCommandPrompt64+' && vcvarsall amd64 && cd /d '+pathvariable.pgsqlCode+'\\'+need+'\\src\\postgresql-'+need+'\\src\\tools\\msvc && install '+pathvariable.pgsqlCode+'\\'+need+'\\build\\'+majorVersion+' > '+pathvariable.pgsqlCode+'\\'+need+'\\logs\\install.log 2>&1"'
        result = os.system(installationTask)
        os.system("exit")
        return result

        #print(installationTask)
        #print(installationTaskok)