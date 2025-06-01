"""
Scraper principal para extraer datos de empleos de Big Tech en Jalisco usando la API de Adzuna
"""

import requests
import pandas as pd
import json
import time
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import os
from urllib.parse import urlencode
import asyncio
import aiohttp

from config import (
    ADZUNA_APP_ID, ADZUNA_API_KEY, ADZUNA_BASE_URL, ADZUNA_COUNTRY,
    BIG_TECH_COMPANIES, TECH_KEYWORDS, JALISCO_LOCATIONS,
    MAX_REQUESTS_PER_MINUTE, DELAY_BETWEEN_REQUESTS, MAX_RESULTS_PER_PAGE,
    MAX_PAGES_PER_SEARCH, DATA_OUTPUT_DIR, HEADERS
)

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraping.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class AdzunaJobScraper:
    """Scraper para extraer datos de empleos usando la API de Adzuna"""
    
    def __init__(self):
        self.app_id = ADZUNA_APP_ID
        self.api_key = ADZUNA_API_KEY
        self.base_url = ADZUNA_BASE_URL
        self.country = ADZUNA_COUNTRY
        self.session = requests.Session()        
        self.session.headers.update(HEADERS)
        self.request_count = 0
        self.start_time = time.time()
    
    def _rate_limit(self):
        """Implementa rate limiting para no exceder límites de la API"""
        self.request_count += 1
        elapsed_time = time.time() - self.start_time
        
        if elapsed_time < 60 and self.request_count >= MAX_REQUESTS_PER_MINUTE:
            sleep_time = 60 - elapsed_time + 1
            logger.info(f"Rate limit alcanzado. Esperando {sleep_time:.2f} segundos...")
            time.sleep(sleep_time)
            self.request_count = 0
            self.start_time = time.time()
        
        time.sleep(DELAY_BETWEEN_REQUESTS)
    
    def build_search_url(self, what: str = "", where: str = "", page: int = 1) -> str:
        """Construye la URL de búsqueda para la API de Adzuna"""
        # Según la documentación de Adzuna, la estructura debe ser:
        # https://api.adzuna.com/v1/api/jobs/{country}/search/{page}?app_id={}&app_key={}
        
        params = {
            'app_id': self.app_id,
            'app_key': self.api_key,
            'results_per_page': MAX_RESULTS_PER_PAGE
        }
        
        # Solo agregar what y where si no están vacíos
        if what:
            params['what'] = what
        if where:
            params['where'] = where
        
        # Construir URL base correcta
        url = f"{self.base_url}/{self.country}/search/{page}?{urlencode(params)}"
        return url
    
    def search_jobs(self, what: str = "", where: str = "", max_pages: int = MAX_PAGES_PER_SEARCH) -> List[Dict]:
        """Busca empleos usando los parámetros especificados"""
        all_jobs = []
        
        logger.info(f"Buscando empleos: what='{what}', where='{where}'")
        
        for page in range(1, max_pages + 1):
            try:
                self._rate_limit()
                
                url = self.build_search_url(what=what, where=where, page=page)
                logger.info(f"Solicitando página {page}: {url}")
                
                response = self.session.get(url, timeout=30)
                response.raise_for_status()
                
                data = response.json()
                
                if 'results' not in data or not data['results']:
                    logger.info(f"No hay más resultados en la página {page}")
                    break
                
                jobs = data['results']
                all_jobs.extend(jobs)
                
                logger.info(f"Página {page}: {len(jobs)} empleos encontrados")
                
                # Si hay menos resultados que el máximo, probablemente sea la última página
                if len(jobs) < MAX_RESULTS_PER_PAGE:
                    break
                    
            except requests.exceptions.RequestException as e:
                logger.error(f"Error en la solicitud para página {page}: {e}")
                continue
            except json.JSONDecodeError as e:
                logger.error(f"Error decodificando JSON en página {page}: {e}")
                continue
            except Exception as e:
                logger.error(f"Error inesperado en página {page}: {e}")
                continue
        
        logger.info(f"Búsqueda completada: {len(all_jobs)} empleos totales encontrados")
        return all_jobs
    
    def extract_job_details(self, job: Dict) -> Dict:
        """Extrae y limpia los detalles relevantes de un empleo"""
        try:
            # Extraer información básica
            job_details = {
                'id': job.get('id', ''),
                'title': job.get('title', ''),
                'company': job.get('company', {}).get('display_name', ''),
                'location': job.get('location', {}).get('display_name', ''),
                'area': ', '.join(job.get('location', {}).get('area', [])),
                'salary_min': job.get('salary_min'),
                'salary_max': job.get('salary_max'),
                'salary_is_predicted': job.get('salary_is_predicted', False),
                'description': job.get('description', ''),
                'created': job.get('created', ''),
                'redirect_url': job.get('redirect_url', ''),
                'category': job.get('category', {}).get('label', ''),
                'contract_type': job.get('contract_type', ''),
                'contract_time': job.get('contract_time', ''),
                'latitude': job.get('latitude'),
                'longitude': job.get('longitude'),
            }
            
            # Clasificar si es Big Tech
            company_name = job_details['company'].lower()
            is_big_tech = any(company.lower() in company_name for company in BIG_TECH_COMPANIES)
            job_details['is_big_tech'] = is_big_tech
            
            # Identificar tecnologías mencionadas
            full_text = f"{job_details['title']} {job_details['description']}".lower()
            mentioned_keywords = [keyword for keyword in TECH_KEYWORDS if keyword.lower() in full_text]
            job_details['mentioned_tech_keywords'] = ', '.join(mentioned_keywords)
            job_details['tech_keywords_count'] = len(mentioned_keywords)
            
            # Timestamp de scraping
            job_details['scraped_at'] = datetime.now().isoformat()
            
            return job_details
            
        except Exception as e:
            logger.error(f"Error extrayendo detalles del empleo {job.get('id', 'N/A')}: {e}")
            return {}
    
    def scrape_big_tech_jobs_jalisco(self) -> pd.DataFrame:
        """Función principal para extraer empleos de Big Tech en Jalisco"""
        all_jobs_data = []
        
        logger.info("Iniciando scraping de empleos Big Tech en Jalisco")
        
        # Estrategia 1: Buscar por empresas específicas
        logger.info("=== Buscando por empresas Big Tech específicas ===")
        for company in BIG_TECH_COMPANIES[:10]:  # Limitamos a las primeras 10 para no hacer demasiadas requests
            for location in JALISCO_LOCATIONS[:3]:  # Limitamos a las 3 ubicaciones principales
                jobs = self.search_jobs(what=company, where=location, max_pages=2)
                
                for job in jobs:
                    job_details = self.extract_job_details(job)
                    if job_details:
                        all_jobs_data.append(job_details)
        
        # Estrategia 2: Buscar por keywords técnicos en Jalisco
        logger.info("=== Buscando por keywords técnicos ===")
        for keyword in TECH_KEYWORDS[:15]:  # Limitamos a los primeros 15 keywords
            for location in JALISCO_LOCATIONS[:2]:  # Solo Guadalajara y Zapopan
                jobs = self.search_jobs(what=keyword, where=location, max_pages=2)
                
                for job in jobs:
                    job_details = self.extract_job_details(job)
                    if job_details:
                        all_jobs_data.append(job_details)
        
        # Estrategia 3: Búsqueda general de tecnología en Jalisco
        logger.info("=== Búsqueda general de empleos tech ===")
        general_terms = ['software', 'technology', 'IT', 'developer', 'engineer']
        for term in general_terms:
            for location in JALISCO_LOCATIONS[:2]:
                jobs = self.search_jobs(what=term, where=location, max_pages=3)
                
                for job in jobs:
                    job_details = self.extract_job_details(job)
                    if job_details:
                        all_jobs_data.append(job_details)
        
        # Convertir a DataFrame y limpiar duplicados
        df = pd.DataFrame(all_jobs_data)
        
        if not df.empty:
            # Eliminar duplicados basados en ID
            initial_count = len(df)
            df = df.drop_duplicates(subset=['id'], keep='first')
            final_count = len(df)
            logger.info(f"Duplicados eliminados: {initial_count - final_count}")
            
            # Filtrar solo empleos en Jalisco (verificación adicional)
            jalisco_terms = ['guadalajara', 'zapopan', 'jalisco', 'tlaquepaque', 'tonalá', 'tlajomulco']
            df = df[df['location'].str.lower().str.contains('|'.join(jalisco_terms), na=False)]
            
            logger.info(f"Dataset final: {len(df)} empleos únicos en Jalisco")
        else:
            logger.warning("No se encontraron empleos")
        
        return df
    
    def save_data(self, df: pd.DataFrame, filename: str = None) -> str:
        """Guarda el dataset extraído"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"jalisco_bigtech_jobs_{timestamp}.csv"
        
        # Crear directorio si no existe
        os.makedirs(DATA_OUTPUT_DIR, exist_ok=True)
        
        filepath = os.path.join(DATA_OUTPUT_DIR, filename)
        df.to_csv(filepath, index=False, encoding='utf-8')
        
        logger.info(f"Dataset guardado: {filepath}")
        logger.info(f"Estadísticas del dataset:")
        logger.info(f"  - Total de empleos: {len(df)}")
        logger.info(f"  - Empleos Big Tech: {df['is_big_tech'].sum()}")
        logger.info(f"  - Empresas únicas: {df['company'].nunique()}")
        logger.info(f"  - Ubicaciones únicas: {df['location'].nunique()}")
        
        return filepath


def main():
    """Función principal para ejecutar el scraping"""
    scraper = AdzunaJobScraper()
    
    try:
        # Realizar scraping
        df = scraper.scrape_big_tech_jobs_jalisco()
        
        if not df.empty:
            # Guardar datos
            filepath = scraper.save_data(df)
            
            # Mostrar resumen
            print("\n" + "="*50)
            print("RESUMEN DEL SCRAPING COMPLETADO")
            print("="*50)
            print(f"📊 Total de empleos extraídos: {len(df)}")
            print(f"🏢 Empleos Big Tech: {df['is_big_tech'].sum()}")
            print(f"🏙️ Ubicaciones en Jalisco: {df['location'].nunique()}")
            print(f"💼 Empresas únicas: {df['company'].nunique()}")
            print(f"💰 Empleos con salario: {df['salary_min'].notna().sum()}")
            print(f"📁 Archivo guardado: {filepath}")
            print("="*50)
            
            # Mostrar top empresas
            if len(df) > 0:
                print("\n🔝 Top 10 empresas con más ofertas:")
                top_companies = df['company'].value_counts().head(10)
                for company, count in top_companies.items():
                    print(f"   {company}: {count} ofertas")
        else:
            print("❌ No se pudieron extraer datos. Revisa la configuración de la API.")
            
    except Exception as e:
        logger.error(f"Error en el proceso principal: {e}")
        print(f"❌ Error durante el scraping: {e}")


if __name__ == "__main__":
    main()
