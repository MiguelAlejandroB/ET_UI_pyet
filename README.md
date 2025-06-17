# Calculadora de Evapotranspiración de Referencia (ET₀) y Balance Hídrico

**Desarrollado por**: Miguel Alejandro Bermúdez Claros  
**Contacto**: mibermudezc@unal.edu.co  
**Institución**: Universidad Nacional de Colombia

## Descripción

Aplicación integral con interfaz gráfica moderna para calcular la **evapotranspiración de referencia (ET₀)** usando la ecuación Penman-Monteith FAO56 y realizar **análisis completos de balance hídrico** para cultivos. Desarrollada con CustomTkinter y la librería científica `pyet`.

## Características Principales

### Evapotranspiración (ET₀)
- 🌡️ Cálculo preciso con ecuación Penman-Monteith FAO56
- 🌱 Interfaz moderna estilo hoja de cálculo
- 📈 Interpretación automática de resultados

### Balance Hídrico
- 💧 Análisis completo de balance hídrico por cultivo
- 🌾 Gestión de coeficientes de cultivo (Kc)
- 🏞️ Cálculo de profundidades de agua disponible
- 📊 Evaluación de necesidades de riego

### Funcionalidades Técnicas
- 📋 Validación de datos en tiempo real
- 💾 Exportación limpia a CSV
- 🧮 Cálculos según estándares FAO-56
- ⚡ Lista para compilar a ejecutable (.exe)

## Instalación

### Opción 1: Instalación automática
```bash
pip install -r requirements.txt
```

### Opción 2: Instalación manual
```bash
pip install customtkinter pandas pyet pyinstaller
```

## Uso

### Ejecutar la aplicación
```bash
python calculadora_et0.py
```

## Variables de Entrada

### Datos Meteorológicos
| Variable | Descripción | Unidad | Rango |
|----------|-------------|--------|-------|
| t_min | Temperatura mínima diaria | °C | -50 a 60 |
| t_max | Temperatura máxima diaria | °C | -50 a 60 |
| rh_min | Humedad relativa mínima | % | 0 a 100 |
| rh_max | Humedad relativa máxima | % | 0 a 100 |
| rs | Radiación solar | MJ/m²/día | 0 a 50 |
| uz | Velocidad del viento a 2m | m/s | 0 a 50 |
| z | Altitud | m | -500 a 5000 |
| lat | Latitud geográfica | grados | -90 a 90 |

### Datos de Balance Hídrico
| Variable | Descripción | Unidad | Rango |
|----------|-------------|--------|-------|
| θ_actual | Humedad del suelo actual | adimensional | 0.0 a 1.0 |
| θ_cc | Humedad a capacidad de campo | adimensional | 0.0 a 1.0 |
| θ_pmp | Humedad en punto marchitez | adimensional | 0.0 a 1.0 |
| θ_umbral | Umbral de riego | adimensional | 0.0 a 1.0 |
| cultivo | Nombre del cultivo | texto | - |
| profundidad | Profundidad radicular | m | 0.1 a 5.0 |
| periodo | Período fenológico | texto | - |
| kc | Coeficiente de cultivo | - | 0.1 a 2.0 |
| precipitacion | Precipitación | mm | 0 a 1000 |

## Resultados

### Evapotranspiración
- **ET₀**: Evapotranspiración de referencia (mm/día)
- **Interpretación**: Categorización (Baja ≤2, Moderada 2-4, Alta 4-6, Muy Alta >6)

### Balance Hídrico
- **ETc**: Evapotranspiración del cultivo (mm/día)
- **Lámina disponible**: Agua disponible para el cultivo (mm)
- **Lámina neta**: Agua neta requerida (mm)
- **Disponibilidad actual**: Agua actualmente disponible (mm)

## Crear Ejecutable

Para generar un archivo `.exe` independiente:

```bash
pyinstaller --onefile --windowed --name "CalculadoraET0" calculadora_et0.py
```

