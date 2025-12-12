"""
Pipeline ETL Profissional com Pandas e Validação de Dados
Exemplo de automação de dados com transformação, validação e relatórios.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import logging
from dataclasses import dataclass
import json

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class PipelineStats:
    """Estatísticas do pipeline"""
    total_records: int = 0
    valid_records: int = 0
    invalid_records: int = 0
    duplicates_removed: int = 0
    missing_values_handled: int = 0
    transformations_applied: int = 0
    execution_time: float = 0.0


class DataValidator:
    """Validador de dados"""
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Validar formato de email"""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def validate_phone(phone: str) -> bool:
        """Validar formato de telefone"""
        import re
        pattern = r'^[\d\s\-\+\(\)]{10,}$'
        return re.match(pattern, str(phone)) is not None
    
    @staticmethod
    def validate_numeric(value, min_val=None, max_val=None) -> bool:
        """Validar valor numérico dentro de range"""
        try:
            num = float(value)
            if min_val is not None and num < min_val:
                return False
            if max_val is not None and num > max_val:
                return False
            return True
        except (ValueError, TypeError):
            return False
    
    @staticmethod
    def validate_date(date_str: str, format: str = "%Y-%m-%d") -> bool:
        """Validar formato de data"""
        try:
            datetime.strptime(date_str, format)
            return True
        except (ValueError, TypeError):
            return False


