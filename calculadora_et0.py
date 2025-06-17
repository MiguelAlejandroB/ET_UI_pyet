#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Calculadora de Evapotranspiración de Referencia (ET₀) y Balance Hídrico
Ecuación de Penman-Monteith FAO56

Autor: Miguel Alejandro Bermúdez Claros
Contacto: mibermudezc@unal.edu.co
Institución: Universidad Nacional de Colombia

Descripción:
Esta aplicación permite calcular la evapotranspiración de referencia (ET₀) 
utilizando la ecuación estándar Penman-Monteith FAO56 y realizar análisis 
completos de balance hídrico para cultivos.

Características principales:
- Cálculo preciso de ET₀ usando la librería PyEt
- Balance hídrico completo con parámetros de suelo y cultivo
- Interfaz gráfica moderna e intuitiva
- Exportación de resultados a CSV
- Validaciones de datos y control de errores
- Interpretación automática de resultados

Aplicaciones:
- Diseño de sistemas de riego
- Planificación agrícola
- Gestión de recursos hídricos
- Investigación en hidrología agrícola

Versión: 2.0
Última actualización: Diciembre 2024
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
        self.resultado_balance = None
        
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
        self.crear_tabla_balance_hidrico()
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
        self.frame_principal = ctk.CTkScrollableFrame(self.ventana, width=1150, height=850)
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
    
    def crear_tabla_balance_hidrico(self):
        """Crear la tabla para balance hídrico"""
        # Frame para balance hídrico
        self.frame_balance = ctk.CTkFrame(self.frame_principal)
        self.frame_balance.pack(fill="x", padx=20, pady=10)
        
        # Título de la sección
        titulo_balance = ctk.CTkLabel(self.frame_balance, 
                                     text="Balance Hídrico",
                                     font=ctk.CTkFont(size=18, weight="bold"))
        titulo_balance.pack(pady=10)
        
        # Variables para balance hídrico con las nuevas especificaciones
        balance_variables = [
            ("humedad_actual", "Contenido de Humedad del Suelo Actual", "adimensional", "Humedad volumétrica actual del suelo (0-1)"),
            ("humedad_cc", "Contenido de Humedad en Capacidad de Campo", "adimensional", "Humedad volumétrica en capacidad de campo (0-1)"),
            ("humedad_pmp", "Contenido de Humedad en Punto de Marchitez Permanente", "adimensional", "Humedad volumétrica en PMP (0-1)"),
            ("humedad_riego", "Contenido de Humedad del Riego (Umbral)", "adimensional", "Umbral de humedad para activar riego (0-1)"),
            ("cultivo", "Cultivo", "texto", "Nombre del cultivo"),
            ("profundidad_radicular", "Profundidad Radicular", "cm", "Profundidad de las raíces del cultivo"),
            ("periodo_fenologico", "Periodo Fenológico del Cultivo", "texto", "Etapa de desarrollo del cultivo"),
            ("kc", "Coeficiente del Cultivo (Kc)", "adimensional", "Factor de cultivo según etapa fenológica"),
            ("precipitacion", "Precipitación", "mm", "Precipitación diaria")
        ]
        
        # Headers de la tabla
        headers_balance = ["Variable", "Descripción", "Unidad", "Valor", "Información"]
        
        # Frame para los headers
        frame_header_balance = ctk.CTkFrame(self.frame_balance)
        frame_header_balance.pack(fill="x", padx=10, pady=5)
        
        for i, header in enumerate(headers_balance):
            label = ctk.CTkLabel(frame_header_balance, text=header, 
                               font=ctk.CTkFont(size=12, weight="bold"))
            label.grid(row=0, column=i, padx=5, pady=5, sticky="ew")
        
        # Configurar weights para las columnas
        for i in range(len(headers_balance)):
            frame_header_balance.grid_columnconfigure(i, weight=1)
        
        # Frame para las filas de datos del balance
        frame_datos_balance = ctk.CTkFrame(self.frame_balance)
        frame_datos_balance.pack(fill="x", padx=10, pady=5)
        
        # Variables para el balance hídrico
        self.variables_balance = {}
        
        # Crear filas para cada variable del balance
        for i, (var_name, descripcion, unidad, info) in enumerate(balance_variables):
            # Código de variable
            label_var = ctk.CTkLabel(frame_datos_balance, text=var_name,
                                   font=ctk.CTkFont(size=11, weight="bold"))
            label_var.grid(row=i, column=0, padx=5, pady=3, sticky="ew")
            
            # Descripción
            label_desc = ctk.CTkLabel(frame_datos_balance, text=descripcion,
                                    font=ctk.CTkFont(size=11))
            label_desc.grid(row=i, column=1, padx=5, pady=3, sticky="ew")
            
            # Unidad
            label_unidad = ctk.CTkLabel(frame_datos_balance, text=unidad,
                                      font=ctk.CTkFont(size=11))
            label_unidad.grid(row=i, column=2, padx=5, pady=3, sticky="ew")
            
            # Entry para el valor
            entry_valor = ctk.CTkEntry(frame_datos_balance, placeholder_text="Ingrese valor",
                                     font=ctk.CTkFont(size=11))
            entry_valor.grid(row=i, column=3, padx=5, pady=3, sticky="ew")
            self.variables_balance[var_name] = entry_valor
            
            # Información adicional
            label_info = ctk.CTkLabel(frame_datos_balance, text=info,
                                    font=ctk.CTkFont(size=10),
                                    text_color="gray")
            label_info.grid(row=i, column=4, padx=5, pady=3, sticky="ew")
        
        # Configurar weights para las columnas
        for i in range(5):
            frame_datos_balance.grid_columnconfigure(i, weight=1)
        
        # Botones para el balance hídrico
        frame_botones_balance = ctk.CTkFrame(self.frame_balance)
        frame_botones_balance.pack(fill="x", padx=10, pady=10)
        
        btn_calcular_balance = ctk.CTkButton(frame_botones_balance, 
                                           text="💧 Calcular Balance Hídrico",
                                           command=self.calcular_balance_hidrico,
                                           height=40,
                                           font=ctk.CTkFont(size=14, weight="bold"))
        btn_calcular_balance.pack(side="left", padx=10, pady=10)
        
        btn_limpiar_balance = ctk.CTkButton(frame_botones_balance, 
                                          text="🗑️ Limpiar Balance",
                                          command=self.limpiar_balance,
                                          height=40,
                                          font=ctk.CTkFont(size=14))
        btn_limpiar_balance.pack(side="left", padx=10, pady=10)
        
        btn_exportar_balance = ctk.CTkButton(frame_botones_balance, 
                                           text="📊 Exportar Balance",
                                           command=self.exportar_balance,
                                           height=40,
                                           font=ctk.CTkFont(size=14))
        btn_exportar_balance.pack(side="right", padx=10, pady=10)
        
        # Resultado del balance hídrico
        self.label_balance_resultado = ctk.CTkLabel(self.frame_balance, 
                                                  text="Primero calcule ET₀, luego ingrese datos del balance hídrico",
                                                  font=ctk.CTkFont(size=12),
                                                  text_color="gray")
        self.label_balance_resultado.pack(pady=10)
    
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

