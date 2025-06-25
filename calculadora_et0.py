#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Calculadora de Evapotranspiración de Referencia (ET₀) y Balance Hídrico
PyET Suite - Versión Comparativa Múltiple

Autor: Miguel Alejandro Bermúdez Claros
Contacto: mibermudezc@unal.edu.co
Institución: Universidad Nacional de Colombia

Características principales:
- 20 métodos oficiales de PyET implementados
- SISTEMA DE COMPARACIÓN MÚLTIPLE DE MÉTODOS
- Selección de múltiples métodos simultáneamente
- Resultados comparativos en tabla vertical
- Selección de método para balance hídrico
- Interfaz dinámica que se adapta a cada método
- Balance hídrico completo para cultivos

Versión: 3.0 - Sistema Comparativo Múltiple
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

class CalculadoraET0Comparativa:
    def __init__(self):
        self.ventana = ctk.CTk()
        self.ventana.title("Calculadora ET₀ - PyET Suite (Sistema Comparativo)")
        self.ventana.geometry("1400x1000")
        self.ventana.resizable(True, True)
        
        # Variables para almacenar los valores de entrada
        self.variables = {}
        self.resultados_et0 = {}  # Diccionario para almacenar resultados múltiples
        self.metodos_seleccionados = ["pm_fao56"]  # Lista de métodos seleccionados
        self.metodo_balance = "pm_fao56"  # Método para balance hídrico
        self.resultado_balance = None
        
        # MÉTODOS CORREGIDOS Y COMPLETOS - 20 MÉTODOS OFICIALES PyET
        self.metodos_et = {
            # 🏆 MÉTODOS PENMAN-MONTEITH (Datos completos - máxima precisión)
            "pm_fao56": {
                "nombre": "FAO-56 Penman-Monteith",
                "funcion": "pm_fao56",
                "requerimientos": ["t_min", "t_max", "rh_min", "rh_max", "rs", "uz", "z", "lat"],
                "descripcion": "🏆 Estándar internacional FAO-56. Máxima precisión (rs=70 s/m)",
                "parametros_pyet": ["tmean", "wind", "rs", "rhmax", "rhmin", "elevation", "lat", "tmax", "tmin"]
            },
            "penman": {
                "nombre": "Penman Original (1948)",
                "funcion": "penman",
                "requerimientos": ["t_min", "t_max", "rh_min", "rh_max", "rs", "uz", "z", "lat"],
                "descripcion": "🏆 Método Penman original clásico. Base histórica PM",
                "parametros_pyet": ["tmean", "wind", "rs", "rhmax", "rhmin", "elevation", "lat", "tmax", "tmin"]
            },
            "pm": {
                "nombre": "Penman-Monteith Genérico",
                "funcion": "pm",
                "requerimientos": ["t_min", "t_max", "rh_min", "rh_max", "rs", "uz", "z", "lat"],
                "descripcion": "🏆 PM genérico configurable. Investigación avanzada",
                "parametros_pyet": ["tmean", "wind", "rs", "rhmax", "rhmin", "elevation", "lat", "tmax", "tmin"]
            },
            "pm_asce": {
                "nombre": "ASCE Penman-Monteith",
                "funcion": "pm_asce",
                "requerimientos": ["t_min", "t_max", "rh_min", "rh_max", "rs", "uz", "z", "lat"],
                "descripcion": "🏆 ASCE estándar americano. etype='os' (pasto) / 'rs' (alfalfa)",
                "parametros_pyet": ["tmean", "wind", "rs", "rhmax", "rhmin", "elevation", "lat", "tmax", "tmin"]
            },
            "kimberly_penman": {
                "nombre": "Kimberly-Penman",
                "funcion": "kimberly_penman",
                "requerimientos": ["t_min", "t_max", "rh_min", "rh_max", "rs", "uz", "z", "lat"],
                "descripcion": "🏆 Variante Penman con corrección estacional de viento",
                "parametros_pyet": ["tmean", "wind", "rs", "rhmax", "rhmin", "elevation", "lat", "tmax", "tmin"]
            },
            "thom_oliver": {
                "nombre": "Thom-Oliver",
                "funcion": "thom_oliver",
                "requerimientos": ["t_min", "t_max", "rh_min", "rh_max", "rs", "uz", "z", "lat"],
                "descripcion": "🏆 Variante PM con resistencias superficiales variables",
                "parametros_pyet": ["tmean", "wind", "rs", "rhmax", "rhmin", "elevation", "lat", "tmax", "tmin"]
            },
            
            # ☀️ MÉTODOS BASADOS EN RADIACIÓN (Sin viento/humedad)
            "priestley_taylor": {
                "nombre": "Priestley-Taylor",
                "funcion": "priestley_taylor",
                "requerimientos": ["t_min", "t_max", "rs", "z", "lat"],
                "descripcion": "☀️ Alpha=1.26. Ideal para zonas húmedas (humedad opcional)",
                "parametros_pyet": ["tmean", "rs", "elevation", "lat", "tmax", "tmin"]
            },
            "makkink": {
                "nombre": "Makkink",
                "funcion": "makkink",
                "requerimientos": ["t_min", "t_max", "rs", "z"],
                "descripcion": "☀️ Método holandés. Climas templados europeos",
                "parametros_pyet": ["tmean", "rs", "elevation"]
            },
            "makkink_knmi": {
                "nombre": "Makkink KNMI",
                "funcion": "makkink_knmi",
                "requerimientos": ["t_min", "t_max", "rs"],
                "descripcion": "☀️ Versión oficial instituto meteorológico holandés",
                "parametros_pyet": ["tmean", "rs"]
            },
            "jensen_haise": {
                "nombre": "Jensen-Haise",
                "funcion": "jensen_haise", 
                "requerimientos": ["t_min", "t_max", "rs"],
                "descripcion": "☀️ Optimizado para zonas áridas/riego. Oeste EE.UU.",
                "parametros_pyet": ["tmean", "rs"]
            },
            "abtew": {
                "nombre": "Abtew",
                "funcion": "abtew",
                "requerimientos": ["t_min", "t_max", "rs"],
                "descripcion": "☀️ Simplificado para regiones tropicales. K=0.53",
                "parametros_pyet": ["tmean", "rs"]
            },
            
            # 🌡️ MÉTODOS SIMPLES (Solo temperatura)
            "hargreaves": {
                "nombre": "Hargreaves",
                "funcion": "hargreaves",
                "requerimientos": ["t_min", "t_max", "lat"],
                "descripcion": "🌡️ Solo temperatura. Más robusto para datos limitados",
                "parametros_pyet": ["tmean", "tmax", "tmin", "lat"]
            },
            "mcguinness_bordne": {
                "nombre": "McGuinness-Bordne",
                "funcion": "mcguinness_bordne",
                "requerimientos": ["t_min", "t_max", "lat"],
                "descripcion": "🌡️ Basado en temperatura y radiación extraterrestre",
                "parametros_pyet": ["tmean", "lat"]
            },
            "hamon": {
                "nombre": "Hamon",
                "funcion": "hamon",
                "requerimientos": ["t_min", "t_max", "lat"],
                "descripcion": "🌡️ Muy simple. Solo temperatura y ubicación",
                "parametros_pyet": ["tmean", "lat"]
            },
            "oudin": {
                "nombre": "Oudin",
                "funcion": "oudin",
                "requerimientos": ["t_min", "t_max", "lat"],
                "descripcion": "🌡️ Francés simplificado. Formula: Ra*(T+5)/(λ*100)",
                "parametros_pyet": ["tmean", "lat"]
            },
            "linacre": {
                "nombre": "Linacre",
                "funcion": "linacre",
                "requerimientos": ["t_min", "t_max", "z", "lat"],
                "descripcion": "🗻 Australiano. Incluye corrección por altitud (lat en grados)",
                "parametros_pyet": ["tmean", "tmax", "tmin", "elevation", "lat"]
            },
            
            # 💧 MÉTODOS CON HUMEDAD
            "turc": {
                "nombre": "Turc",
                "funcion": "turc",
                "requerimientos": ["t_min", "t_max", "rh_min", "rh_max", "rs"],
                "descripcion": "💧 Incluye corrección por humedad <50%. Regiones húmedas",
                "parametros_pyet": ["tmean", "rs", "rh"]
            },
            "romanenko": {
                "nombre": "Romanenko",
                "funcion": "romanenko",
                "requerimientos": ["t_min", "t_max", "rh_min", "rh_max"],
                "descripcion": "💧 Fórmula rusa: 4.5*(1+T/25)²*(1-ea/es)",
                "parametros_pyet": ["tmean", "rh", "tmax", "tmin"]
            },
            "haude": {
                "nombre": "Haude",
                "funcion": "haude",
                "requerimientos": ["t_max", "rh_min"],
                "descripcion": "💨 Alemán muy simple. Solo T_max y RH_min",
                "parametros_pyet": ["tmean", "rh"]
            },
            
            # 🔬 MÉTODOS ESPECIALIZADOS
            "fao_24": {
                "nombre": "FAO-24 Radiation",
                "funcion": "fao_24",
                "requerimientos": ["t_min", "t_max", "rh_min", "rh_max", "rs", "uz", "z"],
                "descripcion": "📊 FAO-24 con corrección radiativa y viento",
                "parametros_pyet": ["tmean", "wind", "rs", "rh", "elevation"]
            },
            "blaney_criddle": {
                "nombre": "Blaney-Criddle",
                "funcion": "blaney_criddle",
                "requerimientos": ["t_min", "t_max", "lat"],
                "descripcion": "🌾 Clásico para riego. Basado en horas de luz y temperatura",
                "parametros_pyet": ["tmean", "lat"]
            }
        }
        
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
        self.crear_selector_metodos_multiple()
        self.crear_tabla_variables()
        self.crear_botones()
        self.crear_resultados_comparativos()
        self.crear_selector_balance()
        self.crear_tabla_balance_hidrico()
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
        self.frame_principal = ctk.CTkScrollableFrame(self.ventana, width=1350, height=950)
        self.frame_principal.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Título principal
        titulo = ctk.CTkLabel(self.frame_principal, 
                             text="🔬 Calculadora ET₀ - Sistema Comparativo Múltiple",
                             font=ctk.CTkFont(size=24, weight="bold"))
        titulo.pack(pady=(0, 10))
        
        # Subtítulo
        subtitulo = ctk.CTkLabel(self.frame_principal,
                                text="20 Métodos PyET | Comparación Simultánea | Análisis Comparativo",
                                font=ctk.CTkFont(size=14), text_color="gray")
        subtitulo.pack(pady=(0, 20))
        
    def crear_selector_metodos_multiple(self):
        """Crear selector múltiple de métodos"""
        frame_selector = ctk.CTkFrame(self.frame_principal)
        frame_selector.pack(fill="x", padx=20, pady=10)
        
        titulo_selector = ctk.CTkLabel(frame_selector,
                                      text="🎯 Selección Múltiple de Métodos",
                                      font=ctk.CTkFont(size=16, weight="bold"))
        titulo_selector.pack(pady=10)
        
        # Frame para botones de categorías
        frame_categorias = ctk.CTkFrame(frame_selector)
        frame_categorias.pack(fill="x", padx=10, pady=5)
        
        # Botones para seleccionar por categorías
        btn_todos = ctk.CTkButton(frame_categorias, text="✅ Todos (20)", 
                                 command=self.seleccionar_todos_metodos,
                                 width=120, height=30)
        btn_todos.pack(side="left", padx=5, pady=5)
        
        btn_pm = ctk.CTkButton(frame_categorias, text="🏆 Penman-M (6)", 
                              command=self.seleccionar_metodos_pm,
                              width=120, height=30)
        btn_pm.pack(side="left", padx=5, pady=5)
        
        btn_radiacion = ctk.CTkButton(frame_categorias, text="☀️ Radiación (5)", 
                                     command=self.seleccionar_metodos_radiacion,
                                     width=120, height=30)
        btn_radiacion.pack(side="left", padx=5, pady=5)
        
        btn_temperatura = ctk.CTkButton(frame_categorias, text="🌡️ Temperatura (5)", 
                                       command=self.seleccionar_metodos_temperatura,
                                       width=120, height=30)
        btn_temperatura.pack(side="left", padx=5, pady=5)
        
        btn_humedad = ctk.CTkButton(frame_categorias, text="💧 Humedad (3)", 
                                   command=self.seleccionar_metodos_humedad,
                                   width=120, height=30)
        btn_humedad.pack(side="left", padx=5, pady=5)
        
        btn_limpiar = ctk.CTkButton(frame_categorias, text="🗑️ Limpiar", 
                                   command=self.limpiar_seleccion_metodos,
                                   width=100, height=30)
        btn_limpiar.pack(side="right", padx=5, pady=5)
        
        # Frame scrollable para checkboxes de métodos
        self.frame_metodos = ctk.CTkScrollableFrame(frame_selector, height=200)
        self.frame_metodos.pack(fill="x", padx=10, pady=10)
        
        # Crear checkboxes para cada método
        self.checkboxes_metodos = {}
        for i, (metodo_id, info) in enumerate(self.metodos_et.items()):
            var = tk.BooleanVar()
            if metodo_id == "pm_fao56":  # FAO-56 seleccionado por defecto
                var.set(True)
            
            checkbox = ctk.CTkCheckBox(self.frame_metodos, 
                                      text=f"{info['nombre']}",
                                      variable=var,
                                      command=self.actualizar_metodos_seleccionados)
            checkbox.pack(anchor="w", padx=5, pady=2)
            self.checkboxes_metodos[metodo_id] = var
        
        # Label con métodos seleccionados
        self.label_seleccionados = ctk.CTkLabel(frame_selector,
                                               text="Métodos seleccionados: FAO-56 Penman-Monteith",
                                               font=ctk.CTkFont(size=12),
                                               text_color="blue")
        self.label_seleccionados.pack(pady=5)
    
    def seleccionar_todos_metodos(self):
        """Seleccionar todos los métodos"""
        for var in self.checkboxes_metodos.values():
            var.set(True)
        self.actualizar_metodos_seleccionados()
    
    def seleccionar_metodos_pm(self):
        """Seleccionar métodos Penman-Monteith"""
        metodos_pm = ["pm_fao56", "penman", "pm", "pm_asce", "kimberly_penman", "thom_oliver"]
        self.limpiar_seleccion_metodos()
        for metodo in metodos_pm:
            if metodo in self.checkboxes_metodos:
                self.checkboxes_metodos[metodo].set(True)
        self.actualizar_metodos_seleccionados()
    
    def seleccionar_metodos_radiacion(self):
        """Seleccionar métodos basados en radiación"""
        metodos_rad = ["priestley_taylor", "makkink", "makkink_knmi", "jensen_haise", "abtew"]
        self.limpiar_seleccion_metodos()
        for metodo in metodos_rad:
            if metodo in self.checkboxes_metodos:
                self.checkboxes_metodos[metodo].set(True)
        self.actualizar_metodos_seleccionados()
    
    def seleccionar_metodos_temperatura(self):
        """Seleccionar métodos basados en temperatura"""
        metodos_temp = ["hargreaves", "mcguinness_bordne", "hamon", "oudin", "linacre"]
        self.limpiar_seleccion_metodos()
        for metodo in metodos_temp:
            if metodo in self.checkboxes_metodos:
                self.checkboxes_metodos[metodo].set(True)
        self.actualizar_metodos_seleccionados()
    
    def seleccionar_metodos_humedad(self):
        """Seleccionar métodos que incluyen humedad"""
        metodos_hum = ["turc", "romanenko", "haude"]
        self.limpiar_seleccion_metodos()
        for metodo in metodos_hum:
            if metodo in self.checkboxes_metodos:
                self.checkboxes_metodos[metodo].set(True)
        self.actualizar_metodos_seleccionados()
    
    def limpiar_seleccion_metodos(self):
        """Limpiar selección de métodos"""
        for var in self.checkboxes_metodos.values():
            var.set(False)
        self.actualizar_metodos_seleccionados()
    
    def actualizar_metodos_seleccionados(self):
        """Actualizar lista de métodos seleccionados"""
        self.metodos_seleccionados = []
        for metodo_id, var in self.checkboxes_metodos.items():
            if var.get():
                self.metodos_seleccionados.append(metodo_id)
        
        # Actualizar texto de métodos seleccionados
        if len(self.metodos_seleccionados) == 0:
            texto = "Ningún método seleccionado"
        elif len(self.metodos_seleccionados) == 1:
            metodo = self.metodos_seleccionados[0]
            texto = f"Método seleccionado: {self.metodos_et[metodo]['nombre']}"
        else:
            texto = f"{len(self.metodos_seleccionados)} métodos seleccionados para comparación"
        
        self.label_seleccionados.configure(text=texto)
        
        # Actualizar tabla de variables según los métodos seleccionados
        self.actualizar_tabla_variables_multiple()
        
        # Limpiar resultados de forma segura
        self.resultados_et0.clear()
        try:
            if hasattr(self, 'frame_tabla_resultados') and self.frame_tabla_resultados.winfo_exists():
                for widget in self.frame_tabla_resultados.winfo_children():
                    try:
                        if widget.winfo_exists():
                            widget.destroy()
                    except:
                        pass
        except Exception as e:
            print(f"Error limpiando widgets: {e}")
    
    def crear_tabla_variables(self):
        """Crear la tabla para variables meteorológicas"""
        self.frame_tabla = ctk.CTkFrame(self.frame_principal)
        self.frame_tabla.pack(fill="x", padx=20, pady=10)
        
        titulo_tabla = ctk.CTkLabel(self.frame_tabla, 
                                   text="📊 Variables Meteorológicas",
                                   font=ctk.CTkFont(size=16, weight="bold"))
        titulo_tabla.pack(pady=10)
        
        self.frame_variables = ctk.CTkFrame(self.frame_tabla)
        self.frame_variables.pack(fill="x", padx=10, pady=10)
        
        self.actualizar_tabla_variables_multiple()
    
    def actualizar_tabla_variables_multiple(self):
        """Actualizar tabla de variables para métodos múltiples"""
        for widget in self.frame_variables.winfo_children():
            widget.destroy()
        
        self.variables.clear()
        
        if not self.metodos_seleccionados:
            label_info = ctk.CTkLabel(self.frame_variables, 
                                     text="Seleccione al menos un método para ver las variables requeridas",
                                     font=ctk.CTkFont(size=12))
            label_info.pack(pady=20)
            return
        
        # Determinar todas las variables necesarias
        variables_necesarias = set()
        for metodo in self.metodos_seleccionados:
            variables_necesarias.update(self.metodos_et[metodo]["requerimientos"])
        
        variables_necesarias = sorted(list(variables_necesarias))
        
        # Info de métodos y variables
        info_text = f"Métodos: {len(self.metodos_seleccionados)} | Variables requeridas: {len(variables_necesarias)}"
        label_info = ctk.CTkLabel(self.frame_variables, text=info_text,
                                 font=ctk.CTkFont(size=12, weight="bold"))
        label_info.pack(pady=5)
        
        # Variables
        variables_info = {
            "t_min": ("Temperatura Mínima", "°C"),
            "t_max": ("Temperatura Máxima", "°C"),
            "rh_min": ("Humedad Relativa Mínima", "%"),
            "rh_max": ("Humedad Relativa Máxima", "%"),
            "rs": ("Radiación Solar", "MJ/m²/día"),
            "uz": ("Velocidad del Viento", "m/s"),
            "z": ("Altitud", "m"),
            "lat": ("Latitud", "grados")
        }
        
        for var_name in variables_necesarias:
            if var_name in variables_info:
                descripcion, unidad = variables_info[var_name]
                
                frame_var = ctk.CTkFrame(self.frame_variables)
                frame_var.pack(fill="x", padx=5, pady=2)
                
                label_var = ctk.CTkLabel(frame_var, text=f"{var_name}:",
                                        font=ctk.CTkFont(size=11, weight="bold"),
                                        width=100)
                label_var.pack(side="left", padx=5, pady=5)
                
                label_desc = ctk.CTkLabel(frame_var, text=descripcion,
                                         font=ctk.CTkFont(size=11), width=200)
                label_desc.pack(side="left", padx=5, pady=5)
                
                entry_valor = ctk.CTkEntry(frame_var, placeholder_text=f"Valor en {unidad}",
                                          font=ctk.CTkFont(size=11), width=120)
                entry_valor.pack(side="left", padx=5, pady=5)
                self.variables[var_name] = entry_valor
                
                label_unidad = ctk.CTkLabel(frame_var, text=unidad,
                                           font=ctk.CTkFont(size=11), width=80)
                label_unidad.pack(side="left", padx=5, pady=5)
    
    def crear_botones(self):
        """Crear botones de acción"""
        frame_botones = ctk.CTkFrame(self.frame_principal)
        frame_botones.pack(fill="x", padx=20, pady=10)
        
        self.btn_calcular = ctk.CTkButton(frame_botones, 
                                         text="🧮 Calcular ET₀ (Comparación)",
                                         command=self.calcular_et0_multiple,
                                         height=40,
                                         font=ctk.CTkFont(size=14, weight="bold"))
        self.btn_calcular.pack(side="left", padx=10, pady=10)
        
        btn_limpiar = ctk.CTkButton(frame_botones, 
                                   text="🗑️ Limpiar",
                                   command=self.limpiar_campos,
                                   height=40,
                                   font=ctk.CTkFont(size=14))
        btn_limpiar.pack(side="left", padx=10, pady=10)
        
        btn_exportar = ctk.CTkButton(frame_botones, 
                                    text="📊 Exportar CSV",
                                    command=self.exportar_csv,
                                    height=40,
                                    font=ctk.CTkFont(size=14))
        btn_exportar.pack(side="right", padx=10, pady=10)
        
        if not self.pyet_disponible:
            mensaje_pyet = ctk.CTkLabel(frame_botones, 
                                       text="⚠️ PyET no instalado. Usar: pip install pyet",
                                       text_color="red",
                                       font=ctk.CTkFont(size=12))
            mensaje_pyet.pack(pady=5)
    
    def crear_resultados_comparativos(self):
        """Crear sección de resultados comparativos"""
        self.frame_resultados = ctk.CTkFrame(self.frame_principal)
        self.frame_resultados.pack(fill="x", padx=20, pady=10)
        
        titulo_resultados = ctk.CTkLabel(self.frame_resultados, 
                                        text="📊 Resultados Comparativos ET₀",
                                        font=ctk.CTkFont(size=16, weight="bold"))
        titulo_resultados.pack(pady=10)
        
        self.frame_tabla_resultados = ctk.CTkScrollableFrame(self.frame_resultados, height=300)
        self.frame_tabla_resultados.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.label_estado_resultados = ctk.CTkLabel(self.frame_resultados,
                                                   text="Seleccione métodos y calcule ET₀ para ver resultados",
                                                   font=ctk.CTkFont(size=12),
                                                   text_color="gray")
        self.label_estado_resultados.pack(pady=5)
    
    def crear_selector_balance(self):
        """Crear selector de método para balance hídrico"""
        self.frame_selector_balance = ctk.CTkFrame(self.frame_principal)
        self.frame_selector_balance.pack(fill="x", padx=20, pady=10)
        
        titulo_selector_balance = ctk.CTkLabel(self.frame_selector_balance,
                                              text="🎯 Selección de Método para Balance Hídrico",
                                              font=ctk.CTkFont(size=16, weight="bold"))
        titulo_selector_balance.pack(pady=10)
        
        info_selector = ctk.CTkLabel(self.frame_selector_balance,
                                    text="Cuando calcule múltiples métodos, seleccione cuál resultado usar para el balance hídrico:",
                                    font=ctk.CTkFont(size=12),
                                    text_color="gray")
        info_selector.pack(pady=5)
        
        self.combo_balance = ctk.CTkComboBox(self.frame_selector_balance,
                                            values=["Primero calcule ET₀"],
                                            state="disabled",
                                            width=400,
                                            font=ctk.CTkFont(size=12))
        self.combo_balance.pack(pady=10)
        
        btn_seleccionar_balance = ctk.CTkButton(self.frame_selector_balance,
                                               text="✅ Usar este método para balance",
                                               command=self.seleccionar_metodo_balance,
                                               height=35)
        btn_seleccionar_balance.pack(pady=5)
        
        self.label_metodo_balance = ctk.CTkLabel(self.frame_selector_balance,
                                                text="Método para balance: No seleccionado",
                                                font=ctk.CTkFont(size=12, weight="bold"),
                                                text_color="blue")
        self.label_metodo_balance.pack(pady=5)
    
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
    
    def calcular_et0_multiple(self):
        """Calcular ET₀ para múltiples métodos seleccionados"""
        try:
            print("🔍 DEBUG: Iniciando cálculo ET₀...")
            
            if not self.pyet_disponible:
                messagebox.showerror("Error", 
                                   "La librería 'pyet' no está instalada.\n\n"
                                   "Para instalarla, ejecute en su terminal:\n"
                                   "pip install pyet")
                return
            
            if not self.metodos_seleccionados:
                messagebox.showerror("Error", "Seleccione al menos un método para calcular")
                return
            
            # Advertencia para muchos métodos
            if len(self.metodos_seleccionados) > 15:
                from tkinter import messagebox as mb
                respuesta = mb.askyesno("Advertencia", 
                                      f"Seleccionó {len(self.metodos_seleccionados)} métodos. "
                                      "Esto puede tomar tiempo y usar mucha memoria.\n\n"
                                      "¿Desea continuar?")
                if not respuesta:
                    return
            
            print(f"🔍 DEBUG: Métodos seleccionados: {self.metodos_seleccionados}")
            print(f"🔍 DEBUG: Variables disponibles: {list(self.variables.keys())}")
            
            # Obtener valores de las entradas
            valores = {}
            for var_name, entry in self.variables.items():
                valor_str = entry.get().strip()
                print(f"🔍 DEBUG: {var_name} = '{valor_str}'")
                
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
            
            # Calcular ET₀ para cada método seleccionado
            import pyet
            
            self.resultados_et0.clear()
            resultados_exitosos = []
            errores = []
            
            for metodo_id in self.metodos_seleccionados:
                try:
                    resultado = self.calcular_metodo_individual(metodo_id, valores, pyet)
                    if resultado is not None:
                        self.resultados_et0[metodo_id] = resultado
                        resultados_exitosos.append((metodo_id, resultado))
                    else:
                        errores.append((metodo_id, "Resultado None"))
                except Exception as e:
                    error_msg = str(e)
                    errores.append((metodo_id, error_msg))
                    print(f"Error en {metodo_id}: {error_msg}")
            
            # Mostrar resultados
            self.mostrar_resultados_comparativos(resultados_exitosos, errores)
            
            # Actualizar selector de balance
            self.actualizar_selector_balance()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error general en el cálculo:\n{str(e)}")
            print(f"Error general: {str(e)}")
    
    def calcular_metodo_individual(self, metodo_id, valores, pyet):
        """Calcular ET₀ para un método individual"""
        try:
            # Crear fecha dummy
            fecha = pd.date_range('2023-01-01', periods=1, freq='D')
            
            # Preparar argumentos básicos
            argumentos = {}
            
            # Temperatura media
            if 't_min' in valores and 't_max' in valores:
                tmean = (valores['t_max'] + valores['t_min']) / 2
                argumentos['tmean'] = pd.Series([tmean], index=fecha)
                argumentos['tmax'] = pd.Series([valores['t_max']], index=fecha)
                argumentos['tmin'] = pd.Series([valores['t_min']], index=fecha)
            
            # Humedad relativa
            if 'rh_min' in valores and 'rh_max' in valores:
                argumentos['rhmax'] = pd.Series([valores['rh_max']], index=fecha)
                argumentos['rhmin'] = pd.Series([valores['rh_min']], index=fecha)
                argumentos['rh'] = pd.Series([(valores['rh_max'] + valores['rh_min']) / 2], index=fecha)
            elif 'rh_min' in valores:
                argumentos['rh'] = pd.Series([valores['rh_min']], index=fecha)
            
            # Radiación solar
            if 'rs' in valores:
                argumentos['rs'] = pd.Series([valores['rs']], index=fecha)
            
            # Viento
            if 'uz' in valores:
                argumentos['wind'] = pd.Series([valores['uz']], index=fecha)
            
            # Elevación
            if 'z' in valores:
                argumentos['elevation'] = valores['z']
            
            # Latitud
            if 'lat' in valores:
                argumentos['lat'] = valores['lat']
                import math
                argumentos['lat_rad'] = math.radians(valores['lat'])
            
            # Obtener función PyET
            funcion_pyet = getattr(pyet, self.metodos_et[metodo_id]['funcion'])
            
            # Ejecutar según método específico
            if metodo_id == 'hargreaves':
                et0_result = funcion_pyet(
                    tmin=argumentos['tmin'],
                    tmax=argumentos['tmax'],
                    tmean=argumentos['tmean'],
                    lat=argumentos['lat_rad']
                )
            elif metodo_id in ['hamon', 'mcguinness_bordne', 'oudin', 'blaney_criddle']:
                et0_result = funcion_pyet(
                    tmean=argumentos['tmean'],
                    lat=argumentos['lat_rad']
                )
            elif metodo_id == 'haude':
                et0_result = funcion_pyet(
                    tmean=argumentos['tmax'] if 't_max' in valores else argumentos['tmean'],
                    rh=argumentos['rh']
                )
            elif metodo_id == 'turc':
                et0_result = funcion_pyet(
                    tmean=argumentos['tmean'],
                    rs=argumentos['rs'],
                    rh=argumentos['rh']
                )
            elif metodo_id == 'romanenko':
                et0_result = funcion_pyet(
                    tmean=argumentos['tmean'],
                    rh=argumentos['rh'],
                    tmax=argumentos['tmax'],
                    tmin=argumentos['tmin']
                )
            elif metodo_id == 'linacre':
                et0_result = funcion_pyet(
                    tmean=argumentos['tmean'],
                    elevation=argumentos['elevation'],
                    lat=argumentos['lat_rad'],
                    tmax=argumentos['tmax'],
                    tmin=argumentos['tmin']
                )
            elif metodo_id in ['abtew', 'jensen_haise', 'makkink_knmi']:
                et0_result = funcion_pyet(
                    tmean=argumentos['tmean'],
                    rs=argumentos['rs']
                )
            elif metodo_id == 'makkink':
                et0_result = funcion_pyet(
                    tmean=argumentos['tmean'],
                    rs=argumentos['rs'],
                    elevation=argumentos['elevation']
                )
            elif metodo_id == 'fao_24':
                et0_result = funcion_pyet(
                    tmean=argumentos['tmean'],
                    wind=argumentos['wind'],
                    rs=argumentos['rs'],
                    rh=argumentos['rh'],
                    elevation=argumentos['elevation']
                )
            elif metodo_id == 'priestley_taylor':
                # Priestley-Taylor con manejo especial
                if 'rhmax' in argumentos and 'rhmin' in argumentos:
                    et0_result = funcion_pyet(
                        tmean=argumentos['tmean'],
                        rs=argumentos['rs'],
                        elevation=argumentos['elevation'],
                        lat=argumentos['lat_rad'],
                        tmax=argumentos['tmax'],
                        tmin=argumentos['tmin'],
                        rhmax=argumentos['rhmax'],
                        rhmin=argumentos['rhmin']
                    )
                else:
                    et0_result = funcion_pyet(
                        tmean=argumentos['tmean'],
                        rs=argumentos['rs'],
                        elevation=argumentos['elevation'],
                        lat=argumentos['lat_rad'],
                        tmax=argumentos['tmax'],
                        tmin=argumentos['tmin'],
                        rh=pd.Series([65.0], index=argumentos['tmean'].index)
                    )
            elif metodo_id == 'pm_asce':
                et0_result = funcion_pyet(
                    tmean=argumentos['tmean'],
                    wind=argumentos['wind'],
                    rs=argumentos['rs'],
                    rhmax=argumentos['rhmax'],
                    rhmin=argumentos['rhmin'],
                    elevation=argumentos['elevation'],
                    lat=argumentos['lat_rad'],
                    tmax=argumentos['tmax'],
                    tmin=argumentos['tmin'],
                    etype="os"
                )
            else:
                # Métodos PM estándar
                et0_result = funcion_pyet(
                    tmean=argumentos['tmean'],
                    wind=argumentos['wind'],
                    rs=argumentos['rs'],
                    rhmax=argumentos['rhmax'],
                    rhmin=argumentos['rhmin'],
                    elevation=argumentos['elevation'],
                    lat=argumentos['lat_rad'],
                    tmax=argumentos['tmax'],
                    tmin=argumentos['tmin']
                )
            
            return round(et0_result.iloc[0], 3)
            
        except Exception as e:
            raise e
    
    def mostrar_resultados_comparativos(self, resultados_exitosos, errores):
        """Mostrar resultados en tabla comparativa"""
        try:
            # Limpiar tabla anterior de forma segura
            if hasattr(self, 'frame_tabla_resultados') and self.frame_tabla_resultados.winfo_exists():
                for widget in self.frame_tabla_resultados.winfo_children():
                    try:
                        if widget.winfo_exists():
                            widget.destroy()
                    except:
                        pass
            
            if not resultados_exitosos and not errores:
                label_sin_datos = ctk.CTkLabel(self.frame_tabla_resultados,
                                              text="No hay resultados para mostrar",
                                              font=ctk.CTkFont(size=12))
                label_sin_datos.pack(pady=20)
                return
        except Exception as e:
            print(f"Error limpiando tabla: {e}")
            return
        
        try:
            # Encabezados
            frame_header = ctk.CTkFrame(self.frame_tabla_resultados)
            frame_header.pack(fill="x", padx=5, pady=5)
            
            headers = ["#", "Método", "ET₀ (mm/día)", "Estado", "Categoría"]
            for i, header in enumerate(headers):
                label = ctk.CTkLabel(frame_header, text=header,
                                    font=ctk.CTkFont(size=12, weight="bold"))
                label.grid(row=0, column=i, padx=5, pady=5, sticky="ew")
            
            # Configurar pesos de columnas
            for i in range(len(headers)):
                frame_header.grid_columnconfigure(i, weight=1)
        except Exception as e:
            print(f"Error creando encabezados: {e}")
            return
        
        # Resultados exitosos
        for idx, (metodo_id, resultado) in enumerate(resultados_exitosos, 1):
            frame_fila = ctk.CTkFrame(self.frame_tabla_resultados)
            frame_fila.pack(fill="x", padx=5, pady=2)
            
            # Determinar categoría
            categoria = self.obtener_categoria_metodo(metodo_id)
            
            # Datos de la fila
            datos = [
                str(idx),
                self.metodos_et[metodo_id]['nombre'][:30] + "..." if len(self.metodos_et[metodo_id]['nombre']) > 30 else self.metodos_et[metodo_id]['nombre'],
                f"{resultado:.3f}",
                "✅ Exitoso",
                categoria
            ]
            
            for i, dato in enumerate(datos):
                color_texto = "green" if i == 3 else "black"
                label = ctk.CTkLabel(frame_fila, text=dato,
                                    font=ctk.CTkFont(size=11),
                                    text_color=color_texto)
                label.grid(row=0, column=i, padx=5, pady=3, sticky="ew")
            
            # Configurar pesos
            for i in range(len(datos)):
                frame_fila.grid_columnconfigure(i, weight=1)
        
        # Errores
        for idx, (metodo_id, error) in enumerate(errores, len(resultados_exitosos) + 1):
            frame_fila = ctk.CTkFrame(self.frame_tabla_resultados)
            frame_fila.pack(fill="x", padx=5, pady=2)
            
            categoria = self.obtener_categoria_metodo(metodo_id)
            
            datos = [
                str(idx),
                self.metodos_et[metodo_id]['nombre'][:30] + "..." if len(self.metodos_et[metodo_id]['nombre']) > 30 else self.metodos_et[metodo_id]['nombre'],
                "Error",
                f"❌ {error[:20]}...",
                categoria
            ]
            
            for i, dato in enumerate(datos):
                color_texto = "red" if i >= 2 else "black"
                label = ctk.CTkLabel(frame_fila, text=dato,
                                    font=ctk.CTkFont(size=11),
                                    text_color=color_texto)
                label.grid(row=0, column=i, padx=5, pady=3, sticky="ew")
            
            for i in range(len(datos)):
                frame_fila.grid_columnconfigure(i, weight=1)
        
        # Estadísticas
        if resultados_exitosos:
            frame_stats = ctk.CTkFrame(self.frame_tabla_resultados)
            frame_stats.pack(fill="x", padx=5, pady=10)
            
            resultados_valores = [r[1] for r in resultados_exitosos]
            promedio = sum(resultados_valores) / len(resultados_valores)
            minimo = min(resultados_valores)
            maximo = max(resultados_valores)
            
            stats_text = f"📊 Estadísticas: Promedio={promedio:.3f} | Mín={minimo:.3f} | Máx={maximo:.3f} | Métodos exitosos={len(resultados_exitosos)}/{len(self.metodos_seleccionados)}"
            
            label_stats = ctk.CTkLabel(frame_stats, text=stats_text,
                                      font=ctk.CTkFont(size=12, weight="bold"),
                                      text_color="blue")
            label_stats.pack(pady=5)
        
        # Actualizar estado
        if resultados_exitosos:
            self.label_estado_resultados.configure(
                text=f"✅ {len(resultados_exitosos)} métodos calculados exitosamente, {len(errores)} con errores",
                text_color="green"
            )
        else:
            self.label_estado_resultados.configure(
                text=f"❌ Todos los métodos fallaron ({len(errores)} errores)",
                text_color="red"
            )
    
    def obtener_categoria_metodo(self, metodo_id):
        """Obtener categoría del método"""
        categorias = {
            "pm_fao56": "🏆 PM", "penman": "🏆 PM", "pm": "🏆 PM", 
            "pm_asce": "🏆 PM", "kimberly_penman": "🏆 PM", "thom_oliver": "🏆 PM",
            "priestley_taylor": "☀️ Rad", "makkink": "☀️ Rad", "makkink_knmi": "☀️ Rad",
            "jensen_haise": "☀️ Rad", "abtew": "☀️ Rad",
            "hargreaves": "🌡️ Temp", "mcguinness_bordne": "🌡️ Temp", "hamon": "🌡️ Temp",
            "oudin": "🌡️ Temp", "linacre": "🌡️ Temp",
            "turc": "💧 Hum", "romanenko": "💧 Hum", "haude": "💧 Hum",
            "fao_24": "🔬 Esp", "blaney_criddle": "🔬 Esp"
        }
        return categorias.get(metodo_id, "❓")
    
    def actualizar_selector_balance(self):
        """Actualizar selector de método para balance hídrico"""
        if self.resultados_et0:
            opciones = []
            for metodo_id, resultado in self.resultados_et0.items():
                nombre = self.metodos_et[metodo_id]['nombre']
                opciones.append(f"{nombre} ({resultado:.3f} mm/día)")
            
            self.combo_balance.configure(values=opciones, state="normal")
            if not hasattr(self, 'metodo_balance') or self.metodo_balance not in self.resultados_et0:
                # Seleccionar el primer método por defecto
                self.metodo_balance = list(self.resultados_et0.keys())[0]
                self.combo_balance.set(opciones[0])
                self.actualizar_label_metodo_balance()
        else:
            self.combo_balance.configure(values=["No hay resultados"], state="disabled")
    
    def seleccionar_metodo_balance(self):
        """Seleccionar método para balance hídrico"""
        seleccion = self.combo_balance.get()
        if seleccion and "(" in seleccion:
            # Extraer el método de la selección
            for metodo_id, resultado in self.resultados_et0.items():
                nombre = self.metodos_et[metodo_id]['nombre']
                if seleccion.startswith(nombre):
                    self.metodo_balance = metodo_id
                    break
            
            self.actualizar_label_metodo_balance()
    
    def actualizar_label_metodo_balance(self):
        """Actualizar label del método seleccionado para balance"""
        if self.metodo_balance in self.resultados_et0:
            nombre = self.metodos_et[self.metodo_balance]['nombre']
            et0_valor = self.resultados_et0[self.metodo_balance]
            texto = f"Método para balance: {nombre} (ET₀ = {et0_valor:.3f} mm/día)"
            self.label_metodo_balance.configure(text=texto, text_color="blue")
        else:
            self.label_metodo_balance.configure(text="Método para balance: No seleccionado", text_color="gray")
    
    def validar_valores(self, valores):
        """Validar que los valores estén en rangos lógicos según las variables disponibles"""
        # Validaciones básicas de temperatura si están disponibles
        if 't_min' in valores and 't_max' in valores:
            if valores['t_min'] >= valores['t_max']:
                messagebox.showerror("Error", "La temperatura mínima debe ser menor que la máxima")
                return False
        
        # Validaciones de humedad relativa si están disponibles    
        if 'rh_min' in valores and 'rh_max' in valores:
            if valores['rh_min'] >= valores['rh_max']:
                messagebox.showerror("Error", "La humedad relativa mínima debe ser menor que la máxima")
                return False
            
            if not (0 <= valores['rh_min'] <= 100) or not (0 <= valores['rh_max'] <= 100):
                messagebox.showerror("Error", "La humedad relativa debe estar entre 0 y 100%")
                return False
        elif 'rh_min' in valores:
            if not (0 <= valores['rh_min'] <= 100):
                messagebox.showerror("Error", "La humedad relativa debe estar entre 0 y 100%")
                return False
        elif 'rh_max' in valores:
            if not (0 <= valores['rh_max'] <= 100):
                messagebox.showerror("Error", "La humedad relativa debe estar entre 0 y 100%")
                return False
            
        # Validación de radiación solar si está disponible
        if 'rs' in valores and valores['rs'] < 0:
            messagebox.showerror("Error", "La radiación solar no puede ser negativa")
            return False
            
        # Validación de velocidad del viento si está disponible
        if 'uz' in valores and valores['uz'] < 0:
            messagebox.showerror("Error", "La velocidad del viento no puede ser negativa")
            return False
            
        # Validación de latitud si está disponible
        if 'lat' in valores and not (-90 <= valores['lat'] <= 90):
            messagebox.showerror("Error", "La latitud debe estar entre -90 y 90 grados")
            return False
            
        return True
    
    def calcular_balance_hidrico(self):
        """Calcular balance hídrico usando el método ET₀ seleccionado"""
        if not self.resultados_et0 or self.metodo_balance not in self.resultados_et0:
            messagebox.showerror("Error", "Primero debe calcular ET₀ y seleccionar un método para el balance")
            return
        
        # Obtener valores del balance
        try:
            valores_balance = {}
            for var_name, entry in self.variables_balance.items():
                valor_str = entry.get().strip()
                if not valor_str and var_name not in ['cultivo', 'periodo_fenologico']:
                    messagebox.showerror("Error", f"Por favor ingrese un valor para {var_name}")
                    return
                
                if var_name in ['cultivo', 'periodo_fenologico']:
                    valores_balance[var_name] = valor_str
                else:
                    try:
                        valores_balance[var_name] = float(valor_str)
                    except ValueError:
                        messagebox.showerror("Error", f"Valor inválido para {var_name}: {valor_str}")
                        return
            
            # Validaciones específicas del balance
            if not (0 <= valores_balance['humedad_actual'] <= 1):
                messagebox.showerror("Error", "La humedad actual debe estar entre 0 y 1")
                return
            if not (0 <= valores_balance['humedad_cc'] <= 1):
                messagebox.showerror("Error", "La capacidad de campo debe estar entre 0 y 1")
                return
            if not (0 <= valores_balance['humedad_pmp'] <= 1):
                messagebox.showerror("Error", "El punto de marchitez permanente debe estar entre 0 y 1")
                return
            if not (0 <= valores_balance['humedad_riego'] <= 1):
                messagebox.showerror("Error", "El umbral de riego debe estar entre 0 y 1")
                return
            
            if valores_balance['humedad_pmp'] >= valores_balance['humedad_cc']:
                messagebox.showerror("Error", "El PMP debe ser menor que la capacidad de campo")
                return
            
            # Obtener ET₀ del método seleccionado
            et0 = self.resultados_et0[self.metodo_balance]
            
            # Cálculos del balance
            lamina_aprovechable = (valores_balance['humedad_cc'] - valores_balance['humedad_pmp']) * valores_balance['profundidad_radicular'] * 10
            lamina_neta = (valores_balance['humedad_cc'] - valores_balance['humedad_riego']) * valores_balance['profundidad_radicular'] * 10
            etc = valores_balance['kc'] * et0
            deficit_hidrico = lamina_aprovechable - (valores_balance['humedad_actual'] * valores_balance['profundidad_radicular'] * 10)
            balance_diario = valores_balance['precipitacion'] - etc
            
            # Determinar recomendación
            if valores_balance['humedad_actual'] <= valores_balance['humedad_riego']:
                necesita_riego = True
                lamina_riego = lamina_neta
            else:
                necesita_riego = False
                lamina_riego = 0
            
            # Crear resultado del balance
            resultado_texto = f"""
💧 BALANCE HÍDRICO CALCULADO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 Método ET₀: {self.metodos_et[self.metodo_balance]['nombre']}
🌱 Cultivo: {valores_balance['cultivo']}
📅 Periodo: {valores_balance['periodo_fenologico']}

📊 RESULTADOS PRINCIPALES:
• ET₀ = {et0:.3f} mm/día
• Kc = {valores_balance['kc']:.2f}
• ETc = {etc:.3f} mm/día
• Precipitación = {valores_balance['precipitacion']:.1f} mm/día
• Balance diario = {balance_diario:.3f} mm/día

💧 LÁMINAS DE AGUA:
• Lámina aprovechable = {lamina_aprovechable:.1f} mm
• Lámina neta de riego = {lamina_neta:.1f} mm
• Déficit hídrico actual = {deficit_hidrico:.1f} mm

🚿 RECOMENDACIÓN DE RIEGO:
"""
            
            if necesita_riego:
                resultado_texto += f"✅ REGAR: Aplicar {lamina_riego:.1f} mm\n"
                resultado_texto += f"💡 La humedad actual ({valores_balance['humedad_actual']:.3f}) está por debajo del umbral ({valores_balance['humedad_riego']:.3f})"
            else:
                resultado_texto += f"❌ NO REGAR: Humedad suficiente\n"
                resultado_texto += f"💡 La humedad actual ({valores_balance['humedad_actual']:.3f}) está por encima del umbral ({valores_balance['humedad_riego']:.3f})"
            
            # Mostrar resultado
            self.label_balance_resultado.configure(text=resultado_texto, text_color="green")
            self.resultado_balance = {
                'et0': et0,
                'etc': etc,
                'balance_diario': balance_diario,
                'lamina_aprovechable': lamina_aprovechable,
                'lamina_neta': lamina_neta,
                'necesita_riego': necesita_riego,
                'lamina_riego': lamina_riego
            }
            
        except Exception as e:
            messagebox.showerror("Error", f"Error en el cálculo del balance hídrico:\n{str(e)}")
    
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
        """Exportar balance hídrico a CSV"""
        if self.resultado_balance is None:
            messagebox.showwarning("Advertencia", "Primero debe calcular el balance hídrico")
            return
        
        try:
            archivo = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("Archivos CSV", "*.csv")],
                title="Guardar balance hídrico como CSV"
            )
            
            if archivo:
                datos_export = {}
                
                # Datos del balance
                for var_name, entry in self.variables_balance.items():
                    datos_export[var_name] = [entry.get()]
                
                # Resultados calculados
                datos_export['et0_mm_dia'] = [self.resultado_balance['et0']]
                datos_export['etc_mm_dia'] = [self.resultado_balance['etc']]
                datos_export['balance_diario_mm'] = [self.resultado_balance['balance_diario']]
                datos_export['lamina_aprovechable_mm'] = [self.resultado_balance['lamina_aprovechable']]
                datos_export['lamina_neta_mm'] = [self.resultado_balance['lamina_neta']]
                datos_export['necesita_riego'] = [self.resultado_balance['necesita_riego']]
                datos_export['lamina_riego_mm'] = [self.resultado_balance['lamina_riego']]
                datos_export['metodo_et0'] = [self.metodos_et[self.metodo_balance]['nombre']]
                datos_export['fecha_calculo'] = [datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
                
                df = pd.DataFrame(datos_export)
                df.to_csv(archivo, index=False, encoding='utf-8')
                
                messagebox.showinfo("Éxito", f"Balance hídrico exportado exitosamente a:\n{archivo}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al exportar balance:\n{str(e)}")
    
    def limpiar_campos(self):
        """Limpiar todos los campos"""
        try:
            # Limpiar campos de entrada
            for entry in self.variables.values():
                try:
                    if entry.winfo_exists():
                        entry.delete(0, 'end')
                except:
                    pass
            
            self.resultados_et0.clear()
            
            # Limpiar tabla de resultados de forma segura
            try:
                if hasattr(self, 'frame_tabla_resultados') and self.frame_tabla_resultados.winfo_exists():
                    for widget in self.frame_tabla_resultados.winfo_children():
                        try:
                            if widget.winfo_exists():
                                widget.destroy()
                        except:
                            pass
            except:
                pass
            
            # Actualizar labels de forma segura
            try:
                if hasattr(self, 'label_estado_resultados') and self.label_estado_resultados.winfo_exists():
                    self.label_estado_resultados.configure(
                        text="Seleccione métodos y calcule ET₀ para ver resultados",
                        text_color="gray"
                    )
            except:
                pass
            
            # Limpiar selector de balance de forma segura
            try:
                if hasattr(self, 'combo_balance') and self.combo_balance.winfo_exists():
                    self.combo_balance.configure(values=["Primero calcule ET₀"], state="disabled")
                if hasattr(self, 'label_metodo_balance') and self.label_metodo_balance.winfo_exists():
                    self.label_metodo_balance.configure(text="Método para balance: No seleccionado", text_color="gray")
            except:
                pass
                
        except Exception as e:
            print(f"Error limpiando campos: {e}")
    
    def exportar_csv(self):
        """Exportar resultados comparativos a CSV"""
        if not self.resultados_et0:
            messagebox.showwarning("Advertencia", "Primero debe calcular ET₀ antes de exportar")
            return
        
        try:
            archivo = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("Archivos CSV", "*.csv")],
                title="Guardar resultados comparativos como CSV"
            )
            
            if archivo:
                datos_export = []
                
                # Variables meteorológicas
                variables_met = {}
                for var_name, entry in self.variables.items():
                    variables_met[var_name] = entry.get()
                
                # Resultados por método
                for metodo_id, resultado in self.resultados_et0.items():
                    fila = variables_met.copy()
                    fila['metodo_id'] = metodo_id
                    fila['metodo_nombre'] = self.metodos_et[metodo_id]['nombre']
                    fila['categoria'] = self.obtener_categoria_metodo(metodo_id)
                    fila['et0_mm_dia'] = resultado
                    fila['fecha_calculo'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    datos_export.append(fila)
                
                df = pd.DataFrame(datos_export)
                df.to_csv(archivo, index=False, encoding='utf-8')
                
                messagebox.showinfo("Éxito", f"Resultados exportados exitosamente a:\n{archivo}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al exportar CSV:\n{str(e)}")
    
    def crear_documentacion(self):
        """Crear sección de documentación"""
        frame_doc = ctk.CTkFrame(self.frame_principal)
        frame_doc.pack(fill="both", expand=True, padx=20, pady=10)
        
        titulo_doc = ctk.CTkLabel(frame_doc, 
                                 text="📚 Documentación - Sistema Comparativo",
                                 font=ctk.CTkFont(size=18, weight="bold"))
        titulo_doc.pack(pady=10)
        
        texto_doc = """
🔬 SISTEMA COMPARATIVO MÚLTIPLE - PyET Suite

Esta versión avanzada permite comparar múltiples métodos de ET₀ simultáneamente:

🎯 CARACTERÍSTICAS PRINCIPALES:
• Selección múltiple de métodos (individual o por categorías)
• Resultados comparativos en tabla vertical con estadísticas
• Selección específica de método para balance hídrico
• Exportación de resultados comparativos
• Análisis estadístico automático (promedio, min, max)

📊 CATEGORÍAS DE MÉTODOS:
🏆 Penman-Monteith (6): PM-FAO56, Penman Original, PM Genérico, ASCE, Kimberly, Thom-Oliver
☀️ Radiación (5): Priestley-Taylor, Makkink, Makkink KNMI, Jensen-Haise, Abtew
🌡️ Temperatura (5): Hargreaves, Hamon, McGuinness-Bordne, Oudin, Linacre
💧 Humedad (3): Turc, Romanenko, Haude
🔬 Especializados (2): FAO-24, Blaney-Criddle

🚀 FLUJO DE TRABAJO:
1. Seleccione métodos (individuales o por categoría)
2. Ingrese variables meteorológicas requeridas
3. Calcule ET₀ para comparación
4. Analice resultados en tabla comparativa
5. Seleccione método específico para balance hídrico
6. Calcule balance hídrico con método seleccionado
7. Exporte resultados individuales o comparativos

💡 VENTAJAS DEL SISTEMA COMPARATIVO:
• Identificar métodos más apropiados según datos disponibles
• Evaluar consistencia entre diferentes enfoques
• Seleccionar método óptimo según condiciones locales
• Análisis de sensibilidad entre métodos
• Documentación completa de comparaciones

⚠️ NOTAS IMPORTANTES:
• Variables requeridas se ajustan automáticamente según métodos seleccionados
• Métodos con errores se muestran separadamente con descripción del problema
• Balance hídrico usa ET₀ del método específicamente seleccionado
• Exportación incluye metadatos completos para trazabilidad
        """
        
        text_widget = ctk.CTkTextbox(frame_doc, height=200, font=ctk.CTkFont(size=11))
        text_widget.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        text_widget.insert("0.0", texto_doc)
        text_widget.configure(state="disabled")
    
    def mostrar_acerca_de(self):
        """Mostrar información acerca del programa"""
        mensaje = """
Calculadora de Evapotranspiración de Referencia (ET₀)
Sistema Comparativo Múltiple - PyET Suite
Versión 3.0 - Sistema Comparativo

🔬 Métodos Incluidos: 20 métodos oficiales PyET
🚀 Nuevas Características: Comparación múltiple simultánea

Desarrollado por: Miguel Alejandro Bermúdez Claros
Contacto: mibermudezc@unal.edu.co
Institución: Universidad Nacional de Colombia

✨ Características Destacadas:
• 20 métodos de cálculo de ET₀ oficiales PyET
• Sistema de selección múltiple por categorías
• Comparación simultánea con estadísticas
• Selección específica para balance hídrico
• Resultados tabulares con análisis comparativo
• Exportación de datos individuales y comparativos
• Validaciones inteligentes automáticas
• Interfaz adaptativa según métodos seleccionados

🎯 Ideal para:
• Investigación en evapotranspiración
• Comparación de métodos según disponibilidad de datos
• Análisis de sensibilidad entre métodos
• Selección de métodos óptimos para regiones específicas
• Estudios de validación de métodos ET₀

© 2024 - Suite completa para análisis comparativo ET₀
        """
        messagebox.showinfo("Acerca de - PyET Suite Comparativo", mensaje)

if __name__ == "__main__":
    app = CalculadoraET0Comparativa()
    app.ventana.mainloop()
