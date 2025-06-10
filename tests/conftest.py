import sys
import os

# Adiciona a pasta-pai (raiz do projeto) ao PYTHONPATH para o pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
