"""
Script principal para ejecutar el scraping y análisis inicial de empleos Big Tech en Jalisco
"""

import os
import sys
import pandas as pd
from datetime import datetime
import logging

# Agregar el directorio src al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.scraper import AdzunaJobScraper
from src.data_processor import JobDataProcessor, save_processed_data, load_and_process_data

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('jalisco_bigtech_analysis.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def main():
    """Función principal que ejecuta todo el pipeline"""
    print("🚀 ANÁLISIS DE EMPLEOS BIG TECH EN JALISCO")
    print("=" * 50)
    
    try:
        # Paso 1: Scraping de datos
        print("\n📡 PASO 1: Extrayendo datos de empleos...")
        scraper = AdzunaJobScraper()
        raw_df = scraper.scrape_big_tech_jobs_jalisco()
        
        if raw_df.empty:
            print("❌ No se pudieron extraer datos. Verifica la configuración de la API.")
            return
        
        # Guardar datos raw
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        raw_filename = f"jalisco_bigtech_jobs_raw_{timestamp}.csv"
        raw_filepath = scraper.save_data(raw_df, raw_filename)
        
        print(f"✅ Datos extraídos exitosamente: {len(raw_df)} empleos")
        
        # Paso 2: Procesamiento de datos
        print("\n🔧 PASO 2: Procesando y limpiando datos...")
        processor = JobDataProcessor(raw_df)
        
        # Limpiar datos
        cleaned_df = processor.clean_data()
        
        # Crear características temporales
        processed_df = processor.create_time_features()
        
        # Preparar para modelado
        model_ready_df, encoders = processor.prepare_for_modeling()
        
        # Guardar datos procesados
        processed_filename = f"jalisco_bigtech_jobs_processed_{timestamp}.csv"
        processed_filepath = save_processed_data(processed_df, processed_filename)
        
        model_ready_filename = f"jalisco_bigtech_jobs_model_ready_{timestamp}.csv"
        model_ready_filepath = save_processed_data(model_ready_df, model_ready_filename)
        
        print(f"✅ Datos procesados exitosamente")
        
        # Paso 3: Análisis inicial
        print("\n📊 PASO 3: Generando estadísticas iniciales...")
        stats = processor.get_summary_stats()
        
        # Mostrar resumen detallado
        print("\n" + "="*60)
        print("📈 RESUMEN ESTADÍSTICO DEL DATASET")
        print("="*60)
        print(f"📊 Total de empleos analizados: {stats['total_jobs']:,}")
        print(f"🏢 Empresas únicas: {stats['unique_companies']:,}")
        print(f"🌍 Ubicaciones únicas: {stats['unique_locations']:,}")
        print(f"🏆 Empleos Big Tech: {stats['big_tech_jobs']:,} ({stats['big_tech_percentage']:.1f}%)")
        print(f"💰 Empleos con información salarial: {stats['jobs_with_salary']:,}")
        
        if stats['avg_salary'] > 0:
            print(f"💵 Salario promedio: ${stats['avg_salary']:,.0f}")
            print(f"💵 Salario mediano: ${stats['median_salary']:,.0f}")
        
        if stats['date_range']['start']:
            print(f"📅 Rango de fechas: {stats['date_range']['start'].date()} a {stats['date_range']['end'].date()}")
        
        # Análisis por empresas
        print(f"\n🔝 TOP 10 EMPRESAS CON MÁS OFERTAS:")
        if len(processed_df) > 0:
            top_companies = processed_df['company'].value_counts().head(10)
            for i, (company, count) in enumerate(top_companies.items(), 1):
                emoji = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i:2d}."
                print(f"   {emoji} {company}: {count} ofertas")
        
        # Análisis por ubicaciones
        print(f"\n🌍 DISTRIBUCIÓN POR UBICACIONES:")
        if len(processed_df) > 0:
            top_locations = processed_df['location'].value_counts().head(5)
            for location, count in top_locations.items():
                percentage = (count / len(processed_df)) * 100
                print(f"   📍 {location}: {count} empleos ({percentage:.1f}%)")
        
        # Análisis de niveles de experiencia
        if 'experience_level' in processed_df.columns:
            print(f"\n🎯 DISTRIBUCIÓN POR NIVEL DE EXPERIENCIA:")
            exp_levels = processed_df['experience_level'].value_counts()
            for level, count in exp_levels.items():
                percentage = (count / len(processed_df)) * 100
                print(f"   👨‍💻 {level}: {count} empleos ({percentage:.1f}%)")
        
        # Tecnologías más demandadas
        print(f"\n💻 TECNOLOGÍAS MÁS MENCIONADAS:")
        tech_columns = [col for col in processed_df.columns if col.startswith('mentions_')]
        if tech_columns:
            tech_counts = {}
            for col in tech_columns:
                tech_name = col.replace('mentions_', '').replace('_', ' ').title()
                tech_counts[tech_name] = processed_df[col].sum()
            
            # Ordenar por frecuencia
            sorted_tech = sorted(tech_counts.items(), key=lambda x: x[1], reverse=True)
            for tech, count in sorted_tech[:10]:
                if count > 0:
                    percentage = (count / len(processed_df)) * 100
                    print(f"   ⚡ {tech}: {count} menciones ({percentage:.1f}%)")
        
        # Series de tiempo básicas
        print(f"\n📈 CREANDO DATOS PARA ANÁLISIS TEMPORAL...")
        time_series_daily = processor.create_time_series_data('D')
        time_series_weekly = processor.create_time_series_data('W')
        
        # Guardar series de tiempo
        if not time_series_daily.empty:
            ts_daily_filename = f"jalisco_bigtech_timeseries_daily_{timestamp}.csv"
            save_processed_data(time_series_daily, ts_daily_filename)
            print(f"✅ Series de tiempo diarias guardadas")
        
        if not time_series_weekly.empty:
            ts_weekly_filename = f"jalisco_bigtech_timeseries_weekly_{timestamp}.csv"
            save_processed_data(time_series_weekly, ts_weekly_filename)
            print(f"✅ Series de tiempo semanales guardadas")
        
        # Resumen final
        print("\n" + "="*60)
        print("🎉 PIPELINE DE SCRAPING COMPLETADO EXITOSAMENTE")
        print("="*60)
        print("📁 Archivos generados:")
        print(f"   📄 Datos raw: {raw_filepath}")
        print(f"   📄 Datos procesados: {processed_filepath}")
        print(f"   📄 Datos para ML: {model_ready_filepath}")
        if not time_series_daily.empty:
            print(f"   📄 Series de tiempo: data/processed/jalisco_bigtech_timeseries_*.csv")
        
        print(f"\n🔄 Próximos pasos recomendados:")
        print(f"   1. 📊 Ejecutar análisis exploratorio completo (EDA)")
        print(f"   2. 🔍 Aplicar técnicas de reducción de dimensionalidad")
        print(f"   3. 📈 Implementar modelos de series de tiempo")
        print(f"   4. 🤖 Desarrollar modelos predictivos")
        print(f"   5. 📋 Generar visualizaciones para el informe")
        
        return processed_df, stats
        
    except Exception as e:
        logger.error(f"Error en el pipeline principal: {e}")
        print(f"❌ Error durante la ejecución: {e}")
        return None, None


def quick_analysis(filepath: str = None):
    """Análisis rápido de datos ya extraídos"""
    if filepath is None:
        # Buscar el archivo más reciente
        data_dir = "data/raw"
        if os.path.exists(data_dir):
            files = [f for f in os.listdir(data_dir) if f.endswith('.csv')]
            if files:
                files.sort(reverse=True)
                filepath = os.path.join(data_dir, files[0])
            else:
                print("❌ No se encontraron archivos de datos.")
                return
        else:
            print("❌ Directorio de datos no encontrado.")
            return
    
    print(f"📊 Analizando datos desde: {filepath}")
    
    try:
        processed_df, stats = load_and_process_data(filepath)
        print("✅ Análisis completado")
        return processed_df, stats
    except Exception as e:
        print(f"❌ Error durante el análisis: {e}")
        return None, None


if __name__ == "__main__":
    # Verificar argumentos de línea de comandos
    if len(sys.argv) > 1 and sys.argv[1] == "analyze":
        # Solo análisis de datos existentes
        filepath = sys.argv[2] if len(sys.argv) > 2 else None
        quick_analysis(filepath)
    else:
        # Pipeline completo de scraping y análisis
        main()
