# Aula 12 — laboratório acompanhado e melhoria do projeto

A aula tem duas práticas com finalidades diferentes:

1. **Laboratório comum no computador:** acompanhar o detector enquanto o
   professor explica funções, módulos, exceções e logs.
2. **Projeto da equipe:** publicar no GitHub a versão apresentada na
   **Aula 10 · Grau A** e, só depois, melhorar esse projeto usando os princípios
   estudados. O detector não é o projeto que deve ocupar o repositório oficial.

## Laboratório: o que o programa faz?

Imagine um indicador fictício de atividade do robô: números maiores significam
mais atividade. O programa calcula a média das três leituras mais recentes e
mostra uma **mensagem de alerta** quando a média passa de 10, se a mensagem ainda
estiver permitida. A mensagem é uma linha de texto no terminal:

```text
EVENTO amostra=4 media=11.00
```

Depois de mostrar essa linha, o programa guarda `ativo=True`, bloqueando novas
mensagens. Quando a média cai para 8 ou menos, guarda `ativo=False` e volta a
permitir uma mensagem se a média ultrapassar 10 novamente. Essa liberação é o
**rearme**: só muda o estado, sem imprimir outra linha `EVENTO` nessa leitura.

O programa lê o arquivo em ordem e termina ao chegar ao fim. Não importa YanAPI
nem move o robô. Os valores são simulados em unidades arbitrárias (u.a.); não
são limites físicos calibrados nem um detector de queda.

- **Leitura ou amostra:** um número do arquivo.
- **Índice da amostra:** sua posição no arquivo, começando em 1.
- **Janela:** conjunto das três leituras mais recentes.
- **Média:** soma dos valores da janela dividida por três.
- **Mensagem de alerta:** texto exibido pelo `print(...)` quando o alerta é ativado.
- **Estado `ativo=True`:** mensagem já exibida; repetição bloqueada.
- **Estado `ativo=False`:** mensagem permitida, se a média ultrapassar 10.
- **Rearme:** média chega a 8 ou menos; volta a permitir uma próxima mensagem.
- **Histerese:** usar 10 para ativar e 8 para liberar novamente; entre eles, manter o estado.
- **Evento:** a ativação do alerta, que produz uma mensagem.

Antes de completar três leituras, o programa não decide. Uma leitura alta isolada
pode não elevar a média o suficiente. Depois da primeira mensagem, novas leituras
altas não produzem mensagens repetidas: é preciso a média baixar até 8 ou menos
para liberar uma próxima ativação.

## Baixar o laboratório do repositório público

Com Git e Python 3 instalados, abram um terminal na pasta onde querem guardar o
material. O roteiro abaixo usa o endereço do repositório atual do professor;
é necessário que ele esteja público e contenha a versão da Aula 12 publicada.

```bash
git clone https://github.com/brunonunesbr/slides_disciplinas.git
cd slides_disciplinas/robotica-humanoide/aulas
cd 12-engenharia-software-robotica/codigo
```

`git clone` baixa uma cópia local; `cd` entra na pasta indicada. Ao final,
`inicial.py`, `acompanhar.py` e `dados/` ficam na pasta atual. Usem esse terminal
para os comandos seguintes. Se o professor indicar um repositório exclusivo
da aula, usem a URL e o caminho que ele fornecer.

O download de um repositório público por HTTPS dispensa login. Se a pasta
`slides_disciplinas` já existir, usem outra pasta de trabalho para esse primeiro
clone. Esse é o material de estudo; o repositório do projeto do Grau A será
preparado na segunda prática.

## Ambiente e preparação

Usem Python 3 no computador, sem instalar pacotes. Abram um terminal dentro da
pasta `codigo/`. Guardem uma cópia de trabalho de `inicial.py` antes de editar.
No Windows, troquem `python3` por `py` ou `python` se esse for o comando que
inicia Python 3 no ambiente da equipe.

O código próprio mantém sintaxe compatível com Python 3.5 por continuidade com
a Aula 07; isso não significa validação no interpretador ou hardware legado
do Yanshee. Usem o ambiente atual do computador, sem instalar um Python antigo.

## Acompanhar enquanto o professor explica

### Executar e observar a saída

```bash
python3 --version
python3 inicial.py
```

```text
EVENTO amostra=4 media=11.00
EVENTO amostra=11 media=11.00
```

Não alterem os parâmetros antes de entender por que existem essas duas mensagens.
`inicial.py` é uma reconstrução didática dos conceitos da Aula 09, não um script
original recuperado daquela aula.

### Percorrer as leituras e prever a decisão

```bash
python3 acompanhar.py
```

Pressionem Enter para cada nova leitura. O programa mostra valores da janela,
a conta da média, a decisão e o estado. Antes de avançar, tentem prever a saída.
Para percorrer tudo sem pausa:

```bash
python3 acompanhar.py --automatico
```

A sequência de `dados/eventos.csv` é:
`6, 6, 12, 15, 15, 12, 6, 6, 6, 12, 15, 15`.

