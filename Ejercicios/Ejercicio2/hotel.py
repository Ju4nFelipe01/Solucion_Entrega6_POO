# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import simpledialog
from datetime import datetime
from tkcalendar import DateEntry


class Habitacion:
    def __init__(self, numero: int, disponible: bool, precioDia: float):
        self._numero = numero
        self._disponible = disponible
        self._precioDia = precioDia
        self._huesped = None

class Hotel:
    def __init__(self):
        nAbitaciones=10
        self._habitaciones = [
            Habitacion(numero=i+1, disponible=True, precioDia=(120000 if i < nAbitaciones//2 else 160000))
            for i in range(nAbitaciones)
        ]
        self._huespedes=[]

class Huesped:
    def __init__(
            self, 
            nombre: str, 
            apellido: str, 
            documento: int, 
            fechaIngreso: datetime, 
            habitacion: Habitacion):
        self.nombre = nombre
        self.apellido = apellido
        self.documento = documento
        self.fechaIngreso = fechaIngreso
        self.fechaSalida = None
        self.habitacion = habitacion 
    @staticmethod
    def validar_info(
        fechaIngreso: str, 
        nombre: str, 
        apellido: str, 
        documento: str
    ):
        fecha = fechaIngreso.strip()
        nombre = nombre.strip()
        apellido = apellido.strip()
        documento = documento.strip()

        # Validamos que ningun campo este vacio
        if not fecha or not nombre or not apellido or not documento:
            raise Exception("Ningún campo puede estar vacío")

        # Validación de nombre y apellido
        if len(nombre) < 2 or len(nombre) > 30:
            raise Exception("El nombre solo puede tener entre 2 y 30 caracteres")

        if len(apellido) < 2 or len(apellido) > 30:
            raise Exception("El apellido solo puede tener entre 2 y 30 caracteres")

        if not nombre.replace(" ", "").isalpha():
            raise Exception("El nombre solo puede tener letras")

        if not apellido.replace(" ", "").isalpha():
            raise Exception("El apellido solo puede tener letras")

        if len(documento) < 6 or len(documento) > 15:
            raise Exception("El documento solo puede tener entre 6 y 15 caracteres")

        # Validar números en documento
        if not documento.isdigit():
            raise Exception("El documento solo puede tener valores numéricos")

        # Validación de fecha
        try:
            fecha_formato = datetime.strptime(fecha, "%Y-%m-%d").date()
        except:
            raise Exception("Fecha inválida. Formato esperado: aaaa-mm-dd")

    def _validar_salida(self, fechaSalida:str):
        if not fechaSalida.strip():
            raise Exception("El campo de fecha de salida no puede estar vacio")
        try:
            fecha_salida_formato = datetime.strptime(fechaSalida, "%Y-%m-%d").date()
        except:
            raise Exception("Fecha invalida. Formato esperado: aaaa-mm-dd")

        # validacion de que no se coloque una fecha inferior a la fecha de ingreso
        if fecha_salida_formato <= self.fechaIngreso:
            raise Exception("La fecha de salida debe ser mayor a la de ingreso.")


class Interfaz:
    def __init__(self):

        self.__hotel = Hotel()
        self.__numeroHabitacion=None

        self._panel_principal = tk.Tk()
        self._panel_principal.title("Sistema de gestión de habitaciones")
        self._panel_principal.resizable(False, False)
        self._panel_principal.configure(bg="#2C3E50")

        self.__panel_actual = None

        self._panel_principal.grid_columnconfigure(0, weight=1)
        self.__crear_menu()
        self.__consulta_habitaciones()

    def __crear_menu(self):
        menu_bar = tk.Menu(self._panel_principal)
        self._panel_principal.config(menu=menu_bar)

        opciones_menu = tk.Menu(menu_bar, tearoff=0)
        opciones_menu.add_command(label="Consultar habitaciones", command=self.__consulta_habitaciones)
        opciones_menu.add_command(label="Salida de huéspedes", command=self.__salida_huespedes)
        menu_bar.add_cascade(label="Menú", menu=opciones_menu)

    def __limpiarPanel(self):
        if self.__panel_actual:
            self.__panel_actual.destroy()

    def __consulta_habitaciones(self):
        self.__limpiarPanel()

        self.__panel_actual = tk.Frame(
            self._panel_principal,
            padx=20,
            bg="#2C3E50"
        )
        self.__panel_actual.grid(row=0, column=0, sticky="nsew")

        titulo = tk.Label(
            self.__panel_actual,
            text="Reserva de habitaciones:",
            font=("Arial", 16, "bold"),
            fg="#ECF0F1",
            bg="#2C3E50"
        )
        titulo.grid(row=0, column=0, pady=20)

        habitaciones_container = tk.Frame(self.__panel_actual, bg="#2C3E50")
        habitaciones_container.grid(row=1, column=0)
        
        style = ttk.Style()
        style.configure("CustomSeparator.TSeparator", background="#2C3E50")

        def habitacion_estandar(numero, precio, estado, col, r):
            habitacion = tk.Frame(
                habitaciones_container,
                bg="#DEC11B",
                width=150,
                height=100
            )
            habitacion.grid(column=col, row=r, padx=10, pady=10)
            habitacion.grid_propagate(False)

            titulo = tk.Label(
                habitacion,
                text=f"Habitación {numero}",
                font=("Arial", 14, "bold"),
                fg="#2C3E50",
                bg="#DEC11B"
            )
            titulo.pack(pady=(5,0))

            ttk.Separator(habitacion, style="CustomSeparator.TSeparator", orient='horizontal', ).pack(fill='x')
            val = tk.Label(
                habitacion,
                text=f"Valor: {precio} $",
                font=("Arial", 12, "bold"),
                fg="#2C3E50",
                bg="#DEC11B"
            )
            val.pack(pady=(7,0), padx=7)

            disponibilidad = tk.Label(
                habitacion,
                text="Disponible" if estado else "No Disponible",
                font=("Arial", 12, "bold"),
                fg="#221BDE" if estado else "#DE1B1B",
                bg="#DEC11B"
            )
            disponibilidad.pack(pady=(2,5))


        for idx, hab in enumerate(self.__hotel._habitaciones):
            col = idx % 5 
            row = idx // 5
            habitacion_estandar(hab._numero, hab._precioDia, hab._disponible, col, row)
        disponibles = False
        for habitacion in self.__hotel._habitaciones:
            if habitacion._disponible:
                disponibles = True
                break

        if disponibles:

            selector_container = tk.Frame(
                self.__panel_actual,
                bg="#2C3E50"
            )
            selector_container.grid(row=2, column=0, pady=(20,7))

            selector_container.grid_columnconfigure(0, weight=1)
            selector_container.grid_columnconfigure(1, weight=1)

            field = tk.Frame(selector_container, bg="#2C3E50")
            field.grid(row=0, column=0)

            tk.Label(
                field,
                text="Habitación a reservar",
                font=("Arial", 10),
                fg="#ECF0F1",
                bg="#2C3E50"
            ).grid(row=0, column=0, pady=3)

            self.__input_numero_habitacion = tk.Spinbox(
                field, 
                from_=1, 
                to=len(self.__hotel._habitaciones), 
                width=3, 
                state="readonly",
                font=("Arial", 12),
                justify="center"
            )
            self.__input_numero_habitacion.grid(row=0, column=1, padx=4)

            boton_aceptar_seleccion_reserva = tk.Button(
                selector_container,
                command=self.__validar_estadado_reserva,
                text="Aceptar",
                width=9, height=1,
                font=("Arial", 10, "bold"),
                bg="#2980B9", fg="white"
            )
            boton_aceptar_seleccion_reserva.grid(row=0, column=1, padx=5)
            tk.Label(
                    self.__panel_actual,
                    text="Recuerda seleccionar una habitacion disponible",
                    font=("Arial", 8),
                    foreground="#BDC3C7",
                    background="#2C3E50"
                ).grid(row=3, column=0, pady=(0, 10))
        else:
            mensaje = tk.Label(self.__panel_actual, 
                            text="No hay habitaciones disponibles para reservar", 
                            font=("Arial", 15, "bold"),
                            fg="#F39C12",
                            bg="#2C3E50")
            mensaje.grid(row=2, column=0, pady=(15, 20), padx=40)
    
    def __validar_estadado_reserva(self):
        self.__numeroHabitacion=int(self.__input_numero_habitacion.get())
        if self.__hotel._habitaciones[self.__numeroHabitacion-1]._disponible:
            # messagebox.showinfo("Info", f"Habitacion {int(self.__input_numero_habitacion.get())} seleccionada. {self.__hotel._habitaciones[int(self.__input_numero_habitacion.get())-1]._disponible}")
            messagebox.showinfo("Info", f"Habitacion {int(self.__numeroHabitacion)} seleccionada.")
            
            self.__formulario_reserva(self.__numeroHabitacion)
        else:
            messagebox.showerror("Info", f"La habitacion número {int(self.__input_numero_habitacion.get())} se escuentra ocupada.")

    def __formulario_reserva(self, numHabitacion):
        self.__limpiarPanel()

        self.__panel_actual = tk.Frame(
            self._panel_principal,
            padx=20,
            pady=20,
            bg="#2C3E50"
        )
        self.__panel_actual.grid(row=0, column=1, sticky="nsew")

        titulo = tk.Label(
            self.__panel_actual,
            text=f"Habitacion {numHabitacion} seleccionada:",
            font=("Arial", 16, "bold"),
            fg="#ECF0F1",
            bg="#2C3E50"
        )
        titulo.grid(row=0, column=0, pady=(0, 12))

        # defino el contenedor en el cual cargare los campos del formulario
        form = tk.Frame(self.__panel_actual, bg="#2C3E50")
        form.grid(row=1, column=0)

        # definimos una funcion que contendra el estilo del label estandar utilizados par los campos
        def label_estandar(texto, fila):
            tk.Label(
                form,
                text=texto,
                font=("Arial", 10),
                fg="#ECF0F1",
                bg="#2C3E50",
                anchor="w"
            ).grid(row=fila, column=0, sticky="w", pady=3)

        label_estandar("Valor Día:", 0)

        valor = tk.Entry(
            form, 
            width=18, 
            font=("Arial", 12), 
            bg="#FFFFFF", 
            justify="left"
        )
        valor.grid(row=0, column=1, pady=3)

        # Insertar valor
        valor.insert(0, f"{self.__hotel._habitaciones[numHabitacion-1]._precioDia} $")

        # Bloquear edición
        valor.config(state="disabled")
        
        label_estandar("Fecha ingreso:", 1)
        self.__input_fecha= DateEntry(
            form,
            width=16,
            font=("Arial", 12),
            date_pattern="yyyy-mm-dd",
            # state="readonly"
        )
        self.__input_fecha.grid(row=1, column=1, pady=3)

        tk.Label(
            form,
            text=f"Informacion huésped:",
            font=("Arial", 15, "bold"),
            fg="#ECF0F1",
            bg="#2C3E50"
        ).grid(row=2, column=0, pady=(12, 7), columnspan=2)


        label_estandar("Nombres:", 3)
        self.__input_nombre = tk.Entry(
            form, width=18, font=("Arial", 12), bg="#FFFFFF", justify="left"
        )
        self.__input_nombre.grid(row=3, column=1, pady=3)
        self.__input_nombre.focus()


        label_estandar("Apellidos:", 4)
        self.__input_apellido = tk.Entry(
            form, width=18, font=("Arial", 12), bg="#FFFFFF", justify="left"
        )
        self.__input_apellido.grid(row=4, column=1, pady=3)
        
        label_estandar("Doc.Identidad:", 5)
        self.__input_documento = tk.Entry(
            form, width=18, font=("Arial", 12), bg="#FFFFFF", justify="left"
        )
        self.__input_documento.grid(row=5, column=1, pady=3)

        
        botones = tk.Frame(self.__panel_actual, bg="#2C3E50")
        botones.grid(row=2, column=0, pady=20)

        boton_aceptar_reserva = tk.Button(
            botones, text="Aceptar",
            command=self.__aceptarReserva,
            width=7, height=1,
            font=("Arial", 10, "bold"),
            bg="#27AE42", fg="white"
        )
        boton_aceptar_reserva.grid(row=0, column=0, padx=5)

        boton_cancelar_reserva = tk.Button(
            botones, text="Cancelar",
            command=self.__cancelarAccion,
            width=8, height=1,
            font=("Arial", 10, "bold"),
            bg="#B92929", fg="white"
        )
        boton_cancelar_reserva.grid(row=0, column=1, padx=5)


        self.__resultado = tk.Label(
            self.__panel_actual,
            text="Recuerda ingresar valores válidos ;)",
            font=("Arial", 11),
            bg="#34495E",
            fg="#F39C12",
            padx=20, pady=10,
            width=35,
            anchor="center"
        )
        self.__resultado.grid(row=3, column=0, pady=10)

        info_enter = tk.Label(
            self.__panel_actual,
            text="Al presionar 'Enter' se confirmara la reserva",
            font=("Arial", 8),
            foreground="#BDC3C7",
            background="#2C3E50"
        )
        info_enter.grid(row=4, column=0, pady=5)

        inputs = [
            self.__input_nombre,
            self.__input_apellido,
            self.__input_fecha,
            self.__input_documento
        ]
        for w in inputs:
            w.bind("<Return>", lambda e: self.__aceptarReserva())
    
    def __aceptarReserva(self):
        try:
            fecha = self.__input_fecha.get()
            nombre = self.__input_nombre.get()
            apellido = self.__input_apellido.get()
            documento = self.__input_documento.get()
            habitacion = self.__hotel._habitaciones[self.__numeroHabitacion-1]
            
            Huesped.validar_info(
                fechaIngreso=fecha,
                nombre=nombre,
                apellido=apellido,
                documento=documento
            )
            fecha_ingreso_formato = datetime.strptime(fecha, "%Y-%m-%d").date()
            huesped=Huesped(
                nombre=nombre,
                apellido=apellido,
                documento=documento,
                habitacion=habitacion,
                fechaIngreso=fecha_ingreso_formato
            )
            self.__hotel._huespedes.append(huesped)
            self.__hotel._habitaciones[self.__numeroHabitacion-1]._disponible=False
            self.__hotel._habitaciones[self.__numeroHabitacion-1]._huesped=huesped
            messagebox.showinfo("Ingreso exitoso", f"La habitacion {self.__numeroHabitacion} ha sido reservada con exito")
            self.__consulta_habitaciones()
            



        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.__resultado.config(text=e, fg="#FF3838")
            
        


    def __cancelarAccion(self): 
        messagebox.showerror("Accion Cancelada", "La accion ha sido cancelada.")
        self.__consulta_habitaciones()
        return
        
    
    
    def __salida_huespedes(self):
        noDisponibles = False
        for habitacion in self.__hotel._habitaciones:
            if not habitacion._disponible:
                noDisponibles=True
                break
        if not noDisponibles:
            messagebox.showerror("Error", f"No hay ninguna habitación actualmente ocupada")
            return

        numero_cancelacion= simpledialog.askinteger(
            "Cancelacion de habitacion",
            "Digite el numero de la habitacion que desea cancelar:",
            minvalue=1,
            maxvalue=len(self.__hotel._habitaciones)
        )
        if self.__hotel._habitaciones[numero_cancelacion-1]._disponible:
            messagebox.showerror("Error", f"La habitacion {numero_cancelacion} actualmente no se encuentra ocupada")
        else:
            # Actualizamos al nuevo numero de haviitacion de referencia
            self.__numeroHabitacion=numero_cancelacion
            self.__formulario_cancelacion()
            
   
    def __formulario_cancelacion(self):
        self.__limpiarPanel()

        self.__panel_actual = tk.Frame(
            self._panel_principal,
            padx=20, pady=20,
            bg="#2C3E50"
        )
        self.__panel_actual.grid(row=0, column=1, sticky="nsew")

        # Título
        titulo = tk.Label(
            self.__panel_actual,
            text=f"Habitacion a cancelar: {self.__numeroHabitacion}",
            font=("Arial", 16, "bold"),
            fg="#ECF0F1",
            bg="#2C3E50"
        )
        titulo.grid(row=0, column=0, pady=(0, 12))

        # Contenedor del formulario
        form = tk.Frame(self.__panel_actual, bg="#2C3E50")
        form.grid(row=1, column=0)

        def label_estandar(texto, fila):
            tk.Label(
                form, text=texto,
                font=("Arial", 10),
                fg="#ECF0F1",
                bg="#2C3E50",
                anchor="w"
            ).grid(row=fila, column=0, sticky="w", pady=3)

        label_estandar("Fecha ingreso:", 0)

        valor = tk.Entry(
            form, width=18,
            font=("Arial", 12),
            bg="#FFFFFF",
            justify="left",
            state="readonly"
        )
        valor.grid(row=0, column=1, pady=3)

        valor.config(state="normal")
        valor.insert(0, self.__hotel._habitaciones[self.__numeroHabitacion-1]._huesped.fechaIngreso)
        valor.config(state="readonly")

        label_estandar("Fecha salida:", 1)

        self.__input_fecha_salida = DateEntry(
            form,
            width=16,
            font=("Arial", 12),
            date_pattern="yyyy-mm-dd",
        )
        self.__input_fecha_salida.grid(row=1, column=1, pady=3)
        self.__input_fecha_salida.focus()
        
        boton_validar_fecha = tk.Button(
            form,
            text="Calcular",
            command=self.__validacion_salida,
            width=13, height=1,
            font=("Arial", 10, "bold"),
            bg="#2980B9", fg="white"
        )
        boton_validar_fecha.grid(row=2, column=0, columnspan=2, pady=(10, 20))
        
        self.__input_fecha_salida.bind(
            "<Return>",
            lambda e: self.__validacion_salida()
        )

        label_estandar("Cantidad Días:", 3)
        
        self.__nDias = tk.Entry(
            form, width=18, font=("Arial", 12),
            bg="#2C3E50", state="readonly"
        )
        self.__nDias.grid(row=3, column=1, pady=3)

        label_estandar("Total:", 4)
        self.__total = tk.Entry(
            form, width=18, font=("Arial", 12),
            bg="#2C3E50", state="readonly"
        )
        self.__total.grid(row=4, column=1, pady=3)

        botones = tk.Frame(self.__panel_actual, bg="#2C3E50")
        botones.grid(row=2, column=0, pady=(15, 10))
        
        self.__boton_aceptar_salida = tk.Button(
            botones, text="Registrar Salida",
            command=lambda: self.__aceptarSalida(),
            width=14, height=1,
            font=("Arial", 10, "bold"),
            bg="#000000", fg="black",
            state="disabled"
        )
        self.__boton_aceptar_salida.grid(row=0, column=0, padx=5)

        boton_cancelar_reserva = tk.Button(
            botones, text="Cancelar",
            command=self.__cancelarAccion,
            width=8, height=1,
            font=("Arial", 10, "bold"),
            bg="#B92929", fg="white"
        )
        boton_cancelar_reserva.grid(row=0, column=1, padx=5)
        
        self.__resultado = tk.Label(
            self.__panel_actual,
            text="Recuerda ingresar valores válidos ;)",
            font=("Arial", 11),
            bg="#34495E",
            fg="#F39C12",
            padx=20, pady=10,
            width=35,
            anchor="center"
        )
        self.__resultado.grid(row=3, column=0, pady=(5, 10))

        info_enter = tk.Label(
            self.__panel_actual,
            text="Al presionar 'Enter' se validara la fecha de salida",
            font=("Arial", 8),
            foreground="#BDC3C7",
            background="#2C3E50"
        )
        info_enter.grid(row=4, column=0, pady=5)


    def __validacion_salida(self):
        fecha_str = self.__input_fecha_salida.get()  
        habitacion = self.__hotel._habitaciones[self.__numeroHabitacion - 1]
        huesped = habitacion._huesped

        try:
            # Validar fecha
            huesped._validar_salida(fecha_str)

            # Convertir string a fecha real
            fecha_salida = datetime.strptime(fecha_str, "%Y-%m-%d").date()

            # Calcular días
            dias = (fecha_salida - huesped.fechaIngreso).days

            # Calcular total
            total_val = dias * habitacion._precioDia

            # Actualizar campos de los Entry
            self.__nDias.config(state="normal")
            self.__nDias.delete(0, tk.END)
            self.__nDias.insert(0, dias)
            self.__nDias.config(state="readonly")

            self.__total.config(state="normal")
            self.__total.delete(0, tk.END)
            self.__total.insert(0, f"{total_val} $")
            self.__total.config(state="readonly")

            # Habilitar el botón de registrar
            self.__boton_aceptar_salida.config(state="normal", bg="#27AE42", fg="white",)
            self.__resultado.config(text=f"Valor total a pagar: {total_val} $", fg="#27AE42")

            

        except Exception as e:
            self.__nDias.config(state="normal")
            self.__nDias.delete(0, tk.END)
            self.__nDias.config(state="readonly")

            self.__total.config(state="normal")
            self.__total.delete(0, tk.END)
            self.__total.config(state="readonly")

            self.__boton_aceptar_salida.config(state="disabled", bg="#000000", fg="black",)

            messagebox.showerror("Error", str(e))
            self.__resultado.config(text=e, fg="#FF3838")

            
        
    def __aceptarSalida(self):

        for huesped in self.__hotel._huespedes:
            if huesped.fechaSalida==None and huesped.habitacion._numero==self.__numeroHabitacion:
                huesped.fechaSalida= datetime.strptime(self.__input_fecha_salida.get()  , "%Y-%m-%d").date()
        for huesped in self.__hotel._huespedes:
            print("="*10)
            print(huesped.nombre)
            print(huesped.apellido)
            print(huesped.documento)
            print(huesped.fechaIngreso)
            print(huesped.fechaSalida)
            print(huesped.habitacion)
            

        self.__hotel._habitaciones[self.__numeroHabitacion-1]._disponible=True
        self.__hotel._habitaciones[self.__numeroHabitacion-1]._huesped=None
        messagebox.showinfo("Salida Exitosa", f"La habitacion {self.__numeroHabitacion} ha sido desalojada con exito")
        self.__consulta_habitaciones()


class Main:
    @staticmethod
    def main():
        app = Interfaz()
        app._panel_principal.mainloop()

if __name__ == "__main__":
    Main.main()
