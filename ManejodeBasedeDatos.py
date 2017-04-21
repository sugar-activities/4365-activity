#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   ManejodeBasedeDatos.py por:
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

import sqlite3

class ManejodeBasedeDatos():

	def __init__(self, direcciondebase):

		self.direcciondebase = direcciondebase
		self.listaderadios = []
		self.coneccion = None
		self.basededatos = None

		print " ***** Cargado el modulo de Base:", self.direcciondebase
	def CargarRadios(self):

	    self.listaderadios = []
		
	    try:
		coneccion = sqlite3.connect(self.direcciondebase)# Conecta a la base de datos
		tabladeradios = coneccion.cursor()# Selecciona la base de datos

		tabladeradios.execute("select * from radios")

		for radio in tabladeradios:
			n = int(radio[0])
			nombre = str(radio[1])
			direccion = str(radio[2])
			pais = str(radio[3])
			descripcion = str(radio[4])

			datos_radio = (n, nombre, direccion, pais, descripcion)

			self.listaderadios.append(datos_radio)	

		tabladeradios.close() # Cierra la base
		coneccion.close()

		print " ***** Se ha cargado la base de datos:", self.direcciondebase

	    except Exception, e:
		print e

	    return self.listaderadios


	def CrearBasededatos (self):
	# Crea la base de datos inicial

	    try:
		self.coneccion = sqlite3.connect(self.direcciondebase)# Conecta a la base de datos
		self.basededatos = self.coneccion.cursor()# Selecciona la base de datos

		# Crea la tabla radios
		self.basededatos.execute("""create table radios (id_radio INTEGER PRIMARY KEY AUTOINCREMENT,
			nombre text, direccion text, anotaciones text, pais text)""")

		self.coneccion.commit() # Confirma instrucciones sql

		self.basededatos.close() # Cierra la base
		self.coneccion.close()

		print " ***** Base de Datos Creada en:", self.direcciondebase
	    except Exception, e:
		print e
	    return True

	def Llenar_Base(self):
		# Llena la base de datos con la lista de radios predeterminada

	    try:
		self.coneccion = sqlite3.connect(self.direcciondebase)# Conecta a la base de datos
		self.basededatos = self.coneccion.cursor()# Selecciona la base de datos

		# Lista de radios predeterminada
		radios = [
			(0, "Oceano FM", "http://radio2.oceanofm.com:8010", "http://oceanofm.com/ - Programacion Variada", "Uruguay"),
			(1, "Radio Sarandi 690AM", "http://radioonline.netgate.com.uy:8000/sarandi", "Programacion Variada", "Uruguay"),
			(2, "810 AM El Espectador", "http://streaming.espectador.com/envivo", "http://www.espectador.com/ - Programacion Variada", "Uruguay"),
			(3, "America FM 103.3", "http://agenda.org.uy:8118/america", "http://www.fmamericadigital.com/ - Programacion Variada", "Uruguay"),
			#(4, "1370 AM - CX 42 Ciudad de Montevideo", "http://66.45.232.218:8040/CX42",
			#	"http://www.emisoraciudaddemontevideo.com.uy/ - Programacion Variada", "Uruguay"),
			(5, "1430 AM - Radio Durazno", "http://usa8.ciudaddigital.com.uy:9000/durazno",
				"http://www.radiodurazno.com/ - Programacion Variada" , "Uruguay"),
			(6, "FM - Sur", "http://radios-online.info:6020", "http://www.surfm.net/ - Programacion Variada", "Uruguay"),
			(7, "FM 106.5 - Del Exodo", "http://agenda.org.uy:8090/als", "http://agenda.org.uy/delexodofm/ - Programacion Variada", "Uruguay"),
			(8, "FM 97.3 Conquistador", "http://usa8.ciudaddigital.com.uy:9100/fmconquistador",
				"http://www.fmconquistador.com/ - Programacion Variada", "Uruguay"),
			(9, "Rural 610 AM - Montevideo", "http://usa2.web2mil.com:8020/CX4", "http://www.cx4radiorural.com/ - Programacion Variada", "Uruguay"),
			(10, "Bulo FM - Montevideo", "http://bulofm.com:19000/", "http://www.bulofm.com/ - Programacion Variada", "Uruguay"),
			#(11, "Radio con Todos", "http://tu-panel.com:8374/", "http://www.radiocontodos.com/ - Programacion Variada", "Uruguay"),
			(12, "Rivera", "http://radios-online.info:3290/", "http://www.radiocien.com/ - Programacion Variada", "Uruguay"),
			#(13, "FM Sauce 89.1 Juan Lacaze", "http://fmsauce.no-ip.biz:8000/", "Programacion Variada", "Uruguay"),
			(14, "Uruguay", "http://radios-online.info:5000/", "Programacion Variada", "Uruguay"),
			#(15, "Uruguay", "http://usa8.ciudaddigital.com.uy:9000/sancarlos", "Programacion Variada", "Uruguay"),

			(16, "Radioshock", "http://streaming.digitalwebs.com.ar:8555/", "http://www.radioshock.net/ - Programacion Variada", "Argentina"),
			(17, "LV7 Tucuman", "http://216.155.143.196:8046/", "Musica Tropical", "Argentina"),
			(18, "Radio Norte 102.3 FM", "http://38.108.120.60:8043/", "http://www.showkolorshow.net/ - Musica Tropical", "Argentina"),
			(19, "Webradio Anitron", "http://64.15.155.49:8565/vivo", "http://anitron.osanproducciones.com/", "Argentina"),
			(20, "Amanecer FM 102.9", "http://streaming1.servidorenlinea.net:8361/", "http://www.amanecerfm.com.ar/", "Argentina"),
			(21, "La Voz 100.5 FM", "http://str3.todosaca.com:1000", "http://www.lavozfm.com.ar/", "Argentina"),
			#(22, "FM Curuzu 96.7", "http://63.247.80.34:8060/", "http://www.fmcuruzu.com.ar/", "Argentina"),
			(23, "Radio Show 88.5 FM", "http://stream.worproducciones.com.ar:9030/",
				"http://www.radioshow885.worproducciones.com.ar/inicio.php", "Argentina"),
			(24, "Estacion Terrena 91.3 FM", "http://200.58.116.222:12095/", "http://www.terrena913.com/", "Argentina"),
			(25, "El Arka 100.1 FM", "http://200.80.36.148:8010/", "http://www.radioelarka.com.ar/", "Argentina"),
			(26, "Radio Universidad CALF 103.7 FM", "http://93.104.209.170:8033/", "http://www.fm1037online.com/", "Argentina"),
			(27, "Radio Total 105.5 FM", "http://www.claxmedia.com:8015/", "http://www.105fmtotal.com.ar/", "Argentina"),
			(28, "Aire Libre 96.3 FM", "http://radios.surio.com:20/", "http://www.airelibre.com.ar/", "Argentina"),
			(29, "Dance", "http://208.43.132.56:8006", None, "Argentina"),
			#(30, "Cumbia", "http://208.43.132.56:8132", None, "Argentina"),
			#(31, "Solo Hits", "http://208.43.132.56:8002", None, "Argentina"),
			#(32, "Argentina", "http://208.43.132.56:8124", None, "Argentina"),
			#(33, "Latinos", "http://208.43.132.56:8122", None, "Argentina"),
			#(34, "Internacionales", "http://208.43.132.56:8084", None, "Argentina"),
			(35, "Elite FM", "http://200.45.184.55:8000/", "http://www.elitefm.org/", "Argentina"),
			(36, "Activa 105.9 FM", "http://208.98.36.254:8056/", "http://www.activa105.com.ar/", "Argentina"),
			#(37, "Activa 105.9 FM", "http://208.98.36.254:8056/", "http://www.activa105.com.ar/", "Argentina"),

			(38, "Radio Retro", "http://216.155.131.180:8024", "http://www.radioretro.com.br/v2/index.php", "Brasil"),
			#(39, "Fortaleza 90.7 FM", "http://174.123.166.131:8068", "http://www.somzoom.com.br/radios/fortaleza.htm", "Brasil"),
			(40, "Aracati 98.1 FM", "http://174.123.166.131:8054", "http://www.somzoom.com.br/radios/aracati.htm", "Brasil"),
			(41, "Baturite 93.3 FM", "http://174.123.166.131:8046", "http://www.somzoom.com.br/radios/baturite.htm", "Brasil"),
			#(42, "Cariri 106.5 FM", "http://174.123.166.131:8042", "http://www.somzoom.com.br/radios/cariri.htm", "Brasil"),
			(43, "Guaraciaba 1190 AM", "http://174.123.166.131:8044", "http://www.somzoom.com.br/radios/guaraciaba.htm", "Brasil"),
			(44, "Redencao 98.7 FM", "http://174.123.166.131:8050", "http://www.somzoom.com.br/radios/redencao.htm", "Brasil"),
			(45, "Sobral 105.1 FM", "http://174.123.166.131:8040", "http://www.somzoom.com.br/radios/sobral.htm", "Brasil"),

			(46, "Clasica 107.1FM", "http://ns7.scbbs.net:8000", "http://www.classicafm.com/p_inicio.asp", "Bolivia"),
			(47, "Radio CHACALTAYA FM 93.7", "http://realserver2.megalink.com:8110", "http://www.radiochacaltayafm.net/chacaltaya.php", "Bolivia"),

			(48, "AMLO", "http://stream.radioamlo.info:8010", "AMLO On Line", "Venezuela"),

			#(49, "La Nueva Republica", "http://76.73.41.107:8704/", None, "Mexico"),

			(50, "RadioChango", "http://transmision.radiobemba.org:8000/", "http://www.radiochango.com - Musica mestiza", "Espana"),

			(51, "Trance", "http://radio.r-b.ru:8000", "Musica Electronica", "Rusia"),

			(52, "Sawt Beirut International", "http://sawtbeirut.com:8068/", "http://sawtbeirut.com/sms.html", "Libano"),		
			(53, "Blooster 89.1 FM", "http://www.lounce.com:7982/", "http://www.boosterfm.net/ - Hip-Hop", "Francia"),
			(54, "RauteMusik JaM", "http://main-office.rautemusik.fm", "http://www.rautemusik.fm", "Alemania"),
			]


		# Se agregan las radios a la base de datos
		for radio in radios:
			self.basededatos.execute ("insert into radios values (?,?,?,?,?)", radio)

		self.coneccion.commit()	# confirmación de la sentencia
		self.basededatos.close() # Cierra la base
		self.coneccion.close()

		print " ***** Se ha llenado la base de datos:", self.direcciondebase
	    except Exception, e:
		print e
	    return True

	def agregar_radio(self, indice, nombre, dir_rep, detalles, pais):
	# agrega una radio a la base de datos
	    try:
		self.coneccion = sqlite3.connect(self.direcciondebase)# Conecta a la base de datos
		self.basededatos = self.coneccion.cursor()# Selecciona la base de datos

		radio = (indice, nombre, dir_rep, detalles, pais)

		self.basededatos.execute ("insert into radios values (?,?,?,?,?)", radio)

		self.coneccion.commit()	# confirmación de la sentencia
		self.basededatos.close() # Cierra la base
		self.coneccion.close()
		print " ***** Se ha agregado una radio a la base:", self.direcciondebase
		

	    except Exception, e:
		print e
	    return True

	def eliminar_radio(self, indice):
	# elimina una radio de la base de datos
	    try:
		self.coneccion = sqlite3.connect(self.direcciondebase)# Conecta a la base de datos
		self.basededatos = self.coneccion.cursor()# Selecciona la base de datos

		sentencia = "delete from radios where id_radio=" + str(indice)
		self.basededatos.execute (sentencia)

		self.coneccion.commit()	# confirmación de la sentencia
		self.basededatos.close() # Cierra la base
		self.coneccion.close()		

	    except Exception, e:
		print e
	    return True

	def leer_base (self):

	    try:
		self.coneccion = sqlite3.connect(self.direcciondebase)# Conecta a la base de datos
		self.basededatos = self.coneccion.cursor()# Selecciona la base de datos

		self.basededatos.execute("select * from radios")
		for row in self.basededatos:
			print row
			print ""

		self.basededatos.close() # Cierra la base
		self.coneccion.close()

	    except Exception, e:
		print e
	    return True


def main():
   gtk.main()
   return 0

if __name__=="__main__":
	import os
   	BasedeDatos = ManejodeBasedeDatos(os.getcwd()+"/Radios.db")
	BasedeDatos.CrearBasededatos()
	BasedeDatos.Llenar_Base()
	#BasedeDatos.leer_base()

	print BasedeDatos.CargarRadios()

	#for radios in BasedeDatos.CargarRadios():
	#	n = int(radios[0])
	#	nombre = str(radios[1])
	#	direccion = str(radios[2])
	#	pais = str(radios[3])
	#	descripcion = str(radios[4])

	#	print n, nombre, direccion, pais, descripcion


