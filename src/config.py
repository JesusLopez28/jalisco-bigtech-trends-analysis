"""
Configuración y constantes para el proyecto de análisis de empleos Big Tech en Jalisco
"""

import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Credenciales API Adzuna
ADZUNA_APP_ID = os.getenv('ADZUNA_APP_ID', '24b6ac00')
ADZUNA_API_KEY = os.getenv('ADZUNA_API_KEY', 'dde84ccd4d8545294d7009fed74ec5ab')

# URLs base de la API
ADZUNA_BASE_URL = "https://api.adzuna.com/v1/api/jobs"
ADZUNA_COUNTRY = "mx"  # México

# Empresas Big Tech a buscar
BIG_TECH_COMPANIES = [
    'Oracle', 'Intel', 'IBM', 'Microsoft', 'Google', 'Amazon', 'Apple',
    'Meta', 'Facebook', 'Salesforce', 'Adobe', 'SAP', 'Dell', 'HP',
    'Cisco', 'VMware', 'NVIDIA', 'Qualcomm', 'Tesla', 'Netflix',
    'Uber', 'Airbnb', 'Twitter', 'LinkedIn', 'PayPal', 'eBay',
    'Zoom', 'Dropbox', 'Slack', 'Spotify', 'TikTok', 'ByteDance'
]

# Términos de búsqueda relacionados con tecnología
TECH_KEYWORDS = [
    'software engineer', 'data scientist', 'machine learning', 'artificial intelligence',
    'cloud engineer', 'devops', 'full stack', 'backend', 'frontend', 'mobile developer',
    'cybersecurity', 'data analyst', 'product manager', 'scrum master', 'technical lead',
    'system administrator', 'network engineer', 'database administrator', 'ui/ux designer',
    'quality assurance', 'python developer', 'java developer', 'javascript developer',
    'react developer', 'angular developer', 'node.js developer', 'blockchain developer'
]

# Ubicaciones en Jalisco
JALISCO_LOCATIONS = [
    'Guadalajara', 'Zapopan', 'Tlaquepaque', 'Tonalá', 'Tlajomulco',
    'El Salto', 'Puerto Vallarta', 'Jalisco'
]

# Configuración de scraping
MAX_REQUESTS_PER_MINUTE = int(os.getenv('MAX_REQUESTS_PER_MINUTE', 10))
DELAY_BETWEEN_REQUESTS = int(os.getenv('DELAY_BETWEEN_REQUESTS', 6))
MAX_RESULTS_PER_PAGE = 50
MAX_PAGES_PER_SEARCH = 5

# Directorios de datos
DATA_OUTPUT_DIR = os.getenv('DATA_OUTPUT_DIR', 'data/raw')
PROCESSED_DATA_DIR = os.getenv('PROCESSED_DATA_DIR', 'data/processed')
RESULTS_DIR = os.getenv('RESULTS_DIR', 'results')

# Headers para requests
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'application/json',
    'Accept-Language': 'es-MX,es;q=0.9,en;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
}