💧 Balance Hídrico del Suelo:

El balance hídrico analiza la disponibilidad de agua en el suelo para los cultivos:

• Lámina aprovechable: Agua total disponible entre CC y PMP
• Lámina neta: Agua disponible entre CC y umbral de riego  
• ETc: Evapotranspiración del cultivo (ET₀ × Kc)
• Lámina actual: Agua disponible considerando consumo del cultivo

🌾 Variables del Balance:

• Humedad actual: Estado hídrico actual del suelo (adimensional 0-1)
• Capacidad de campo (CC): Máxima retención de agua del suelo
• Punto de marchitez permanente (PMP): Mínima agua disponible
• Umbral de riego: Nivel crítico para activar riego
• Coeficiente Kc: Factor específico del cultivo y etapa fenológica

🎯 Aplicaciones Prácticas:

• Cálculo de requerimientos de riego para cultivos
• Estimación de consumo de agua en jardines y césped
• Planificación de recursos hídricos en cuencas
• Estudios de cambio climático y sequías
• Diseño de sistemas de drenaje agrícola
• Programación de riegos automatizados
• Análisis de eficiencia hídrica en cultivos
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
y Balance Hídrico
Versión 2.0

Ecuación: Penman-Monteith FAO56
Librería: pyet

Desarrollado por: Miguel Alejandro Bermúdez Claros
Contacto: mibermudezc@unal.edu.co
Institución: Universidad Nacional de Colombia

Características:
• Cálculo preciso de ET₀ usando ecuación FAO56
• Balance hídrico completo para cultivos
• Análisis de láminas de agua en el suelo
• Recomendaciones de riego automatizadas
• Exportación de datos a CSV
• Interfaz intuitiva y moderna

Desarrollado para cálculos de balance hídrico y diseño de riego.

