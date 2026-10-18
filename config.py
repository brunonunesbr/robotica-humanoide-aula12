# -*- coding: utf-8 -*-
"""Parâmetros didáticos: valores simulados em unidades arbitrárias (u.a.)."""

TAMANHO_JANELA = 3
LIMITE_ENTRADA = 10.0
LIMITE_SAIDA = 8.0


def validar_configuracao():
    """Impede uma janela vazia e limiares sem histerese."""
    if TAMANHO_JANELA < 1 or LIMITE_SAIDA >= LIMITE_ENTRADA:
        raise ValueError("Exija janela >= 1 e limite de saída < entrada.")