El ejecutable se generará en la carpeta `dist/`.

### Opciones avanzadas de PyInstaller
```bash
# Con icono personalizado
pyinstaller --onefile --windowed --icon=icono.ico --name "CalculadoraET0" calculadora_et0.py

# Sin consola de debug
pyinstaller --onefile --noconsole --name "CalculadoraET0" calculadora_et0.py
```

## Flujo de Trabajo

### 1. Cálculo de ET₀
1. **Datos meteorológicos**: Complete todas las variables climáticas
2. **Calcular**: Presione "🧮 Calcular ET₀"
3. **Resultado**: Visualice ET₀ e interpretación automática

### 2. Balance Hídrico (Opcional)
1. **Prerequisito**: Debe haber calculado ET₀ primero
2. **Datos del cultivo**: Complete información de humedad del suelo y cultivo
3. **Calcular balance**: Presione "⚖️ Calcular Balance Hídrico"
4. **Análisis**: Revise láminas de agua y recomendaciones

### 3. Gestión de Datos
- **Limpiar ET₀**: "🗑️ Limpiar" (solo datos meteorológicos)
- **Limpiar Balance**: "🧹 Limpiar Balance" (solo datos de balance)
- **Exportar**: "📊 Exportar CSV" o menú Archivo → Exportar CSV
- **Formato**: CSV limpio sin prefijos, listo para análisis

### 4. Validaciones Automáticas
- ✅ Verificación de rangos de entrada
- ⚠️ Alertas de valores inconsistentes
- 🔒 Bloqueo de balance sin ET₀ calculado

## Aplicaciones Profesionales

### Agricultura de Precisión
- 💧 **Programación de riego**: Cálculo preciso de necesidades hídricas
- 🌾 **Manejo de cultivos**: Optimización del uso del agua por fenología
- 📈 **Eficiencia hídrica**: Reducción de costos y aumenta de rendimientos

### Gestión de Recursos Hídricos
- 🏞️ **Balance hídrico cuencas**: Evaluación de disponibilidad de agua
- 🌊 **Planificación hídrica**: Diseño de sistemas de riego
- 📊 **Monitoreo ambiental**: Estudios de sequía y cambio climático

### Investigación y Academia
- 🔬 **Estudios hidrológicos**: Validación de modelos de ET₀
- 📚 **Enseñanza**: Herramienta didáctica para cursos de hidrología
- 📖 **Publicaciones**: Datos para investigación científica

## Base Científica

### Ecuación Penman-Monteith FAO56
Estándar internacional recomendado por la FAO para cálculo de ET₀:

```
ET₀ = (0.408 × Δ × (Rn - G) + γ × (900/(T+273)) × u₂ × (es - ea)) / (Δ + γ × (1 + 0.34 × u₂))
```

**Variables de la ecuación:**
- Δ = Pendiente de la curva de presión de vapor (kPa/°C)
- Rn = Radiación neta en superficie del cultivo (MJ/m²/día)
- G = Flujo de calor del suelo (MJ/m²/día)
- γ = Constante psicométrica (kPa/°C)
- T = Temperatura media del aire a 2m (°C)
- u₂ = Velocidad del viento a 2m (m/s)
- es = Presión de vapor de saturación (kPa)
- ea = Presión de vapor actual (kPa)

### Balance Hídrico
Las ecuaciones de balance utilizadas incluyen:

**Evapotranspiración del cultivo:**
```
ETc = ET₀ × Kc
```

**Lámina de agua disponible:**
```
LA = (θcc - θpmp) × Pr × 1000
```

**Lámina neta requerida:**
```
LN = (θcc - θumbral) × Pr × 1000
```

**Disponibilidad actual:**
```
DA = (θactual - θpmp) × Pr × 1000
```

Donde θ representa contenidos de humedad adimensionales y Pr la profundidad radicular en metros.

## Requisitos del Sistema

