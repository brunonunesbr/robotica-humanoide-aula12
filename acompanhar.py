# -*- coding: utf-8 -*-
"""Percorre o detector leitura por leitura durante a explicação em aula.

Os dados representam um indicador fictício de atividade, em unidades
arbitrárias. O programa só escreve no terminal e não acessa o robô.
"""

import argparse
from collections import deque
import math
import os
import sys

from aquisicao import ErroAquisicao, ler_valores
from config import LIMITE_ENTRADA, LIMITE_SAIDA, TAMANHO_JANELA
from processamento import calcular_media, detectar_evento


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dados", default=os.path.join(
        os.path.dirname(__file__), "dados", "eventos.csv"))
    parser.add_argument("--janela", type=int, default=TAMANHO_JANELA)
    parser.add_argument("--entrada", type=float, default=LIMITE_ENTRADA)
    parser.add_argument("--saida", type=float, default=LIMITE_SAIDA)
    parser.add_argument("--automatico", action="store_true",
                        help="Mostra todas as leituras sem esperar Enter.")
    args = parser.parse_args()
    if (args.janela < 1 or not math.isfinite(args.entrada)
            or not math.isfinite(args.saida) or args.saida >= args.entrada):
        parser.error("Exija janela >= 1 e limites finitos com saida < entrada.")

    janela = deque(maxlen=args.janela)
    ativo = False
    leituras_com_mensagem = []
    print("MONITOR DIDATICO DE ATIVIDADE — dados simulados em u.a.")
    print("Mostrar mensagem se a media > {0:g}; liberar outra "
          "quando a media <= {1:g}.".format(args.entrada, args.saida))
    print("Janela: {0} leitura(s). Nenhum movimento sera executado."
          .format(args.janela))
    try:
        for indice, valor in enumerate(ler_valores(args.dados), 1):
            if not args.automatico:
                input("\nPressione Enter para receber a leitura {0}..."
                      .format(indice))
            janela.append(valor)
            print("\nLeitura {0}: valor={1:g}".format(indice, valor))
            print("  Valores usados agora: [{0}]".format(
                ", ".join("{0:g}".format(v) for v in janela)))
            if len(janela) < args.janela:
                print("  Ainda faltam leituras para calcular a media.")
                continue
            media = calcular_media(janela)
            print("  Media: ({0}) / {1} = {2:.2f}".format(
                " + ".join("{0:g}".format(v) for v in janela),
                len(janela), media))
            anterior = ativo
            ativo, novo = detectar_evento(
                media, ativo, args.entrada, args.saida)
            if novo:
                leituras_com_mensagem.append(indice)
                print("  EVENTO amostra={0} media={1:.2f}".format(indice, media))
                print("  Mensagem exibida; bloquear repeticoes (ativo=True).")
            elif anterior and not ativo:
                print("  REARME: permitir outra mensagem (ativo=False).")
                print("  Nesta leitura nao ha nova mensagem EVENTO.")
            elif ativo:
                print("  Alerta continua ativo; mensagem repetida bloqueada.")
            else:
                print("  Alerta inativo; aguardar media acima do limite.")
            print("  Estado guardado: ativo={0}".format(ativo))
    except ErroAquisicao as exc:
        print("Falha de aquisicao: {0}. Analise interrompida.".format(exc),
              file=sys.stderr)
        return 1
    except (KeyboardInterrupt, EOFError):
        print("\nAcompanhamento encerrado pelo operador.")
        return 130
    print("\nLeituras com mensagem de alerta: {0}".format(leituras_com_mensagem))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
