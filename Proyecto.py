import json
# Se importa la librería Gobject Instrospection (gi)
import gi
# Selecciona la versión de GTK a trabajar (3.0)
gi.require_version("Gtk", "3.0")
# Importa Gtk
from gi.repository import Gtk

archivo = "/home/raimundoosf/Escritorio/Proyecto1U2/muroescalada.json"
archivo_ui = "/home/raimundoosf/Escritorio/Proyecto1U2/proyecto.ui"
archivo_data_especifica = "/home/raimundoosf/Escritorio/Proyecto1U2/busquedadata.json"

# se abre archivo json
def abrir_archivo(Archivo):

    try:
        with open(Archivo, 'r') as fichero:
            data = json.load(fichero)
    except IOError:
        data = []
    
    return data

# se añade data en archivo json
def guardar_data(data, Archivo):

    with open(Archivo, "w") as fichero:
        json.dump(data, fichero, indent=4)

class Main():

    def __init__(self):
        print("constructor")
        """se llama a widget para realizar introspeccion"""
        builder = Gtk.Builder()
        """se inspecciona archivo ui"""
        builder.add_from_file(archivo_ui)
        """se asocia objeto window"""
        ventana = builder.get_object("ventana_principal")
        # se setea tamaño de ventana emergente y agrega titulo a ventana
        ventana.set_default_size(800, 600)
        ventana.set_title("Gimnasio de Escalada")
        ventana.connect("destroy", Gtk.main_quit)


        # boton para reservar bloque
        reservar_bloque = builder.get_object("boton_reservar_bloque")
        reservar_bloque.set_label("Reservar Bloque")
        reservar_bloque.connect("clicked", self.abre_dialogo)

        boton_exit = builder.get_object("boton_exit")
        boton_exit.connect("clicked", self.click_salir)
        boton_exit.set_label("Salir")


        # boton abre dialogo
        registro_reservas = builder.get_object("boton_registro_reservas")
        registro_reservas.set_label("Registro de reservas")
        registro_reservas.connect("clicked", self.click_registro_reservas)

        ventana.show_all()

    """se cierra programa"""
    def click_salir(self, btn=None):
        Gtk.main_quit()

    """se abre ventana de dialogo asociada a reserva"""
    def abre_dialogo(self, btn=None):
        ventana_dialogo = Dialogo_reserva()
        
        response = ventana_dialogo.dialogo.run()

        if response == Gtk.ResponseType.OK:
            print("se presiono el boton oK")
            ventana_dialogo_data = Dialogo_data_reservas()
            ventana_dialogo_data.borrar_data_completa()
            ventana_dialogo_data.cargar_data_desde_json()
            pass
        else:
            pass
        
        ventana_dialogo.dialogo.destroy()
    
    """se abre ventana de dialogo asociada a data de reservas"""
    def click_registro_reservas(self, btn=None):
        ventana_dialogo_data = Dialogo_data_reservas()
        #respuesta = ventana_dialogo.dialogo.run()

