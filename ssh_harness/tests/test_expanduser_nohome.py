# -*- coding: utf-8-unix; -*-
#
#  Copyright © 2014-2015, Nicolas CANIART <nicolas@caniart.net>
#
#  This file is part of vcs-ssh.
#
#  vcs-ssh is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License version 2 as
#  published by the Free Software Foundation.
#
#  vcs-ssh is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with vcs-ssh.  If not, see <http://www.gnu.org/licenses/>.
#
from __future__ import print_function, unicode_literals
import os
import pwd
from unittest import TestCase

from ssh_harness import expanduser_nohome


class ExpandUserNoHomeTestCase(TestCase):

    def setUp(self):
        self._OLDHOME = os.environ.get('HOME', None)
        self._REALHOME = pwd.getpwuid(os.getuid()).pw_dir
        os.environ['HOME'] = self._REALHOME

    def tearDown(self):
        if self._OLDHOME is not None:
            os.environ['HOME'] = self._OLDHOME

    def test_expanduser_nohome_home_is_same_as_in_passwd_db(self):
        res = expanduser_nohome('~/to/go')

        self.assertEqual(res,
                         os.path.join(self._REALHOME, 'to/go'))

    def test_expanduser_nohome_home_spoofed(self):
        os.environ['HOME'] = '/some/directory'

        res = expanduser_nohome('~/to/go')

        self.assertEqual(res,
                         os.path.join(self._REALHOME, 'to/go'))

    def test_expanduser_nohome_no_tilda(self):
        path = '/some/path/to/go'
        res = expanduser_nohome(path)

        self.assertEqual(path, res)

    def test_expanduser_nohome_tilda_not_the_first_char(self):
        path = '/~some/path/to/go'
        res = expanduser_nohome(path)

        self.assertEqual(path, res)


# vim: syntax=python:sws=4:sw=4:et:
