# -*- coding: utf-8 -*-
"""Adaptador CSV. Não importa YanAPI nem acessa hardware."""

import csv
import math


class ErroAquisicao(Exception):
    """A fonte de dados falhou ou forneceu uma amostra inválida."""


def ler_valores(caminho):
    """Produz floats finitos em ordem; exige CSV não vazio com coluna valor.

    O índice da amostra é sua posição no arquivo, não um tempo físico.
    A primeira falha encerra a leitura; não há substituição por zero.
    """
    try:
        with open(caminho, newline="", encoding="utf-8") as arquivo:
            leitor = csv.DictReader(arquivo, strict=True)
            if leitor.fieldnames != ["valor"]:
                raise ErroAquisicao("Cabeçalho esperado: valor.")
            quantidade = 0
            for indice, linha in enumerate(leitor, 1):
                if set(linha) != {"valor"} or linha["valor"] is None:
                    raise ErroAquisicao("Formato inválido: amostra {0}.".format(indice))
                try:
                    valor = float(linha["valor"])
                except (TypeError, ValueError) as exc:
                    raise ErroAquisicao(
                        "Número inválido: amostra {0}.".format(indice)
                    ) from exc
                if not math.isfinite(valor):
                    raise ErroAquisicao("Valor não finito: amostra {0}.".format(indice))
                quantidade += 1
                yield valor
            if quantidade == 0:
                raise ErroAquisicao("Arquivo sem amostras.")
    except (OSError, csv.Error, UnicodeError) as exc:
        raise ErroAquisicao("Falha na leitura do CSV: {0}".format(exc)) from exc
