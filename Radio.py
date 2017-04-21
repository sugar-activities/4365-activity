#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Radio.py por:
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

import gtk
import pygtk
pygtk.require("2.0")

import pango

class Radio(gtk.Button):

	def __init__(self, datos_radio, directoriodeimagenes):
		# datos_radio es una tupla

		celeste1 = gtk.gdk.Color(0,33000,33000,1)

		self.id_en_base = datos_radio[0]
		nombrederadio = datos_radio[1]
		direccionderadio = datos_radio[2]
		anotaciones = datos_radio[3]
		pais = datos_radio[4]

		# Botón
		gtk.Button.__init__(self)
		self.modify_bg(gtk.STATE_NORMAL, celeste1)

		self.direccionderadio = direccionderadio

		bandera = None
		# Imagen Bandera
		bandera_radio = gtk.Image()
		try:
			bandera = directoriodeimagenes + pais + ".png"
			pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(bandera,60,60)
			bandera_radio.set_from_pixbuf(pixbuf)
		except Exception, e:
			print e


		# Texto informativo para la radio
		Informacion = (nombrederadio + "\n" + "Reproducción: " + direccionderadio + "\n" + "Detalle: " + anotaciones)

		# Etiqueta de Información
		self.etiquetadeinformacion = gtk.Label(Informacion)
		self.etiquetadeinformacion.modify_font(pango.FontDescription("purisa 6"))
		self.etiquetadeinformacion.modify_bg(gtk.STATE_NORMAL, celeste1)

		# Imagen "radio"
		imagenderadio = gtk.Image()
		pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(directoriodeimagenes + "radio.png",120,120)
		imagenderadio.set_from_pixbuf(pixbuf)

		# Caja contenedora del boton
		caja_principal = gtk.HBox()

		# ***** Armado de Interfaz *****
		caja_principal.pack_start(imagenderadio, False, False,5)
		caja_principal.pack_start(bandera_radio, False, False,5)
		caja_principal.pack_start(self.etiquetadeinformacion, False, False,5)
		self.add(caja_principal)
		self.show_all()

	def pintame(self, color):
		self.modify_bg(gtk.STATE_NORMAL, color)
		self.etiquetadeinformacion.modify_bg(gtk.STATE_NORMAL, color)
		
