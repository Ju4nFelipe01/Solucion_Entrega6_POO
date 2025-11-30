# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import os
import pickle



class Nomina:
    def __init__(self):
        base_ruta = os.path.dirname(os.path.abspath(__file__))
        self.__ruta_archivo_auxiliar = os.path.join(base_ruta, "aux.pkl")
        self._informacion = self.__get_informacion()

    def __get_informacion(self):
        if not os.path.exists(self.__ruta_archivo_auxiliar):
            with open(self.__ruta_archivo_auxiliar, "wb") as f:
                pickle.dump([], f)  # lista vacía
        with open(self.__ruta_archivo_auxiliar, "rb") as f:
            return pickle.load(f)

    def _set_informacion(self, informacion):
        with open(self.__ruta_archivo_auxiliar, "wb") as f:
            pickle.dump(informacion, f)
        self._informacion = informacion

    def _calcular_nomina(self):
        total_nomina = 0
        for empleado in self._informacion:
            total_nomina += empleado.nomina
        return total_nomina

    def _guardar_nomina(self, archivo):
        base_ruta = os.path.dirname(os.path.abspath(__file__))
        ruta_carpeta = os.path.join(base_ruta, archivo)

        # Crear la carpeta si no existe
        if not os.path.exists(ruta_carpeta):
            os.makedirs(ruta_carpeta)

        # Ruta completa del archivo
        self.__ruta_archivo_nomina = os.path.join(ruta_carpeta, "Nómina.txt")

        # Guardar la información en el archivo
        with open(self.__ruta_archivo_nomina, "w", encoding="utf-8") as f:
            for empleado in self._informacion:
                f.write(f"Nombre = {empleado.nombres}\n")
                f.write(f"Apellido = {empleado.apellidos}\n")
                f.write(f"Cargo = {empleado.cargo}\n")
                f.write(f"Género = {empleado.genero}\n")
                f.write(f"Salario Día = {empleado.salarioDia} $\n")
                f.write(f"Días Trabajados = {empleado.diasTrabajados}\n")
                f.write(f"Otros Ingresos = {empleado.otrosIngresos} $\n")
                f.write(f"Pagos Salud = {empleado.pagosSalud} $\n")
                f.write(f"Aportes Pensiones = {empleado.aportesPension} $\n")
                f.write(f"Nómina Empleado = {empleado.nomina} $\n")
                f.write("="*40 + "\n")
            f.write(f"Total nómina = {self._calcular_nomina()} $\n")

class Empleado:
    def __init__(
        self, 
        nombres: str, 
        apellidos: str,
        cargo: str,  
        genero: str,
        salarioDia: float,
        diasTrabajados: int,
        otrosIngresos: float,
        pagosSalud: float,
        aportesPension: float
    ):
        
        self.nombres = nombres
        self.apellidos = apellidos
        self.cargo = cargo
        self.genero = genero
        self.salarioDia = salarioDia
        self.diasTrabajados = diasTrabajados
        self.otrosIngresos = otrosIngresos
        self.pagosSalud = pagosSalud
        self.aportesPension = aportesPension
        self.nomina = self.calcularNomina()

    def calcularNomina(self) -> float:
        return (
            (self.diasTrabajados * self.salarioDia) 
            + self.otrosIngresos 
            - (self.pagosSalud + self.aportesPension)
        )
    @staticmethod
    def validarInfo(
            nombre,
            apellido,
            salario_dia,
            dias_trabajados,
            otros_ingresos,
            pagos_salud,
            aporte_pensiones):
        # validamos que ningun campo este vacio
            if (not nombre.strip() or 
                not apellido.strip() or
                not salario_dia.strip() or
                not dias_trabajados.strip() or
                not otros_ingresos.strip() or
                not pagos_salud.strip() or
                not aporte_pensiones.strip()):
                raise Exception("Ningún campo puede estar vacío.")

            # validamos el formato de la info de los nombres y apellidos
            if not nombre.replace(" ", "").isalpha():
                raise Exception("El nombre únicamente puede contener letras.")

            if not apellido.replace(" ", "").isalpha():
                raise Exception("El apellido únicamente puede contener letras.")

            # convertimos los campos numericos a su respectivo formato, validando de una vez el formato de estos
            try:
                salario_dia_val = float(salario_dia)
                dias_trabajados_val = int(dias_trabajados)
                otros_ingresos_val = float(otros_ingresos)
                pagos_salud_val = float(pagos_salud)
                aporte_pensiones_val = float(aporte_pensiones)
            except ValueError:
                raise Exception("Los campos numéricos contienen valores inválidos.")

            # validamos la info dentro de los campos numericos
            if salario_dia_val <= 0:
                raise Exception("El salario por día debe ser mayor a cero.")

            if dias_trabajados_val < 1 or dias_trabajados_val > 31:
                raise Exception("Los días trabajados deben estar entre 1 y 31.")

            if pagos_salud_val <= 0:
                raise Exception("El pago a salud debe ser mayor a cero.")

            if aporte_pensiones_val <= 0:
                raise Exception("El aporte a pensión debe ser mayor a cero.")

            if otros_ingresos_val < 0:
                raise Exception("Los ingresos adicionales no pueden ser negativos.") 

