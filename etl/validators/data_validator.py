# etl/validators/data_validator.py

import re
from datetime import datetime
from typing import Any, Optional, List
from dataclasses import dataclass
from ..config.logger import setup_logger

logger = setup_logger(__name__)

@dataclass
class ValidationResult:
    """Resultado de validação"""
    is_valid: bool
    errors: List[str]
    warnings: List[str]

class DataValidator:
    """Validador de dados profissional"""
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Validar formato de email"""
        if not isinstance(email, str):
            return False
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def validate_phone(phone: str) -> bool:
        """Validar formato de telefone"""
        if not isinstance(phone, str):
            return False
        pattern = r'^[\d\s\-\+\(\)]{10,}$'
        return re.match(pattern, str(phone)) is not None
    
    @staticmethod
    def validate_numeric(value: Any, min_val: Optional[float] = None, max_val: Optional[float] = None) -> bool:
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
        if not isinstance(date_str, str):
            return False
        try:
            datetime.strptime(date_str, format)
            return True
        except (ValueError, TypeError):
            return False
    
    @staticmethod
    def validate_string_length(value: str, min_length: int = 0, max_length: Optional[int] = None) -> bool:
        """Validar comprimento de string"""
        if not isinstance(value, str):
            return False
        if len(value) < min_length:
            return False
        if max_length is not None and len(value) > max_length:
            return False
        return True
    
    @staticmethod
    def validate_in_list(value: Any, allowed_values: List[Any]) -> bool:
        """Validar se valor está em lista de valores permitidos"""
        return value in allowed_values
    
    @classmethod
    def validate_row(cls, row: dict, schema: dict) -> ValidationResult:
        """
        Validar uma linha de dados contra um schema
        
        Args:
            row: Linha de dados
            schema: Schema de validação
            
        Returns:
            ValidationResult com resultado da validação
        """
        errors = []
        warnings = []
        
        for field, rules in schema.items():
            if field not in row:
                errors.append(f"Campo obrigatório ausente: {field}")
                continue
            
            value = row[field]
            
            # Validar tipo
            if "type" in rules:
                expected_type = rules["type"]
                if not isinstance(value, expected_type):
                    errors.append(f"Campo {field}: tipo esperado {expected_type}, recebido {type(value)}")
            
            # Validar email
            if rules.get("email") and not cls.validate_email(str(value)):
                errors.append(f"Campo {field}: email inválido")
            
            # Validar numérico
            if rules.get("numeric"):
                min_val = rules.get("min")
                max_val = rules.get("max")
                if not cls.validate_numeric(value, min_val, max_val):
                    errors.append(f"Campo {field}: valor numérico inválido")
            
            # Validar data
            if rules.get("date"):
                date_format = rules.get("date_format", "%Y-%m-%d")
                if not cls.validate_date(str(value), date_format):
                    errors.append(f"Campo {field}: data inválida (formato esperado: {date_format})")
        
        is_valid = len(errors) == 0
        return ValidationResult(is_valid=is_valid, errors=errors, warnings=warnings)