© 2024 - Script generado para uso académico y profesional
        """
        messagebox.showinfo("Acerca de", mensaje)
    
    def calcular_balance_hidrico(self):
        """Calcular el balance hídrico con los nuevos parámetros solicitados"""
        # Verificar que ET₀ esté calculado
        if self.resultado_et0 is None:
            messagebox.showwarning("Advertencia", "Primero debe calcular ET₀")
            return
        
        try:
            # Obtener valores del balance hídrico
            valores_balance = {}
            for var_name, entry in self.variables_balance.items():
                valor_str = entry.get().strip()
                if not valor_str:
                    messagebox.showerror("Error", f"Por favor ingrese un valor para {var_name}")
                    return
                
                # Para variables de texto
                if var_name in ['cultivo', 'periodo_fenologico']:
                    valores_balance[var_name] = valor_str
                else:
                    try:
                        valores_balance[var_name] = float(valor_str)
                    except ValueError:
                        messagebox.showerror("Error", f"Valor inválido para {var_name}: {valor_str}")
                        return
            
            # Validar valores del balance
            if not self.validar_balance(valores_balance):
                return
            
            # Obtener valores
            humedad_actual = valores_balance['humedad_actual']
            humedad_cc = valores_balance['humedad_cc']
            humedad_pmp = valores_balance['humedad_pmp']
            humedad_riego = valores_balance['humedad_riego']
            profundidad_radicular = valores_balance['profundidad_radicular'] / 100  # Convertir cm a m
            kc = valores_balance['kc']
            precipitacion = valores_balance['precipitacion']
            et0 = self.resultado_et0
            
            # CÁLCULOS SOLICITADOS:
            
            # 1. Lámina de agua aprovechable
            lamina_aprovechable = (humedad_cc - humedad_pmp) * profundidad_radicular * 1000  # mm
            
            # 2. Lámina neta
            lamina_neta = (humedad_cc - humedad_riego) * profundidad_radicular * 1000  # mm
            
            # 3. ETc (Evapotranspiración del cultivo)
            etc = kc * et0
            
            # 4. Lámina actual o disponible
            lamina_actual = (humedad_cc - humedad_actual) * profundidad_radicular * 1000 - etc  # mm
            
            # Cálculos adicionales útiles
            deficit_hidrico = max(0, etc - precipitacion)
            superavit_hidrico = max(0, precipitacion - etc)
            
            # Determinar estado del cultivo
            if lamina_actual > lamina_neta * 0.5:
                estado_cultivo = "Óptimo - No requiere riego"
            elif lamina_actual > 0:
                estado_cultivo = "Moderado - Considerar riego pronto"
            else:
                estado_cultivo = "Crítico - Requiere riego inmediato"
            
            # Mostrar resultados
            resultado_texto = f"""
💧 BALANCE HÍDRICO CALCULADO:

📊 DATOS DEL CULTIVO:
• Cultivo: {valores_balance['cultivo']}
• Periodo fenológico: {valores_balance['periodo_fenologico']}
• Coeficiente Kc: {kc}
• Profundidad radicular: {valores_balance['profundidad_radicular']} cm

🌱 PARÁMETROS DE HUMEDAD:
• Humedad actual: {valores_balance['humedad_actual']:.3f} (adimensional)
• Capacidad de campo: {valores_balance['humedad_cc']:.3f} (adimensional)
• Punto marchitez permanente: {valores_balance['humedad_pmp']:.3f} (adimensional)
• Umbral de riego: {valores_balance['humedad_riego']:.3f} (adimensional)

💧 CÁLCULOS PRINCIPALES:
• Lámina de agua aprovechable: {lamina_aprovechable:.2f} mm
• Lámina neta: {lamina_neta:.2f} mm
• ETc (Evapotranspiración cultivo): {etc:.2f} mm/día
• Lámina actual disponible: {lamina_actual:.2f} mm

🌧️ BALANCE DIARIO:
• Precipitación: {precipitacion} mm
• Déficit hídrico: {deficit_hidrico:.2f} mm
• Superávit hídrico: {superavit_hidrico:.2f} mm