class Interfaz:
    def __init__(self):
        # Estanciamos un objeto de cotnactos a fin de poder acceder a sus metodos e _informacion
        self.__nomina=Nomina()
        self.__empleados=self.__nomina._informacion
        self._panel_principal = tk.Tk()
        self._panel_principal.title("Sistema de gestion de nómina")
        # self._panel_principal.geometry("400x380")
        self._panel_principal.resizable(False, False)
        self._panel_principal.configure(bg="#2C3E50")
        
        self.__panel_actual=None

        self._panel_principal.grid_columnconfigure(0, weight=1)
        self._panel_principal.grid_columnconfigure(1, weight=0)
        self._panel_principal.grid_columnconfigure(2, weight=1)
        self.__crear_menu()


        self.__interfaz_calcular_nomina()

        # self.__interfaz_calcular_nomina()

    def __crear_menu(self):
        menu_bar = tk.Menu(self._panel_principal)
        self._panel_principal.config(menu=menu_bar)

        opciones_menu = tk.Menu(menu_bar, tearoff=0)
        opciones_menu.add_command(label="Agregar Empleado", command=self.__interfaz_añadir_empleado)
        opciones_menu.add_command(label="Calcular Nómina", command=self.__interfaz_calcular_nomina)
        opciones_menu.add_separator()
        opciones_menu.add_command(label="Guardar Nómina", command=self.__interfaz_guardar_nomina)
        
        menu_bar.add_cascade(label="Opciones", menu=opciones_menu)

    # Método que elimina el panel anterior y crea uno nuevo
    def __limpiarPanel(self):
        if self.__panel_actual:
            self.__panel_actual.destroy()

    def __interfaz_calcular_nomina(self):
        if len(self.__empleados)>0:
            
            # limpiamos el contenedor anterios
            self.__limpiarPanel()
            
            # self._panel_principal.geometry("400x380")
            # Definimos un panel con la nueva _informacion
            self.__panel_actual = tk.Frame(self._panel_principal, padx=10, pady=10)

            self.__panel_actual.grid(row=0, column=1, sticky="nsew")
            self.__panel_actual.grid_columnconfigure(0, weight=1)
            self.__panel_actual.grid_columnconfigure(1, weight=0)
            self.__panel_actual.grid_columnconfigure(2, weight=1)
            self.__panel_actual.configure(bg="#2C3E50")

            
            titulo = tk.Label(self.__panel_actual, 
                            text="Calcular nómina:", 
                            font=("Arial", 16, "bold"),
                            foreground="#ECF0F1",
                            background="#2C3E50")
            titulo.grid(row=0, column=0, columnspan=3, pady=15)

            
           
            

            # Definimos un contenedor de la tabla
            tabla_frame = tk.Frame(self.__panel_actual, bg="#2C3E50")
            tabla_frame.grid(row=2, column=0, columnspan=3, pady=0)


            
            self.__boton_agregar_empleado = tk.Button(
                self.__panel_actual,
                text="Agregar Empleado",
                command=self.__interfaz_añadir_empleado,
                width=15,
                height=1,
                font=("Arial", 10, "bold"),
                bg="#27AE42",
                fg="white"
                )
            self.__boton_agregar_empleado.grid(row=1, column=0, pady=(0,7), sticky="w")

            
            scrollbar_y = tk.Scrollbar(tabla_frame, orient="vertical")
            scrollbar_y.pack(side="right", fill="y")

            # Definimos el styl para modificar el estilo del componente de la tabla
            style = ttk.Style()
            # Customizamos el cuerpo de la tabla
            style.configure("Custom.Treeview",
                            background="#2C3E50",      
                            foreground="white",          
                            fieldbackground="#2C3E50",  
                            font=("Arial", 11))
            # Customizamos el encabezado
            style.configure("Custom.Treeview.Heading",
                    background="#34495E",
                    foreground="black",
                    font=("Arial", 11, "bold"))

            style.map("Custom.Treeview",
                    background=[("selected", "#405A74")])  
            

            empleados = [(
                id+1,
                empleado.nombres,
                empleado.apellidos,
                f"{empleado.nomina} $",
                ) for id, empleado in enumerate(self.__empleados)]
            
    
            nregistros=min(len(empleados), 5)


            # Crear Treeview para empleados
            self.__tabla_empleados = ttk.Treeview(
                tabla_frame,
                columns=(
                    "ID",
                    "Nombres",
                    "Apellidos",
                    "Sueldo"
                ),
                show="headings",
                height=nregistros,
                yscrollcommand=scrollbar_y.set,
                style="Custom.Treeview"
            )

            # Configurar encabezados
            for col in self.__tabla_empleados["columns"]:
                self.__tabla_empleados.heading(col, text=col)

            # Ajustar ancho de algunas columnas
            self.__tabla_empleados.column("ID", width=45, anchor="center")
            self.__tabla_empleados.column("Nombres", width=120, anchor="center")
            self.__tabla_empleados.column("Apellidos", width=120, anchor="center")
            self.__tabla_empleados.column("Sueldo", width=110, anchor="center")

            # Empaquetar Treeview y configurar scroll
            self.__tabla_empleados.pack(fill="both", expand=True)
            scrollbar_y.config(command=self.__tabla_empleados.yview)

            for emp in empleados:
                self.__tabla_empleados.insert("", "end", values=emp)

            self.__tabla_empleados.bind("<<TreeviewSelect>>", self.__on_employ_select)

            self.__boton_guardar_nomina = tk.Button(
                self.__panel_actual,
                text="Guardar Nomina",
                command=self.__interfaz_guardar_nomina,
                width=13,
                height=1,
                font=("Arial", 10, "bold"),
                 bg="#2980B9",
                fg="white"
            )
            self.__boton_guardar_nomina.grid(row=3, column=0, pady=10, sticky="w")
            self.__resultado = tk.Label(
                self.__panel_actual,
                text=f"Nómina total = {self.__nomina._calcular_nomina()} $",
                font=("Arial", 11),
                bg="#34495E",
                fg="#38FFF5",
                padx=20, pady=10,
                width=35,
                anchor="center"
            )
            self.__resultado.grid(row=4, column=0, pady=10)

            info_enter = tk.Label(
                self.__panel_actual,
                text="Al seleccionar un empleado podra ver su nómina",
                font=("Arial", 8),
                foreground="#BDC3C7",
                background="#2C3E50"
            )
            info_enter.grid(row=5, column=0, pady=5)
            
            
        else:
            self.__interfaz_añadir_empleado()


    def __on_employ_select(self, event):
        seleccionado = self.__tabla_empleados.selection() 

        valores = self.__tabla_empleados.item(seleccionado[0], "values")  # corregido
        self.__resultado.config(
            text=f"Nómina de '{valores[1]} {valores[2]}' = {valores[3]}",
            fg="#27AE42")


    def __interfaz_añadir_empleado(self):
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
            text="Añadir empleado:",
            font=("Arial", 16, "bold"),
            fg="#ECF0F1",
            bg="#2C3E50"
        )
        titulo.grid(row=0, column=0, pady=(0, 20))

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


        label_estandar("Nombres:", 0)
        self.__input_nombre = tk.Entry(
            form, width=18, font=("Arial", 12), bg="#FFFFFF", justify="left"
        )
        self.__input_nombre.grid(row=0, column=1, pady=3)


        label_estandar("Apellidos:", 1)
        self.__input_apellido = tk.Entry(
            form, width=18, font=("Arial", 12), bg="#FFFFFF", justify="left"
        )
        self.__input_apellido.grid(row=1, column=1, pady=3)

        label_estandar("Cargo:", 2)
        opciones = ["Directivo", "Estratégico", "Operativo"]
        self.__input_cargo = ttk.Combobox(
            form, values=opciones, state="readonly", font=("Arial", 12),width=16, justify="left"
        )
        self.__input_cargo.current(0)
        self.__input_cargo.grid(row=2, column=1, pady=3, sticky="w", padx=(4,0))

        label_estandar("Género:", 3)

        f_genero = tk.Frame(form, bg="#2C3E50")
        f_genero.grid(row=3, column=1, pady=3, sticky="w")

        self.__input_genero = tk.StringVar(value="Masculino")

        rb_m = tk.Radiobutton(
            f_genero, text="Masculino", value="Masculino",
            variable=self.__input_genero,
            font=("Arial", 10), fg="#ECF0F1", bg="#2C3E50",
            selectcolor="#34495E", activebackground="#2C3E50"
        )
        rb_m.pack(side="left")

        rb_f = tk.Radiobutton(
            f_genero, text="Femenino", value="Femenino",
            variable=self.__input_genero,
            font=("Arial", 10), fg="#ECF0F1", bg="#2C3E50",
            selectcolor="#34495E", activebackground="#2C3E50"
        )
        rb_f.pack(side="left")

        label_estandar("Salario por día:", 4)
        self.__input_sario_dia = tk.Entry(
            form, width=18, font=("Arial", 12), bg="#FFFFFF", justify="left"
        )
        self.__input_sario_dia.grid(row=4, column=1, pady=3)

        label_estandar("Días trabajados al mes:", 5)
        self.__input_dias_trabajados = tk.Spinbox(
            form, from_=1, to=31, width=5, font=("Arial", 12), bg="#FFFFFF", justify="center"
        )
        self.__input_dias_trabajados.grid(row=5, column=1, padx=(4,0), pady=3, sticky="w")

        label_estandar("Otros ingresos:", 6)
        self.__input_otros_ingresos = tk.Entry(
            form, width=18, font=("Arial", 12), bg="#FFFFFF", justify="left"
        )
        self.__input_otros_ingresos.grid(row=6, column=1, pady=3)

        label_estandar("Pagos por salud:", 7)
        self.__input_pagos_salud = tk.Entry(
            form, width=18, font=("Arial", 12), bg="#FFFFFF", justify="left"
        )
        self.__input_pagos_salud.grid(row=7, column=1, pady=3)


        label_estandar("Aportes pensiones:", 8)
        self.__input_aporte_pensiones = tk.Entry(
            form, width=18, font=("Arial", 12), bg="#FFFFFF", justify="left"
        )
        self.__input_aporte_pensiones.grid(row=8, column=1, pady=3)

        botones = tk.Frame(self.__panel_actual, bg="#2C3E50")
        botones.grid(row=2, column=0, pady=20)

        self.boton_crear_empleado = tk.Button(
            botones, text="Crear Empleado",
            command=self.__guardarempleado,
            width=13, height=1,
            font=("Arial", 10, "bold"),
            bg="#27AE42", fg="white"
        )
        self.boton_crear_empleado.grid(row=0, column=0, padx=5)

        self.boton_calcular_nomina = tk.Button(
            botones, text="Calcular Nómina",
            command=self.__interfaz_calcular_nomina,
            width=14, height=1,
            font=("Arial", 10, "bold"),
            bg="#2980B9", fg="white"
        )
        self.boton_calcular_nomina.grid(row=0, column=1, padx=5)


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
            text="Al presionar 'Enter' se guardará el empleado",
            font=("Arial", 8),
            foreground="#BDC3C7",
            background="#2C3E50"
        )
        info_enter.grid(row=4, column=0, pady=5)

        inputs = [
            self.__input_nombre,
            self.__input_apellido,
            self.__input_cargo,
            self.__input_sario_dia,
            self.__input_dias_trabajados,
            self.__input_otros_ingresos,
            self.__input_pagos_salud,
            self.__input_aporte_pensiones
        ]
        for w in inputs:
            w.bind("<Return>", lambda e: self.__guardarempleado())
 
    def __interfaz_guardar_nomina(self):
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
            text="Guardar nómina:",
            font=("Arial", 16, "bold"),
            fg="#ECF0F1",
            bg="#2C3E50"
        )
        titulo.grid(row=0, column=0, pady=(0, 20))
        
        tk.Label(
                self.__panel_actual,
                text="Nombre carpeta:",
                font=("Arial", 10),
                fg="#ECF0F1",
                bg="#2C3E50",
                justify="center"
            ).grid(row=1, column=0, pady=3)

        self.__input_archivo = tk.Entry(
            self.__panel_actual, 
            width=23, 
            font=("Arial", 12), 
            bg="#FFFFFF", 
            justify="center"
        )
        self.__input_archivo.grid(row=2, column=0, pady=7)
        self.__input_archivo.insert(0, "nómina1") 
        self.__input_archivo.focus_set()


        botones = tk.Frame(self.__panel_actual, bg="#2C3E50")
        botones.grid(row=3, column=0, pady=20)

        self.__boton_confirmar_guardado = tk.Button(
            botones, text="Guardar",
            command=self.__confirmar_guardado,
            width=7, height=1,
            font=("Arial", 10, "bold"),
            bg="#2980B9", fg="white"
        )
        self.__boton_confirmar_guardado.grid(row=0, column=0, padx=5)

        self.__boton_volver = tk.Button(
            botones, text="Volver",
            command=self.__interfaz_calcular_nomina,
            width=6, height=1,
            font=("Arial", 10, "bold"),
            bg="#27AE42", fg="white"
        )
        self.__boton_volver.grid(row=0, column=1, padx=5)


        self.__resultado = tk.Label(
            self.__panel_actual,
            text="Defina una carpeta en la que almacenar la nómina",
            font=("Arial", 11),
            bg="#34495E",
            fg="#F39C12",
            padx=20, pady=10,
            width=35,
            anchor="center"
        )
        self.__resultado.grid(row=4, column=0, pady=10)

        tk.Label(
            self.__panel_actual,
            text="Al presionar 'Enter' se guardara la nómina",
            font=("Arial", 8),
            foreground="#BDC3C7",
            background="#2C3E50"
        ).grid(row=5, column=0, pady=5)

        
        self.__input_archivo.bind("<Return>", lambda e: self.__confirmar_guardado())
 
    def __confirmar_guardado(self):
        try:
            # Obtener nombre del archivo o carpeta desde el Entry
            nombre_archivo = self.__input_archivo.get()

            if not nombre_archivo.strip():
                raise ValueError("El nombre de la carpeta no puede estar vacio")

            # Llamar al método de guardar nómina pasando el string
            self.__nomina._guardar_nomina(nombre_archivo)

            messagebox.showinfo(
                "Operación Exitosa",
                f"La nómina ha sido guardada exitosamente en la carpeta '{nombre_archivo}'"
            )
            self.__interfaz_calcular_nomina()

        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.__resultado.config(text=str(e), fg="#FF3838")


    def __guardarempleado(self):
        try:
            # cargamos la info de los inputs
            nombre = self.__input_nombre.get()
            apellido = self.__input_apellido.get()
            genero = self.__input_genero.get()
            cargo = self.__input_cargo.get()
            salario_dia = self.__input_sario_dia.get()
            dias_trabajados = self.__input_dias_trabajados.get()
            otros_ingresos = self.__input_otros_ingresos.get()
            pagos_salud = self.__input_pagos_salud.get()
            aporte_pensiones = self.__input_aporte_pensiones.get()
            
            # Validamos la info asociada ala empleado
            Empleado.validarInfo(
                nombre,
                apellido,
                salario_dia,
                dias_trabajados,
                otros_ingresos,
                pagos_salud,
                aporte_pensiones
            )
            # Si los campos cumplen con el formato requerido estanciamos un objeto con esta clase
            self.__empleados.append(Empleado(
                nombre,
                apellido,
                cargo,
                genero,
                float(salario_dia),
                int(dias_trabajados),
                float(otros_ingresos),
                float(pagos_salud),
                float(aporte_pensiones)
            )) 
            self.__nomina._set_informacion(self.__empleados)
            
            # Si la operacion se reliza con exito, mostramos mensaje de exito
            messagebox.showinfo(
                "Empleado guardado",
                f"El empleado '{nombre} {apellido}' ha sido guardado exitosamente."
            )
            self.__interfaz_calcular_nomina()



        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.__resultado.config(text=str(e), fg="#FF3838")



class Main:
    @staticmethod
    def main():
        app = Interfaz()
        app._panel_principal.mainloop()

    
# Condicional para ejecutar el programa prinicipal
if __name__ == "__main__":
    Main.main()