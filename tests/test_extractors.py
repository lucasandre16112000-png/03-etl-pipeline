# tests/test_extractors.py

import pytest
import pandas as pd
import json
from pathlib import Path
import tempfile
from etl.extractors.data_extractor import DataExtractor

@pytest.fixture
def sample_csv_file():
    """Criar arquivo CSV de exemplo"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        f.write("id,name,email\n")
        f.write("1,John,john@example.com\n")
        f.write("2,Jane,jane@example.com\n")
        f.write("3,Bob,bob@example.com\n")
        return f.name

@pytest.fixture
def sample_json_file():
    """Criar arquivo JSON de exemplo"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        data = [
            {"id": 1, "name": "John", "email": "john@example.com"},
            {"id": 2, "name": "Jane", "email": "jane@example.com"},
            {"id": 3, "name": "Bob", "email": "bob@example.com"}
        ]
        json.dump(data, f)
        return f.name

class TestDataExtractor:
    """Testes para o extrator de dados"""
    
    def test_extract_csv(self, sample_csv_file):
        """Testar extração de CSV"""
        df = DataExtractor.extract_csv(sample_csv_file)
        
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 3
        assert list(df.columns) == ["id", "name", "email"]
    
    def test_extract_json(self, sample_json_file):
        """Testar extração de JSON"""
        df = DataExtractor.extract_json(sample_json_file)
        
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 3
        assert "id" in df.columns
    
    def test_extract_auto_detect_csv(self, sample_csv_file):
        """Testar extração com detecção automática de tipo (CSV)"""
        df = DataExtractor.extract(sample_csv_file)
        
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 3
    
    def test_extract_auto_detect_json(self, sample_json_file):
        """Testar extração com detecção automática de tipo (JSON)"""
        df = DataExtractor.extract(sample_json_file)
        
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 3
    
    def test_extract_explicit_type(self, sample_csv_file):
        """Testar extração com tipo explícito"""
        df = DataExtractor.extract(sample_csv_file, file_type="csv")
        
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 3
    
    def test_extract_invalid_file(self):
        """Testar extração de arquivo inexistente"""
        with pytest.raises(Exception):
            DataExtractor.extract("nonexistent_file.csv")
    
    def test_extract_unsupported_format(self, sample_csv_file):
        """Testar extração de formato não suportado"""
        with pytest.raises(ValueError):
            DataExtractor.extract(sample_csv_file, file_type="unsupported")
