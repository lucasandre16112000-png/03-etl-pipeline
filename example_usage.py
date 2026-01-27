# example_usage.py

"""
Exemplo de uso do Pipeline ETL Profissional

Este script demonstra como usar o pipeline ETL para:
1. Extrair dados de um arquivo CSV
2. Transformar os dados
3. Carregar em múltiplos formatos
"""

import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta
import numpy as np
import sys
import os

# Adicionar diretório raiz ao path para imports
sys.path.insert(0, str(Path(__file__).parent))

from etl.pipeline import ETLPipeline
from etl.config.logger import setup_logger

logger = setup_logger(__name__)

def create_sample_data():
    """Criar dados de exemplo para demonstração"""
    np.random.seed(42)
    
    num_records = 100
    
    data = {
        'customer_id': list(range(1, num_records + 1)),
        'name': [f"Cliente {i}" for i in range(1, num_records + 1)],
        'email': [f"cliente{i}@example.com" for i in range(1, num_records + 1)],
        'age': np.random.randint(18, 80, num_records),
        'purchase_amount': np.random.uniform(10, 1000, num_records),
        'last_purchase': [
            (datetime.now() - timedelta(days=int(np.random.randint(0, 365)))).strftime("%Y-%m-%d")
            for _ in range(num_records)
        ],
        'status': np.random.choice(['active', 'inactive', 'pending'], num_records),
    }
    
    df = pd.DataFrame(data)
    
    # Adicionar alguns valores faltantes
    missing_indices = np.random.choice(num_records, int(num_records * 0.05), replace=False)
    for idx in missing_indices:
        df.loc[idx, 'email'] = None
    
    # Adicionar algumas duplicatas
    df = pd.concat([df, df.iloc[:5]], ignore_index=True)
    
    # Salvar em arquivo CSV
    input_file = Path("data/input/sample_data.csv")
    input_file.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(input_file, index=False)
    
    logger.info(f"✓ Dados de exemplo criados: {input_file}")
    return str(input_file)

def main():
    """Executar exemplo do pipeline"""
    logger.info("=" * 80)
    logger.info("EXEMPLO DE USO - PIPELINE ETL PROFISSIONAL")
    logger.info("=" * 80)
    
    try:
        # Criar dados de exemplo
        input_file = create_sample_data()
        
        # Inicializar pipeline
        pipeline = ETLPipeline()
        pipeline.run()
        
        # Executar transformações
        logger.info("\n📊 Iniciando transformações...")
        
        pipeline.extract(input_file) \
            .remove_duplicates() \
            .handle_missing_values(strategy="drop") \
            .rename_columns({
                'customer_id': 'id',
                'purchase_amount': 'amount',
                'last_purchase': 'last_purchase_date'
            }) \
            .filter_rows(lambda df: df['age'] >= 18) \
            .convert_types({
                'age': 'int',
                'amount': 'float'
            }) \
            .add_column('age_group', lambda row: 'Senior' if row['age'] >= 60 else 'Adult' if row['age'] >= 30 else 'Young') \
            .add_column('purchase_category', lambda row: 'High' if row['amount'] >= 500 else 'Medium' if row['amount'] >= 200 else 'Low')
        
        # Salvar resultados em múltiplos formatos
        logger.info("\n💾 Salvando resultados...")
        
        output_dir = Path("data/output")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        pipeline.load(str(output_dir / "processed_data.csv")) \
            .load(str(output_dir / "processed_data.json")) \
            .load(str(output_dir / "processed_data.xlsx"))
        
        # Exibir estatísticas
        logger.info("\n📈 Estatísticas do Pipeline:")
        stats = pipeline.get_stats()
        
        for key, value in stats.items():
            if key not in ['start_time', 'end_time']:
                logger.info(f"  {key}: {value}")
        
        # Salvar estatísticas
        pipeline.finish(execution_time=10.5)
        pipeline.save_stats(str(output_dir / "pipeline_stats.json"))
        
        # Exibir amostra dos dados processados
        logger.info("\n📋 Amostra dos dados processados:")
        logger.info(f"\nPrimeiras 5 linhas:")
        logger.info(pipeline.df.head().to_string())
        
        logger.info("\n" + "=" * 80)
        logger.info("✓ PIPELINE CONCLUÍDO COM SUCESSO!")
        logger.info("=" * 80)
        
        return 0
        
    except Exception as e:
        logger.error(f"✗ Erro durante execução: {str(e)}", exc_info=True)
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
