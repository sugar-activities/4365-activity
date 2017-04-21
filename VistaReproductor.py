#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   VistaReproductor.py por:
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

from Reproductor import Reproductor
from BarradeReproduccion import BarradeReproduccion
from Radio import Radio
import os
import shutil
import pango

from sugar.activity import activity
from ManejodeBasedeDatos import ManejodeBasedeDatos

# Directorio para crear la base de datos
directorio_base = os.path.join(activity.get_activity_root(), 'data/')
mi_base = os.path.join(directorio_base + "Radios.db")

# Si el directorio no existe, crearlo
if not os.path.exists(directorio_base):
	os.mkdir(directorio_base)

# Si la base de datos no existe, crearla
if not os.path.exists(mi_base):
	BasedeDatos = ManejodeBasedeDatos(mi_base)
	BasedeDatos.CrearBasededatos()
	BasedeDatos.Llenar_Base()
	os.chmod(os.path.join(directorio_base, 'Radios.db'), 0660)




class VistaReproductor(gtk.Table):

    def __init__(self):
	
        gtk.Table.__init__(self, 10, 30, False)

	# para los archivos mp3 - wav - ogg
	self.treeview = gtk.TreeView()
	self.liststore = gtk.ListStore(str)
	self.treeselection = self.treeview.get_selection()
	self.treeselection.set_mode(gtk.SELECTION_SINGLE)

	self.directorio_de_reproduccion = None # el directorio desde donde se cargaron los archivos
	self.indice_archivo_en_reproduccion = 0 # para mantener una lista de reproduccion con los archivos

	# La base de datos con las radios
	self.BasedeDatos = ManejodeBasedeDatos(mi_base)
	self.listaderadios = []

	# Reproductor helix
        self.reproductor = Reproductor(self)
	self.is_radio = False
        self.fuentededatosparareproducir = None

	self.directoriodeiconos = os.getcwd() + "/Iconos/"
	self.rosado = gtk.gdk.Color(65000,13000,25000,1)
	self.celeste1 = gtk.gdk.Color(0,33000,33000,1)

	# ******************** Interface Grafica *****************************
	# Zona Central.
	# Definicion de radios online
	viewportderadios = gtk.ScrolledWindow()
	viewportderadios.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
	self.caja_radios = gtk.VBox()

	self.cargar_radios()

	viewportderadios.add_with_viewport(self.caja_radios)
	self.attach(viewportderadios, 0, 8, 0, 29)

	# Barra vertical derecha para la lista de reproduccion
        self.viewportderecho = gtk.ScrolledWindow()
        self.viewportderecho.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.attach(self.viewportderecho, 8, 10, 0, 29)
	# Informacion adicional de la actividad
	self.viewportderecho.add_with_viewport(self.crear_barra_info())

	# Barra con controles de reproduccion
	# Zona inferior
        self.barradereproduccion = BarradeReproduccion()
	self.reproductor.asignacion_de_barra_de_reproduccion(self.barradereproduccion)
        self.attach(self.barradereproduccion, 0, 10, 29, 30)
        self.show_all()

	# Conexion de eventos de los controles de la barra de reproduccion con las
	# funciones de reproduccion del reproductor

        # Abre un selector de archivos
        self.barradereproduccion.botonabrir.connect("clicked", self.abrirdirectoriomp3)
	self.barradereproduccion.botonstop.connect("clicked", self.reproductor.stop)
	self.barradereproduccion.botonplay.connect("clicked", self.reproductor.pause)# moficar para un click en la lista
	self.barradereproduccion.botonatras.connect("clicked", self.tema_anterior)
	self.barradereproduccion.botonsiguiente.connect("clicked", self.siguiente_tema)






