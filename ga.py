import random
import numpy as np
import matplotlib.pyplot as plt
from maze import Maze


POP_SIZE     = 700
STEPS        = 200
MUT_RATE     = 0.1
GENERATIONS  = 100

ELITE_FRAC   = 0.2
TOURNEY_K    = 8
FINE_WALL = 5
REWARD_NEW = 20
REWARD_CLOSER_GOAL = 20
FINE_FURTHER_GOAL = 10
REWARD_GOAL = 1000
REWARD_FEW_STEPS = 10
REWARD_EXPLORE = 10
FINE_ALREADY_VISITED = 20
maze = Maze()


def create_individual():
    return [random.randrange(4) for n in range(STEPS)]


def simulate(individual):
    position = maze.START
    for m in individual:
        position = maze.move(position, m)
        if position == maze.GOAL:
            break
    return position


def euclidean_dist(position, ziel):
    return np.linalg.norm(np.array(position) - np.array(ziel))

def fitness(individual, generation):
    """
    Fitness orientiert sich stark an:
    - Zielerreichung + Schnelligkeit
    - Verringerung der Distanz zum Ziel
    - Belohnung für neue Felder
    - Strafung für Wände und Weg vom Ziel weg
    """
    position = maze.START
    visited = set([position])
    score = 0.0

    best_dist = euclidean_dist(position, maze.GOAL)

    for step, movement in enumerate(individual):
        new_pos = maze.move(position, movement)
        distance_old = euclidean_dist(position, maze.GOAL)
        distance_new = euclidean_dist(new_pos, maze.GOAL)
        progress_to_goal = distance_old - distance_new

        if new_pos == position:
            score -= FINE_WALL
        else:
            if new_pos not in visited:
                score += REWARD_NEW
                visited.add(new_pos)
            else:
                if step > 0 and new_pos == maze.move(position, (individual[step - 1] + 2) % 4):
                    score -= FINE_ALREADY_VISITED

            score += progress_to_goal * REWARD_CLOSER_GOAL
            if progress_to_goal < 0:
                score += progress_to_goal * FINE_FURTHER_GOAL

        best_dist = min(best_dist, distance_new)
        position = new_pos

        if position == maze.GOAL:
            score += REWARD_GOAL
            score += (STEPS - step) * REWARD_FEW_STEPS
            return score

    explore_factor = max(0, 1 - generation / GENERATIONS)
    score += explore_factor * REWARD_EXPLORE * (new_pos not in visited)

    return score


def evaluate_population(population, generation):
    return [fitness(individual, generation) for individual in population]


def tournament_selection(population, fitness, k=TOURNEY_K):
    n = len(population)
    parents = []
    for m in range(n):
        candidates = random.sample(range(n), k)
        bester_candidate = max(candidates, key=lambda i: fitness[i])
        parents.append(population[bester_candidate][:])
    return parents


def crossover(p1, p2):
    cut1 = random.randint(0, STEPS // 2)
    cut2 = random.randint(STEPS // 2, STEPS)
    child = p1[:cut1] + p2[cut1:cut2] + p1[cut2:]
    return child


def mutate(individual, generation):
    dynamic_rate = MUT_RATE + (generation / max(1, GENERATIONS)) * 0.25
    rate = min(0.5, dynamic_rate)

    for i in range(STEPS):
        if random.random() < rate:
            if random.random() < 0.5:
                individual[i] = random.randrange(4)
            else:
                individual[i] = (individual[i] + random.choice([-1, 1])) % 4
    return individual

def visualize_population(population, generation, title_suffix=""):
    plt.imshow(maze.grid, cmap="gray")
    plt.axis("off")

    best_individual = population[0]
    pos = maze.START
    x, y = [pos[1]], [pos[0]]
    for m in best_individual:
        pos = maze.move(pos, m)
        x.append(pos[1])
        y.append(pos[0])
        if pos == maze.GOAL:
            break
    plt.plot(x, y, linewidth=1,)
    plt.scatter(x[-1], y[-1], s=50)

    for individual in population[1:] :
        pos = maze.START
        x, y = [pos[1]], [pos[0]]
        for m in individual:
            pos = maze.move(pos, m)
            x.append(pos[1])
            y.append(pos[0])
            if pos == maze.GOAL:
                break
        plt.plot(x, y, linewidth=1)
        plt.scatter(x[-1], y[-1], s=20)

    plt.scatter(maze.START[1], maze.START[0], s=100, marker="o")
    plt.scatter(maze.GOAL[1], maze.GOAL[0], s=100, marker="x")

    plt.title(f"Generation {generation} {title_suffix}")
    plt.pause(0.5)
    plt.clf()



def run():
    population= [create_individual() for n in range(POP_SIZE)]
    plt.ion()

    best_global_fitness = -10**9
    best_global_ind = None

    for gen in range(GENERATIONS):
        fits = evaluate_population(population, gen)

        fitness_values = sorted(
            zip(population, fits),
            key=lambda x: x[1],
            reverse=True
        )

        best_individual, best_fitness = fitness_values[0]

        if best_fitness > best_global_fitness:
            best_global_fitness = best_fitness
            best_global_ind = best_individual[:]

        elite_count = max(2, int(POP_SIZE * ELITE_FRAC))
        elite = [ind[:] for ind, _ in fitness_values[:elite_count]]

        top_10 = [ind for ind, _ in fitness_values[:min(10, POP_SIZE)]]
        visualize_population(top_10, gen, title_suffix=f"(best={best_fitness:.1f})")

        if simulate(best_individual) == maze.GOAL:
            print(f"Ziel erreicht in Generation {gen}, Fitness {best_fitness:.2f}")
            best_global_ind = best_individual[:]
            break

        parents = tournament_selection(population, fits, k=TOURNEY_K)

        children = []
        while len(children) < POP_SIZE - elite_count:
            p1, p2 = random.sample(parents, 2)
            child = crossover(p1, p2)
            child = mutate(child, gen)
            children.append(child)

        population = elite + children

    plt.ioff()

    print(f"Beste gefundene Fitness: {best_global_fitness:.2f}")
    plt.figure()
    visualize_population([best_global_ind], gen, title_suffix="(Best Path)")
    plt.show()


if __name__ == "__main__":
    run()