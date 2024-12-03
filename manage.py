#!/usr/bin/env python
import os
import sys


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "jogo_rank.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        # Se o Django não estiver instalado, lance uma exceção
        raise ImportError(
            "Não foi possível importar o Django. Certifique-se de que o Django está instalado corretamente."
        )
    execute_from_command_line(sys.argv)
