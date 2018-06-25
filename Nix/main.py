import os

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


os.environ['PYTHON_HOME']="/usr/bin"
os.environ['LD_LIBRARY_PATH']="/usr/lib"
os.environ['LDFLAGS']="-WL, -rpath,"+os.environ['pwd']+" -L/usr/lib"
os.environ['CPPFLAGS']="-I/usr/include/python3.5m"
os.environ['PYTHON']="/usr/bin/python3"




# Setting up folder structure
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


                # Running configure
                print("Running configure ...")
                configuration.runConfiguration(version['fullVersion'], version["majorVersion"])

                # Running build
                print("Running build ...")
                build.runBuild(version["fullVersion"])

                # Running regression
                print("Running regression ...")
                regression.runRegression(version["fullVersion"])

                # Running install
                print("Running install ...")
                install.runInstall(version["fullVersion"])


                print("\n*********************************************************************\n")
                print("\n                       Adding Postgis feature                        \n")
                print("\n*********************************************************************\n")


                # Running configure on postgis
                print("Running configure on postgis ...")
                os.system("cd "+paths.currentProject+"/"+version["fullVersion"]+"/src/postgis-"+postgisVersion+" && ./configure --prefix=/opt/linux_shared_lib --with-pgconfig="+paths.currentProject+"/"+version["fullVersion"]+"/build/"+version["majorVersion"]+"/bin/pg_config --with-gdalconfig=/opt/linux_shared_lib/bin/gdal-config  --with-geosconfig=/opt/linux_shared_lib/bin/geos-config --with-projdir=/opt/linux_shared_lib > "+paths.currentProject+"/"+version["fullVersion"]+"/logs/postgisConfigure.log 2>&1")

                # Running build
                print("Running make ...")
                os.system("cd "+paths.currentProject+"/"+version["fullVersion"]+"/src/postgis-"+postgisVersion+" && make > "+paths.currentProject+"/"+version["fullVersion"]+"/logs/postgisBuild.log 2>&1")

                # Running regression
                print("Running regression ...")
                os.system("cd " + paths.currentProject + "/" + version[
                    "fullVersion"] + "/src/postgis-" + postgisVersion + " && make check > " + paths.currentProject + "/" +
                          version["fullVersion"] + "/logs/postgisRegression.log 2>&1")

                # Running install
                print("Running make install ...")
                os.system("cd "+paths.currentProject+"/"+version["fullVersion"]+"/src/postgis-"+postgisVersion+" && make install > "+paths.currentProject+"/"+version["fullVersion"]+"/logs/postgisInstall.log 2>&1")


                # Copying required libraries to build
                print("Copying required libraries to build ...")
                src = paths.shareLib
                dest = ""+paths.currentProject+"/"+version["fullVersion"]+"/build/"+version["majorVersion"]+"/"
                copyFile.copy(src, dest)

                # Setting Rpath
                binPath = paths.currentProject+"/"+version["fullVersion"]+"/build/"+version["majorVersion"]+"/bin"
                print("Setting RPATH for bin ...")
                for file in os.listdir(binPath):
                    os.system('cd '+binPath+' && chrpath -r "\${ORIGIN}/../lib/" ./'+file+" > "+paths.currentProject+"/"+version["fullVersion"]+"/logs/binRpath.log 2>&1")

                libPath = paths.currentProject+"/"+version["fullVersion"]+"/build/"+version["majorVersion"]+"/lib"
                print("Setting RPATH for lib ...")
                for file in os.listdir(libPath):
                    os.system('cd '+libPath+' && chrpath -r "\${ORIGIN}/../lib/" ./' + file+ " > "+paths.currentProject+"/"+version["fullVersion"]+"/logs/libRpath.log 2>&1")

                # Copying documentation
                print("copying documentation files ...")
                src = paths.root + "/workDir/" + currentDateTime + "/" + version[
                    "fullVersion"] + "/src/postgresql-" + version["fullVersion"] \
                    + "/doc/src/sgml/html"
                dest = paths.root + "/workDir/" + currentDateTime + "/" + version[
                    'fullVersion'] + "/build/" + version['majorVersion'] + "/doc"
                copyFile.copy(src, dest)

                # Removing extra files
                os.system("rm -rf postgresql-"+version["fullVersion"]+".tar.gz postgis-"+postgisVersion+".tar.gz")


                # Generating zip file
                print("Generating zip file ...")
                os.system("cd "+paths.currentProject+"/"+version["fullVersion"]+" && tar -zcvf postgresql-linux.tar.gz build > "+paths.currentProject+"/"+version["fullVersion"]+"/logs/zip.log 2>&1")

                # Final message
                print("All binaries are placed at : " + dirBuild)
            else:
                print("Something went wrong with unzipping the postgresql")
        else:
            print("Something went wrong with downloading step please refer download.log file for more details")