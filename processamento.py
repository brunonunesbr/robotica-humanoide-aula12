# -*- coding: utf-8 -*-
"""Regras independentes de arquivos, rede, logging e robô."""


def calcular_media(janela):
    """Média de uma janela não vazia, na mesma unidade das amostras."""
    if not janela:
        raise ValueError("A janela não pode estar vazia.")
    return sum(janela) / len(janela)


def detectar_evento(media, ativo, limite_entrada, limite_saida):
    """Retorna (novo_estado_ativo, novo_evento).

    Exige valores finitos e limite_saida < limite_entrada.
    Entra acima do limite de entrada; rearma em ou abaixo da saída.
    Não modifica estado global nem a janela recebida pelo chamador.
    """
    if not ativo and media > limite_entrada:
        return True, True
    if ativo and media <= limite_saida:
        return False, False
    return ativo, False
