# -*- coding: utf-8 -*-
"""Orquestra aquisição, processamento e atuação de ensaio."""

import argparse
from collections import deque
import logging
import os

from aquisicao import ErroAquisicao, ler_valores
from atuacao import sinalizar_evento
from config import (LIMITE_ENTRADA, LIMITE_SAIDA, TAMANHO_JANELA,
                    validar_configuracao)
from processamento import calcular_media, detectar_evento

logger = logging.getLogger(__name__)


def executar(caminho):
    """Executa um replay finito. Erros de aquisição chegam ao chamador."""
    validar_configuracao()
    janela = deque(maxlen=TAMANHO_JANELA)
    ativo = False
    eventos = 0
    logger.info("inicio fonte=%s janela=%s entrada=%s saida=%s",
                caminho, TAMANHO_JANELA, LIMITE_ENTRADA, LIMITE_SAIDA)
    for indice, valor in enumerate(ler_valores(caminho), 1):
        janela.append(valor)
        if len(janela) < TAMANHO_JANELA:
            logger.debug("aquecimento amostra=%s valor=%s", indice, valor)
            continue
        media = calcular_media(janela)
        ativo, novo = detectar_evento(media, ativo, LIMITE_ENTRADA, LIMITE_SAIDA)
        logger.debug("amostra=%s valor=%.2f media=%.2f ativo=%s novo=%s",
                     indice, valor, media, ativo, novo)
        if novo:
            logger.info("evento amostra=%s media=%.2f", indice, media)
            sinalizar_evento(indice, media)
            eventos += 1
    logger.info("replay_concluido eventos=%s", eventos)
    return eventos


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    padrao = os.path.join(os.path.dirname(__file__), "dados", "eventos.csv")
    parser.add_argument("--dados", default=padrao)
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()
    logging.basicConfig(
        level=logging.DEBUG if args.debug else logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(message)s")
    try:
        executar(args.dados)
        return 0
    except ErroAquisicao:
        logger.exception("aquisicao_falhou; replay interrompido")
        return 1
    except KeyboardInterrupt:
        logger.warning("interrupcao solicitada pelo operador")
        return 130
    finally:
        logger.info("fim; atuacao apenas no terminal")


if __name__ == "__main__":
    raise SystemExit(main())
