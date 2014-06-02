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
import sys
import os

import xbmcaddon
import xbmc
from resources.lib import ConfigDownload, HyperionControl


__author__ = "Tomek (lightberry.eu)"
__url__ = "http://lightberry.eu"
__addonname__ = "Lightberry Config Downloader"
__svn_url__ = ""
__credits__ = "Hyperion Switcher plugin for Raspbmc written and maintained by lightberry.eu"
__icon__ = "./icon.png"

__settings__ = xbmcaddon.Addon()
__addondir__ = __settings__.getAddonInfo('path')

delayTime = 5000
msgLine = ""
exceptionLine = ""
devVideoName = "/dev/video"

ledConfigPrev = __settings__.getSetting("ledConfig")
ledControlSystemPrev = __settings__.getSetting("ledControlSystem")

if ConfigDownload.addonConfigUpdate(__addondir__):
    msgLine = "Successfully downloaded new addon configuration."
    xbmc.executebuiltin('Notification(%s, %s, %d, %s)' % (__addonname__, msgLine, delayTime, __icon__))
else:
    msgLine = "Addon Configuration is up to date."
    xbmc.executebuiltin('Notification(%s, %s, %d, %s)' % (__addonname__, msgLine, delayTime, __icon__))

try:
    __settings__.openSettings()
except KeyboardInterrupt, SystemExit:
    sys.exit(0)

if __settings__.getSetting("downloadNow") == "true" \
        or ledConfigPrev != __settings__.getSetting("ledConfig")\
        or ledControlSystemPrev != __settings__.getSetting("ledControlSystem"):
    try:
        ConfigDownload.downloadConfig(__settings__.getSetting("ledConfig"),
                                      __settings__.getSetting("ledControlSystem"))

        if (os.uname()[1] != "OpenELEC") :
            msgLine = "Successfully downloaded configuration " + __settings__.getSetting(
            "ledConfig") + " for " + __settings__.getSetting("ledControlSystem")

        else:
            msgLine = "Successfully downloaded configuration " + __settings__.getSetting(
            "ledConfig") + " for " + __settings__.getSetting("ledControlSystem") + ".\n" \
                                                                                   " Restart Raspberry Pi to apply settings."

    except:
        msgLine = "Error occurred. Check your internet connection."

    xbmc.executebuiltin('Notification(%s, %s, %d, %s)' % (__addonname__, msgLine, delayTime, __icon__))


    if ((os.path.exists(devVideoName) and __settings__.getSetting("grabberReplaceLogic") == "Default") \
            or __settings__.getSetting("grabberReplaceLogic") == "Force replace") \
            and __settings__.getSetting("ledControlSystem") == "hyperion":
        
        ConfigDownload.replaceGrabberSection()

        msgLine = "Grabber section replaced "
        xbmc.executebuiltin('Notification(%s, %s, %d, %s)' % (__addonname__, msgLine, delayTime, __icon__))

hss = HyperionControl.HyperionControl()
hss.service("restart")

__settings__.setSetting("downloadNow","false")