#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Reproductor.py por:
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

import sys, os, gtk, gobject
import time
import datetime

from sugar.activity import activity

#os.environ["HELIX_LIBS"] = activity.get_bundle_path() + "/helix"
os.environ["HELIX_LIBS"] = os.getcwd() + "/helix"
helix_libs = os.environ.get("HELIX_LIBS")
sys.path.append(helix_libs)

import hxplay

class Reproductor():

	def __init__(self, vista_reproductor):

		self.vista_reproductor = vista_reproductor
		self.is_radio = False
		self.estado = "detenido"
		self.player = None
		self.on_stop_usuario = True

		self.fuentededatos = None

		self.longitud_de_reproduccion = 0
		self.longitud_reproducida = 0

		self.needRepos = 0
		self.currentPos = 0

		self.buffering = 0
		
		self.barradereproduccion = None
		self.mantener_reproduccion_en_radio = gobject.timeout_add(1000, self.mantener_reproduccion)

	def idle_function(self):
	# mientras se reproduce, captura eventos
		try:
			hxplay.doevent()
			
		except Exception, e:
			print e

		return True


	def abrirfuentededatos(self, widget, fuentededatos, is_radio):
	# Abre y Reproduce un archivo o un stream de radio
		self.on_stop_usuario = True
		self.fuentededatos = fuentededatos
		self.is_radio = is_radio
		site = None

		retrollamadas = [
                    (hxplay.ON_PRESENTATION_OPENED, self.on_presentation_opened, None),
                    (hxplay.ON_ERROR,               self.on_error,               None),
                    (hxplay.ON_PRESENTATION_CLOSED, self.on_presentation_closed, None),
                    (hxplay.ON_POS_LENGTH,          self.on_pos_length,          None),
                    (hxplay.ON_BUFFERING,           self.on_buffering,           None),
                    (hxplay.ON_PAUSE,               self.on_pause,               None),
                    (hxplay.ON_STOP,                self.on_stop,                None),
                    (hxplay.ON_BEGIN,               self.on_begin,               None)
                    ]

		if self.player == None:
			self.player = hxplay.open(self.fuentededatos, callbacks=retrollamadas, site=site)
		else:
			if self.estado == "reproduciendo":
				self.player.stop()
				#self.is_radio = is_radio # De lo contrario no funciona "mantener_reproduccion"
		
		self.player.open(self.fuentededatos)
		self.idlefunction = gobject.idle_add(self.idle_function)# Permite la reproducción
		self.player.start()
		self.estado = "reproduciendo"
		self.barradereproduccion.actualizarimagenes(None, "reproduciendo")
		print "******* Reproduciendo: ", self.fuentededatos
		self.on_stop_usuario = False


	def on_buffering(self, player, data, data1, data2):
	#Se crea el buffer
		ulArgs, bufferPercent = data2
		if (bufferPercent == 100):
			self.buffering = 0
			self.estado = "reproduciendo"
			self.longitud_de_reproduccion = int(self.player.length())
		else:
			self.buffering = 1
			self.estado = "detenido"
		self.barradereproduccion.mostrar_carga_del_buffer(bufferPercent)


	def on_pos_length(self, player, cb, args, (pos,length)):
	#Se ejecuta continuamente al iniciar la reproduccion

		if self.estado == "reproduciendo":
			if self.longitud_reproducida != int(self.player.time()):
				self.longitud_reproducida = int(self.player.time())
				self.barradereproduccion.actualizar_etiqueta(self.longitud_de_reproduccion, self.longitud_reproducida)

        	if (self.needRepos):
            		self.needRepos=0
			print "POSICION"

	def on_presentation_closed(self, player, one, two, three):
	# mientras no se reproduce nada
		print "Reproduccion Cerrada. def on_presentation_closed ", player, one, two, three
		self.estado = "detenido"

	def on_presentation_opened(self, player, one, two, three):
	# mientras se reproduce
		print "Reproduccion Abierta. def on_presentation_opened ", player, one, two, three
        	self.currentPos = 0	

	def on_begin(self, player, data, data1, data2):
	# mientras inicia
		print "Comenzando Reproducción. def on_begin", player, data, data1, data2	

    	def on_error(self, player, one, two, three):
        	severity, hxcode, usercode, msg, userstring, moreinfo = three
        	#self.mediaPlayer.error_dialog(msg, userstring)
		print "ERROR"

	def on_pause(self, player, data, data1, data2):
	# mientras está pausado
		self.estado = "pausado"
		print "Reproducción pausada. def on_pause. ", player, data, data1, data2

	def on_stop(self,player,one,two,three):
	# mientras está detenido
		print "Reproducción detenida. def on_stop ", player,one,two,three




	# **************************************************************		
	# **************** Funciones Extra hxplay **********************

	def asignacion_de_barra_de_reproduccion(self, barra):
	# La interfaz asignará una barra de reproducción a traves de esta función
		self.barradereproduccion = barra

	def mantener_reproduccion(self):
	# Se ejecuta cada segundo
		# Se ejecuta cuando no se logra cargar el buffer con la radio
		if self.estado == "detenido" and self.is_radio == True and self.on_stop_usuario == False:
			self.stop(None)
			self.abrirfuentededatos(None, self.fuentededatos, True)

		if self.estado == "detenido" and self.on_stop_usuario == False and self.is_radio == False:
			self.vista_reproductor.siguiente_tema(None)
		# el reloj
		mihora = time.strftime("%H:%M:%S")
          	self.barradereproduccion.etiqueta_hora.set_text(str(datetime.date.today()) + " " + mihora)
		return True


	def stop(self,widget):
	# Detener reproduccion
		if widget != None:
			self.on_stop_usuario = True

		if self.idlefunction:
			gobject.source_remove(self.idlefunction)

		#self.is_radio = False
		self.player.stop()

		self.estado = "detenido"
		self.barradereproduccion.actualizarimagenes(None, "detenido")
		print "Deteniendo el programa manualmente . . . def stop"


	def pause(self, widget):
	# play/Pausa reproduccion

		if self.estado == "pausado":
			#self.estado = "reproduciendo"
			self.barradereproduccion.actualizarimagenes(None, "reproduciendo")
			self.idlefunction = gobject.idle_add(self.idle_function)
			self.player.start()
		elif self.estado == "reproduciendo":
			#self.estado = "pausado"
			self.barradereproduccion.actualizarimagenes(None, "pausado")
			self.player.pause()
		elif self.estado == "detenido":
			#self.estado = "reproduciendo"
			self.barradereproduccion.actualizarimagenes(None, "reproduciendo")
			self.abrirfuentededatos(None, self.fuentededatos, self.is_radio)
		print "Pausando/Reproduciendo manualmente . . . def pause/play"


hxplay.init()

def main():
   gtk.main()
   return 0

if __name__=="__main__":
   #reproductor = Reproductor()
   #main()
   pass
