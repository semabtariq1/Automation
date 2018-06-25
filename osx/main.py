import os
import time
import configFile
import paths
import currentDateTime
import srcDownload.download
import srcInstallation.installation
import copyFile
import configuration
import regression
import build
import install


install = install.Install()
build = build.Build()
regression = regression.Regression()
configuration = configuration.Configuration()
copyFile = copyFile.CopyFile()
srcInstallation = srcInstallation.installation.Install()
srcDownload = srcDownload.download.Download()
currentDateTime = currentDateTime.savedDateTime
configFile = configFile.ConfigFile()
paths = paths.Path()



print("\n*********************************************************************\n")
print("\n                        Starting automation                          \n")
print("\n*********************************************************************\n")
time.sleep(3)

# Setting up folder structure
dirBuild = ""
print("Setting up folder structure")
for version in configFile.decoded['v']:
    dirSrc = paths.root+ "/workDir/"+currentDateTime+ "/"+ version['fullVersion']+"/src"
    dirLog = paths.root+ "/workDir/"+currentDateTime+ "/"+ version['fullVersion']+"/logs"
    dirBuild = paths.root + "/workDir/" + currentDateTime + "/" + version[
        'fullVersion'] + "/build/" + version['majorVersion']

    if not os.path.exists(dirSrc):
        os.makedirs(dirSrc)
        print(dirSrc)
    if not os.path.exists(dirLog):
        os.makedirs(dirLog)
        print(dirLog)
    if not os.path.exists(dirBuild):
        os.makedirs(dirBuild)
        print(dirBuild)


