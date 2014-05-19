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
import subprocess

import HyperionControl


configFolder = "/etc/"
tempFolder = "/tmp/"

lightberryRepoAddress = "http://lightberry.eu/download/General/"
configOptions = {'hyperion': 'hyperion.config.json', 'boblight': 'boblight.conf'}

hss = HyperionControl.HyperionControl()


def downloadConfig(config, configFor):
    fileAddress = lightberryRepoAddress + config + "/" + configOptions[configFor]

    tempFile = tempFolder + configOptions[configFor]
    destFile = configFolder + configOptions[configFor]
    bkpFile = destFile + "_bkp"

    urllib.urlretrieve(fileAddress, tempFile)

    execute("mv " + destFile + " " + bkpFile, sudo=True)
    execute("chmod 755 " + bkpFile, sudo=True)
    execute("chown root:root " + bkpFile, sudo=True)
    execute("mv " + tempFile + " " + destFile, sudo=True)
    execute("chmod 755 " + destFile, sudo=True)
    execute("chown root:root " + destFile, sudo=True)

    hss.service("restart")


def execute(command, sudo=False):
    if sudo:
        child = subprocess.Popen("sudo " + command, shell=True)
    else:
        child = subprocess.Popen(command, shell=True)
    child.wait()


def addonConfigUpdate(addonDir):
    """

    :rtype : bool
    """
    lightberryAddonConfigLocalVersionFile = addonDir + "/resources/version.info"
    lightberryAddonConfigLocal = addonDir + "/resources/settings.xml"

    lightberryAddonConfigRemoteVersionFile = "http://img.lightberry.eu/xbmcAddons/config-downloader/version.info"
    lightberryAddonConfigRemoteVersionTmp = addonDir + "/resources/version.info.remote"
    lightberryAddonConfigRemote = "http://img.lightberry.eu/xbmcAddons/config-downloader/settings.xml"

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