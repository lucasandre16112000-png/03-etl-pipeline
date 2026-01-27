# tests/test_validators.py

import pytest
from etl.validators.data_validator import DataValidator, ValidationResult

class TestDataValidator:
    """Testes para o validador de dados"""
    
    def test_validate_email_valid(self):
        """Testar validação de email válido"""
        assert DataValidator.validate_email("user@example.com") is True
        assert DataValidator.validate_email("test.user@domain.co.uk") is True
    
    def test_validate_email_invalid(self):
        """Testar validação de email inválido"""
        assert DataValidator.validate_email("invalid.email") is False
        assert DataValidator.validate_email("@example.com") is False
        assert DataValidator.validate_email("user@") is False
        assert DataValidator.validate_email(123) is False
    
    def test_validate_phone_valid(self):
        """Testar validação de telefone válido"""
        assert DataValidator.validate_phone("(11) 98765-4321") is True
        assert DataValidator.validate_phone("+55 11 98765-4321") is True
        assert DataValidator.validate_phone("11 98765 4321") is True
    
    def test_validate_phone_invalid(self):
        """Testar validação de telefone inválido"""
        assert DataValidator.validate_phone("123") is False
        assert DataValidator.validate_phone("abc") is False
        assert DataValidator.validate_phone(123) is False
    
    def test_validate_numeric_valid(self):
        """Testar validação de número válido"""
        assert DataValidator.validate_numeric(10) is True
        assert DataValidator.validate_numeric(10.5) is True
        assert DataValidator.validate_numeric("20") is True
    
    def test_validate_numeric_with_range(self):
        """Testar validação de número com range"""
        assert DataValidator.validate_numeric(50, min_val=0, max_val=100) is True
        assert DataValidator.validate_numeric(150, min_val=0, max_val=100) is False
        assert DataValidator.validate_numeric(-10, min_val=0, max_val=100) is False
    
    def test_validate_numeric_invalid(self):
        """Testar validação de número inválido"""
        assert DataValidator.validate_numeric("abc") is False
        assert DataValidator.validate_numeric(None) is False
    
    def test_validate_date_valid(self):
        """Testar validação de data válida"""
        assert DataValidator.validate_date("2025-12-12") is True
        assert DataValidator.validate_date("2025-01-01") is True
    
    def test_validate_date_invalid(self):
        """Testar validação de data inválida"""
        assert DataValidator.validate_date("2025-13-01") is False
        assert DataValidator.validate_date("invalid-date") is False
        assert DataValidator.validate_date(123) is False
    
    def test_validate_date_custom_format(self):
        """Testar validação de data com formato customizado"""
        assert DataValidator.validate_date("12/12/2025", "%d/%m/%Y") is True
        assert DataValidator.validate_date("2025-12-12", "%d/%m/%Y") is False
    
    def test_validate_string_length_valid(self):
        """Testar validação de comprimento de string"""
        assert DataValidator.validate_string_length("hello", min_length=1, max_length=10) is True
        assert DataValidator.validate_string_length("hi", min_length=2) is True
    
    def test_validate_string_length_invalid(self):
        """Testar validação de comprimento de string inválido"""
        assert DataValidator.validate_string_length("hi", min_length=3) is False
        assert DataValidator.validate_string_length("hello", max_length=3) is False
        assert DataValidator.validate_string_length(123, min_length=1) is False
    
    def test_validate_in_list_valid(self):
        """Testar validação de valor em lista"""
        assert DataValidator.validate_in_list("active", ["active", "inactive", "pending"]) is True
        assert DataValidator.validate_in_list(1, [1, 2, 3]) is True
    
    def test_validate_in_list_invalid(self):
        """Testar validação de valor não em lista"""
        assert DataValidator.validate_in_list("unknown", ["active", "inactive"]) is False
        assert DataValidator.validate_in_list(4, [1, 2, 3]) is False
    
    def test_validate_row_valid(self):
        """Testar validação de linha válida"""
        schema = {
            "email": {"type": str, "email": True},
            "age": {"type": int, "numeric": True, "min": 0, "max": 150}
        }
        row = {"email": "user@example.com", "age": 25}
        result = DataValidator.validate_row(row, schema)
        
        assert result.is_valid is True
        assert len(result.errors) == 0
    
    def test_validate_row_missing_field(self):
        """Testar validação de linha com campo faltante"""
        schema = {
            "email": {"type": str, "email": True},
            "age": {"type": int}
        }
        row = {"email": "user@example.com"}
        result = DataValidator.validate_row(row, schema)
        
        assert result.is_valid is False
        assert len(result.errors) > 0
    
    def test_validate_row_invalid_email(self):
        """Testar validação de linha com email inválido"""
        schema = {
            "email": {"type": str, "email": True}
        }
        row = {"email": "invalid.email"}
        result = DataValidator.validate_row(row, schema)
        
        assert result.is_valid is False
        assert len(result.errors) > 0
