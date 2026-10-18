# -*- coding: utf-8 -*-
"""Evidência de equivalência e interrupção; não requer hardware."""

from contextlib import redirect_stdout
import importlib
import io
import os
import subprocess
import sys
import tempfile
import unittest

from aquisicao import ErroAquisicao, ler_valores
from processamento import calcular_media, detectar_evento

BASE = os.path.dirname(os.path.abspath(__file__))


def rodar(nome, *argumentos):
    processo = subprocess.Popen(
        [sys.executable, os.path.join(BASE, nome)] + list(argumentos),
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    saida, erros = processo.communicate()
    return processo.returncode, saida, erros


class Regressao(unittest.TestCase):
    def test_equivalencia_com_saida_esperada(self):
        antes = rodar("inicial.py")
        depois = rodar("main.py", "--debug")
        esperado = ("EVENTO amostra=4 media=11.00\n"
                    "EVENTO amostra=11 media=11.00\n")
        self.assertEqual(antes[0], 0)
        self.assertEqual(depois[0], 0)
        self.assertEqual(antes[1], esperado)
        self.assertEqual(depois[1], esperado)
        self.assertIn("DEBUG", depois[2])

    def test_limiares_e_nao_repeticao(self):
        self.assertEqual(detectar_evento(10, False, 10, 8), (False, False))
        self.assertEqual(detectar_evento(11, False, 10, 8), (True, True))
        self.assertEqual(detectar_evento(12, True, 10, 8), (True, False))
        self.assertEqual(detectar_evento(9, True, 10, 8), (True, False))
        self.assertEqual(detectar_evento(8, True, 10, 8), (False, False))

    def test_media_e_janela_vazia(self):
        self.assertEqual(calcular_media([6, 12, 15]), 11)
        with self.assertRaises(ValueError):
            calcular_media([])

    def test_falha_interrompe_sem_atuar_nas_linhas_seguintes(self):
        codigo, saida, erros = rodar("main.py", "--dados",
                                     os.path.join(BASE, "dados", "falha.csv"))
        self.assertEqual(codigo, 1)
        self.assertEqual(saida, "")
        self.assertIn("aquisicao_falhou", erros)
        self.assertIn("amostra 3", erros)
        self.assertIn("fim;", erros)

    def test_arquivo_ausente(self):
        with tempfile.TemporaryDirectory() as pasta:
            codigo, saida, erros = rodar("main.py", "--dados",
                                         os.path.join(pasta, "ausente.csv"))
        self.assertEqual(codigo, 1)
        self.assertEqual(saida, "")
        self.assertIn("aquisicao_falhou", erros)

    def test_contrato_csv(self):
        casos = ("valor\nNaN\n", "valor\ninf\n", "outro\n1\n",
                 "valor\n", "valor\n1,2\n", 'valor\n"sem fechamento\n')
        with tempfile.TemporaryDirectory() as pasta:
            caminho = os.path.join(pasta, "caso.csv")
            for conteudo in casos:
                with self.subTest(conteudo=conteudo):
                    with open(caminho, "w", encoding="utf-8") as arquivo:
                        arquivo.write(conteudo)
                    with self.assertRaises(ErroAquisicao):
                        list(ler_valores(caminho))

    def test_importar_nao_inicia_replay(self):
        saida = io.StringIO()
        with redirect_stdout(saida):
            importlib.import_module("main")
        self.assertEqual(saida.getvalue(), "")


if __name__ == "__main__":
    unittest.main()
