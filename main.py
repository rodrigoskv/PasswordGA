import random
import numpy as np
import matplotlib.pyplot as plt
import time

passcode_length = 500
passcode_lower_bound = 0
passcode_upper_bound = 9


population_size = 200   # 100–400 é um bom intervalo inicial
num_parents = 50        # ~20–30% da população
elite_size = 5          # ~2–5% da população


secret_passcode = [random.randint(passcode_lower_bound, passcode_upper_bound)
                   for _ in range(passcode_length)]
print("Secret passcode:", secret_passcode)

population = []
for i in range(population_size):
    chromosome = [random.randint(passcode_lower_bound, passcode_upper_bound)
                  for _ in range(passcode_length)]
    population.append(chromosome)

def fitness(population):
    fitness_scores = []
    for chromosome in population:
        matches = 0
        for index in range(passcode_length):
            if secret_passcode[index] == chromosome[index]:
                matches += 1
        result = [chromosome, matches]
        fitness_scores.append(result)
    return fitness_scores

def select_parents(fitness_scores):
    parents_list = []
    for chromosome in sorted(fitness_scores, key=lambda x: x[1], reverse=True)[:num_parents]:
        parents_list.append(chromosome[0])
    return parents_list


def breed(parent1, parent2):
    child = []
    geneA = int(random.random() * passcode_length)
    geneB = int(random.random() * passcode_length)
    startGene = min(geneA, geneB)
    endGene = max(geneA, geneB)

    for i in range(passcode_length):
        if (i < startGene) or (i > endGene):
            child.append(parent1[i])
        else:
            child.append(parent2[i])
    return child

def create_children(parents_pool):
    children = []
    num_new_children = population_size - elite_size  # usa tamanho alvo da população

    # elitism
    for i in range(elite_size):
        children.append(parents_pool[i])

    # crossover
    for i in range(num_new_children):
        parent1 = parents_pool[int(random.random() * len(parents_pool))]
        parent2 = parents_pool[int(random.random() * len(parents_pool))]
        children.append(breed(parent1, parent2))
    return children


def mutation(children_set):
    for i in range(len(children_set)):
        if random.random() > 0.1: # mutation - está em 0.1, pode alterar para 0.5 para acompanhar
            continue
        mutated_position = int(random.random() * passcode_length)
        mutation_value = random.randint(passcode_lower_bound, passcode_upper_bound)
        children_set[i][mutated_position] = mutation_value
    return children_set

success = []
generations = 0
t0 = time.time()
while True:
    fitness_scores = fitness(population)
    success.append(max([i[1] for i in fitness_scores]))
    if max([i[1] for i in fitness_scores]) == passcode_length:
        print("Cracked in {} generations, and {:.6f} seconds! \nSecret passcode = {} \nDiscovered passcode = {}".format(
            generations, time.time() - t0, secret_passcode,
            [i[0] for i in fitness_scores if i[1] == passcode_length][0]
        ))
        break
    parents = select_parents(fitness_scores)
    children = create_children(parents)
    population = mutation(children)
    generations += 1

fig, ax = plt.subplots()

ax.plot(range(len(success)), success)  
ax.set_title('Fitness Score by Generation', fontweight='bold')
ax.set_xlabel('Generation')
ax.set_ylabel('Fitness Score')

ax.set_ylim(0, passcode_length)
ax.set_xlim(0, max(1, len(success)-1))

fig.tight_layout()
plt.show()


