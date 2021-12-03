import json
# Se importa la librería Gobject Instrospection (gi)
import gi
# Selecciona la versión de GTK a trabajar (3.0)
gi.require_version("Gtk", "3.0")
# Importa Gtk
from gi.repository import Gtk


# se abre archivo json
def abrir_archivo():

    try:
        with open("/home/raimundoosf/Escritorio/proyecto1/muroescalada.json", 'r') as archivo:
            data = json.load(archivo)
    except IOError:
        data = []
    
    return data

# se añade data en archivo json
def guardar_data(data):

    # guardamos
    with open("/home/raimundoosf/Escritorio/proyecto1/muroescalada.json", "w") as archivo:
        json.dump(data, archivo, indent=4)


class Main():

    def __init__(self):
        print("constructor")
        """se llama a widget para realizar introspeccion"""
        builder = Gtk.Builder()
        """se inspecciona archivo ui"""
        builder.add_from_file("/home/raimundoosf/Escritorio/proyecto1/proyecto1_borrador.ui")
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

    # se cierra programa
    def click_salir(self, btn=None):
        Gtk.main_quit()

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
        
    
    def click_registro_reservas(self, btn=None):
        ventana_dialogo_data = Dialogo_data_reservas()
        #respuesta = ventana_dialogo.dialogo.run()


class Dialogo_data_reservas():

    def __init__(self):

        builder = Gtk.Builder()
        builder.add_from_file("/home/raimundoosf/Escritorio/proyecto1/proyecto1_borrador.ui")

        self.dialogo = builder.get_object("dialogo_data_reservas")

        # boton editar
        boton_editar = builder.get_object("boton_editar")
        boton_editar.connect("clicked", self.editar_data_seleccionada)

        # boton eliminar
        boton_eliminar = builder.get_object("boton_eliminar")
        boton_eliminar.connect("clicked", self.borrar_dato_seleccionado)

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
        datos = abrir_archivo()
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

        data = abrir_archivo()
        for item in data:
            if item['fecha'] == model.get_value(it, 0):
                data.remove(item)
        guardar_data(data)

        self.borrar_data_completa()
        self.cargar_data_desde_json()
    
    def editar_data_seleccionada(self, btn=None):
        """Edita datos seleccionados."""
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
            data = abrir_archivo()
            for item in data:
                if item['fecha'] == model.get_value(it, 0):
                    data.remove(item)

            guardar_data(data)
            self.borrar_data_completa()
            self.cargar_data_desde_json()

        ventana_dialogo.dialogo.destroy()


class Dialogo_reserva():

    def __init__(self):

        builder = Gtk.Builder()
        builder.add_from_file("/home/raimundoosf/Escritorio/proyecto1/proyecto1_borrador.ui")

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
        print("presionó el boton ok dialogo")
        fecha = self.fecha.get_text()
        bloque = self.bloque.get_text()
        nombre = self.nombre.get_text()
        apellido = self.apellido.get_text()
        telefono = self.telefono.get_text()

        data = abrir_archivo()
        new_data = {"fecha": fecha,
                    "bloque": bloque,
                    "nombre": nombre,
                    "apellido": apellido,
                    "telefono": telefono
                    }
        data.append(new_data)
        guardar_data(data)


if __name__ == "__main__":
    # Llama
    Main()
    Gtk.main()
