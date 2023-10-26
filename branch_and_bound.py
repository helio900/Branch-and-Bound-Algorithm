from mip import Model, xsum, maximize, BINARY

# Função para ler os dados do arquivo
# Sempre atualizar com o nome do arquivo que será usado
def ler_dados(teste1):  # Atualizar aqui
    with open(teste1, 'r') as arquivo:  # Aqui também e na linha 49
        linhas = arquivo.readlines()
    
    # Extrair o número de variáveis e restrições
    num_variaveis, num_restricoes = map(int, linhas[0].split())
    
    # Coeficientes da função objetivo
    coef_objetivo = list(map(int, linhas[1].split()))
    
    # Coeficientes e limites das restrições
    coef_restricoes = []
    limites_variaveis = []
    for i in range(2, num_restricoes + 2):
        linha = list(map(int, linhas[i].split()))
        coef_restricoes.append(linha[:-1])  # Os últimos elementos são os limites, então excluímos eles
        limites_variaveis.append(linha[-1])  # O último elemento é o limite
    
    return coef_objetivo, coef_restricoes, limites_variaveis

# Função para resolver o problema de programação linear inteira binária usando branch-and-bound
def branch_and_bound(coef_objetivo, coef_restricoes, limites_variaveis):
    model = Model(solver_name='cbc')  # Usando o solver CBC
    num_variaveis = len(coef_objetivo)
    variaveis = [model.add_var(var_type=BINARY) for _ in range(num_variaveis)]
    
    # Função objetivo
    model.objective = maximize(xsum(coef_objetivo[i] * variaveis[i] for i in range(num_variaveis)))
    
    # Restrições
    for coef, limite in zip(coef_restricoes, limites_variaveis):
        model += xsum(coef[i] * variaveis[i] for i in range(num_variaveis)) <= limite
    
    # Otimizar o modelo
    model.optimize()
    
    # Retornar a solução
    if model.num_solutions:
        solucao = [int(var.x) for var in variaveis]
        return model.objective_value, solucao
    else:
        return None

# Leitura dos dados do arquivo
teste = 'teste4.txt'   # Atualizar com o nome do arquivo que será usado, teste1, teste2, ..., testeN
coef_objetivo, coef_restricoes, limites_variaveis = ler_dados(teste)

# Chamada da função branch_and_bound
melhor_valor, melhor_solucao = branch_and_bound(coef_objetivo, coef_restricoes, limites_variaveis)

# Resultados
if melhor_solucao:
    print(f'Melhor valor da função objetivo: {melhor_valor}')
    print(f'Melhor solução: {melhor_solucao}')
else:
    print('Nenhuma solução encontrada :(')