- **Sistema Operativo**: Windows 10/11, macOS, Linux
- **Python**: 3.8 o superior
- **RAM**: 512 MB mínimo
- **Espacio**: 100 MB disponible

## Solución de Problemas

### Errores de Instalación
```bash
# Error: pyet no encontrada
pip install pyet

# Error: customtkinter no encontrada  
pip install customtkinter

# Reinstalar todas las dependencias
pip install -r requirements.txt --force-reinstall
```

### Problemas de Validación
- **"Valores fuera de rango"**: Verificar rangos en tablas de variables
- **"Calcule ET₀ primero"**: Balance hídrico requiere ET₀ previo
- **"Datos incompletos"**: Completar todos los campos obligatorios

### Problemas del Ejecutable
- Verificar instalación completa de dependencias
- Compilar con flags: `--onefile --windowed`
- Revisar permisos de ejecución en Windows
- Ejecutar como administrador si es necesario

### Problemas de Exportación
- Verificar permisos de escritura en carpeta destino
- Cerrar archivos CSV abiertos en Excel antes de exportar
- Usar nombres de archivo sin caracteres especiales

## Estructura del Proyecto

```
📁 ET/
├── 📄 calculadora_et0.py    # Script principal
├── 📄 requirements.txt      # Dependencias
├── 📄 README.md            # Documentación
└── 📁 dist/               # Ejecutables (generado por PyInstaller)
```

## Licencia

Script desarrollado para uso académico y profesional. Libre uso con fines educativos y de investigación.

## Soporte

Para problemas o mejoras, verificar:
1. Versión de Python (3.8+)
2. Instalación de dependencias
3. Valores de entrada válidos
4. Conexión a internet (primera instalación de pyet)

---

## Versión y Desarrollo

**Versión Actual**: 2.0  
**Última actualización**: Diciembre 2024  
**Estado**: Estable para uso profesional

### Próximas Características (v2.1)
- 📱 Interfaz responsive para diferentes resoluciones
- 🌍 Soporte multiidioma (Inglés/Español)
- 📈 Gráficos de tendencias ET₀/Balance
- 🔄 Análisis de series temporales

---

**Nota**: Esta aplicación implementa los estándares **FAO-56** para cálculo de evapotranspiración de referencia y balance hídrico, metodologías ampliamente utilizadas en hidrología agrícola y gestión sostenible de recursos hídricos.

## Bibliografía

### Referencias Principales

**FAO-56**: Allen, R.G., Pereira, L.S., Raes, D., Smith, M., 1998. *Crop evapotranspiration - Guidelines for computing crop water requirements*. FAO Irrigation and drainage paper 56. FAO, Rome, Italy.

**PyEt Library**: Si usa PyEt en sus estudios, por favor cite:
> Vremec, M., Collenteur, R. A., and Birk, S.: Technical note: Improved handling of potential evapotranspiration in hydrological studies with PyEt, Hydrol. Earth Syst. Sci. Discuss. [preprint], https://doi.org/10.5194/hess-2022-417, in review, 2023.

### Citas en Formato BibTeX

```bibtex
@techreport{allen1998crop,
  title={Crop evapotranspiration-Guidelines for computing crop water requirements},
  author={Allen, Richard G and Pereira, Luis S and Raes, Dirk and Smith, Martin},
  year={1998},
  institution={FAO},
  address={Rome, Italy},
  number={56}
}

@Article{hess-2022-417,
  AUTHOR = {Vremec, M. and Collenteur, R. A. and Birk, S.},
  TITLE = {Technical note: Improved handling of potential evapotranspiration in hydrological studies with \textit{PyEt}},
  JOURNAL = {Hydrology and Earth System Sciences Discussions},
  VOLUME = {2023},
  YEAR = {2023},
  PAGES = {1--23},
  URL = {https://hess.copernicus.org/preprints/hess-2022-417/},
  DOI = {10.5194/hess-2022-417}
}
```



