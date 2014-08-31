#  Copyright (C) 2014 lightberry.eu
#
#  This Program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2, or (at your option)
#  any later version.
#
#  This Program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with XBMC; see the file COPYING.  If not, write to
#  the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.
#  http://www.gnu.org/copyleft/gpl.html
import urllib
import os
import re
import subprocess

infoStr = "/// ***\n" \
          "        /// Section for \"grabber-v4l2\" commented out.\n" \
          "        /// Configure v4l to use this feature\n"

tempFolder = "/tmp/"

configOptions = {'hyperion': 'hyperion.config.json', 'boblight': 'boblight.conf'}


def downloadConfig(config, configFor):
    if os.uname()[1] == "raspbmc":
        lightberryRepoAddress = "http://lightberry.eu/download/General/"
        configFolder = "/etc/"
        replaceEffectsInd = False
    elif os.uname()[1] == "OpenELEC":
        lightberryRepoAddress = "http://lightberry.eu/download/General/"
        configFolder = "/storage/.config/"
        replaceEffectsInd = True
    else :
        lightberryRepoAddress = "http://lightberry.eu/download/General/"
        configFolder = "/etc/"
        replaceEffectsInd = False

    fileAddress = lightberryRepoAddress + config + "/" + configOptions[configFor]

    tempFile = tempFolder + configOptions[configFor]
    destFile = configFolder + configOptions[configFor]
    bkpFile = destFile + "_bkp"

    urllib.urlretrieve(fileAddress, tempFile)

    if replaceEffectsInd:
        replaceEffectsFolder(tempFile)

    mvFromTo(destFile,bkpFile)
    mvFromTo(tempFile,destFile)

def replaceEffectsFolder(tfile):
    tempFile = tfile + "_replace"
    destFile = tfile

    with open(destFile, 'r') as f:
        with open(tempFile, 'w+') as t:
            t.write(f.read().replace('"/opt/hyperion/effects"','"/storage/hyperion/effects"',1))

    mvFromTo(tempFile,destFile)

def execute(command):
    if os.uname()[1] == "raspbmc":
        s = True
    elif os.uname()[1] == "OpenELEC":
        s = False
    else :
        s = False

    if s:
        child = subprocess.Popen("sudo " + command, shell=True)
    else:
        child = subprocess.Popen(command, shell=True)
    child.wait()

def mvFromTo(f,t):
    execute("mv " + f + " " + t)
    execute("chmod 755 " + t)
    execute("chown root:root " + t)

def cpFromTo(f,t):
    execute("cp " + f + " " + t)
    execute("chmod 755 " + t)
    execute("chown root:root " + t)

def addonConfigUpdate(addonDir):
    lightberryAddonConfigLocalVersionFile = addonDir + "/resources/version.info"
    lightberryAddonConfigLocal = addonDir + "/resources/settings.xml"

    lightberryAddonConfigRemoteVersionFile = "http://img.lightberry.eu/xbmcAddons/config-downloaderV2/version.info"
    lightberryAddonConfigRemoteVersionTmp = addonDir + "/resources/version.info.remote"
    lightberryAddonConfigRemote = "http://img.lightberry.eu/xbmcAddons/config-downloaderV2/settings.xml"

    urllib.urlretrieve(lightberryAddonConfigRemoteVersionFile, lightberryAddonConfigRemoteVersionTmp)

    with open(lightberryAddonConfigRemoteVersionTmp, 'r') as f:
        remoteVersion = f.readline()

    with open(lightberryAddonConfigLocalVersionFile, 'r') as f:
        localVersion = f.readline()

    if remoteVersion != localVersion:
        urllib.urlretrieve(lightberryAddonConfigRemote, lightberryAddonConfigLocal)
        urllib.urlretrieve(lightberryAddonConfigRemoteVersionFile, lightberryAddonConfigLocalVersionFile)
        return True
    else:
        return False

def replaceGrabberSection():
    if os.uname()[1] == "raspbmc":
        configFolder = "/etc/"
    elif os.uname()[1] == "OpenELEC":
        configFolder = "/storage/.config/"
    else :
        configFolder = "/etc/"

    tempFile = tempFolder + configOptions["hyperion"]
    destFile = configFolder + configOptions["hyperion"]

    with open(destFile, 'r') as f:
        with open(tempFile, 'w+') as t:
            t.write(re.sub(r"(\"grabber-v4l2\")+(.*)\n((.*)\{([\s\S]*?)\}(.*),)",infoStr, f.read(), re.MULTILINE))

    mvFromTo(tempFile, destFile)

def copyFromUsb(configFor):
    if os.uname()[1] == "raspbmc":
        configFolder = "/etc/"
    elif os.uname()[1] == "OpenELEC":
        configFolder = "/storage/.config/"
    else :
        configFolder = "/etc/"

    destFile = configFolder + configOptions[configFor]

    filePath = findFileToCopy(configOptions[configFor])
    if filePath != "":
        cpFromTo(filePath,destFile)
    else:
        raise Exception("File not found")

def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)

    return ""

def findFileToCopy(fileName):
    try:
        usbMediaPath = "/media"
        return find(fileName, usbMediaPath)
    except:
        return ""