class ETLPipeline:
    """Pipeline ETL profissional"""
    
    def __init__(self):
        self.stats = PipelineStats()
        self.validator = DataValidator()
        self.df = None
        self.validation_errors = []
    
    def extract(self, source: str, file_type: str = "csv") -> pd.DataFrame:
        """
        Extrair dados de diferentes fontes
        
        Args:
            source: Caminho do arquivo ou URL
            file_type: Tipo de arquivo (csv, json, excel)
        """
        logger.info(f"Extraindo dados de {source}...")
        
        try:
            if file_type == "csv":
                self.df = pd.read_csv(source)
            elif file_type == "json":
                self.df = pd.read_json(source)
            elif file_type == "excel":
                self.df = pd.read_excel(source)
            else:
                raise ValueError(f"Tipo de arquivo não suportado: {file_type}")
            
            self.stats.total_records = len(self.df)
            logger.info(f"✓ Extraído {self.stats.total_records} registros")
            
            return self.df
            
        except Exception as e:
            logger.error(f"Erro ao extrair dados: {str(e)}")
            raise
    
    def generate_sample_data(self, num_records: int = 1000) -> pd.DataFrame:
        """Gerar dados de exemplo para demonstração"""
        logger.info(f"Gerando {num_records} registros de exemplo...")
        
        np.random.seed(42)
        
        data = {
            'customer_id': list(range(1, num_records + 1)),
            'name': [f"Cliente {i}" for i in range(1, num_records + 1)],
            'email': [f"cliente{i}@example.com" for i in range(1, num_records + 1)],
            'phone': [f"(11) 9{np.random.randint(10000000, 99999999)}" for _ in range(num_records)],
            'age': [int(x) for x in np.random.randint(18, 80, num_records)],
            'purchase_amount': list(np.random.uniform(10, 1000, num_records)),
            'last_purchase': [
                (datetime.now() - timedelta(days=int(np.random.randint(0, 365)))).strftime("%Y-%m-%d")
                for _ in range(num_records)
            ],
            'status': list(np.random.choice(['active', 'inactive', 'pending'], num_records)),
            'registration_date': [
                (datetime.now() - timedelta(days=int(np.random.randint(0, 730)))).strftime("%Y-%m-%d")
                for _ in range(num_records)
            ]
        }
        
        # Converter para DataFrame primeiro e depois adicionar valores faltantes
        df_temp = pd.DataFrame(data)
        
        # Adicionar alguns valores faltantes propositalmente
        for col in ['email', 'phone', 'age']:
            missing_indices = np.random.choice(num_records, int(num_records * 0.05), replace=False)
            for idx in missing_indices:
                df_temp.loc[idx, col] = np.nan
        
        data = df_temp.to_dict('list')
        
        self.df = pd.DataFrame(data)
        self.stats.total_records = len(self.df)
        
        logger.info(f"✓ Gerado {self.stats.total_records} registros")
        return self.df
    
    def clean(self) -> pd.DataFrame:
        """Limpeza de dados"""
        logger.info("Iniciando limpeza de dados...")
        
        if self.df is None:
            raise ValueError("Nenhum dado para limpar. Execute extract() primeiro.")
        
        initial_count = len(self.df)
        
        # Remover duplicatas
        duplicates = self.df.duplicated().sum()
        self.df = self.df.drop_duplicates()
        self.stats.duplicates_removed = duplicates
        logger.info(f"  - Removidas {duplicates} duplicatas")
        
        # Tratar valores faltantes
        for col in self.df.columns:
            missing = self.df[col].isna().sum()
            if missing > 0:
                if self.df[col].dtype in ['float64', 'int64']:
                    self.df[col].fillna(self.df[col].median(), inplace=True)
                else:
                    self.df[col].fillna("N/A", inplace=True)
                self.stats.missing_values_handled += missing
        
        logger.info(f"  - Tratados {self.stats.missing_values_handled} valores faltantes")
        logger.info(f"✓ Limpeza concluída ({len(self.df)} registros restantes)")
        
        return self.df
    
    def validate(self) -> Tuple[pd.DataFrame, List[Dict]]:
        """Validar dados"""
        logger.info("Iniciando validação de dados...")
        
        if self.df is None:
            raise ValueError("Nenhum dado para validar. Execute extract() primeiro.")
        
        validation_errors = []
        valid_rows = []
        
        for idx, row in self.df.iterrows():
            row_errors = []
            
            # Validar email se existir
            if 'email' in self.df.columns and pd.notna(row['email']):
                if not self.validator.validate_email(str(row['email'])):
                    row_errors.append(f"Email inválido: {row['email']}")
            
            # Validar telefone se existir
            if 'phone' in self.df.columns and pd.notna(row['phone']):
                if not self.validator.validate_phone(str(row['phone'])):
                    row_errors.append(f"Telefone inválido: {row['phone']}")
            
            # Validar idade se existir
            if 'age' in self.df.columns and pd.notna(row['age']):
                if not self.validator.validate_numeric(row['age'], 0, 150):
                    row_errors.append(f"Idade inválida: {row['age']}")
            
            # Validar valor de compra se existir
            if 'purchase_amount' in self.df.columns and pd.notna(row['purchase_amount']):
                if not self.validator.validate_numeric(row['purchase_amount'], 0):
                    row_errors.append(f"Valor de compra inválido: {row['purchase_amount']}")
            
            if row_errors:
                validation_errors.append({
                    'row_index': idx,
                    'errors': row_errors
                })
            else:
                valid_rows.append(idx)
        
        self.stats.valid_records = len(valid_rows)
        self.stats.invalid_records = len(validation_errors)
        
        logger.info(f"  - Registros válidos: {self.stats.valid_records}")
        logger.info(f"  - Registros inválidos: {self.stats.invalid_records}")
        logger.info(f"✓ Validação concluída")
        
        return self.df.iloc[valid_rows], validation_errors
    
    def transform(self) -> pd.DataFrame:
        """Transformar dados"""
        logger.info("Iniciando transformação de dados...")
        
        if self.df is None:
            raise ValueError("Nenhum dado para transformar. Execute extract() primeiro.")
        
        # Converter tipos de dados
        if 'age' in self.df.columns:
            self.df['age'] = pd.to_numeric(self.df['age'], errors='coerce')
            self.stats.transformations_applied += 1
        
        if 'purchase_amount' in self.df.columns:
            self.df['purchase_amount'] = pd.to_numeric(self.df['purchase_amount'], errors='coerce')
            self.stats.transformations_applied += 1
        
        # Converter datas
        date_columns = [col for col in self.df.columns if 'date' in col.lower()]
        for col in date_columns:
            self.df[col] = pd.to_datetime(self.df[col], errors='coerce')
            self.stats.transformations_applied += 1
        
        # Criar novas colunas derivadas
        if 'age' in self.df.columns:
            self.df['age_group'] = pd.cut(
                self.df['age'],
                bins=[0, 25, 35, 50, 65, 150],
                labels=['18-25', '26-35', '36-50', '51-65', '65+']
            )
            self.stats.transformations_applied += 1
        
        if 'purchase_amount' in self.df.columns:
            self.df['purchase_category'] = pd.cut(
                self.df['purchase_amount'],
                bins=[0, 100, 500, 1000],
                labels=['Baixo', 'Médio', 'Alto']
            )
            self.stats.transformations_applied += 1
        
        # Normalizar nomes de colunas
        self.df.columns = self.df.columns.str.lower().str.replace(' ', '_')
        
        logger.info(f"✓ Transformação concluída ({self.stats.transformations_applied} transformações)")
        
        return self.df
    
    def load(self, destination: str, file_type: str = "csv") -> None:
        """Carregar dados para destino"""
        logger.info(f"Carregando dados para {destination}...")
        
        if self.df is None:
            raise ValueError("Nenhum dado para carregar. Execute extract() primeiro.")
        
        try:
            if file_type == "csv":
                self.df.to_csv(destination, index=False)
            elif file_type == "json":
                self.df.to_json(destination, orient='records', indent=2)
            elif file_type == "excel":
                self.df.to_excel(destination, index=False)
            else:
                raise ValueError(f"Tipo de arquivo não suportado: {file_type}")
            
            logger.info(f"✓ Dados carregados com sucesso")
            
        except Exception as e:
            logger.error(f"Erro ao carregar dados: {str(e)}")
            raise
    
    def get_statistics(self) -> Dict:
        """Obter estatísticas do pipeline"""
        if self.df is None:
            return {}
        
        data_types_dict = {str(k): str(v) for k, v in self.df.dtypes.to_dict().items()}
        
        stats = {
            'total_records': int(self.stats.total_records),
            'valid_records': int(self.stats.valid_records),
            'invalid_records': int(self.stats.invalid_records),
            'duplicates_removed': int(self.stats.duplicates_removed),
            'missing_values_handled': int(self.stats.missing_values_handled),
            'transformations_applied': int(self.stats.transformations_applied),
            'columns': list(self.df.columns),
            'data_types': data_types_dict,
            'shape': tuple(int(x) for x in self.df.shape),
            'memory_usage_mb': float(self.df.memory_usage(deep=True).sum() / 1024 / 1024)
        }
        
        return stats


