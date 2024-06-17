<div align="center">

<h2>Problema de seleção de projetos <br>(Trabalho de Grafos)</h2>
</div>

<details open="open">
  <summary> Tabela de Conteúdos</summary>
  <ol>
    <li>
      <a href="#logica-da-questao">Lógica da Questão</a>
    </li>
    <li>
      <a href="#como-rodar">Como Rodar</a>
    </li>
  </ol>
</details>

## Logica da Questao

<ul>
    <li>
        <a>Verificar a existência de ciclo orientado:</a>
        <p>- Caso haja ciclo orientado no grafo, a saída do programa consta em "DIGRAFO INVÁLIDO", já que ficaremos em uma dependência circular de projeto.</p>
    </li>
    <br>
    <li>
        <a>Modelagem do problema de programação linear binária:</a>
        <p>
        - O problema pode ser resolvido por PLB. Podemos modelar a equação a partir da entrada da seguinte forma:
        </p>
    </li>
</ul>

```
ENTRADA
8                       -> Representa a quantidade de vértices
0 0 0 0 1 1 0 0
0 0 1 0 0 1 0 0
0 0 0 0 0 0 1 0
0 0 0 0 0 0 1 1
0 0 0 0 0 0 0 0         -> Restrições
0 0 0 0 1 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
4 6 2 3 -2 -3 -5 -8     -> Representa o valor de cada projeto (Função Objetivo)
```

**_Obs_**: Restrições:

Onde tem 1 na linha representa que o projeto da linha tem dependência do projeto da coluna:

Ex:
Linha 1:
0 0 0 0 1 1 0 0

Restrições dessa linha:

x1 - x5 <= 0

x1 - x6 <= 0

Pois o projeto da linha só pode ser escolhido(x = 1) se o projeto da coluna tiver sido escolhido (x = 1).

Modelagem dessa entrada:

```
Max Z = 4x1 + 6x2 + 2x3 + 3x4 - 2x5 - 3x6 - 5x7 - 8x8

sujeito a:
        x1 - x5 <= 0
        x1 - x6 <= 0
        x2 - x3 <= 0
        x2 - x6 <= 0
        x3 - x7 <= 0
        x4 - x7 <= 0
        x4 - x8 <= 0
        x6 - x5 <= 0
        xi, onde i = 1, ..., 8 = {0,1}
```

## Como Rodar

Rode o seguinte comando para instalar as dependências:

```
pip install -r .\requirements.txt
```

Após a instalação das dependências, basta iniciar o projeto com o comando:

```
python .\trabalho2.py
ou
python3 .\trabalho2.py
```
