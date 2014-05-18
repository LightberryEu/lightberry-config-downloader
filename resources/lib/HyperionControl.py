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

import subprocess

__author__ = 'lightberry.eu'


class HyperionControl:
    currentHyperionSource = ""

    hyperiondName = "hyperiond"
    hyperionPid = None

    hyperiondServiceCommand = "service hyperion"

    def __init__(self):
        self.processNum()

    def processNum(self):
        self.hyperionPid = subprocess.check_output(
            'ps -eo pid,command | grep "{0:s}" | grep -v grep | awk \'{{print $1}}\''.format(self.hyperiondName),
            shell=True)

    def service(self, mode):
        try:
            if mode.lower() == "start" or mode.lower() == "restart":
                self.processNum()
                if self.hyperionPid == "":
                    self.execute(self.hyperiondServiceCommand + " start", sudo=True)
                else:
                    self.execute(self.hyperiondServiceCommand + " restart", sudo=True)
            elif mode.lower == "stop":
                self.processNum()
                if self.hyperionPid != "":
                    self.execute(self.hyperiondServiceCommand + " stop", sudo=True)
        except subprocess.CalledProcessError:
            raise Exception("Something went wrong with hyperion service. \nIs hyperion installed?")

    @staticmethod
    def execute(command, sudo=False):
        if sudo:
            subprocess.check_call("sudo " + command, shell=True)
        else:
            subprocess.check_call(command, shell=True)

    pass