class Dialogo_data_reservas():

    def __init__(self):

        builder = Gtk.Builder()
        builder.add_from_file(archivo_ui)

        self.dialogo = builder.get_object("dialogo_data_reservas")

        # boton editar
        boton_editar = builder.get_object("boton_editar")
        boton_editar.connect("clicked", self.editar_data_seleccionada)

        # boton eliminar
        boton_eliminar = builder.get_object("boton_eliminar")
        boton_eliminar.connect("clicked", self.borrar_dato_seleccionado)


        self.lista = ["Seleccione parametro de busqueda",
                     "Busqueda por fecha",
                     "Busqueda por fecha y bloque",
                     "Busqueda por nombre completo",
                     "Busqueda completa"]


        # comboboxtext
        self.comboboxtext = builder.get_object("comboboxtext")
        for item in self.lista:
            self.comboboxtext.append_text(item)

        self.comboboxtext.set_active(0)

        self.boton_aplicar_busqueda = builder.get_object("boton_aplicar_busqueda")
        self.boton_aplicar_busqueda.connect("clicked", self.realizar_busqueda)

        self.tree = builder.get_object("tree")

        self.modelo = Gtk.ListStore(str, str, str, str, str)
        self.tree.set_model(model=self.modelo)

        nombre_columnas = ("Fecha", "Bloque", "Nombre", "Apellido", "Numero Telefonico")
        cell = Gtk.CellRendererText()
        for item in range(len(nombre_columnas)):
            column = Gtk.TreeViewColumn(nombre_columnas[item], cell, text=item)
            self.tree.append_column(column)

        self.cargar_data_desde_json()

        self.dialogo.show_all()

    """Carga datos desde archvio json"""
    def cargar_data_desde_json(self):
        # llamamos al metodo de abrir el archivo
        datos = abrir_archivo(archivo)
        for item in datos:
            # proceso por medio de listas por comprensión
            line = [x for x in item.values()]
            print(line)
            self.modelo.append(line)

    """Elimina todo el contenido del TreeView (modelo, ListStore)."""
    def borrar_data_completa(self):
        for index in range(len(self.modelo)):
            # iter(0) por que nunca va a estar vacio.
            iter_ = self.modelo.get_iter(0)
            self.modelo.remove(iter_)

    """Elimina datos seleccionados."""
    def borrar_dato_seleccionado(self, btn=None):
        model, it = self.tree.get_selection().get_selected()
        # Validación no selección
        if model is None or it is None:
            return

        data = abrir_archivo(archivo)
        for item in data:
            if item['fecha'] == model.get_value(it, 0):
                data.remove(item)
        guardar_data(data, archivo)

        self.borrar_data_completa()
        self.cargar_data_desde_json()
    

    def realizar_busqueda(self, btn=None):

        Dialogo_busqueda_en_data()
        
    """Edita datos seleccionados."""
    def editar_data_seleccionada(self, btn=None):
        
        model, it = self.tree.get_selection().get_selected()
        # Validación no selección
        if model is None or it is None:
            return

        ventana_dialogo = Dialogo_reserva()

        ventana_dialogo.fecha.set_text(model.get_value(it, 0))
        ventana_dialogo.bloque.set_text(model.get_value(it, 1))
        ventana_dialogo.nombre.set_text(model.get_value(it, 2))
        ventana_dialogo.apellido.set_text(model.get_value(it, 3))
        ventana_dialogo.telefono.set_text(model.get_value(it, 4))

        response = ventana_dialogo.dialogo.run()

        if response == Gtk.ResponseType.CANCEL:
            pass
        elif response == Gtk.ResponseType.OK:
            data = abrir_archivo(archivo)
            for item in data:
                if item['fecha'] == model.get_value(it, 0):
                    data.remove(item)

            guardar_data(data, archivo)
            self.borrar_data_completa()
            self.cargar_data_desde_json()

        ventana_dialogo.dialogo.destroy()    

class Dialogo_busqueda_en_data():

    def __init__(self):

        Data = Dialogo_data_reservas()
        """ Error: variable que se llama desde otra clase siempre tiene valor = 0 """
        self.parametros_busqueda = Data.comboboxtext.get_active()
        
        print(self.parametros_busqueda)
        self.parametros_busqueda = 4

        labels = ['Ingrese fecha (dd-mm-aa): ', 'Ingrese bloque: ', 'Ingrese nombre: ', 'Ingrese apellido']

        builder = Gtk.Builder()
        builder.add_from_file(archivo_ui)

        dialogo = builder.get_object("dialogo_busqueda_en_data")
        
        parametro = ['parametro_1', 'parametro_2', 'parametro_3', 'parametro_4']
        objeto_label = ['busqueda_4.1', 'busqueda_4.2', 'busqueda_4.3', 'busqueda_4.4']
        objeto_entry = ['entrada1', 'entrada2', 'entrada3', 'entrada4']
        self.entrada_parametro = ['entrada_parametro_1', 'entrada_parametro_2', 'entrada_parametro_3', 'entrada_parametro_4']

        for indice in range(0,len(parametro)):
            parametro[indice] = builder.get_object(objeto_label[indice])
            self.entrada_parametro[indice] = builder.get_object(objeto_entry[indice])
            if self.parametros_busqueda == 3:
                parametro[0].set_label(labels[2])
                parametro[1].set_label(labels[3])
            else:
                parametro[indice].set_label(labels[indice])

        boton_ok = builder.get_object('boton_ok')
        boton_ok.connect("clicked", self.consultar_data)

        dialogo.show()
        if self.parametros_busqueda < 4:
            parametro[2].hide()
            parametro[3].hide()
            self.entrada_parametro[2].hide()
            self.entrada_parametro[3].hide()
            if self.parametros_busqueda == 1:
                parametro[1].hide()
                self.entrada_parametro[1].hide()

        self.coincidencia = False
    
    def consultar_data(self, btn = None):

        data = abrir_archivo(archivo)
        registro_solicitado = []
        entrada_parametro = []
        self.coincidencia = False

        for indice in range(0, 4):
            entrada_parametro.append(self.entrada_parametro[indice].get_text())

        #keys = ['fecha', 'bloque', 'nombre', 'apellido', 'telefono']

    
        for item in data:
            if self.parametros_busqueda != 3:
                if item['fecha'] == entrada_parametro[0]:
                    if self.parametros_busqueda == 1:
                        registro_solicitado.append(item)
                        self.coincidencia = True
                    else:
                        if item['bloque'] == entrada_parametro[1]:
                            if self.parametros_busqueda == 2:
                                registro_solicitado.append(item)
                                self.coincidencia = True
                            else:
                                if item['nombre'] == entrada_parametro[2] and entrada_parametro[3] == item['apellido']:
                                    registro_solicitado.append(item)
                                    self.coincidencia = True
                                else:
                                    continue
                        else:
                            continue
                else:
                    continue
            else:
                if item['nombre'] == entrada_parametro[0] and entrada_parametro[1] == item['apellido']:
                    registro_solicitado.append(item)
                    self.coincidencia = True
                else:
                    continue

        guardar_data(registro_solicitado, archivo_data_especifica)
        Ventana_muestra_datos_solicitados()
        
        