# ***************************************************************************
# ************************** FUNCIONES **************************************

    def cargar_radios(self):
	# se llama al iniciar la actividad y al agregar o eliminar una radio

        for child in self.caja_radios:
            self.caja_radios.remove(child)

	radios = self.BasedeDatos.CargarRadios() # Devuelve una lista de tuplas
	self.listaderadios = []

	for radio in radios:
		self.listaderadios.append(Radio(radio, self.directoriodeiconos))

	for radio in self.listaderadios:
		radio.connect("button_press_event", self.handler_click_Radio)
		self.caja_radios.pack_start(radio, True, True, 5)

    def handler_click_Radio(self, widget, event):
	# reacciona a los clicks sobre las radios
	boton = event.button
	pos = (event.x, event.y)
	tiempo = event.time

	if boton == 1:
		self.cargar_fuente_de_datos (widget, widget.direccionderadio, True)
		self.pintar_radios_no_seleccionadas(widget)
		print "Reproducir radio"
		return
	elif boton == 3:
		print "Abrir menu - popup"
		self.crear_menu_emergente_para_radios(widget, boton, pos, tiempo)
		return

    def crear_menu_emergente_para_radios(self, widget, boton, pos, tiempo):
	# un menu para agregar o eliminar radios de la base de datos
	menu = gtk.Menu()

	# Items del menu
	agregar = gtk.MenuItem("Agregar nueva Radio . . .")
	eliminar = gtk.MenuItem("Eliminar de la lista")
	eliminar2 = gtk.MenuItem("Eliminar definitivamente")

	# Agregar los items al menu
	menu.append(agregar)
	menu.append(eliminar)
	menu.append(eliminar2)

        # Se conectan las funciones de retrollamada a la senal "activate"
        agregar.connect_object("activate", self.construir_dialogo_agregar_radio, None)
        eliminar.connect_object("activate", self.destruirwidget, widget, widget)
        eliminar2.connect_object("activate", self.eliminar_radio, widget)

	menu.show_all()
	menu.popup(None, None, self.posicionar_menu, boton, tiempo, None)

    def posicionar_menu(self, widget, pos):
	# Establece la posicion del menu desplegable
	print "Posicionando menu desplegable"

    def construir_dialogo_agregar_radio(self, widget):
	# Crea un cuadro de dialogo para ingresar los datos de una nueva radio

	dialog = gtk.Dialog("Agregar Radio", None, gtk.DIALOG_MODAL, None)

	etiqueta0 = gtk.Label("No utilices tildes ni ñ en los datos.")
	dialog.vbox.pack_start(etiqueta0, True, True, 5)

	renglo1 = gtk.HBox()
	etiqueta1 = gtk.Label("Nombre de la Radio: ")
	texto1 = gtk.Entry()
	renglo1.pack_start(etiqueta1, True, True, 5)
	renglo1.pack_start(texto1, True, True, 5)
	dialog.vbox.pack_start(renglo1, True, True, 5)

	renglo2 = gtk.HBox()
	etiqueta2 = gtk.Label("Direccion de Reproduccion: ")
	texto2 = gtk.Entry()
	renglo2.pack_start(etiqueta2, True, True, 5)
	renglo2.pack_start(texto2, True, True, 5)
	dialog.vbox.pack_start(renglo2, True, True, 5)

	renglo3 = gtk.HBox()
	etiqueta3 = gtk.Label("Descripcion: ")
	texto3 = gtk.Entry()
	renglo3.pack_start(etiqueta3, True, True, 5)
	renglo3.pack_start(texto3, True, True, 5)
	dialog.vbox.pack_start(renglo3, True, True, 5)

	renglo4 = gtk.HBox()
	etiqueta4 = gtk.Label("Pais de procedencia: ")
	texto4 = gtk.Entry()
	renglo4.pack_start(etiqueta4, True, True, 5)
	renglo4.pack_start(texto4, True, True, 5)
	dialog.vbox.pack_start(renglo4, True, True, 5)

	dialog.add_button("Guardar", 1)
	dialog.add_button("Cancelar", 2)

	dialog.show_all()

        if dialog.run() == 1:
		# verificar y guardar

		if texto2.get_text() != "":
			radio = self.listaderadios[-1]
			id_de_radio = radio.id_en_base
			indice = int (id_de_radio + 1)

			nombre = texto1.get_text()

			dir_rep = texto2.get_text()

			detalles = texto3.get_text()

			pais = texto4.get_text()

			self.BasedeDatos.agregar_radio(indice, nombre, dir_rep, detalles, pais)
			self.cargar_radios()
		
	elif dialog.run() == 2:
		# sale automaticamente
		pass
        dialog.destroy()

    def eliminar_radio (self, widget):
	indice = widget.id_en_base
	self.BasedeDatos.eliminar_radio(indice)
	self.cargar_radios()

    def crear_barra_info(self):
	# Informacion
	self.barra_ceibal_radio_info = gtk.VBox()
	imagen1 = gtk.Image()
	imagen1.set_from_file(self.directoriodeiconos + "Flavio.png")

	etiquetadeinformacion1 = gtk.Label("Ceibal Radio" + "\n" + "fdanesse@hotmail.com" + "\n" + "http://sites.google.com/" + "\n" + "site/sugaractivities/home")
	etiquetadeinformacion1.modify_font(pango.FontDescription("purisa 4"))
	etiquetadeinformacion1.set_justify(gtk.JUSTIFY_CENTER)

	etiquetadeinformacion2 = gtk.Label("http://drupal.ceibaljam.org/"  + "\n" + "webmaster@ceibaljam.org")
	etiquetadeinformacion2.modify_font(pango.FontDescription("purisa 4"))
	etiquetadeinformacion2.set_justify(gtk.JUSTIFY_CENTER)

	imagen2 = gtk.Image()
	imagen2.set_from_file(self.directoriodeiconos + "ceibaljam.png")

	self.barra_ceibal_radio_info.pack_start(imagen2, True, True, 5)
	self.barra_ceibal_radio_info.pack_start(etiquetadeinformacion2, True, True, 5)
	self.barra_ceibal_radio_info.pack_start(imagen1, True, True, 5)
	self.barra_ceibal_radio_info.pack_start(etiquetadeinformacion1, True, True, 5)

	self.barra_ceibal_radio_info.show_all()
	return self.barra_ceibal_radio_info

    def pintar_radios_no_seleccionadas (self, widget):
	# Cambia los colores de los controles al hacerles click
	for radio in self.listaderadios:
		radio.pintame(self.celeste1)
	widget.pintame(self.rosado)


    def abrirdirectoriomp3(self,widget):
	# Abre un Filechooser para cargar un directorio con archivos mp3 - wav - ogg
	selectordedirectorio = gtk.FileChooserDialog("Abrir directorio MP3", None, gtk.FILE_CHOOSER_ACTION_OPEN, None)
	selectordedirectorio.set_current_folder_uri("file:///media")
	selectordedirectorio.set_select_multiple(True)

	# extras
	frame = gtk.Frame()
	hbox = gtk.HBox()
	frame.add(hbox)
	botonabrirdirectorio = gtk.Button("Abrir")
	botonseleccionartodo = gtk.Button("Seleccionar Todos")
	botonsalir = gtk.Button("Salir")
	hbox.pack_end(botonsalir, False, False, 5)
	hbox.pack_end(botonseleccionartodo, False, False, 5)
	hbox.pack_end(botonabrirdirectorio, False, False, 5)
	selectordedirectorio.set_extra_widget(frame)

	botonsalir.connect("clicked",self.destruirwidget,selectordedirectorio)
	botonabrirdirectorio.connect("clicked",self.abrirdirectorio,selectordedirectorio)
	botonseleccionartodo.connect("clicked",self.seleccionartodo,selectordedirectorio)

	# filtro Musica
	filter = gtk.FileFilter()
	filter.set_name("Musica")
	filter.add_mime_type("sound/mp3")
	filter.add_mime_type("sound/ogg")
	filter.add_mime_type("sound/wav")
	filter.add_pattern("*.mp3")
	filter.add_pattern("*.ogg")
	filter.add_pattern("*.wav")
	selectordedirectorio.add_filter(filter)
	selectordedirectorio.add_shortcut_folder_uri("file:///media/")

	selectordedirectorio.show_all()

    def seleccionartodo(self,widget,selectordedirectorio):
	selectordedirectorio.select_all()

    def abrirdirectorio(self,widget,selectordedirectorio):
	# Carga los mp3 del directorio seleccionado
        listadereproduccion = selectordedirectorio.get_filenames()
        self.cargardirectorio(listadereproduccion)
        self.destruirwidget(None, selectordedirectorio)

