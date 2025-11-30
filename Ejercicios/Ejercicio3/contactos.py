# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import re
from datetime import datetime
from tkcalendar import DateEntry


class Contacto:
    def __init__(self, 
                 nombre: str, 
                 apellido: str, 
                 fechaNacimiento: datetime, 
                 direccion: str, 
                 telefono: str, 
                 correo: str):
        self.nombre = nombre
        self.apellido = apellido
        self.fechaNacimiento = fechaNacimiento
        self.direccion = direccion
        self.telefono = telefono
        self.correo = correo
    @staticmethod
    def validar_info(nombre: str,
                      apellido: str,
                      fechaNacimiento: str,
                      direccion: str,
                      telefono: str,
                      correo: str):
            
            nombre = nombre.strip()
            apellido = apellido.strip()
            fechaNacimiento = fechaNacimiento.strip()
            direccion = direccion.strip()
            telefono = telefono.strip()
            correo = correo.strip()

            # validacion campos vacios
            if (not nombre or 
                not apellido or 
                not fechaNacimiento or 
                not direccion or 
                not telefono or 
                not correo):
                raise Exception("Todos los campos son obligatorios.")
            
            # validacion formato fecha
            try:
                fecha_formato = datetime.strptime(fechaNacimiento, "%Y-%m-%d").date()
            except:
                raise Exception("Fecha invalida. Formato esperado: aaaa-mm-dd")

            # validacion de que no se coloque una fecha futura
            if fecha_formato > datetime.now().date():
                raise Exception("La fecha de nacimiento no puede ser futura.")

            # validavcion telefono
            if not re.match(r'^\+?\d[\d\s-]{6,14}$', telefono):
                raise Exception("Telefono invalido, no cumple con el formato")  
    
            # validacion formato del correo
            if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', correo):
                raise Exception("El formato del correo ingresado no es válido.")



