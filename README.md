Lightberry Config Download
==========================

Simple plugin to easily download hyperion/boblight config files. 

What it has to offer:
---------------------
   * Downloads hyperion/boblight configs for different led placements (horizontal x vertical)
   * Differentiate between OpenELEC (different config and effects placement) and other systems
   * Replace grabber section (causes hyperion to fail if there is no /dev/video device)

How to install:
---------------
   1. Download latest release from [github releases](https://github.com/tszczerba/lightberry-config-downloader/releases)
   2. Copy to raspberry pi or make avaliable in local network (you can use smb e.g. \\raspbmc or \\openelec)
   3. From XBMC menu go **System** -> **Add-ons** -> **Install from zip file** -> *Find zip file from previous point and install it*
   4. Plugin should appear under **Programs** menu
   5. For easy access go **System** -> **Appearance** -> **Skin** -> **Settings** *Click on what appears to be just a spacer* -> **Add-on Shortcuts** -> **Home Page Programs Sub-menu** -> *Set plugin on desired position* (first two are already taken by raspbmc specific add-ons if you are running raspbmc, so pick 3rd or forward place in this case)

Please create issues, functionality requests here - I can use any sugestion, I'm python begginner. Thank you in advance.
