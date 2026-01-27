# etl/utils.py

"""
Utilitários para o Pipeline ETL
"""

import os
import sys
from pathlib import Path
from typing import Union, Optional, List
from datetime import datetime
import json

def get_file_size(file_path: Union[str, Path]) -> str:
    """
    Obter tamanho do arquivo em formato legível
    
    Args:
        file_path: Caminho do arquivo
        
    Returns:
        Tamanho formatado (ex: "1.5 MB")
    """
    file_path = Path(file_path)
    if not file_path.exists():
        return "0 B"
    
    size = file_path.stat().st_size
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024.0:
            return f"{size:.2f} {unit}"
        size /= 1024.0
    
    return f"{size:.2f} TB"

def get_file_info(file_path: Union[str, Path]) -> dict:
    """
    Obter informações sobre um arquivo
    
    Args:
        file_path: Caminho do arquivo
        
    Returns:
        Dicionário com informações do arquivo
    """
    file_path = Path(file_path)
    
    if not file_path.exists():
        return {"exists": False}
    
    stat = file_path.stat()
    return {
        "exists": True,
        "path": str(file_path),
        "name": file_path.name,
        "size": get_file_size(file_path),
        "size_bytes": stat.st_size,
        "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
        "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
        "is_file": file_path.is_file(),
        "is_dir": file_path.is_dir(),
    }

def ensure_directory(path: Union[str, Path]) -> Path:
    """
    Garantir que um diretório existe
    
    Args:
        path: Caminho do diretório
        
    Returns:
        Path do diretório
    """
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path

def get_platform_info() -> dict:
    """
    Obter informações sobre a plataforma
    
    Returns:
        Dicionário com informações da plataforma
    """
    return {
        "system": sys.platform,
        "python_version": sys.version,
        "is_windows": sys.platform.startswith('win'),
        "is_linux": sys.platform.startswith('linux'),
        "is_mac": sys.platform == 'darwin',
    }

def format_duration(seconds: float) -> str:
    """
    Formatar duração em segundos para formato legível
    
    Args:
        seconds: Duração em segundos
        
    Returns:
        Duração formatada (ex: "1h 30m 45s")
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    
    parts = []
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0:
        parts.append(f"{minutes}m")
    if secs > 0 or not parts:
        parts.append(f"{secs}s")
    
    return " ".join(parts)

def save_json(data: dict, file_path: Union[str, Path], pretty: bool = True) -> None:
    """
    Salvar dados em JSON
    
    Args:
        data: Dados para salvar
        file_path: Caminho do arquivo
        pretty: Se True, formata com indentação
    """
    file_path = Path(file_path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        indent = 2 if pretty else None
        json.dump(data, f, indent=indent, ensure_ascii=False)

def load_json(file_path: Union[str, Path]) -> dict:
    """
    Carregar dados de JSON
    
    Args:
        file_path: Caminho do arquivo
        
    Returns:
        Dados carregados
    """
    file_path = Path(file_path)
    
    if not file_path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def list_files(directory: Union[str, Path], extension: Optional[str] = None) -> List[Path]:
    """
    Listar arquivos em um diretório
    
    Args:
        directory: Caminho do diretório
        extension: Extensão para filtrar (ex: '.csv')
        
    Returns:
        Lista de caminhos de arquivos
    """
    directory = Path(directory)
    
    if not directory.exists():
        return []
    
    if extension:
        return sorted(directory.glob(f"*{extension}"))
    else:
        return sorted([f for f in directory.iterdir() if f.is_file()])

def get_memory_usage() -> dict:
    """
    Obter informações de uso de memória
    
    Returns:
        Dicionário com informações de memória
    """
    try:
        import psutil
        process = psutil.Process(os.getpid())
        memory_info = process.memory_info()
        
        return {
            "rss_mb": memory_info.rss / (1024 * 1024),
            "vms_mb": memory_info.vms / (1024 * 1024),
            "percent": process.memory_percent(),
        }
    except ImportError:
        return {"error": "psutil não está instalado"}
    except Exception as e:
        return {"error": str(e)}
