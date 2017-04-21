#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   BarradeReproduccion.activity.py por:
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
#!/usr/bin/env python

import gtk
import pygtk
pygtk.require ("2.0")

from sugar.activity import activity

class BarradeReproduccion(gtk.HBox):

	def __init__(self):

		self.directoriodeiconos = activity.get_bundle_path() + "/Iconos/"

        	self.gris = gtk.gdk.Color(50000, 50000, 50000, 1)
        	self.rosado = gtk.gdk.Color(65000,13000,25000,1)

        	gtk.HBox.__init__(self, False,5)

		self.ajuste = gtk.Adjustment(0,0,100,1,1)
		self.barradeprogreso = gtk.HScrollbar(self.ajuste)
                self.barradeprogreso.modify_bg(gtk.STATE_NORMAL, self.rosado)

		#self.barradeprogreso.connect("value-changed", self.srollmove)

		self.etiqueta_progreso = gtk.Label("¡¡¡ CeibalRadio !!!")
		caja_progreso = gtk.VBox()
		caja_progreso.pack_start(self.barradeprogreso, True,True,5)
		caja_progreso.pack_start(self.etiqueta_progreso, True, True, 0)
		self.pack_start(caja_progreso, True, True, 5)
		
		caja_de_botones = gtk.HBox(False, 0)
		# ****** BOTON_ATRAS
                self.imagenatras = gtk.Image()
                self.imagenatras.set_from_file(self.directoriodeiconos + "atras.png")
                self.botonatras = gtk.Button()
                self.botonatras.modify_bg(gtk.STATE_NORMAL, self.gris)
                self.botonatras.add(self.imagenatras)
                #self.botonatras.connect("clicked",self.clickenatras)
                caja_de_botones.pack_start(self.botonatras, False, False,5)

		# ****** BOTON PLAY
        	self.imagenplay = gtk.Image()
        	self.imagenplay.set_from_file(self.directoriodeiconos + "play.png")
        	self.botonplay = gtk.Button()
		self.botonplay.modify_bg(gtk.STATE_NORMAL, self.gris)
        	self.botonplay.add(self.imagenplay)
		#self.botonplay.connect("clicked",self.clickenplay_pausa)
        	caja_de_botones.pack_start(self.botonplay, False, False,5)

		# ****** BOTON SIGUIENTE
                self.imagensiguiente = gtk.Image()
                self.imagensiguiente.set_from_file(self.directoriodeiconos + "siguiente.png")
                self.botonsiguiente = gtk.Button()
                self.botonsiguiente.modify_bg(gtk.STATE_NORMAL, self.gris)
                self.botonsiguiente.add(self.imagensiguiente)
                #self.botonsiguiente.connect("clicked",self.clickensiguiente)
                caja_de_botones.pack_start(self.botonsiguiente, False, False,5)

		# ****** BOTON STOP
        	self.imagenstop = gtk.Image()
        	self.imagenstop.set_from_file(self.directoriodeiconos + "stop.png")
        	self.botonstop = gtk.Button()
		self.botonstop.modify_bg(gtk.STATE_NORMAL, self.gris)
        	self.botonstop.add(self.imagenstop)
		#self.botonstop.connect("clicked",self.clickenstop)
        	caja_de_botones.pack_start(self.botonstop, False, False,5)

		# ****** BOTON ABRIR DIRECTORIO
        	self.imagenabrir = gtk.Image()
        	self.imagenabrir.set_from_file(self.directoriodeiconos + "abrir.png")
        	self.botonabrir = gtk.Button()
		self.botonabrir.modify_bg(gtk.STATE_NORMAL, self.gris)
        	self.botonabrir.add(self.imagenabrir)
		#self.botonabrir.connect("clicked",self.clickenabrir)
        	caja_de_botones.pack_start(self.botonabrir, False, False,5)
	
		self.etiqueta_hora = gtk.Label("Hora")
		caja_de_botones_y_hora = gtk.VBox()
		caja_de_botones_y_hora.pack_start(caja_de_botones, False, False,5)
		caja_de_botones_y_hora.pack_start(self.etiqueta_hora, False, False,5)

		self.pack_start(caja_de_botones_y_hora, False, False,5)

		self.show_all()

	def actualizar_etiqueta(self, longitud_de_reproduccion, longitud_reproducida):
		
		if longitud_de_reproduccion > longitud_reproducida:
			porcentaje = str(longitud_reproducida * 100 / longitud_de_reproduccion) + "%"
			self.ajuste.upper = longitud_de_reproduccion
			self.ajuste.value = longitud_reproducida
		else:
			porcentaje = "--. Escuchando una Radio en la web .--"
			self.ajuste.upper = 100
			self.ajuste.value = 50

		self.etiqueta_progreso.set_text(porcentaje)

	def mostrar_carga_del_buffer(self, porcentaje):
		self.etiqueta_progreso.set_text("Buffer al " + str(porcentaje) + "%")
		self.ajuste.upper = 100
		self.ajuste.value = porcentaje

	def actualizarimagenes(self, widget, estado):
		if estado == "detenido":
			self.imagenplay.set_from_file(self.directoriodeiconos + "play.png")
		if estado == "reproduciendo":
			self.imagenplay.set_from_file(self.directoriodeiconos + "pausa.png")
		if estado == "pausado":
			self.imagenplay.set_from_file(self.directoriodeiconos + "play.png")

	def clickenplay_pausa(self,widget):
		pass		

	def clickenstop(self,widget):
		pass

	def clickenabrir(self,widget):
		pass

	def clickenatras(self,widget):
		pass

	def clickensiguiente(self, widget):
		pass


