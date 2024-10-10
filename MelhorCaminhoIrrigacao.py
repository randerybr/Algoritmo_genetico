import numpy as np
import pandas as pd
import random
from scipy.spatial.distance import euclidean
import matplotlib.pyplot as plt

# Carregar os dados usando raw string
df = pd.read_excel(r'Dados Plantas.xlsx')

# Ponto de partida (0, 0) para a irrigação
source_point = (0, 0)

# Extrair as coordenadas das plantas
plants = df[['X', 'Y']].values
plant_names = df['Planta'].values

# Função para calcular a distância total de um caminho sem retorno à origem
def total_distance(route):
    total = 0
    current_point = source_point
    for idx in route:
        next_point = plants[idx]
        total += euclidean(current_point, next_point)
        current_point = next_point
    return total  # Sem retorno à origem

# Algoritmo genético
def genetic_algorithm(population_size=100, generations=1000, mutation_rate=0.01):
    # Inicializar população
    population = [np.random.permutation(len(plants)) for _ in range(population_size)]

    for gen in range(generations):
        # Avaliar fitness
        fitness_scores = [1 / total_distance(individual) for individual in population]
        total_fitness = sum(fitness_scores)

        # Seleção
        selected = [population[np.random.choice(len(population), p=[f/total_fitness for f in fitness_scores])] for _ in range(population_size)]
        
        # Cruzamento
        next_generation = []
        for i in range(0, population_size, 2):
            parent1, parent2 = selected[i], selected[i+1]
            cut = random.randint(1, len(parent1) - 1)
            child1 = np.concatenate((parent1[:cut], [gene for gene in parent2 if gene not in parent1[:cut]]))
            child2 = np.concatenate((parent2[:cut], [gene for gene in parent1 if gene not in parent2[:cut]]))
            next_generation.extend([child1, child2])

        # Mutação
        for individual in next_generation:
            if random.random() < mutation_rate:
                swap_idx = np.random.randint(0, len(individual), size=2)
                individual[swap_idx[0]], individual[swap_idx[1]] = individual[swap_idx[1]], individual[swap_idx[0]]

        # Substituir população
        population = next_generation

    # Melhor indivíduo
    best_individual = min(population, key=total_distance)
    return best_individual, total_distance(best_individual)

# Função para desenhar o caminho de irrigação sem o retorno à origem
def plot_route_with_table(route, plants, plant_names, best_distance):
    # Criar uma figura maior para incluir a tabela e o gráfico
    fig, ax = plt.subplots(figsize=(12, 10))

    # Desenhar o ponto de partida (0,0)
    ax.scatter(0, 0, color='red', label='Origem')
    ax.text(0, 0, "Origem", fontsize=12, verticalalignment='bottom', horizontalalignment='right')

    # Desenhar as plantas
    for i, (x, y) in enumerate(plants):
        ax.scatter(x, y, color='green')
        ax.text(x, y, plant_names[i], fontsize=12, verticalalignment='bottom', horizontalalignment='right')

    # Desenhar o caminho e mostrar a sequência
    current_point = (0, 0)
    for step, idx in enumerate(route):
        next_point = plants[idx]
        # Desenha a linha do caminho
        ax.plot([current_point[0], next_point[0]], [current_point[1], next_point[1]], 'b-')

        # Adiciona a sequência do caminho
        ax.text(next_point[0], next_point[1], f"{step+1}", fontsize=14, color='blue', fontweight='bold')
        current_point = next_point

    # Título e distância total
    ax.set_title(f"Melhor Caminho de Irrigação - Distância Total: {best_distance:.2f} (Sem retorno à origem)", fontsize=16)

    # Configurações do gráfico
    ax.set_xlabel('Coordenada X')
    ax.set_ylabel('Coordenada Y')
    ax.grid(True)
    ax.legend()

    # Ajustar a posição da tabela para ocupar mais espaço na tela
    plt.subplots_adjust(left=0.05, right=0.6)  # Deixar espaço à direita para a tabela

    # Criar tabela com a sequência das plantas
    table_data = [[i+1, plant_names[idx]] for i, idx in enumerate(route)]
    
    # Criar a tabela no lado direito
    table_ax = fig.add_subplot(111, frame_on=False)  # Frame invisível para a tabela
    table_ax.xaxis.set_visible(False)  # Esconder o eixo X
    table_ax.yaxis.set_visible(False)  # Esconder o eixo Y
    table_ax.table(cellText=table_data, colLabels=["Ordem", "Planta"], cellLoc='center', loc='right', colWidths=[0.05, 0.1])

    # Mostrar o gráfico e a tabela juntos
    plt.show()

# Executar o algoritmo genético
best_route, best_distance = genetic_algorithm()

# Desenhar o resultado com a tabela
plot_route_with_table(best_route, plants, plant_names, best_distance)
