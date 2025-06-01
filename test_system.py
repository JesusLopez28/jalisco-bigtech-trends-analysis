"""
Script de prueba rápida del sistema de scraping
Extrae una muestra pequeña de datos para verificar que todo funciona correctamente
"""

import sys
import os
sys.path.append('src')

from src.scraper import AdzunaJobScraper
from src.data_processor import JobDataProcessor

def test_scraping():
    """Prueba rápida del sistema de scraping"""
    print("🧪 PRUEBA RÁPIDA DEL SISTEMA DE SCRAPING")
    print("=" * 50)
    
    try:
        # Inicializar scraper
        scraper = AdzunaJobScraper()
        print("✅ Scraper inicializado correctamente")
        
        # Hacer una búsqueda pequeña de prueba
        print("\n🔍 Realizando búsqueda de prueba...")
        test_jobs = scraper.search_jobs(what="software", where="Guadalajara", max_pages=1)
        
        if test_jobs:
            print(f"✅ Búsqueda exitosa: {len(test_jobs)} empleos encontrados")
            
            # Procesar algunos empleos
            processed_jobs = []
            for job in test_jobs[:5]:  # Solo los primeros 5
                job_details = scraper.extract_job_details(job)
                if job_details:
                    processed_jobs.append(job_details)
            
            print(f"✅ Procesamiento exitoso: {len(processed_jobs)} empleos procesados")
            
            # Mostrar ejemplo
            if processed_jobs:
                example_job = processed_jobs[0]
                print(f"\n📋 Ejemplo de empleo extraído:")
                print(f"   🏢 Empresa: {example_job.get('company', 'N/A')}")
                print(f"   💼 Título: {example_job.get('title', 'N/A')}")
                print(f"   📍 Ubicación: {example_job.get('location', 'N/A')}")
                print(f"   🏆 Big Tech: {example_job.get('is_big_tech', False)}")
                print(f"   🔧 Keywords tech: {example_job.get('tech_keywords_count', 0)}")
            
            print("\n🎉 ¡Sistema funcionando correctamente!")
            return True
            
        else:
            print("❌ No se encontraron empleos en la búsqueda de prueba")
            return False
            
    except Exception as e:
        print(f"❌ Error durante la prueba: {e}")
        return False

def check_dependencies():
    """Verifica que todas las dependencias estén instaladas"""
    print("📦 VERIFICANDO DEPENDENCIAS")
    print("=" * 30)
    
    dependencies = [
        'requests', 'pandas', 'numpy', 'matplotlib', 
        'seaborn', 'scikit-learn', 'plotly'
    ]
    
    missing = []
    
    for dep in dependencies:
        try:
            __import__(dep)
            print(f"✅ {dep}")
        except ImportError:
            print(f"❌ {dep}")
            missing.append(dep)
    
    if missing:
        print(f"\n⚠️  Dependencias faltantes: {', '.join(missing)}")
        print("💡 Instalar con: pip install " + " ".join(missing))
        return False
    else:
        print("\n🎉 Todas las dependencias están instaladas")
        return True

def check_api_config():
    """Verifica la configuración de la API"""
    print("\n🔑 VERIFICANDO CONFIGURACIÓN DE API")
    print("=" * 35)
    
    try:
        from src.config import ADZUNA_APP_ID, ADZUNA_API_KEY
        
        if ADZUNA_APP_ID and ADZUNA_API_KEY:
            print(f"✅ App ID configurado: {ADZUNA_APP_ID}")
            print(f"✅ API Key configurado: {ADZUNA_API_KEY[:8]}...")
            return True
        else:
            print("❌ Credenciales de API no configuradas")
            print("💡 Verificar archivo .env o src/config.py")
            return False
            
    except ImportError as e:
        print(f"❌ Error importando configuración: {e}")
        return False

def main():
    """Función principal de prueba"""
    print("🚀 SISTEMA DE ANÁLISIS DE EMPLEOS BIG TECH JALISCO")
    print("🧪 MODO DE PRUEBA")
    print("=" * 60)
    
    # Verificar dependencias
    deps_ok = check_dependencies()
    
    # Verificar configuración API
    api_ok = check_api_config()
    
    # Si todo está bien, hacer prueba de scraping
    if deps_ok and api_ok:
        print("\n" + "=" * 60)
        test_ok = test_scraping()
        
        print("\n" + "=" * 60)
        print("📋 RESUMEN DE PRUEBAS")
        print("=" * 20)
        print(f"📦 Dependencias: {'✅ OK' if deps_ok else '❌ ERROR'}")
        print(f"🔑 Configuración API: {'✅ OK' if api_ok else '❌ ERROR'}")
        print(f"🔍 Scraping: {'✅ OK' if test_ok else '❌ ERROR'}")
        
        if deps_ok and api_ok and test_ok:
            print("\n🎉 ¡SISTEMA LISTO PARA USO COMPLETO!")
            print("💡 Ejecutar: python main.py")
        else:
            print("\n⚠️  Hay problemas que resolver antes del uso completo")
            
    else:
        print("\n❌ Resolver problemas de configuración antes de continuar")

if __name__ == "__main__":
    main()
