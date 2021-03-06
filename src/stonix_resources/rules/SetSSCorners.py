###############################################################################
#                                                                             #
# Copyright 2015.  Los Alamos National Security, LLC. This material was       #
# produced under U.S. Government contract DE-AC52-06NA25396 for Los Alamos    #
# National Laboratory (LANL), which is operated by Los Alamos National        #
# Security, LLC for the U.S. Department of Energy. The U.S. Government has    #
# rights to use, reproduce, and distribute this software.  NEITHER THE        #
# GOVERNMENT NOR LOS ALAMOS NATIONAL SECURITY, LLC MAKES ANY WARRANTY,        #
# EXPRESS OR IMPLIED, OR ASSUMES ANY LIABILITY FOR THE USE OF THIS SOFTWARE.  #
# If software is modified to produce derivative works, such modified software #
# should be clearly marked, so as not to confuse it with the version          #
# available from LANL.                                                        #
#                                                                             #
# Additionally, this program is free software; you can redistribute it and/or #
# modify it under the terms of the GNU General Public License as published by #
# the Free Software Foundation; either version 2 of the License, or (at your  #
# option) any later version. Accordingly, this program is distributed in the  #
# hope that it will be useful, but WITHOUT ANY WARRANTY; without even the     #
# implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.    #
# See the GNU General Public License for more details.                        #
#                                                                             #
###############################################################################
'''
Created on Apr 27, 2015
The screen saver should be set to turn on after a period of inactivity, and should require a password to dismiss. 
Disabling the screen saver would disable the screen lock. This rule removes the functionality of using a 'hot corner'
to disable the screen saver.
@author: Breen Malmberg
'''

from __future__ import absolute_import
import os
import re
import traceback
from ..rule import Rule
from ..logdispatcher import LogPriority
from ..CommandHelper import CommandHelper


class SetSSCorners(Rule):
    '''
    classdocs
    '''

    def __init__(self, config, environ, logger, statechglogger):
        '''
        Constructor
        '''
        Rule.__init__(self, config, environ, logger, statechglogger)
        self.logger = logger
        self.rulenumber = 188
        self.rulename = 'SetSSCorners'
        self.compliant = True
        self.formatDetailedResults("initialize")
        self.mandatory = True
        self.rootrequired = False
        self.helptext = "The screen saver should be set to turn on after a period of inactivity, and should require a password to dismiss. " + \
"Disabling the screen saver would disable the screen lock. This rule removes the functionality of using a 'hot corner' " + \
"to disable the screen saver."
        self.guidance = ['CIS', '1.4.8.1', '1.4.8.2']
        self.applicable = {'type': 'white',
                           'os': {'Mac OS X': ['10.9', 'r', '10.10.5']}}

        # set up configuration items for this rule
        datatype = 'bool'
        key = 'SetSSCorners'
        instructions = 'To disable this rule, set the value of ' + \
        'SetSSCorners to False'
        default = True
        self.ci = self.initCi(datatype, key, instructions, default)

    def setVars(self):
        '''
        '''

        ssfound = False

        try:

            self.homedir = self.environ.geteuidhome()
            self.conffile = self.homedir + '/Library/Preferences/com.apple.dock.plist'
            self.readcmd = '/usr/bin/defaults read ' + self.conffile
            self.optlist = ["wvous-bl-corner",
                            "wvous-br-corner",
                            "wvous-tl-corner",
                            "wvous-tr-corner"]
            self.optdict = {}
            self.writecmd = '/usr/bin/defaults write ' + self.conffile
            self.detailedresults = ""
            self.cmdhelper = CommandHelper(self.logger)
            self.compliant = True
            self.moddict = {}
            for opt in self.optlist:
                self.cmdhelper.executeCommand(self.readcmd + ' ' + opt)
                output = self.cmdhelper.getOutputString()
                if re.search('^5', output):
                    self.optdict[opt] = 5
                    ssfound = True
                else:
                    self.optdict[opt] = 1
            if not ssfound:
                self.optdict = {"wvous-bl-corner": 1,
                                "wvous-br-corner": 1,
                                "wvous-tl-corner": 1,
                                "wvous-tr-corner": 5}

        except Exception:
            raise

    def report(self):
        '''
        '''

        found = False

        try:

            if self.environ.geteuid() == 0:
                self.detailedresults += '\nYou are running SetSSCorners in Admin mode. This rule must be run in regular user context.'
                self.logger.log(LogPriority.WARNING, self.detailedresults)
                return False

            self.setVars()

            if os.path.exists(self.conffile):
                for item in self.optdict:
                    self.cmdhelper.executeCommand(self.readcmd + ' ' + item)
                    output = self.cmdhelper.getOutputString()
                    errout = self.cmdhelper.getErrorString()
                    sitem = item.split('-')
                    location = str(sitem[1])
                    if errout:
                        self.compliant = False
                        self.detailedresults += '\nspecified key not found : ' + str(item)
                    elif re.search('^6', output):
                        self.compliant = False
                        self.detailedresults += '\nincorrect configuration value for key: ' + str(item)
                        self.moddict['wvous-' + location + '-modifier'] = 1048576
                    elif re.search('^5', output):
                        found = True
                        self.moddict['wvous-' + location + '-modifier'] = 0
                if not found:
                    self.compliant = False
                    self.detailedresults += '\nno corner is configured to activate screen saver'

            else:
                self.compliant = False
                self.detailedresults += '\nrequired configuration file com.apple.dock.plist could not be found'

        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception:
            self.detailedresults += traceback.format_exc()
            self.logdispatch.log(LogPriority.ERROR, self.detailedresults)
        self.formatDetailedResults("report", self.compliant,
                                   self.detailedresults)
        self.logdispatch.log(LogPriority.INFO, self.detailedresults)
        return self.compliant

    def fix(self):
        '''
        '''

        success = True

        try:

            if self.environ.geteuid() == 0:
                self.detailedresults += '\nYou are running SetSSCorners in Admin mode. This rule must be run in regular user context.'
                self.logger.log(LogPriority.WARNING, self.detailedresults)
                return False

            if os.path.exists(self.conffile):
                if self.ci.getcurrvalue():
                    for item in self.optdict:
                        cmd = self.writecmd + ' ' + item + ' -int ' + str(self.optdict[item])
                        self.cmdhelper.executeCommand(cmd)
                        errout = self.cmdhelper.getErrorString()

                        if errout:
                            success = False
                            self.detailedresults += '\nunable to execute command ' + str(cmd)
            if self.moddict:
                for item in self.moddict:
                    cmd = self.writecmd + ' ' + item + ' -int ' + str(self.moddict[item])
                    self.cmdhelper.executeCommand(cmd)
                    errout = self.cmdhelper.getErrorString()
                    if errout:
                        success = False

        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception:
            self.detailedresults += traceback.format_exc()
            self.logdispatch.log(LogPriority.ERROR, self.detailedresults)
        self.formatDetailedResults("fix", success,
                                   self.detailedresults)
        self.logdispatch.log(LogPriority.INFO, self.detailedresults)
        return success