| Leitura | Últimos três valores | Média | Decisão |
|---:|---|---:|---|
| 1–2 | ainda não há três | — | esperar |
| 3 | 6, 6, 12 | 8 | nenhuma mensagem |
| 4 | 6, 12, 15 | 11 | primeira mensagem; `ativo=True` |
| 5 | 12, 15, 15 | 14 | mensagem repetida bloqueada |
| 6 | 15, 15, 12 | 14 | alerta ativo; sem mensagem |
| 7 | 15, 12, 6 | 11 | alerta ativo; sem mensagem |
| 8 | 12, 6, 6 | 8 | rearme; `ativo=False` |
| 9–10 | 6, 6, 6 / 6, 6, 12 | 6 / 8 | nenhuma mensagem |
| 11 | 6, 12, 15 | 11 | segunda mensagem; `ativo=True` |
| 12 | 12, 15, 15 | 14 | mensagem repetida bloqueada |

Perguntas: por que a média 14 na leitura 5 não produz outra mensagem? O que a leitura
8 muda no estado? Por que a média 11 da leitura 11 pode produzir outra mensagem?

### Fazer pequenas experiências

Antes de cada execução, prevejam o resultado; depois anotem o que mudou.

```bash
python3 acompanhar.py --janela 1
python3 acompanhar.py --entrada 12
```

Com janela 1, aparecem mensagens nas leituras **3 e 10**. Com janela 3 e limite de
início 12, nas leituras **5 e 12**. São mudanças intencionais da regra do ensaio,
não refatorações. Essas opções não editam `config.py`, `inicial.py` ou `main.py`;
sem opções, o acompanhamento volta à configuração original (3, 10 e 8).
A saída pode ser ajustada por `--saida`; é necessário saída < entrada.

### Analisar funções e módulos

Abram `processamento.py`. Confiram que `calcular_media` recebe a janela e
retorna um resultado sem mudar a entrada. Testem:

```bash
python3 -c "from processamento import calcular_media; print(calcular_media([6,12,15]))"
```

Resultado: `11.0`. Na cópia de `inicial.py`, importem essa função e substituam
apenas a conta direta por `media = calcular_media(janela)`. Executem novamente:
as mensagens devem continuar nas leituras 4 e 11.

Depois leiam `detectar_evento`, que recebe o estado anterior e retorna
`(novo_estado_ativo, novo_evento)`. Abram o principal e sigam as chamadas:

```bash
python3 main.py
```

| Arquivo | Responsabilidade |
|---|---|
| `inicial.py` | referência com leitura, cálculo, decisão e saída no mesmo laço |
| `acompanhar.py` | apoio à aula: mostrar conta e decisão a cada leitura |
| `aquisicao.py` | ler e validar o CSV; sinalizar `ErroAquisicao` |
| `processamento.py` | média e transição de estado, sem I/O externo |
| `atuacao.py` | exibir a mensagem de alerta no terminal |
| `config.py` | constantes e validação de configuração |
| `main.py` | coordenar o fluxo e configurar logging |
| `test_regressao.py` | evidências adicionais de equivalência e falhas |
| `dados/` | entradas pequenas simuladas |

O estado e a janela pertencem a uma execução. `deque(maxlen=3)` descarta a leitura
mais antiga. Importar os módulos não deve iniciar uma missão.

### Provocar uma falha e encontrar a causa

Abram `dados/falha.csv`: a terceira leitura contém texto onde se espera número.

```bash
python3 main.py --dados dados/falha.csv
python3 main.py --dados dados/nao-existe.csv
```

As duas execuções terminam com código 1 e diagnóstico de erro. No CSV de falha,
não há evento antes da leitura inválida e as linhas posteriores não são
processadas. A aquisição valida cabeçalho, formato, conversão e finitude;
zero não é substituto de dado inválido.

### Comparar mensagem de alerta e diagnóstico

```bash
python3 main.py
python3 main.py --debug
python3 main.py --debug 2>execucao.log
python3 -m unittest -v test_regressao
```

As mensagens de alerta no terminal continuam iguais. Os logs em stderr detalham execução;
`--debug` inclui valores, médias e estado por amostra. Localizem no arquivo o
rearme na leitura 8 e expliquem por que não houve outra mensagem na leitura 7.
O timestamp do log não substitui o instante de aquisição de um sensor real.

## Aplicar ao projeto apresentado no Grau A

### Preservar e publicar antes de melhorar

Cada equipe usa um repositório oficial do **seu projeto do robô da Aula 10**.
Se ele já existe, usem-no e identifiquem o commit correspondente à apresentação;
não reescrevam o histórico nem criem outro repositório oficial.

Para um repositório novo, uma pessoa cria no GitHub o repositório com README,
nome e visibilidade acordados, convida integrantes e professor e confere acesso.
Cada pessoa usa sua conta e autenticação HTTPS ou SSH, sem compartilhar senhas.
Substituam DONO e NOME e executem fora do repositório da disciplina:

