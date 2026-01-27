# etl/profiler.py

"""
Módulo de profiling e monitoramento de performance
"""

import time
from functools import wraps
from typing import Callable, Any
from datetime import datetime
from .config.logger import setup_logger

logger = setup_logger(__name__)

class PerformanceMonitor:
    """Monitor de performance para operações"""
    
    def __init__(self):
        self.measurements = {}
        self.start_time = None
    
    def start(self) -> None:
        """Iniciar medição"""
        self.start_time = time.time()
    
    def stop(self, operation_name: str) -> float:
        """
        Parar medição
        
        Args:
            operation_name: Nome da operação
            
        Returns:
            Tempo decorrido em segundos
        """
        if self.start_time is None:
            logger.warning("Monitor não foi iniciado")
            return 0.0
        
        elapsed = time.time() - self.start_time
        self.measurements[operation_name] = elapsed
        
        logger.info(f"⏱️  {operation_name}: {elapsed:.4f}s")
        return elapsed
    
    def get_measurements(self) -> dict:
        """Obter todas as medições"""
        return self.measurements.copy()
    
    def reset(self) -> None:
        """Resetar medições"""
        self.measurements.clear()
        self.start_time = None

def measure_time(func: Callable) -> Callable:
    """
    Decorator para medir tempo de execução
    
    Args:
        func: Função a medir
        
    Returns:
        Função decorada
    """
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        start = time.time()
        try:
            result = func(*args, **kwargs)
            elapsed = time.time() - start
            logger.info(f"⏱️  {func.__name__}: {elapsed:.4f}s")
            return result
        except Exception as e:
            elapsed = time.time() - start
            logger.error(f"✗ {func.__name__} falhou após {elapsed:.4f}s: {str(e)}")
            raise
    
    return wrapper

class Timer:
    """Context manager para medir tempo de bloco de código"""
    
    def __init__(self, name: str = "Operação"):
        self.name = name
        self.start_time = None
        self.elapsed = 0.0
    
    def __enter__(self):
        self.start_time = time.time()
        logger.info(f"⏱️  Iniciando: {self.name}")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.elapsed = time.time() - self.start_time
        
        if exc_type is None:
            logger.info(f"✓ {self.name} concluído em {self.elapsed:.4f}s")
        else:
            logger.error(f"✗ {self.name} falhou após {self.elapsed:.4f}s")
        
        return False
