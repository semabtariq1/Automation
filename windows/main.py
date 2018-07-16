

import windows.configFile
import windows.pathVariables

import windows.srcDownloads.downloadFile

import windows.srcInstallation.installSoftware



import windows.currentDateTime

import windows.build
import windows.regression
import windows.install
import windows.copyFile

import platform
import os
import time



from distutils.dir_util import copy_tree

# Getting system properties
operatingSystem = platform.system();
# Process completed


# Initializing config file
configFile = windows.configFile.ConfigFile()
# Process ends


# Initializing path variable file
pathVariable = windows.pathVariables.PathVarriables()
# Process ends

# Initialize install software
installSoftware = windows.srcInstallation.installSoftware.InstallSoftware()
# Process done

# Getting saved date time
savedDateTime = windows.currentDateTime.savedDateTime
# Process ends


# Initializing build
buildProc = windows.build.Building()
# Process ends


# Initializing regression
regressionProc = windows.regression.Regression()
# Process ends


# Initializing regression
instalationProc = windows.install.Installation()
# Process ends



# Initializing copyFile
copyFile = windows.copyFile.CopyFile()
# Process ends



if operatingSystem is "Windows":

    # # Setting up folder hierarchy..
    print("\nFollowing directories are being created ...")
    for version in configFile.decoded['v']:
        rootPathSrc = pathVariable.rootDirectory + "\\workDir\\"+savedDateTime+"\\"+version['fullVersion']+"\\src"
        rootPathBuild = pathVariable.rootDirectory + "\\workDir\\" + savedDateTime + "\\" + version['fullVersion']+"\\build\\"+version['majorVersion']
        installationLogs = pathVariable.rootDirectory+ "\\workDir\\"+savedDateTime+"\\"+version['fullVersion']+"\\logs"
        if not os.path.exists(rootPathSrc):
            os.makedirs(rootPathSrc)
            print(rootPathSrc)
            time.sleep(1)
        # Setting build folder
        if not os.path.exists(rootPathBuild):
            os.makedirs(rootPathBuild)
            print(rootPathBuild)
            time.sleep(1)
        # Setting log directory
        if not os.path.exists(installationLogs):
            os.makedirs(installationLogs)
            print(installationLogs)
            time.sleep(1)
    # Process endds


    # Downloading Python
    if configFile.python[0] == "1":
        downloadFile = windows.srcDownloads.downloadFile.DownloadFile()
        downloadFile.downloadFile(configFile.python[1], configFile.python[2])
        # Installation
        path = pathVariable.windowsCmd + " /c cd " + pathVariable.rootDirectory
        command = ' && python-3.3.0.amd64.msi /qn'
        installSoftware.installSoftware("Python", path+command)



    # Downloading Diff
    if configFile.diff[0] == "1":
        downloadFile = windows.srcDownloads.downloadFile.DownloadFile()
        downloadFile.downloadFile(configFile.diff[1], configFile.diff[2])
        # Installation

        path = pathVariable.windowsCmd + " /c cd " + pathVariable.rootDirectory
        command = ' && diffutils-2.8.7-1.exe /SILENT, /VERYSILENT'
        installSoftware.installSoftware("Diff", path + command)


    # Downloading Pgsql code
    if configFile.pgSql == 1:
        #downloadFile = windows.srcDownloads.downloadFile.DownloadFile()
        for version in configFile.decoded['v']:
            # link = "https://ftp.postgresql.org/pub/source/v" + version['fullVersion'] + "/postgresql-" + version[
            #     'fullVersion'] + ".tar.gz"
            # downloadFile.downloadFile(link, "postgres-"+version['fullVersion']+".tar.gz")

            installSoftware.unzipPostgres(version['fullVersion'])


    # Generating envoirnment files
    for version in configFile.decoded['v']:
        print("Generating envoirnment file for version ...", version['fullVersion'])
        f = open(os.path.dirname(os.path.abspath(__file__))+"\\workDir\\"+savedDateTime+"\\"+version['fullVersion']+"\\src\\postgresql-"+version['fullVersion']+"\\src\\tools\\msvc\\buildenv.pl", "w+")
        # f.write("$ENV{PATH}=$ENV{PATH} . ';C:\Program Files (x86)\GnuWin32\\bin';")
        f.write("$ENV{PATH}=$ENV{PATH} . ';"+pathVariable.diffPath+"';")
        time.sleep(3)
        f.close()
    # Process ends


    # Adding paths in config_default.pl file
    print("Updating config_default.pl file")
    number = 0
    for version in configFile.decoded['v']:
        config_default = pathVariable.rootDirectory+"\\workDir\\"+savedDateTime+"\\"+version['fullVersion']+"\\src\\postgresql-"+version['fullVersion']+"\\src\\tools\\msvc\\config_default.pl"
        file = open(config_default)
        line = file.read().splitlines()
        for li in line:
            if 'python' in li:
                line[number] = "    python    => 'c:\python33',    # --with-python=<path>"
                open(config_default, 'w').write('\n'.join(line))
            elif "openssl" in li:
                line[number] = "    openssl   => '"+pathVariable.rootDirectory+"\\winShareLib\\openssl',    # --with-openssl=<path>"
                open(config_default, 'w').write('\n'.join(line))
            elif "zlib" in li:
                line[number] = "    zlib      => '"+pathVariable.rootDirectory+"\\winShareLib\\zlib'    # --with-zlib=<path>"
                open(config_default, 'w').write('\n'.join(line))
            number += 1;
        file.close()
    # Process ends


    # copying openssl and zlib into installation directory
    print("copying openssl and zlib files ...")
    for version in configFile.decoded['v']:
        # openssl
        src = pathVariable.rootDirectory + "\\winShareLib\\openssl"
        dest = pathVariable.rootDirectory + "\\workDir\\" + savedDateTime + "\\" + version['fullVersion'] + "\\build\\"+version['majorVersion']
        copyFile.copy(src, dest)
        # zlib
        src = pathVariable.rootDirectory + "\\winShareLib\\zlib"
        dest = pathVariable.rootDirectory + "\\workDir\\" + savedDateTime + "\\" + version['fullVersion'] + "\\build\\" + \
               version['majorVersion']
        copyFile.copy(src, dest)
    time.sleep(3)


    # Build + Regression + installation
    for version in configFile.decoded['v']:
        print("Build + Regression + Installation for version ... ", version['fullVersion'])
        print("\n\nRunning build ...")
        time.sleep(3)
        resultBuild = buildProc.startBuildProcess(version['fullVersion'])
        if resultBuild == 0:

            print("\n\nRunning regression ...")
            time.sleep(3)
            #resultRegression = regressionProc.startRegresstion(version['fullVersion'])
            resultRegression = 0
            if resultRegression == 0:


                print("\n\nRunning instalation ...")
                time.sleep(3)
                resultInstallation = instalationProc.startInstation(version['fullVersion'], version['majorVersion'])

                if resultInstallation == 0:
                    # Add postgis support
                    print("Adding postgis support ...")
                    src = pathVariable.rootDirectory + "\\winShareLib\\postgis"
                    dest = pathVariable.rootDirectory + "\\workDir\\" + savedDateTime + "\\" + version[
                        'fullVersion'] + "\\build\\" + version['majorVersion']
                    copyFile.copy(src, dest)

                    # copying documentation into installation directory
                    print("copying documentation files ...")
                    for version in configFile.decoded['v']:
                        # documentation
                        src = pathVariable.rootDirectory + "\\workDir\\" + savedDateTime + "\\" + version[
                            "fullVersion"] + "\\src\\postgresql-" + version["fullVersion"] \
                              + "\\doc\\src\\sgml\\html"
                        dest = pathVariable.rootDirectory + "\\workDir\\" + savedDateTime + "\\" + version[
                            'fullVersion'] + "\\build\\" + version['majorVersion'] + "\\doc"
                        copyFile.copy(src, dest)
                    time.sleep(3)

                else:
                    print("Something went wrong with installation process please refer to install log file to see details")
            else:
                print("Something went wrong with regression process please refer to regression log file to see details")
        else:
            print("Something went wrong with build process please refer to build log file to see details")


elif operatingSystem is "Linux":
    print("...")
else:
    print("Undefined platform found = ", os);