if configFile.postgresql == 1:
    print("Downloading postgres ...")
    for version in configFile.decoded['v']:
        downloadResult = srcDownload.download(version["url"], version["fullVersion"])

        if downloadResult == 0:
            # unzipping the postgresql
            print("Unzipping the postgresql ...")
            resultUnzip = srcInstallation.unzipPostgresql(version["fullVersion"])

            if resultUnzip == 0:
                # Downloading postgis
                print("Downloading postgis ...")
                postgisVersion = ""
                for postgis in configFile.decodedPostgis['postgisV']:
                    srcDownload.download(postgis["url"], version["fullVersion"])
                    postgisVersion = postgis["fullVersion"]

                    # Unzipping postgis
                    print("Unzipping postgis ...")
                    srcInstallation.unzipPostgis(version["fullVersion"], postgis["fullVersion"])


                # Setting paths
                os.environ['PYTHON_HOME'] = "/Users/2ndquadrant/2UDA/Python-3.4.4/inst"
                os.environ['OPENSSL_HOME'] = "/Users/2ndquadrant/2UDA/openssl-1.0.2g/inst"
                os.environ['LD_LIBRARY_PATH'] = os.environ['PYTHON_HOME'] + "/lib:" + os.environ[
                    'OPENSSL_HOME'] + "/lib:/Users/2ndquadrant/pythonAutomation/srcBuild/lib"
                os.environ['LDFLAGS'] = "-Wl,-rpath," + os.environ['PWD'] + " -L" + os.environ[
                    'PYTHON_HOME'] + "/lib -L" + os.environ[
                                            'OPENSSL_HOME'] + "/lib -L/Users/2ndquadrant/pythonAutomation/srcBuild/lib"
                os.environ['CPPFLAGS'] = "-I" + os.environ['PYTHON_HOME'] + "/include/python3.4m" + " -I" + os.environ[
                    'OPENSSL_HOME'] + "/include -I/Users/2ndquadrant/pythonAutomation/srcBuild/include"
                os.environ['PYTHON'] = "/Users/2ndquadrant/2UDA/Python-3.4.4/inst/bin/python3"


                # Running configure
                print("Running configure ...")
                configuration.runConfiguration(version['fullVersion'], version["majorVersion"])

                # Running build
                print("Running build ...")
                build.runBuild(version["fullVersion"])


                # Running install
                print("Running install ...")
                install.runInstall(version["fullVersion"])



                print("\n*********************************************************************\n")
                print("\n                       Adding Postgis feature                        \n")
                print("\n*********************************************************************\n")
                time.sleep(3)


                # Running configure on postgis
                print("Running configure on postgis ...")
                os.system("cd "+paths.currentProject+"/"+version["fullVersion"]+"/src/postgis-"+postgisVersion+" && ./configure --prefix=/Users/2ndquadrant/pythonAutomation/srcBuild --with-pgconfig="+paths.currentProject+"/"+version["fullVersion"]+"/build/"+version["majorVersion"]+"/bin/pg_config --with-gdalconfig=/Users/2ndquadrant/pythonAutomation/srcBuild/bin/gdal-config  --with-geosconfig=/Users/2ndquadrant/pythonAutomation/srcBuild/bin/geos-config --with-projdir=/Users/2ndquadrant/pythonAutomation/srcBuild > "+paths.currentProject+"/"+version["fullVersion"]+"/logs/postgisConfigure.log 2>&1")

                # Running build
                print("Running make ...")
                os.system("cd "+paths.currentProject+"/"+version["fullVersion"]+"/src/postgis-"+postgisVersion+" && make > "+paths.currentProject+"/"+version["fullVersion"]+"/logs/postgisBuild.log 2>&1")

                # Running regression
                print("Running regression ...")
                os.system("cd " + paths.currentProject + "/" + version[
                    "fullVersion"] + "/src/postgis-" + postgisVersion + " && make check> " + paths.currentProject + "/" +
                          version["fullVersion"] + "/logs/postgisRegression.log 2>&1")

                # Running install
                print("Running make install ...")
                os.system("cd "+paths.currentProject+"/"+version["fullVersion"]+"/src/postgis-"+postgisVersion+" && make install > "+paths.currentProject+"/"+version["fullVersion"]+"/logs/postgisInstall.log 2>&1")

                print("\n*********************************************************************\n")
                print("\n                      Finalizing the automation                      \n")
                print("\n*********************************************************************\n")
                time.sleep(3)

                # Copying required libraries to build
                print("Copying required libraries to build ...")
                src= paths.shareLib
                dest = ""+paths.currentProject+"/"+version["fullVersion"]+"/build/"+version["majorVersion"]+"/"
                copyFile.copy(src, dest)

                # Setting RunTime path
                # Bin
                binPath = paths.currentProject + "/" + version["fullVersion"] + "/build/" + version[
                    "majorVersion"] + "/bin"
                print("Setting RPATH for bin ...")
                for file in os.listdir(binPath):
                    os.system(
                        'cd ' + binPath + ' && install_name_tool -add_rpath @executable_path/../lib "./' + file + '" >> ' + paths.currentProject + "/" +
                        version["fullVersion"] + "/logs/binRpath.log 2>&1")

                # Lib
                libPath = paths.currentProject + "/" + version["fullVersion"] + "/build/" + version[
                    "majorVersion"] + "/lib"
                print("Setting RPATH for lib ...")
                for file in os.listdir(libPath):
                    os.system(
                        'cd ' + libPath + ' && install_name_tool -add_rpath @executable_path/../lib "./' + file + '" >> ' + paths.currentProject + "/" +
                        version["fullVersion"] + "/logs/libRpath.log 2>&1")


                # copying documentation files
                print("copying documentation files ...")
                src = paths.root + "/workDir/" + currentDateTime + "/" + version[
                        "fullVersion"] + "/src/postgresql-" + version["fullVersion"] \
                          + "/doc/src/sgml/html"
                dest = paths.root + "/workDir/" + currentDateTime + "/" + version[
                        'fullVersion'] + "/build/" + version['majorVersion'] + "/doc"
                copyFile.copy(src, dest)


                # Removing extra files
                os.system(
                    "rm -rf postgresql-" + version["fullVersion"] + ".tar.gz postgis-" + postgisVersion + ".tar.gz")

                # Generating zip file
                print("Generating zip file ...")
                os.system("cd " + paths.currentProject + "/" + version[
                    "fullVersion"] + " && tar -zcvf postgresql-osx.tar.gz build > " + paths.currentProject + "/" +
                        version["fullVersion"] + "/logs/zip.log 2>&1")

                print("\n*********************************************************************\n")
                print("\n                           Process completed                         \n")
                print("\n*********************************************************************\n")
                # Final message
                print("All binaries are placed at : "+ dirBuild)

            else:
                print("Something went wrong with unzipping the postgresql")
        else:
            print("Something went wrong with downloading step please refer download.log file for more details")