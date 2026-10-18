# -*- coding: utf-8 -*-
"""Reconstrução didática dos conceitos da Aula 09, para refatorar.

Não é um script original daquela aula. Mistura leitura, regra e saída.
Use primeiro o CSV válido; falhas serão tratadas na versão modular.
"""

import csv
import math
import os
import sys


def main():
    caminho = (sys.argv[1] if len(sys.argv) > 1 else
               os.path.join(os.path.dirname(__file__), "dados", "eventos.csv"))
    janela = []
    ativo = False
    with open(caminho, newline="", encoding="utf-8") as arquivo:
        leitor = csv.DictReader(arquivo)
        if leitor.fieldnames != ["valor"]:
            raise ValueError("Cabeçalho esperado: valor.")
        for indice, linha in enumerate(leitor, 1):
            valor = float(linha["valor"])
            if not math.isfinite(valor):
                raise ValueError("Valor não finito.")
            janela.append(valor)
            janela = janela[-3:]
            if len(janela) < 3:
                continue
            media = sum(janela) / len(janela)
            if not ativo and media > 10.0:
                ativo = True
                print("EVENTO amostra={0} media={1:.2f}".format(indice, media))
            elif ativo and media <= 8.0:
                ativo = False
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
