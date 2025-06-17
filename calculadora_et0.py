#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Calculadora de Evapotranspiración de Referencia (ET₀)
Ecuación de Penman-Monteith FAO56

Autor: Miguel Alejandro Bermúdez Claros (mibermudezc@unal.edu.co)
        Script generado para cálculo de ET₀
Versión: 1.0
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, filedialog, scrolledtext
import csv
import datetime
import pandas as pd
import os
import sys

# Configuración del tema de customtkinter
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class CalculadoraET0:
    def __init__(self):
        self.ventana = ctk.CTk()
        self.ventana.title("Calculadora de Evapotranspiración de Referencia (ET₀)")
        self.ventana.geometry("1000x700")
        self.ventana.resizable(True, True)
        
        # Variables para almacenar los valores de entrada
        self.variables = {}
        self.resultado_et0 = None
        
        # Verificar si pyet está disponible
        self.pyet_disponible = self.verificar_pyet()
        
        self.crear_interfaz()
        
    def verificar_pyet(self):
        """Verificar si la librería pyet está instalada"""
        try:
            import pyet
            return True
        except ImportError:
            return False
    
    def crear_interfaz(self):
        """Crear todos los elementos de la interfaz"""
        self.crear_menu()
        self.crear_frame_principal()
        self.crear_tabla_variables()
        self.crear_botones()
        self.crear_resultado()
        self.crear_documentacion()
        
    def crear_menu(self):
        """Crear barra de menú"""
        menubar = tk.Menu(self.ventana)
        self.ventana.configure(menu=menubar)
        
        # Menú Archivo
        menu_archivo = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Archivo", menu=menu_archivo)
        menu_archivo.add_command(label="Exportar CSV", command=self.exportar_csv)
        menu_archivo.add_separator()
        menu_archivo.add_command(label="Salir", command=self.ventana.quit)
        
        # Menú Ayuda
        menu_ayuda = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ayuda", menu=menu_ayuda)
        menu_ayuda.add_command(label="Acerca de", command=self.mostrar_acerca_de)
        
    def crear_frame_principal(self):
        """Crear el frame principal con scroll"""
        self.frame_principal = ctk.CTkScrollableFrame(self.ventana, width=950, height=650)
        self.frame_principal.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Título principal
        titulo = ctk.CTkLabel(self.frame_principal, 
                             text="Calculadora de Evapotranspiración de Referencia (ET₀)",
                             font=ctk.CTkFont(size=24, weight="bold"))
        titulo.pack(pady=(0, 20))
        
        # Subtítulo
        subtitulo = ctk.CTkLabel(self.frame_principal, 
                                text="Ecuación de Penman-Monteith FAO56",
                                font=ctk.CTkFont(size=16))
        subtitulo.pack(pady=(0, 20))
        
    def crear_tabla_variables(self):
        """Crear la tabla estilo Excel para ingresar variables"""
        # Frame para la tabla
        frame_tabla = ctk.CTkFrame(self.frame_principal)
        frame_tabla.pack(fill="x", padx=20, pady=10)
        
        # Título de la sección
        titulo_tabla = ctk.CTkLabel(frame_tabla, 
                                   text="Variables Meteorológicas",
                                   font=ctk.CTkFont(size=18, weight="bold"))
        titulo_tabla.pack(pady=10)
        
        # Definir las variables y sus propiedades
        variables_info = [
            ("t_min", "Temperatura Mínima", "°C", "Temperatura mínima diaria del aire"),
            ("t_max", "Temperatura Máxima", "°C", "Temperatura máxima diaria del aire"),
            ("rh_min", "Humedad Relativa Mínima", "%", "Humedad relativa mínima diaria"),
            ("rh_max", "Humedad Relativa Máxima", "%", "Humedad relativa máxima diaria"),
            ("rs", "Radiación Solar", "MJ/m²/día", "Radiación solar incidente"),
            ("uz", "Velocidad del Viento", "m/s", "Velocidad del viento a 2m de altura"),
            ("z", "Altitud", "m", "Altitud sobre el nivel del mar"),
            ("lat", "Latitud", "grados", "Latitud del sitio en grados decimales")
        ]
        
        # Headers de la tabla
        headers = ["Variable", "Descripción", "Unidad", "Valor", "Información"]
        
        # Frame para los headers
        frame_header = ctk.CTkFrame(frame_tabla)
        frame_header.pack(fill="x", padx=10, pady=5)
        
        for i, header in enumerate(headers):
            label = ctk.CTkLabel(frame_header, text=header, 
                               font=ctk.CTkFont(size=12, weight="bold"))
            label.grid(row=0, column=i, padx=5, pady=5, sticky="ew")
        
        # Configurar weights para que las columnas se expandan
        for i in range(len(headers)):
            frame_header.grid_columnconfigure(i, weight=1)
        
        # Frame para las filas de datos
        frame_datos = ctk.CTkFrame(frame_tabla)
        frame_datos.pack(fill="x", padx=10, pady=5)
        
        # Crear filas para cada variable
        for i, (var_name, descripcion, unidad, info) in enumerate(variables_info):
            # Código de variable
            label_var = ctk.CTkLabel(frame_datos, text=var_name,
                                   font=ctk.CTkFont(size=11, weight="bold"))
            label_var.grid(row=i, column=0, padx=5, pady=3, sticky="ew")
            
            # Descripción
            label_desc = ctk.CTkLabel(frame_datos, text=descripcion,
                                    font=ctk.CTkFont(size=11))
            label_desc.grid(row=i, column=1, padx=5, pady=3, sticky="ew")
            
            # Unidad
            label_unidad = ctk.CTkLabel(frame_datos, text=unidad,
                                      font=ctk.CTkFont(size=11))
            label_unidad.grid(row=i, column=2, padx=5, pady=3, sticky="ew")
            
            # Entry para el valor
            entry_valor = ctk.CTkEntry(frame_datos, placeholder_text="Ingrese valor",
                                     font=ctk.CTkFont(size=11))
            entry_valor.grid(row=i, column=3, padx=5, pady=3, sticky="ew")
            self.variables[var_name] = entry_valor
            
            # Información adicional
            label_info = ctk.CTkLabel(frame_datos, text=info,
                                    font=ctk.CTkFont(size=10),
                                    text_color="gray")
            label_info.grid(row=i, column=4, padx=5, pady=3, sticky="ew")
        
        # Configurar weights para las columnas
        for i in range(5):
            frame_datos.grid_columnconfigure(i, weight=1)
    
    def crear_botones(self):
        """Crear los botones de acción"""
        frame_botones = ctk.CTkFrame(self.frame_principal)
        frame_botones.pack(fill="x", padx=20, pady=20)
        
        # Botón calcular
        self.btn_calcular = ctk.CTkButton(frame_botones, 
                                         text="🧮 Calcular ET₀",
                                         command=self.calcular_et0,
                                         height=40,
                                         font=ctk.CTkFont(size=14, weight="bold"))
        self.btn_calcular.pack(side="left", padx=10, pady=10)
        
        # Botón limpiar
        btn_limpiar = ctk.CTkButton(frame_botones, 
                                   text="🗑️ Limpiar",
                                   command=self.limpiar_campos,
                                   height=40,
                                   font=ctk.CTkFont(size=14))
        btn_limpiar.pack(side="left", padx=10, pady=10)
        
        # Botón exportar
        btn_exportar = ctk.CTkButton(frame_botones, 
                                    text="📊 Exportar CSV",
                                    command=self.exportar_csv,
                                    height=40,
                                    font=ctk.CTkFont(size=14))
        btn_exportar.pack(side="right", padx=10, pady=10)
        
        # Mensaje sobre pyet si no está disponible
        if not self.pyet_disponible:
            mensaje_pyet = ctk.CTkLabel(frame_botones, 
                                       text="⚠️ Librería 'pyet' no encontrada. Instalar con: pip install pyet",
                                       text_color="orange",
                                       font=ctk.CTkFont(size=12))
            mensaje_pyet.pack(pady=5)
    
    def crear_resultado(self):
        """Crear la sección de resultados"""
        self.frame_resultado = ctk.CTkFrame(self.frame_principal)
        self.frame_resultado.pack(fill="x", padx=20, pady=10)
        
        titulo_resultado = ctk.CTkLabel(self.frame_resultado, 
                                       text="Resultado",
                                       font=ctk.CTkFont(size=18, weight="bold"))
        titulo_resultado.pack(pady=10)
        
        self.label_resultado = ctk.CTkLabel(self.frame_resultado, 
                                           text="Ingrese los valores y presione 'Calcular ET₀'",
                                           font=ctk.CTkFont(size=14),
                                           text_color="gray")
        self.label_resultado.pack(pady=10)
    
    def crear_documentacion(self):
        """Crear la sección de documentación"""
        frame_doc = ctk.CTkFrame(self.frame_principal)
        frame_doc.pack(fill="both", expand=True, padx=20, pady=10)
        
        titulo_doc = ctk.CTkLabel(frame_doc, 
                                 text="📚 Documentación",
                                 font=ctk.CTkFont(size=18, weight="bold"))
        titulo_doc.pack(pady=10)
        
        # Texto de documentación
        texto_doc = """
🌱 ¿Qué es la Evapotranspiración de Referencia (ET₀)?

La evapotranspiración de referencia (ET₀) es la cantidad de agua que se evapora del suelo y se transpira 
por las plantas en condiciones estándar, expresada en mm/día. Es fundamental para:

• 💧 Diseño de sistemas de riego
• 🌾 Planificación agrícola
• 📊 Balance hídrico de cultivos
• 🏞️ Gestión de recursos hídricos

📐 Ecuación de Penman-Monteith FAO56:

Esta es la ecuación estándar recomendada por la FAO para calcular ET₀. Considera:
• Temperatura del aire (máxima y mínima)
• Humedad relativa (máxima y mínima)  
• Radiación solar
• Velocidad del viento
• Altitud del sitio

🔬 Variables Explicadas:

• t_min, t_max: Temperaturas extremas diarias que afectan la presión de vapor
• rh_min, rh_max: Humedad relativa que determina el déficit de presión de vapor
• rs: Radiación solar disponible para el proceso de evapotranspiración
• uz: Velocidad del viento que facilita el transporte de vapor de agua
• z: Altitud que afecta la presión atmosférica y otros parámetros
• lat: Latitud geográfica necesaria para cálculos de radiación solar

🎯 Aplicaciones Prácticas:

• Cálculo de requerimientos de riego para cultivos
• Estimación de consumo de agua en jardines y césped
• Planificación de recursos hídricos en cuencas
• Estudios de cambio climático y sequías
• Diseño de sistemas de drenaje agrícola
        """
        
        text_widget = ctk.CTkTextbox(frame_doc, height=200, font=ctk.CTkFont(size=11))
        text_widget.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        text_widget.insert("0.0", texto_doc)
        text_widget.configure(state="disabled")
    
    def calcular_et0(self):
        """Calcular ET₀ usando la ecuación de Penman-Monteith"""
        if not self.pyet_disponible:
            messagebox.showerror("Error", 
                               "La librería 'pyet' no está instalada.\n\n"
                               "Para instalarla, ejecute en su terminal:\n"
                               "pip install pyet")
            return
        
        try:
            # Obtener valores de las entradas
            valores = {}
            for var_name, entry in self.variables.items():
                valor_str = entry.get().strip()
                if not valor_str:
                    messagebox.showerror("Error", f"Por favor ingrese un valor para {var_name}")
                    return
                
                try:
                    valores[var_name] = float(valor_str)
                except ValueError:
                    messagebox.showerror("Error", f"Valor inválido para {var_name}: {valor_str}")
                    return
            
            # Validar rangos lógicos
            if not self.validar_valores(valores):
                return
            
            # Importar pyet
            import pyet
            
            # Crear una fecha dummy para el cálculo
            fecha = pd.date_range('2023-01-01', periods=1, freq='D')
            
            # Calcular temperatura media
            tmean = (valores['t_max'] + valores['t_min']) / 2
            
            # Crear series de pandas para los datos
            tmean_series = pd.Series([tmean], index=fecha)
            tmax_series = pd.Series([valores['t_max']], index=fecha)
            tmin_series = pd.Series([valores['t_min']], index=fecha)
            rhmax_series = pd.Series([valores['rh_max']], index=fecha)
            rhmin_series = pd.Series([valores['rh_min']], index=fecha)
            rs_series = pd.Series([valores['rs']], index=fecha)
            wind_series = pd.Series([valores['uz']], index=fecha)
            
            # Calcular ET₀ usando la función correcta
            et0_result = pyet.pm_fao56(
                tmean=tmean_series,
                wind=wind_series,
                rs=rs_series,
                elevation=valores['z'],
                lat=valores['lat'],
                tmax=tmax_series,
                tmin=tmin_series,
                rhmax=rhmax_series,
                rhmin=rhmin_series
            )
            
            # Obtener el resultado
            self.resultado_et0 = round(et0_result.iloc[0], 3)
            
            # Mostrar resultado
            resultado_texto = f"🎯 ET₀ = {self.resultado_et0} mm/día"
            self.label_resultado.configure(text=resultado_texto, text_color="green")
            
            # Agregar interpretación
            interpretacion = self.interpretar_resultado(self.resultado_et0)
            resultado_completo = f"{resultado_texto}\n\n{interpretacion}"
            self.label_resultado.configure(text=resultado_completo)
            
        except Exception as e:
            messagebox.showerror("Error en el cálculo", f"Error al calcular ET₀:\n{str(e)}")
    
    def validar_valores(self, valores):
        """Validar que los valores estén en rangos lógicos"""
        # Validaciones básicas
        if valores['t_min'] >= valores['t_max']:
            messagebox.showerror("Error", "La temperatura mínima debe ser menor que la máxima")
            return False
            
        if valores['rh_min'] >= valores['rh_max']:
            messagebox.showerror("Error", "La humedad relativa mínima debe ser menor que la máxima")
            return False
            
        if not (0 <= valores['rh_min'] <= 100) or not (0 <= valores['rh_max'] <= 100):
            messagebox.showerror("Error", "La humedad relativa debe estar entre 0 y 100%")
            return False
            
        if valores['rs'] < 0:
            messagebox.showerror("Error", "La radiación solar no puede ser negativa")
            return False
            
        if valores['uz'] < 0:
            messagebox.showerror("Error", "La velocidad del viento no puede ser negativa")
            return False
            
        if not (-90 <= valores['lat'] <= 90):
            messagebox.showerror("Error", "La latitud debe estar entre -90 y 90 grados")
            return False
            
        return True
    
    def interpretar_resultado(self, et0):
        """Proporcionar interpretación del resultado"""
        if et0 < 2:
            categoria = "Baja"
            descripcion = "Condiciones de baja demanda evapotranspirativa"
        elif et0 < 4:
            categoria = "Moderada"
            descripcion = "Demanda evapotranspirativa típica para climas templados"
        elif et0 < 6:
            categoria = "Alta"
            descripcion = "Alta demanda evapotranspirativa, clima cálido"
        else:
            categoria = "Muy Alta"
            descripcion = "Demanda evapotranspirativa muy alta, condiciones áridas"
        
        return f"📊 Interpretación: {categoria}\n💡 {descripcion}"
    
    def limpiar_campos(self):
        """Limpiar todos los campos de entrada"""
        for entry in self.variables.values():
            entry.delete(0, 'end')
        
        self.label_resultado.configure(text="Ingrese los valores y presione 'Calcular ET₀'",
                                      text_color="gray")
        self.resultado_et0 = None
    
    def exportar_csv(self):
        """Exportar los datos y resultado a CSV"""
        if self.resultado_et0 is None:
            messagebox.showwarning("Advertencia", "Primero debe calcular ET₀ antes de exportar")
            return
        
        try:
            archivo = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("Archivos CSV", "*.csv")],
                title="Guardar resultado como CSV"
            )
            
            if archivo:
                # Recopilar datos
                datos_export = {}
                for var_name, entry in self.variables.items():
                    datos_export[var_name] = [entry.get()]
                
                datos_export['ET0_mm_dia'] = [self.resultado_et0]
                datos_export['fecha_calculo'] = [datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
                
                # Crear DataFrame y guardar
                df = pd.DataFrame(datos_export)
                df.to_csv(archivo, index=False, encoding='utf-8')
                
                messagebox.showinfo("Éxito", f"Datos exportados exitosamente a:\n{archivo}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al exportar CSV:\n{str(e)}")
    
    def mostrar_acerca_de(self):
        """Mostrar información acerca del programa"""
        mensaje = """
Calculadora de Evapotranspiración de Referencia (ET₀)
Versión 1.0

Ecuación: Penman-Monteith FAO56
Librería: pyet

Desarrollado para cálculos de balance hídrico y diseño de riego.

© 2024 - Script generado para uso académico y profesional
        """
        messagebox.showinfo("Acerca de", mensaje)
    
    def ejecutar(self):
        """Ejecutar la aplicación"""
        self.ventana.mainloop()

def main():
    """Función principal"""
    try:
        app = CalculadoraET0()
        app.ejecutar()
    except Exception as e:
        print(f"Error al iniciar la aplicación: {e}")
        input("Presione Enter para salir...")

if __name__ == "__main__":
    main() 