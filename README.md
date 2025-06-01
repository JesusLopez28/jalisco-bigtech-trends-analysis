# 🚀 Análisis de Tendencias de Empleos Big Tech en Jalisco

## 📋 Descripción del Proyecto

Este proyecto desarrolla un sistema funcional de análisis de datos en tiempo real para monitorear tendencias de contratación en empresas Big Tech ubicadas en Jalisco, México. Utilizando web scraping con la API de Adzuna, el sistema permite analizar patrones de contratación, habilidades demandadas, y tendencias salariales en el sector tecnológico.

**🎯 Objetivo General:** Desarrollar un sistema funcional de análisis de datos que permita monitorear tendencias, aplicar procesamiento y visualización de datos, implementar reducción de dimensionalidad y generar predicciones basadas en series de tiempo para el mercado laboral tech en Jalisco.

## 🏢 Empresas Objetivo

El análisis se enfoca en empresas Big Tech con presencia en Jalisco:
- Oracle, Intel, IBM, Microsoft, Google, Amazon, Apple
- Meta, Salesforce, Adobe, SAP, Dell, HP, Cisco
- VMware, NVIDIA, Qualcomm, Tesla, Netflix, Uber
- Y más...

## 🌍 Alcance Geográfico

- **Región Principal:** Jalisco, México
- **Ciudades Específicas:** Guadalajara, Zapopan, Tlaquepaque, Tonalá, Tlajomulco, El Salto

## 📊 Estructura del Proyecto

```
jalisco-bigtech-trends-analysis/
├── data/
│   ├── raw/              # Datos extraídos directamente de la API
│   └── processed/        # Datos procesados y limpios
├── src/
│   ├── config.py         # Configuración y constantes
│   ├── scraper.py        # Scraper principal de Adzuna API
│   └── data_processor.py # Procesamiento y análisis de datos
├── notebooks/
│   └── scraping_empleos_bigtech_jalisco.ipynb  # Notebook de scraping
├── results/              # Resultados de análisis y visualizaciones
├── main.py              # Script principal de ejecución
├── requirements.txt     # Dependencias del proyecto
└── README.md           # Este archivo
```

## 🛠️ Tecnologías Utilizadas

- **Web Scraping:** API de Adzuna
- **Procesamiento:** Python, Pandas, NumPy
- **Visualización:** Matplotlib, Seaborn, Plotly
- **Machine Learning:** Scikit-learn
- **Series de Tiempo:** ARIMA, Prophet (próximamente)

## 🚀 Instalación y Uso

### 1. Clonar el repositorio
```bash
git clone https://github.com/tu-usuario/jalisco-bigtech-trends-analysis.git
cd jalisco-bigtech-trends-analysis
```

### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 3. Configurar credenciales
Crear archivo `.env` con las credenciales de la API de Adzuna:
```env
ADZUNA_APP_ID=tu_app_id
ADZUNA_API_KEY=tu_api_key
```

### 4. Ejecutar scraping
```bash
python main.py
```

O para análisis de datos existentes:
```bash
python main.py analyze
```

### 5. Usar Jupyter Notebook
```bash
jupyter lab notebooks/scraping_empleos_bigtech_jalisco.ipynb
```

## 📈 Características del Dataset

El dataset extraído incluye:

### 📊 Información Básica
- **ID único** del empleo
- **Título** del puesto
- **Empresa** ofertante
- **Ubicación** específica en Jalisco
- **Fecha** de publicación

### 💰 Información Salarial
- Salario mínimo y máximo
- Indicador de salario predicho
- Salario promedio calculado

### 🔧 Información Técnica
- **Descripción** completa del empleo
- **Categoría** laboral
- **Tipo de contrato** (tiempo completo, medio tiempo)
- **Modalidad** (presencial, remoto, híbrido)

### 🏆 Clasificaciones Generadas
- **is_big_tech:** Clasificación automática Big Tech
- **experience_level:** Nivel de experiencia requerido
- **mentioned_tech_keywords:** Tecnologías mencionadas
- **tech_keywords_count:** Cantidad de tecnologías mencionadas

### 🌐 Información Geográfica
- Coordenadas (latitud, longitud)
- Área específica dentro de Jalisco

## 📋 Análisis Implementados

### 1. 📊 Análisis Exploratorio de Datos (EDA)
- Estadísticas descriptivas
- Distribución por empresas y ubicaciones
- Análisis de salarios
- Tecnologías más demandadas

### 2. 🔍 Reducción de Dimensionalidad
- PCA (Principal Component Analysis)
- t-SNE para visualización
- Clustering de empleos similares

### 3. 📈 Análisis Temporal
- Tendencias de publicación de empleos
- Estacionalidad en contrataciones
- Predicciones con series de tiempo

### 4. 🤖 Modelado Predictivo
- Predicción de salarios
- Clasificación de nivel de experiencia
- Recomendación de habilidades

## 📊 Resultados Esperados

1. **Dashboard interactivo** con tendencias en tiempo real
2. **Modelo predictivo** de demanda por tecnologías
3. **Análisis de competitividad** salarial por empresa
4. **Recomendaciones** para estudiantes próximos a egresar
5. **Mapeo de habilidades** más valoradas en el mercado

## 📚 Metodología de Investigación

### Adquisición de Datos
- **Fuente:** API de Adzuna (adzuna.com)
- **Método:** Web scraping automatizado
- **Frecuencia:** Actualización periódica

### Preprocesamiento
- Limpieza de duplicados
- Normalización de texto
- Codificación de variables categóricas
- Creación de características derivadas

### Análisis
- Estadísticas descriptivas
- Visualizaciones interactivas
- Análisis de correlaciones
- Modelado predictivo

## 🎓 Aplicación Académica

Este proyecto cumple con los requisitos de la materia **Análisis de Datos**:

✅ **Fuente de datos reales** (API de Adzuna)  
✅ **Técnicas de reducción de dimensionalidad** (PCA, t-SNE)  
✅ **Modelos de series de tiempo** (ARIMA, Prophet)  
✅ **Visualizaciones avanzadas** (matplotlib, plotly, seaborn)  
✅ **Análisis temporal** con datos de fechas de publicación  
✅ **Procesamiento de datos** completo y documentado  

## 🚧 Estado del Proyecto

- [x] ✅ Configuración inicial del proyecto
- [x] ✅ Implementación del scraper con API de Adzuna
- [x] ✅ Procesamiento y limpieza de datos
- [x] ✅ Notebook de scraping interactivo
- [ ] 🔄 Análisis exploratorio completo (EDA)
- [ ] 🔄 Implementación de reducción de dimensionalidad
- [ ] 🔄 Análisis de series de tiempo
- [ ] 🔄 Modelos predictivos avanzados
- [ ] 🔄 Dashboard interactivo
- [ ] 🔄 Informe final

## 👥 Equipo

**Estudiantes CETI Colomos - 7mo Semestre**  
**Materia:** Análisis de Datos - 3er Parcial  
**Profesor:** [Nombre del profesor]

## 📞 Contacto

Para dudas o contribuciones, contactar a través de:
- Email institucional CETI
- Issues en este repositorio

---

**📅 Última actualización:** Junio 2025  
**🎯 Próxima entrega:** [Fecha del 3er parcial]