class Ventana_muestra_datos_solicitados():

    def __init__(self):

        builder = Gtk.Builder()
        builder.add_from_file(archivo_ui)

        data_solicitada = abrir_archivo(archivo_data_especifica)

        dialogo = builder.get_object("Ventana_muestra_data_solicitada")

        tree = builder.get_object("tree_busqueda")

        modelo = Gtk.ListStore(str, str, str, str, str)
        tree.set_model(model=modelo)

        nombre_columnas = ("Fecha", "Bloque", "Nombre", "Apellido", "Numero Telefonico")
        cell = Gtk.CellRendererText()
        for item in range(len(nombre_columnas)):
            column = Gtk.TreeViewColumn(nombre_columnas[item], cell, text=item)
            tree.append_column(column)

        datos = abrir_archivo(archivo_data_especifica)
        for item in datos:
            # proceso por medio de listas por comprensión
            line = [x for x in item.values()]
            print(line)
            modelo.append(line)

        for line in data_solicitada:
            data = abrir_archivo(archivo_data_especifica)
            new_data = {"fecha": line["fecha"],
                        "bloque": line["bloque"],
                        "nombre": line["nombre"],
                        "apellido": line["apellido"],
                        "telefono": line["telefono"]
                        }
            data.append(new_data)
            guardar_data(data, archivo_data_especifica)

        noticacion_dato_no_encontrado = builder.get_object("dato_no_encontrado")
        noticacion_dato_no_encontrado.set_label("Dato solicitado no ha sido encontrado")

        dialago_busqueda = Dialogo_busqueda_en_data()
        coincidencia = dialago_busqueda.coincidencia

        print("la coindidencia es", Dialogo_busqueda_en_data.coincidencia)

        dialogo.show()

        if Dialogo_busqueda_en_data.coincidencia == False:
            tree.hide()
        else:
            noticacion_dato_no_encontrado.hide()


class Dialogo_reserva():

    def __init__(self):

        builder = Gtk.Builder()
        builder.add_from_file(archivo_ui)

        self.dialogo = builder.get_object("dialogo_reserva")

        boton_aceptar = builder.get_object("boton_ok_dialogo")
        boton_aceptar.connect("clicked", self.boton_ok_clicked)

        # cuadro de texto
        self.fecha = builder.get_object("entrada_fecha")
        self.bloque = builder.get_object("entrada_bloque")
        self.nombre = builder.get_object("entrada_nombre")
        self.apellido = builder.get_object("entrada_apellido")
        self.telefono = builder.get_object("entrada_telefono")


        self.dialogo.show_all()

    def boton_ok_clicked(self, btn=None):
        fecha = self.fecha.get_text()
        bloque = self.bloque.get_text()
        nombre = self.nombre.get_text()
        apellido = self.apellido.get_text()
        telefono = self.telefono.get_text()

        data = abrir_archivo(archivo)
        new_data = {"fecha": fecha,
                    "bloque": bloque,
                    "nombre": nombre,
                    "apellido": apellido,
                    "telefono": telefono
                    }
        data.append(new_data)
        guardar_data(data, archivo)

if __name__ == "__main__":
    # Llama
    Main()
    Gtk.main()
