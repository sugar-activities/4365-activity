#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   CeibalRadio.py por:
#   Flavio Danesse <fdanesse@gmail.com>
#   Ceibal Jam - Uruguay - Plan Ceibal
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

from sugar.activity import activity

import gtk
import pygtk
pygtk.require("2.0")

from VistaReproductor import VistaReproductor

class CeibalRadioActivity(activity.Activity):

	def __init__(self,handle):

		activity.Activity.__init__(self,handle,False)

		self.set_title("Ceibal_Radio")

	        self.celeste1  = gtk.gdk.Color(0, 42000, 42000, 1)

		barraprincipal = activity.ActivityToolbox(self)

		# Vista Reproductor
		vistareproductor = VistaReproductor()
		#etiquetareproductor = gtk.Label("Mi Música")

		self.set_toolbox(barraprincipal)
		self.set_canvas(vistareproductor)
		#self.set_tray(barradestado,gtk.POS_BOTTOM)

		self.show_all()


