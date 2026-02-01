# src/backend/etl/utils/core.py
import os
import logging
from datetime import datetime

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
RAW_DIR = os.path.join(DATA_DIR, "raw")
CLEAN_DIR = os.path.join(DATA_DIR, "clean")

# garante diretórios
os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(CLEAN_DIR, exist_ok=True)

def setup_logger(name="etl", log_file=None, level=logging.INFO):
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger
    logger.setLevel(level)
    fmt = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
    ch = logging.StreamHandler()
    ch.setFormatter(fmt)
    logger.addHandler(ch)
    if log_file:
        fh = logging.FileHandler(log_file)
        fh.setFormatter(fmt)
        logger.addHandler(fh)
    return logger

def timestamped_filename(prefix, ext="csv"):
    ts = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    # se prefix vier com extensão, remove
    prefix = prefix.replace(f".{ext}", "")
    return f"{prefix}_{ts}.{ext}"
