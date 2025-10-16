import random, time
import matplotlib.pyplot as plt

passcode_length = 500

population_size = 200
num_parents = 50
elite_size = 5
mutation_rate = 0.05

secret_passcode = [random.randint(0, 9) for _ in range(passcode_length)]
print("Secret:", secret_passcode)

population = [[random.randint(0,9) for _ in range(passcode_length)]
              for _ in range(population_size)]

def fitness(chromosome):
    return sum(1 for a,b in zip(chromosome, secret_passcode) if a == b)

def select_parents(pop):
    return sorted(pop, key=fitness, reverse=True)[:num_parents]

def breed(p1, p2):
    a, b = sorted(random.sample(range(passcode_length), 2))
    child = p1[:a] + p2[a:b+1] + p1[b+1:]
    return child

def create_children(parents_pool):
    elites = parents_pool[:elite_size]
    children = elites[:]
    while len(children) < population_size:
        p1, p2 = random.sample(parents_pool, 2)
        children.append(breed(p1, p2))
    return children

def mutate(pop):
    for i in range(elite_size, len(pop)):
        if random.random() < mutation_rate:
            j = random.randrange(passcode_length)
            pop[i][j] = random.randint(0, 9)
    return pop

success = []
generations = 0
t0 = time.time()

while True:
    best_fit = max(map(fitness, population))
    success.append(best_fit)
    if best_fit == passcode_length:
        elapsed = time.time() - t0
        champ = max(population, key=fitness)
        print(f"Cracked in {generations} generations, {elapsed:.3f}s!")
        print("Discovered:", champ)
        break
    parents = select_parents(population)
    children = create_children(parents)
    population = mutate(children)
    generations += 1

plt.plot(range(len(success)), success)
plt.title('Fitness by Generation')
plt.xlabel('Generation')
plt.ylabel('Fitness')
plt.show()
