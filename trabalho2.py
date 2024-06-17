import pulp
import numpy as np
from pyvis.network import Network
import webbrowser

def detect_cycle(graph):
    visited = [False] * len(graph)
    rec_stack = [False] * len(graph)

    def cycle_util(v):
        visited[v] = True
        rec_stack[v] = True

        for neighbor in range(len(graph[v])):
            if graph[v][neighbor] == 1:
                if not visited[neighbor]:
                    if cycle_util(neighbor):
                        return True
                elif rec_stack[neighbor]:
                    return True

        rec_stack[v] = False
        return False

    for node in range(len(graph)):
        if not visited[node]:
            if cycle_util(node):
                return True
    return False

projectFile = open('project.txt', 'r')
NumEdges = int(projectFile.readline().strip())

restricoes = []
for i in range(NumEdges):
    line = projectFile.readline().strip().split(" ")
    line = [int(num) for num in line]
    restricoes.append(line)

funcaoObjetivo = projectFile.readline().strip().split(" ")
funcaoObjetivo = [int(num) for num in funcaoObjetivo]

if detect_cycle(restricoes):
    print("DIGRAFO INVALIDO")
else:
    model = pulp.LpProblem("Maximizar_Funcao_Objetivo", pulp.LpMaximize)

    variables = [pulp.LpVariable(f'x{i+1}', cat='Binary') for i in range(len(funcaoObjetivo))]

    model += pulp.lpSum([funcaoObjetivo[i] * variables[i] for i in range(len(funcaoObjetivo))])

    for i in range(len(restricoes)):
        for j in range(len(restricoes[i])):
            if restricoes[i][j] == 1:
                model += variables[i] <= variables[j]

    model.solve()

    resposta = []
    for variable in model.variables():
        if variable.varValue == 1:
            resposta.append(int(variable.name.replace("x", "")))

    valor_otimo = pulp.value(model.objective)
    
    funcao_obj_str = "Max Z = " + " + ".join([f"{funcaoObjetivo[i]}x{i+1}" for i in range(len(funcaoObjetivo))])

    restricoes_str = []
    for i in range(len(restricoes)):
        for j in range(len(restricoes[i])):
            if restricoes[i][j] == 1:
                restricoes_str.append(f"x{i+1} - x{j+1} <= 0")
    restricoes_str = "; ".join(restricoes_str)

    print("============================== RESULTADO ==============================")
    print("X =", resposta)
    print("Valor otimo:", valor_otimo)
    print("=============================== FIM ===================================")

    net = Network(directed=True)
    net.toggle_physics(True)

    for i in range(len(funcaoObjetivo)):
        color = 'green' if (i+1) in resposta else 'red'
        net.add_node(i+1, label=f'P{i+1} ({funcaoObjetivo[i]})', color=color)

    for i in range(len(restricoes)):
        for j in range(len(restricoes[i])):
            if restricoes[i][j] == 1:
                net.add_edge(i+1, j+1)

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Grafo Interativo</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
            }}
            .container {{
                display: flex;
                flex-direction: column;
                align-items: center;
                margin: 20px;
            }}
            .info {{
                margin-bottom: 20px;
            }}
            .info p {{
                margin: 5px 0;
            }}
            .legend {{
                display: flex;
                flex-direction: row;
                align-items: center;
                margin-bottom: 20px;
            }}
            .legend div {{
                display: flex;
                align-items: center;
                margin-right: 10px;
            }}
            .legend .color-box {{
                width: 20px;
                height: 20px;
                margin-right: 5px;
            }}
            .selected-projects {{
                border: 2px solid #000;
                padding: 10px;
                background-color: #f0f0f0;
                margin-top: 10px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="info">
                <h2>Informacoes do Problema</h2>
                <p><strong>Funcao Objetivo:</strong> {funcao_obj_str}</p>
                <p><strong>Restricoes:</strong> {restricoes_str}</p>
                <p><strong>Valor Otimo:</strong> {valor_otimo}</p>
                <p class="selected-projects"><strong>Projetos Selecionados:</strong> X = {resposta}</p>
                <p>O resultado tambem foi printado no terminal.</p>
            </div>
            <div class="legend">
                <div>
                    <div class="color-box" style="background-color: green;"></div>
                    <span>Projeto Selecionado</span>
                </div>
                <div>
                    <div class="color-box" style="background-color: red;"></div>
                    <span>Projeto Nao Selecionado</span>
                </div>
            </div>
            <div id="grafo"></div>
        </div>
        <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/vis/4.21.0/vis-network.min.js"></script>
        <link href="https://cdnjs.cloudflare.com/ajax/libs/vis/4.21.0/vis-network.min.css" rel="stylesheet" type="text/css" />
        {net.generate_html('graph.html')}
    </body>
    </html>
    """

    html_file_path = 'graph_interactive.html'
    with open(html_file_path, 'w') as file:
        file.write(html_content)
    
    webbrowser.open(html_file_path)