🎯 ESTADO DEL CULTIVO: {estado_cultivo}
            """
            
            self.label_balance_resultado.configure(text=resultado_texto, text_color="blue")
            
            # Guardar resultados para exportar
            self.resultado_balance = {
                'cultivo': valores_balance['cultivo'],
                'periodo_fenologico': valores_balance['periodo_fenologico'],
                'kc': kc,
                'profundidad_radicular_cm': valores_balance['profundidad_radicular'],
                'humedad_actual': valores_balance['humedad_actual'],
                'humedad_cc': valores_balance['humedad_cc'],
                'humedad_pmp': valores_balance['humedad_pmp'],
                'humedad_riego': valores_balance['humedad_riego'],
                'precipitacion_mm': precipitacion,
                'et0_mm_dia': et0,
                'etc_mm_dia': etc,
                'lamina_aprovechable_mm': lamina_aprovechable,
                'lamina_neta_mm': lamina_neta,
                'lamina_actual_mm': lamina_actual,
                'deficit_hidrico_mm': deficit_hidrico,
                'superavit_hidrico_mm': superavit_hidrico,
                'estado_cultivo': estado_cultivo
            }
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al calcular balance hídrico:\n{str(e)}")
    
    def validar_balance(self, valores):
        """Validar valores del balance hídrico"""
        # Validar rangos de humedad (0-1) para valores adimensionales
        humedades = ['humedad_actual', 'humedad_cc', 'humedad_pmp', 'humedad_riego']
        for humedad in humedades:
            if not (0 <= valores[humedad] <= 1):
                messagebox.showerror("Error", f"La {humedad} debe estar entre 0 y 1 (adimensional)")
                return False
        
        # Validar relaciones lógicas entre humedades
        if valores['humedad_pmp'] >= valores['humedad_cc']:
            messagebox.showerror("Error", "La humedad en punto de marchitez permanente debe ser menor que capacidad de campo")
            return False
        
        if valores['humedad_actual'] > valores['humedad_cc']:
            messagebox.showerror("Error", "La humedad actual no puede ser mayor que la capacidad de campo")
            return False
            
        if valores['humedad_riego'] < valores['humedad_pmp'] or valores['humedad_riego'] > valores['humedad_cc']:
            messagebox.showerror("Error", "El umbral de riego debe estar entre PMP y capacidad de campo")
            return False
        
        # Validar coeficiente de cultivo
        if valores['kc'] <= 0:
            messagebox.showerror("Error", "El coeficiente de cultivo (Kc) debe ser mayor que 0")
            return False
        
        # Validar profundidad radicular
        if valores['profundidad_radicular'] <= 0:
            messagebox.showerror("Error", "La profundidad radicular debe ser mayor que 0")
            return False
        
        # Validar precipitación
        if valores['precipitacion'] < 0:
            messagebox.showerror("Error", "La precipitación no puede ser negativa")
            return False
        
        return True
    
    def limpiar_balance(self):
        """Limpiar campos del balance hídrico"""
        for entry in self.variables_balance.values():
            entry.delete(0, 'end')
        
        self.label_balance_resultado.configure(
            text="Primero calcule ET₀, luego ingrese datos del balance hídrico",
            text_color="gray"
        )
        self.resultado_balance = None
    
    def exportar_balance(self):
        """Exportar los datos del balance hídrico a CSV"""
        if self.resultado_balance is None:
            messagebox.showwarning("Advertencia", "Primero debe calcular el balance hídrico antes de exportar")
            return
        
        try:
            archivo = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("Archivos CSV", "*.csv")],
                title="Guardar balance hídrico como CSV"
            )
            
            if archivo:
                # Crear DataFrame con datos organizados sin nomenclaturas
                datos_completos = {}
                
                # 1. Variables meteorológicas (ET₀)
                for var_name, entry in self.variables.items():
                    datos_completos[var_name] = [entry.get()]
                datos_completos['et0_resultado_mm_dia'] = [self.resultado_et0]
                
                # 2. Variables del balance hídrico (entrada - sin duplicar)
                for var_name, entry in self.variables_balance.items():
                    datos_completos[var_name] = [entry.get()]
                
                # 3. Resultados calculados (solo los cálculos, no las entradas duplicadas)
                calculos_unicos = {
                    'etc_mm_dia': self.resultado_balance['etc_mm_dia'],
                    'lamina_aprovechable_mm': self.resultado_balance['lamina_aprovechable_mm'],
                    'lamina_neta_mm': self.resultado_balance['lamina_neta_mm'],
                    'lamina_actual_mm': self.resultado_balance['lamina_actual_mm'],
                    'deficit_hidrico_mm': self.resultado_balance['deficit_hidrico_mm'],
                    'superavit_hidrico_mm': self.resultado_balance['superavit_hidrico_mm'],
                    'estado_cultivo': self.resultado_balance['estado_cultivo']
                }
                
                # Agregar solo los cálculos únicos
                for key, value in calculos_unicos.items():
                    datos_completos[key] = [value]
                
                # Agregar fecha de cálculo
                datos_completos['fecha_calculo'] = [datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
                
                # Crear DataFrame y guardar
                df = pd.DataFrame(datos_completos)
                df.to_csv(archivo, index=False, encoding='utf-8')
                
                messagebox.showinfo("Éxito", f"Balance hídrico exportado exitosamente a:\n{archivo}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al exportar balance hídrico:\n{str(e)}")
    
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