class Interfaz:
    def __init__(self):
        self.__contactos = []
        self._panel_principal = tk.Tk()
        self._panel_principal.title("Sistema de gestión de contactos")
        self._panel_principal.resizable(False, False)
        self._panel_principal.configure(bg="#2C3E50")

        self.__panel_contactos = None
        self.__panel_formulario = None

        self.__ver_contactos()
        self.__añadir_contacto()
    
    def __ver_contactos(self):
        # coloco una validacion para destruir el panel con la tabla para volverlo a ver de modo q se actualice cada que haya un cambio
        if self.__panel_contactos:
            self.__panel_contactos.destroy()

        # defino mi panel principal de visualizacion de contactos
        self.__panel_contactos = tk.Frame(self._panel_principal, pady=10, padx=10, bg="#2C3E50")
        self.__panel_contactos.grid(row=0, column=1, sticky="n")

        titulo = tk.Label(self.__panel_contactos, 
                        text="Listado de contactos", 
                        font=("Arial", 16, "bold"),
                        fg="#ECF0F1",
                        bg="#2C3E50")
        titulo.grid(row=0, column=0, pady=15)

        contactos = [
            (i+1, c.nombre, c.apellido, str(c.fechaNacimiento), c.telefono, c.correo, c.direccion)
            for i, c in enumerate(self.__contactos)
        ]

        # se hay por lo menos un contacto renderizo el contenido de la tabla
        if len(contactos) > 0:
            # ajuste el tamaño de la tabla en funcion a la cantidad de registros con un tamaño maximo de 12 registros
            nregistros = min(len(contactos), 12)

            # Defino el contenedor en el cual estara almacenada los componentes de mi tabla
            tabla_container = tk.Frame(self.__panel_contactos)
            tabla_container.grid(row=2, column=0)

            # defino un canva, a fin de inyectarle la tabla, asi cuando se desborde del tamaño total del contenedor horizontalmente, este no se desbordara ni rompera el layout
            canvas = tk.Canvas(tabla_container, bg="#2C3E50", highlightthickness=0)
            canvas.pack(side="left", fill="both")

            # defino mi barra de scrolling vertical y lo coloco al lado derecho del contenedor de mi tabla
            scrollbar_y = tk.Scrollbar(tabla_container, orient="vertical")
            scrollbar_y.pack(side="right", fill="y")

            # defino mi barra de scrolling horizontal y lo coloco en la parte baja del contenedor de visualizacion principal
            scrollbar_x = tk.Scrollbar(self.__panel_contactos, orient="horizontal")
            scrollbar_x.grid(row=3, column=0, sticky="ew")
            # actualizo el comportamiento del scrollbar y del canva en funcion a la accion ejecutada por el usuario
            canvas.configure(xscrollcommand=scrollbar_x.set)
            scrollbar_x.config(command=canvas.xview)

            # defino un frame el cual es el que inyectare en el canva en el cual se visualizara la tabla
            frame_interno = tk.Frame(canvas, bg="#2C3E50")
            # le inyecto dicho frame al canva
            canvas.create_window((0, 0), window=frame_interno, anchor="nw")

            # definimos una funcion que actualiza el area de scroll dependiendo del tamaño del canva cada vez que se agrega un nuevo registro
            def actualizar_scroll(event):
                canvas.configure(scrollregion=canvas.bbox("all"))

            frame_interno.bind("<Configure>", actualizar_scroll)

            # Definimos el estilo de la tabla
            style = ttk.Style()
            style.configure("Custom.Treeview",
                            background="#2C3E50",
                            foreground="white",
                            fieldbackground="#2C3E50",
                            font=("Arial", 11))
            style.configure("Custom.Treeview.Heading",
                            background="#34495E",
                            foreground="black",
                            font=("Arial", 11, "bold"))
            style.map("Custom.Treeview",
                    background=[("selected", "#405A74")])
            
            # creamos la tabla donde estara el contenido con un ttk.Treeview el cual tiene un comportamiento analogo a una tabla
            self.__tabla_contactos = ttk.Treeview(
                frame_interno,
                columns=("ID", "Nombre", "Apellido", "FechaNacimiento", "Telefono", "Correo", "Direccion"),
                show="headings",
                height=nregistros,
                style="Custom.Treeview",
                yscrollcommand=scrollbar_y.set

            )
            self.__tabla_contactos.pack()

            # definimos y configuramos las columnas
            self.__tabla_contactos.heading("ID", text="ID")
            self.__tabla_contactos.heading("Nombre", text="Nombre")
            self.__tabla_contactos.heading("Apellido", text="Apellido")
            self.__tabla_contactos.heading("FechaNacimiento", text="Fecha Nac.")
            self.__tabla_contactos.heading("Telefono", text="Teléfono")
            self.__tabla_contactos.heading("Correo", text="Correo")
            self.__tabla_contactos.heading("Direccion", text="Dirección")


            self.__tabla_contactos.column("ID", width=45, anchor="center")
            self.__tabla_contactos.column("Nombre", width=130, anchor="center")
            self.__tabla_contactos.column("Apellido", width=130, anchor="center")
            self.__tabla_contactos.column("FechaNacimiento", width=100, anchor="center")
            self.__tabla_contactos.column("Telefono", width=130, anchor="center")
            self.__tabla_contactos.column("Correo", width=200, anchor="center")
            self.__tabla_contactos.column("Direccion", width=220, anchor="center")

            # conectamos el scrollbar vertical con la tabla
            scrollbar_y.config(command=self.__tabla_contactos.yview)
            
            # renderizamos todos los contactos
            for contacto in contactos:
                self.__tabla_contactos.insert("", "end", values=contacto)

        # si no hay contactos registrados entonces le avisamos al usuario
        else:
            mensaje = tk.Label(self.__panel_contactos, 
                            text="No hay contactos registrados", 
                            font=("Arial", 15, "bold"),
                            fg="#F39C12",
                            bg="#2C3E50")
            mensaje.grid(row=2, column=0, pady=(15, 20), padx=40)


    def __añadir_contacto(self):

        if self.__panel_formulario:
            self.__panel_formulario.destroy()

        self.__panel_formulario = tk.Frame(
            self._panel_principal,
            padx=20,
            pady=20,
            bg="#2C3E50"
        )
        self.__panel_formulario.grid(row=0, column=0, sticky="nsew")

        titulo = tk.Label(
            self.__panel_formulario,
            text="Añadir contacto:",
            font=("Arial", 16, "bold"),
            fg="#ECF0F1",
            bg="#2C3E50"
        )
        titulo.grid(row=0, column=0, pady=(0, 20))

        form = tk.Frame(self.__panel_formulario, bg="#2C3E50")
        form.grid(row=1, column=0)

        def label_estandar(texto, fila):
            tk.Label(
                form,
                text=texto,
                font=("Arial", 10),
                fg="#ECF0F1",
                bg="#2C3E50",
                anchor="w"
            ).grid(row=fila, column=0, sticky="w", pady=3)

        label_estandar("Nombres:", 0)
        self.__input_nombre = tk.Entry(form, width=18, font=("Arial", 12))
        self.__input_nombre.grid(row=0, column=1, pady=3)
        self.__input_nombre.focus()

        label_estandar("Apellidos:", 1)
        self.__input_apellido = tk.Entry(form, width=18, font=("Arial", 12))
        self.__input_apellido.grid(row=1, column=1, pady=3)

        label_estandar("Fecha Nacimiento:", 2)
        self.__input_fecha_nacimiento = DateEntry(
            form,
            width=16,
            font=("Arial", 12),
            date_pattern="yyyy-mm-dd",
            # state="readonly"
        )
        self.__input_fecha_nacimiento.grid(row=2, column=1, pady=3)

        label_estandar("Dirección:", 3)
        self.__input_direccion = tk.Entry(form, width=18, font=("Arial", 12))
        self.__input_direccion.grid(row=3, column=1, pady=3)

        label_estandar("Teléfono:", 4)
        self.__input_telefono = tk.Entry(form, width=18, font=("Arial", 12))
        self.__input_telefono.grid(row=4, column=1, pady=3)

        label_estandar("Correo:", 5)
        self.__input_correo = tk.Entry(form, width=18, font=("Arial", 12))
        self.__input_correo.grid(row=5, column=1, pady=3)

        botones = tk.Frame(self.__panel_formulario, bg="#2C3E50")
        botones.grid(row=2, column=0, pady=(15, 10))

        boton_crear_contacto = tk.Button(
            botones, text="Agregar",
            command=self.__guardarContacto,
            width=8, height=1,
            font=("Arial", 10, "bold"),
            bg="#27AE42", fg="white"
        )
        boton_crear_contacto.grid(row=0, column=0, padx=5)

        boton_limpiar = tk.Button(
            botones, text="Limpiar",
            command=self.__limpiarInfo,
            width=8, height=1,
            font=("Arial", 10, "bold"),
            bg="#FF3838", fg="white"
        )
        boton_limpiar.grid(row=0, column=1, padx=5)

        self.__resultado = tk.Label(
            self.__panel_formulario,
            text="Recuerda ingresar valores válidos ;)",
            font=("Arial", 11),
            bg="#34495E",
            fg="#F39C12",
            padx=20, pady=10,
            width=35,
            anchor="center"
        )
        self.__resultado.grid(row=3, column=0, pady=(0,10))

        info_enter = tk.Label(
            self.__panel_formulario,
            text="Al presionar 'Enter' se añadira el contacto",
            font=("Arial", 8),
            foreground="#BDC3C7",
            background="#2C3E50"
        )
        info_enter.grid(row=4, column=0)

        inputs = [
            self.__input_nombre,
            self.__input_apellido,
            self.__input_fecha_nacimiento,
            self.__input_direccion,
            self.__input_telefono,
            self.__input_correo
        ]

        for w in inputs:
            w.bind("<Return>", lambda e: self.__guardarContacto())


    def __guardarContacto(self):
        try:
            # capturamos la informacion del formulario
            nombre = self.__input_nombre.get()
            apellido = self.__input_apellido.get()
            fechaNacimiento = self.__input_fecha_nacimiento.get()
            direccion = self.__input_direccion.get()
            telefono = self.__input_telefono.get()
            correo = self.__input_correo.get()
            
            Contacto.validar_info(nombre, apellido, fechaNacimiento, direccion, telefono, correo)
            fechaNacimiento=datetime.strptime(fechaNacimiento, "%Y-%m-%d").date()
            
            contacto = Contacto(nombre, apellido, fechaNacimiento, direccion, telefono, correo)
            self.__contactos.append(contacto)

            messagebox.showinfo("Contacto guardado", f"El contacto de '{nombre}' ha sido guardado exitosamente.")
            self.__resultado.config(text=f"El contacto de '{nombre}' ha sido creado con exito.", fg="#38FF56")

            self.__limpiarInfo()
            self.__ver_contactos()

        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.__resultado.config(text=str(e), fg="#FF3838")


    def __limpiarInfo(self):
        self.__input_nombre.delete(0, tk.END)
        self.__input_apellido.delete(0, tk.END)
        # self.__input_fecha_nacimiento.delete(0, tk.END)
        self.__input_direccion.delete(0, tk.END)
        self.__input_telefono.delete(0, tk.END)
        self.__input_correo.delete(0, tk.END)



class Main:
    @staticmethod
    def main():
        app = Interfaz()
        app._panel_principal.mainloop()


if __name__ == "__main__":
    Main.main()