```bash
git clone https://github.com/DONO/humanoide-equipe-NOME.git
cd humanoide-equipe-NOME
git config user.name "Nome Sobrenome"
git config user.email "EMAIL_ASSOCIADO_A_CONTA"
```

Copiem os **arquivos reais do projeto apresentado**, preservando os nomes e a
organização. O detector do laboratório não precisa entrar nesse repositório.
Incluam um README da equipe e `.gitignore` adequado ao projeto. Caches,
ambiente virtual, segredos e logs locais ficam de fora. Código, instruções e
recursos necessários e autorizados entram; revisem gravações e dados pessoais.

No roteiro, a branch principal se chama `main`; confiram o nome em repositórios
existentes. Revisem a seleção antes do commit e da publicação:

```bash
git status
git add .
git diff --cached
git commit -m "Preserva projeto apresentado no Grau A"
git push origin main
```

`git add .` prepara os arquivos não ignorados da pasta; confiram o conteúdo
antes de gravar. Para retirar da seleção um arquivo indevido, substituam o nome:
`git restore --staged nome_do_arquivo`. `.gitignore` não remove arquivos já
rastreados. Se houver credencial exposta, revoguem/rotacionem e avisem o responsável;
apagar em novo commit não elimina as versões anteriores.

Abram o GitHub e verifiquem os arquivos e o commit **antes de começar a melhoria**.
Nome/e-mail de Git identificam commits, não autenticam acesso. Um commit local
não comprova publicação.

### Escolher uma melhoria e abrir uma branch

Identifiquem um problema real no código ou nas instruções do projeto: função
que faz muitas coisas, aquisição misturada com decisão, falha sem contexto,
parâmetro sem nome, ausência de log ou README insuficiente. Escolham uma melhoria
pequena, com trecho afetado e critério de verificação definidos.

```bash
git switch main
git pull --ff-only
git switch -c melhoria-modularizacao
```

Adaptem o nome à tarefa escolhida. Guardem entrada, resultado conhecido,
parâmetros e condições de parada da versão do Grau A. Implementem uma mudança
por vez e repitam o mesmo cenário. Reorganizar não deve mudar a resposta conhecida;
se alterarem uma regra, documentem como mudança funcional e definam o novo esperado.

Na execução física, rever API, limitações e parada. Começar por dados gravados
ou modo de ensaio, quando disponível. Movimentos devem ser limitados e
supervisionados; executar o programa no clone não autoriza movimento automático.

### Registrar, revisar e integrar

```bash
git status
git diff
git add .
git diff --cached
git commit -m "Separa leitura de sensores da decisao"
git push -u origin melhoria-modularizacao
```

Adaptem a mensagem à mudança real. Abram PR para `main` com problema, princípio
aplicado, alteração e evidência de verificação. Outro integrante revisa,
solicita correções e confere o procedimento antes da integração.

Um colega deve clonar em uma pasta nova e usar **o comando do README do próprio
projeto**, sem presumir que ele se chama `main.py`. Documentem também os limites
de reprodução sem o robô. Sem rede, façam commits locais e registrem publicação
e verificação de acesso como pendentes.

Não usem force push para contornar uma recusa sem entender a causa. Em conflito,
leiam as duas alterações, resolvam o conteúdo, removam marcadores e executem
novamente antes do commit. Se `pull --ff-only` falhar, entendam a divergência.

## Entrega e discussão

- URL oficial do projeto da Aula 10 · Grau A e acesso de integrantes e professor.
- Identificação da versão apresentada, preservada e publicada.
- Uma melhoria justificada por funções, módulos, exceções, logs ou legibilidade.
- Commit/PR, revisão de colega e evidência da verificação.
- README atualizado e issue da próxima tarefa, com responsável e aceite.

Não exigir os eventos 4 e 11 para projetos com outros comportamentos: cada equipe
usa seu próprio cenário de referência. A demonstração curta mostra como estava,
o que mudou, qual princípio orientou a mudança e como foi verificado.

## Limites da ponte com o hardware

Dados reais exigem unidade, eixos, gravidade, timestamps, taxa real e lacunas
confirmados. A média pode atrasar eventos e atenuar picos. Não provocar impactos
ou quedas. `try/except` não configura timeout nem interrompe chamada bloqueada;
verifiquem cliente e exceções na YanAPI instalada. Retentativas devem ter limites,
e um movimento com resposta perdida pode já ter ocorrido. `finally` permite uma
tentativa de limpeza, mas encerrar Python não comprova a parada de um atuador.
Definam operação documentada de parada, confirmação e intervenção externa.

## Fontes

Documentação oficial de referência já consultada para a aula:
[Python — módulos](https://docs.python.org/3/tutorial/modules.html),
[exceções](https://docs.python.org/3/tutorial/errors.html),
[logging](https://docs.python.org/3/howto/logging.html),
[Git — gitignore](https://git-scm.com/docs/gitignore),
[switch](https://git-scm.com/docs/git-switch),
[push](https://git-scm.com/docs/git-push) e
[GitHub — repositórios](https://docs.github.com/en/repositories/creating-and-managing-repositories/quickstart-for-repositories).
