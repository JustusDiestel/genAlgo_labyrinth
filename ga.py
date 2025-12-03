import random
import numpy as np
import matplotlib.pyplot as plt
from maze import Maze

POP_SIZE = 20
STEPS = 1000
MUT_RATE = 0.1
GENERATIONS = 100

maze = Maze()

def create_individual():
    return [random.randrange(4) for _ in range(STEPS)]

def simulate(ind):
    pos = maze.START
    for m in ind:
        pos = maze.move(pos, m)
        if pos == maze.GOAL:
            break
    return pos

def fitness(ind):
    pos = maze.START
    score = 0
    visited = set([pos])
    best_dist = np.linalg.norm(np.array(pos) - np.array(maze.GOAL))

    for step, m in enumerate(ind):
        new_pos = maze.move(pos, m)
        d_old = np.linalg.norm(np.array(pos) - np.array(maze.GOAL))
        d_new = np.linalg.norm(np.array(new_pos) - np.array(maze.GOAL))

        if new_pos == pos:  # wall
            score -= 5
        else:
            score += 1  # movement reward

        if new_pos in visited:
            score -= 2  # avoid loops
        else:
            visited.add(new_pos)

        # reward actual progress
        if d_new < d_old:
            score += (d_old - d_new) * 10

        # punish going back
        else:
            score -= (d_new - d_old) * 5

        pos = new_pos
        best_dist = min(best_dist, d_new)

        if pos == maze.GOAL:
            score += 1000
            score += (STEPS - step) * 2  # reward faster finish
            break

    # global final reward = how near we got
    score += max(0, 200 - best_dist * 10)

    return score

def select(elite):
    return [e[:] for e in elite]

def crossover(p1, p2):
    cut1 = random.randint(0, STEPS // 2)
    cut2 = random.randint(STEPS // 2, STEPS)
    child = p1[:cut1] + p2[cut1:cut2] + p1[cut2:]
    return child

def mutate(ind):
    for i in range(STEPS):
        if random.random() < MUT_RATE:
            if random.random() < 0.5:
                ind[i] = random.randrange(4)
            else:
                # local directional bias
                ind[i] = (ind[i] + random.choice([-1, 1])) % 4
    return ind

def visualize_population(pop, gen):
    plt.imshow(maze.grid, cmap='gray')
    for ind in pop:
        pos = maze.START
        xs, ys = [pos[1]], [pos[0]]
        for m in ind:
            pos = maze.move(pos, m)
            xs.append(pos[1])
            ys.append(pos[0])
            if pos == maze.GOAL:
                break
        plt.plot(xs, ys, linewidth=1)
        plt.scatter(xs[-1], ys[-1], c="red", s=40)

    plt.scatter(maze.START[1], maze.START[0], c="blue", s=100)
    plt.scatter(maze.GOAL[1], maze.GOAL[0], c="green", s=100)
    plt.title(f"Generation {gen}")
    plt.pause(0.8)
    plt.clf()

def run():
    pop = [create_individual() for _ in range(POP_SIZE)]
    plt.ion()

    for gen in range(GENERATIONS):
        visualize_population(pop, gen)

        # Evaluate fitness once per generation and keep top 4 as elite
        fitness_values = [(ind, fitness(ind)) for ind in pop]
        fitness_values.sort(key=lambda x: x[1], reverse=True)

        elite = [fv[0][:] for fv in fitness_values[:4]]  # Top 4 survive

        parents = select(elite)
        children = []

        while len(children) < POP_SIZE - len(elite):
            p1, p2 = random.sample(parents, 2)
            children.append(mutate(crossover(p1, p2)))

        pop = elite + children

    plt.ioff()
    visualize_population(pop, GENERATIONS)
    plt.show()

if __name__ == "__main__":
    run()