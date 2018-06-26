# This class will contain all the hard coded paths

import os
import windows.currentDateTime

# Find VsCommand Window path
def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)
# Process completed


# Getting saved date time
savedDateTime = windows.currentDateTime.savedDateTime
# Process ends

class PathVarriables:
    temp = "C:\\Program Files (x86)\\Microsoft Visual Studio\\2017\\Community\\VC\\Auxiliary\\Build\\vcvars64.bat"
    vsCommandPrompt64 = "C:\\Program Files (x86)\\Microsoft Visual Studio 14.0\\VC"
    windowsCmd = 'C:\\Windows\\system32\\cmd.exe'
    rootDirectory = os.path.dirname(os.path.abspath(__file__))
    pgSqlMsvc = os.path.dirname(os.path.abspath(__file__))+"\\workDir\\"+savedDateTime+"\\version\\src\\postgresql-10.3\\src\\tools\\msvc"
    pgsqlCode = os.path.dirname(os.path.abspath(__file__)) + "\\workDir\\"+savedDateTime
    diffPath = "C:\Program Files (x86)\GnuWin32\\bin"

    postgresContrib = rootDirectory+"\\workDir\\"+savedDateTime+"\\"




