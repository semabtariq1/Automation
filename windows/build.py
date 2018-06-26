import os

import windows.pathVariables


# Initializing path variable file
pathvariable = windows.pathVariables.PathVarriables;
# Process ends


class Building:

    def startBuildProcess(self, need):

        #correct command
        # buildTask = pathvariable.windowsCmd + ' /c ' + '""' + pathvariable.vsCommandPrompt64 + '"  & cd ' + pathvariable.pgsqlCode + '\\' + need + '\\src\\postgresql-' + need + '\\src\\tools\\msvc  &  ' + pathvariable.build + ' > "' + pathvariable.pgsqlCode + '\\' + need + '\\logs\\build.log" 2>&1"'
        # buildTask = pathvariable.windowsCmd + ' /c ' + '"   cd /d '+pathvariable.vsCommandPrompt64+' && vcvarsall amd64 && cd /d F:\\python-Automation\\Automation\\windows\\workDir\\20180625224303\\10.4\\src\\postgresql-10.4\\src\\tools\\msvc && build "'
        buildTask = pathvariable.windowsCmd + ' /c ' + '"   cd /d '+pathvariable.vsCommandPrompt64+' && vcvarsall amd64 && cd /d '+pathvariable.pgsqlCode+'\\'+need+'\\src\\postgresql-'+need+'\\src\\tools\\msvc && build > '+pathvariable.pgsqlCode+'\\'+need+'\\logs\\build.log 2>&1"'


        #print(buildTask)
        result = os.system(buildTask)

        return result
# o = Building()
# o.startBuildProcess("10.4")