#****************
#****************

    def cargardirectorio(self, listadereproduccion):

	self.liststore = gtk.ListStore(str)
        for archivo in listadereproduccion:
	    if os.path.isfile(archivo):
		nombre_de_archivo = os.path.basename(archivo)
		self.liststore.append([nombre_de_archivo])

	if len(self.liststore) > 0:
		for child in self.viewportderecho:
			self.viewportderecho.remove(child)

		# el directorio de reproduccion
		self.directorio_de_reproduccion = os.path.dirname(listadereproduccion[0])

		self.treeview = gtk.TreeView()
		self.treeview.connect("row-activated", self.open_file)
		self.treeview.set_model(self.liststore)
		self.treeview.append_column(gtk.TreeViewColumn('Mi música', gtk.CellRendererText(), text=0))
		self.viewportderecho.add_with_viewport(self.treeview)

		self.viewportderecho.show_all()
		self.treeview.show_all()

		self.indice_archivo_en_reproduccion = 0
		self.open_file(self.treeview, self.indice_archivo_en_reproduccion, 0)
		self.treeselection = self.treeview.get_selection()
		self.treeselection.set_mode(gtk.SELECTION_SINGLE)
		self.treeselection.select_path(self.indice_archivo_en_reproduccion)

    def siguiente_tema(self, widget):
	if int(self.indice_archivo_en_reproduccion) + 1 < len(self.liststore) and self.is_radio == False:
		self.indice_archivo_en_reproduccion += 1
		self.open_file(self.treeview, self.indice_archivo_en_reproduccion, 0)
		self.treeselection = self.treeview.get_selection()
		self.treeselection.set_mode(gtk.SELECTION_SINGLE)
		self.treeselection.select_path(self.indice_archivo_en_reproduccion)

    def tema_anterior(self, widget):
	if int(self.indice_archivo_en_reproduccion) - 1 > -1 and self.is_radio == False:
		self.indice_archivo_en_reproduccion -= 1
		self.open_file(self.treeview, self.indice_archivo_en_reproduccion, 0)
		self.treeselection = self.treeview.get_selection()
		self.treeselection.set_mode(gtk.SELECTION_SINGLE)
		self.treeselection.select_path(self.indice_archivo_en_reproduccion)
	
    def open_file(self, treeview, path, column):
	# def callback(treeview, iter, path, user_data)
	# metodo de la interfase treeview

        model = treeview.get_model()
        iterador = model.get_iter(path)
        archivo = self.directorio_de_reproduccion + "/" + model.get_value(iterador, 0)
	self.cargar_fuente_de_datos(None, archivo, False)
	
	# El path es de tipo (1,) hay que sacar la coma y los parentesis para usarlo como indice entero
	indice1 = str(path)
	indice = ""
	for x in indice1:
		if x != "," and x != "(" and x != ")":
			indice += x
	#self.indice_archivo_en_reproduccion = path
	self.indice_archivo_en_reproduccion = int(indice)
	print "self.indice_archivo_en_reproduccion: ", self.indice_archivo_en_reproduccion

    def cargar_fuente_de_datos(self, widget, archivo, is_radio):
	# Se carga la fuente de datos que se va a reproducir
	self.is_radio = is_radio
	if is_radio == False:
		self.fuentededatosparareproducir = "file://" + archivo
	else:
		self.fuentededatosparareproducir = archivo
        
	self.reproductor.abrirfuentededatos(None, self.fuentededatosparareproducir, is_radio)

    def destruirwidget(self,widgetquedalasenal,widgetquesedestruira):
	# Elimina un widget (filechooser y radio eliminada por el menu contextual)
        widgetquesedestruira.destroy()
        return False
