import pulp
import numpy as np

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
    print("DIGRAFO INVÁLIDO")
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

    print("============================== RESULTADO ==============================")
    print("X =", resposta)
    print("=============================== FIM ===================================")
    print("Valor da Função Objetivo:", pulp.value(model.objective))