# ============================================================================
# EXEMPLO DE USO
# ============================================================================

def main():
    """Exemplo de uso do pipeline ETL"""
    
    print("=" * 80)
    print("PIPELINE ETL PROFISSIONAL - EXEMPLO DE USO")
    print("=" * 80)
    
    start_time = datetime.now()
    
    # Criar pipeline
    pipeline = ETLPipeline()
    
    # Gerar dados de exemplo
    print("\n📊 FASE 1: EXTRAÇÃO")
    print("-" * 80)
    pipeline.generate_sample_data(1000)
    
    # Limpar dados
    print("\n🧹 FASE 2: LIMPEZA")
    print("-" * 80)
    pipeline.clean()
    
    # Validar dados
    print("\n✓ FASE 3: VALIDAÇÃO")
    print("-" * 80)
    valid_df, errors = pipeline.validate()
    if errors:
        print(f"⚠️  Encontrados {len(errors)} erros de validação")
        for error in errors[:5]:  # Mostrar primeiros 5 erros
            print(f"   Linha {error['row_index']}: {error['errors']}")
    
    # Transformar dados
    print("\n🔄 FASE 4: TRANSFORMAÇÃO")
    print("-" * 80)
    pipeline.transform()
    
    # Carregar dados
    print("\n💾 FASE 5: CARREGAMENTO")
    print("-" * 80)
    pipeline.load("processed_data.csv", "csv")
    pipeline.load("processed_data.json", "json")
    
    # Exibir estatísticas
    end_time = datetime.now()
    execution_time = (end_time - start_time).total_seconds()
    
    print("\n" + "=" * 80)
    print("ESTATÍSTICAS DO PIPELINE")
    print("=" * 80)
    
    stats = pipeline.get_statistics()
    stats['execution_time'] = execution_time
    
    print(f"Total de registros: {stats['total_records']}")
    print(f"Registros válidos: {stats['valid_records']}")
    print(f"Registros inválidos: {stats['invalid_records']}")
    print(f"Duplicatas removidas: {stats['duplicates_removed']}")
    print(f"Valores faltantes tratados: {stats['missing_values_handled']}")
    print(f"Transformações aplicadas: {stats['transformations_applied']}")
    print(f"Dimensão final: {stats['shape']}")
    print(f"Memória utilizada: {stats['memory_usage_mb']:.2f} MB")
    print(f"Tempo de execução: {execution_time:.2f}s")
    
    # Exibir amostra de dados
    print("\n" + "=" * 80)
    print("AMOSTRA DE DADOS PROCESSADOS")
    print("=" * 80)
    print(pipeline.df.head(10).to_string())
    
    # Salvar estatísticas
    # Converter tipos numpy para tipos Python padrão
    stats_serializable = {
        k: int(v) if isinstance(v, (np.integer, np.int64)) else v
        for k, v in stats.items()
    }
    with open("pipeline_statistics.json", "w", encoding="utf-8") as f:
        json.dump(stats_serializable, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Pipeline concluído com sucesso!")
    print(f"📁 Arquivos gerados:")
    print(f"   - processed_data.csv")
    print(f"   - processed_data.json")
    print(f"   - pipeline_statistics.json")


if __name__ == "__main__":
    main()
