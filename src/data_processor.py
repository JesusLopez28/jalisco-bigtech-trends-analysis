"""
Utilidades para el preprocesamiento y análisis de datos de empleos
"""

import pandas as pd
import numpy as np
import re
from datetime import datetime, timedelta
import logging
from typing import List, Dict, Optional, Tuple
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
import warnings
warnings.filterwarnings('ignore')

logger = logging.getLogger(__name__)


class JobDataProcessor:
    """Clase para preprocesar y analizar datos de empleos"""
    
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        self.original_shape = df.shape
        
    def clean_data(self) -> pd.DataFrame:
        """Limpia y preprocesa los datos básicos"""
        logger.info("Iniciando limpieza de datos...")
        
        # Convertir fechas
        if 'created' in self.df.columns:
            self.df['created'] = pd.to_datetime(self.df['created'], errors='coerce')
        
        if 'scraped_at' in self.df.columns:
            self.df['scraped_at'] = pd.to_datetime(self.df['scraped_at'], errors='coerce')
        
        # Limpiar salarios
        self.df['salary_min'] = pd.to_numeric(self.df['salary_min'], errors='coerce')
        self.df['salary_max'] = pd.to_numeric(self.df['salary_max'], errors='coerce')
        
        # Calcular salario promedio
        self.df['salary_avg'] = (self.df['salary_min'] + self.df['salary_max']) / 2
        
        # Limpiar texto
        text_columns = ['title', 'description', 'company', 'location']
        for col in text_columns:
            if col in self.df.columns:
                self.df[col] = self.df[col].astype(str).str.strip()
                self.df[col] = self.df[col].replace('nan', np.nan)
        
        # Extraer características adicionales del título y descripción
        self._extract_job_features()
        
        logger.info(f"Limpieza completada. Shape: {self.original_shape} -> {self.df.shape}")
        return self.df
    
    def _extract_job_features(self):
        """Extrae características adicionales de los textos"""
        
        # Niveles de experiencia
        senior_patterns = r'\b(senior|sr\.|lead|principal|architect|manager|director)\b'
        junior_patterns = r'\b(junior|jr\.|entry|trainee|intern|graduate)\b'
        mid_patterns = r'\b(mid|middle|intermediate)\b'
        
        self.df['is_senior'] = self.df['title'].str.lower().str.contains(senior_patterns, regex=True, na=False)
        self.df['is_junior'] = self.df['title'].str.lower().str.contains(junior_patterns, regex=True, na=False)
        self.df['is_mid'] = self.df['title'].str.lower().str.contains(mid_patterns, regex=True, na=False)
        
        # Determinar nivel basado en patrones
        def determine_level(row):
            if row['is_senior']:
                return 'Senior'
            elif row['is_junior']:
                return 'Junior'
            elif row['is_mid']:
                return 'Mid'
            else:
                return 'No especificado'
        
        self.df['experience_level'] = self.df.apply(determine_level, axis=1)
        
        # Modalidad de trabajo
        remote_patterns = r'\b(remote|remoto|home office|trabajo desde casa|wfh)\b'
        hybrid_patterns = r'\b(hybrid|híbrido|mixto)\b'
        onsite_patterns = r'\b(onsite|presencial|office|oficina)\b'
        
        full_text = (self.df['title'] + ' ' + self.df['description']).str.lower()
        
        self.df['is_remote'] = full_text.str.contains(remote_patterns, regex=True, na=False)
        self.df['is_hybrid'] = full_text.str.contains(hybrid_patterns, regex=True, na=False)
        self.df['is_onsite'] = full_text.str.contains(onsite_patterns, regex=True, na=False)
        
        # Tecnologías específicas
        tech_patterns = {
            'python': r'\bpython\b',
            'java': r'\bjava\b',
            'javascript': r'\b(javascript|js)\b',
            'react': r'\breact\b',
            'angular': r'\bangular\b',
            'node': r'\b(node\.js|nodejs)\b',
            'sql': r'\b(sql|mysql|postgresql|oracle)\b',
            'cloud': r'\b(aws|azure|gcp|cloud)\b',
            'machine_learning': r'\b(machine learning|ml|ai|artificial intelligence)\b',
            'docker': r'\bdocker\b',
            'kubernetes': r'\bkubernetes\b',
            'agile': r'\b(agile|scrum|kanban)\b'
        }
        
        for tech, pattern in tech_patterns.items():
            self.df[f'mentions_{tech}'] = full_text.str.contains(pattern, regex=True, na=False)
    
    def create_time_features(self) -> pd.DataFrame:
        """Crea características temporales para análisis de series de tiempo"""
        if 'created' in self.df.columns:
            self.df['year'] = self.df['created'].dt.year
            self.df['month'] = self.df['created'].dt.month
            self.df['day'] = self.df['created'].dt.day
            self.df['day_of_week'] = self.df['created'].dt.dayofweek
            self.df['week_of_year'] = self.df['created'].dt.isocalendar().week
            self.df['quarter'] = self.df['created'].dt.quarter
            
            # Agregar nombres de días y meses
            self.df['day_name'] = self.df['created'].dt.day_name()
            self.df['month_name'] = self.df['created'].dt.month_name()
            
            # Características de estacionalidad
            self.df['is_weekend'] = self.df['day_of_week'].isin([5, 6])
            self.df['is_month_start'] = self.df['created'].dt.is_month_start
            self.df['is_month_end'] = self.df['created'].dt.is_month_end
        
        return self.df
    
    def get_summary_stats(self) -> Dict:
        """Genera estadísticas resumidas del dataset"""
        stats = {
            'total_jobs': len(self.df),
            'unique_companies': self.df['company'].nunique() if 'company' in self.df.columns else 0,
            'unique_locations': self.df['location'].nunique() if 'location' in self.df.columns else 0,
            'big_tech_jobs': self.df['is_big_tech'].sum() if 'is_big_tech' in self.df.columns else 0,
            'big_tech_percentage': (self.df['is_big_tech'].sum() / len(self.df) * 100) if 'is_big_tech' in self.df.columns else 0,
            'jobs_with_salary': self.df['salary_min'].notna().sum() if 'salary_min' in self.df.columns else 0,
            'avg_salary': self.df['salary_avg'].mean() if 'salary_avg' in self.df.columns else 0,
            'median_salary': self.df['salary_avg'].median() if 'salary_avg' in self.df.columns else 0,
            'date_range': {
                'start': self.df['created'].min() if 'created' in self.df.columns else None,
                'end': self.df['created'].max() if 'created' in self.df.columns else None
            }
        }
        
        return stats
    
    def prepare_for_modeling(self) -> Tuple[pd.DataFrame, Dict]:
        """Prepara los datos para modelado de machine learning"""
        logger.info("Preparando datos para modelado...")
        
        # Crear DataFrame de características
        feature_df = self.df.copy()
        
        # Encoding categórico
        categorical_columns = ['company', 'location', 'category', 'contract_type', 'contract_time', 'experience_level']
        encoders = {}
        
        for col in categorical_columns:
            if col in feature_df.columns:
                le = LabelEncoder()
                # Manejar valores nulos
                feature_df[col] = feature_df[col].fillna('Unknown')
                feature_df[f'{col}_encoded'] = le.fit_transform(feature_df[col])
                encoders[col] = le
        
        # Características numéricas
        numeric_features = ['salary_min', 'salary_max', 'salary_avg', 'tech_keywords_count',
                           'latitude', 'longitude', 'year', 'month', 'day', 'day_of_week']
        
        # Rellenar valores nulos en características numéricas
        for col in numeric_features:
            if col in feature_df.columns:
                feature_df[col] = feature_df[col].fillna(feature_df[col].median())
        
        # Características booleanas (convertir a int)
        boolean_features = [col for col in feature_df.columns if col.startswith(('is_', 'mentions_'))]
        for col in boolean_features:
            feature_df[col] = feature_df[col].astype(int)
        
        logger.info(f"Datos preparados para modelado. Features: {len(feature_df.columns)}")
        
        return feature_df, encoders
    
    def create_time_series_data(self, freq: str = 'D') -> pd.DataFrame:
        """Crea datos agregados para análisis de series de tiempo"""
        if 'created' not in self.df.columns:
            logger.warning("No hay columna de fecha para crear series de tiempo")
            return pd.DataFrame()
        
        # Agregar por fecha
        time_series = self.df.set_index('created').resample(freq).agg({
            'id': 'count',  # Número de empleos por periodo
            'is_big_tech': 'sum',  # Empleos Big Tech por periodo
            'salary_avg': 'mean',  # Salario promedio por periodo
            'tech_keywords_count': 'mean',  # Promedio de keywords tech
        }).rename(columns={'id': 'job_count', 'is_big_tech': 'big_tech_count'})
        
        # Calcular métricas adicionales
        time_series['big_tech_percentage'] = (time_series['big_tech_count'] / time_series['job_count']) * 100
        time_series['cumulative_jobs'] = time_series['job_count'].cumsum()
        
        # Rellenar valores nulos
        time_series = time_series.fillna(0)
        
        return time_series


def save_processed_data(df: pd.DataFrame, filename: str, output_dir: str = "data/processed"):
    """Guarda datos procesados"""
    import os
    
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, filename)
    
    df.to_csv(filepath, index=False, encoding='utf-8')
    logger.info(f"Datos procesados guardados: {filepath}")
    
    return filepath


def load_and_process_data(filepath: str) -> Tuple[pd.DataFrame, Dict]:
    """Carga y procesa datos desde un archivo CSV"""
    logger.info(f"Cargando datos desde: {filepath}")
    
    df = pd.read_csv(filepath)
    processor = JobDataProcessor(df)
    
    # Procesar datos
    cleaned_df = processor.clean_data()
    time_features_df = processor.create_time_features()
    
    # Obtener estadísticas
    stats = processor.get_summary_stats()
    
    return time_features_df, stats
