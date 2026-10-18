# -*- coding: utf-8 -*-
"""Saída de ensaio: só escreve no terminal, sem movimento físico."""


def sinalizar_evento(indice, media):
    """Produz um aviso por entrada no estado ativo."""
    print("EVENTO amostra={0} media={1:.2f}".format(indice, media))
