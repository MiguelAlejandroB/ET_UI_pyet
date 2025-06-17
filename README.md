# Calculadora de Evapotranspiración de Referencia (ET₀)

**Desarrollado por**: Miguel Alejandro Bermúdez Claros  
**Contacto**: mibermudezc@unal.edu.co

## Descripción
Aplicación con interfaz gráfica moderna para calcular la evapotranspiración de referencia diaria (ET₀) usando la ecuación de **Penman-Monteith FAO56**. Desarrollada con CustomTkinter y la librería `pyet`.

## Características
- 🌱 Interfaz moderna estilo tabla de Excel
- 🧮 Cálculo preciso usando ecuación Penman-Monteith FAO56
- 📊 Exportación de resultados a CSV
- 📚 Documentación integrada
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

### Variables requeridas
| Variable | Descripción | Unidad |
|----------|-------------|--------|
| t_min | Temperatura mínima diaria | °C |
| t_max | Temperatura máxima diaria | °C |
| rh_min | Humedad relativa mínima | % |
| rh_max | Humedad relativa máxima | % |
| rs | Radiación solar | MJ/m²/día |
| uz | Velocidad del viento a 2m | m/s |
| z | Altitud | m |
| lat | Latitud geográfica | grados |

### Resultado
- **ET₀**: Evapotranspiración de referencia en mm/día
- **Interpretación**: Categorización del resultado (Baja, Moderada, Alta, Muy Alta)

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

## Funcionalidades

### Cálculo ET₀
1. Ingrese todos los valores meteorológicos
2. Presione "🧮 Calcular ET₀"
3. Visualice el resultado e interpretación

### Exportar Datos
1. Realice un cálculo
2. Use "📊 Exportar CSV" o menú Archivo → Exportar CSV
3. Seleccione ubicación y nombre del archivo

### Limpiar Campos
- Use "🗑️ Limpiar" para resetear todos los valores

## Aplicaciones

- 💧 **Riego agrícola**: Cálculo de requerimientos hídricos
- 🌾 **Planificación de cultivos**: Estimación de consumo de agua
- 🏞️ **Gestión hídrica**: Balance de recursos en cuencas
- 📊 **Investigación**: Estudios climáticos y de sequía

## Ecuación Penman-Monteith FAO56

La ecuación utilizada es el estándar internacional recomendado por la FAO:

```
ET₀ = (0.408 × Δ × (Rn - G) + γ × (900/(T+273)) × u₂ × (es - ea)) / (Δ + γ × (1 + 0.34 × u₂))
```

Donde:
- Δ = pendiente de la curva de presión de vapor
- Rn = radiación neta
- G = flujo de calor del suelo
- γ = constante psicométrica
- T = temperatura media del aire
- u₂ = velocidad del viento a 2m
- es = presión de vapor de saturación
- ea = presión de vapor actual

## Requisitos del Sistema

- **Sistema Operativo**: Windows 10/11, macOS, Linux
- **Python**: 3.8 o superior
- **RAM**: 512 MB mínimo
- **Espacio**: 100 MB disponible

## Solución de Problemas

### Error: "pyet no encontrada"
```bash
pip install pyet
```

### Error: "customtkinter no encontrada"
```bash
pip install customtkinter
```

### El ejecutable no inicia
- Verificar que todas las librerías estén instaladas
- Compilar con `--onefile --windowed`
- Revisar permisos de ejecución

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

**Nota**: Esta aplicación implementa los estándares FAO-56 para cálculo de evapotranspiración de referencia, ampliamente utilizados en hidrología agrícola y gestión de recursos hídricos.

## Bibliografía

Si usa pyet en sus estudios, por favor cite el siguiente trabajo:

Vremec, M., Collenteur, R. A., and Birk, S.: Technical note: Improved handling of potential evapotranspiration in hydrological studies with PyEt, Hydrol. Earth Syst. Sci. Discuss. [preprint], https://doi.org/10.5194/hess-2022-417, in review, 2023.

```bibtex
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

