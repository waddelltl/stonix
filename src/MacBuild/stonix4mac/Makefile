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

# This makefile creates a package or a dmg from any application
# that sits next to it
# make pkg
# make dmg

USE_PKGBUILD=1

include /usr/local/share/luggage/luggage.make

pack-stonix: l_Applications
	@sudo ${CP} -R ./dist/${TITLE}.app ${WORK_D}/Applications
	@sudo chown -R root:admin ${WORK_D}/Applications/${TITLE}.app
	@sudo chmod -R +rwx ${WORK_D}/Applications/${TITLE}.app
	@-sudo /usr/bin/xattr -dr com.apple.quarantine ${WORK_D}/Applications/${TITLE}.app


pack-stonix-manpage: l_usr_man_man8
	@sudo ${INSTALL} -m 644  ${MANPG} ${MAN8PATH}/stonix.8

pack-stonix4mac-install :
	@sudo ${INSTALL} -m 755 ${PI} ${SCRIPT_D}/postinstall
	@sudo ${INSTALL} -m 755 ${PRE} ${SCRIPT_D}/preinstall

MYPWD=$(shell pwd)
TITLE := stonix4mac
REVERSE_DOMAIN=gov.lanl.ds
PACKAGE_VERSION=
PI=postinstall
PRE=preinstall
MANPG=../../usr/share/man/man8/stonix.8
MAN8PATH=/usr/share/man/man8
PAYLOAD=pack-stonix \
	pack-stonix-manpage \
	pack-stonix4mac-install


