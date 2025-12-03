import random
import numpy as np
import matplotlib.pyplot as plt
from maze import Maze

# ==========================
# Hyperparameter
# ==========================

POP_SIZE     = 100     # Populationsgröße
STEPS        = 200     # maximale Schrittzahl pro Individuum
MUT_RATE     = 0.1     # Basis-Mutationsrate
GENERATIONS  = 100     # maximale Generationen

ELITE_FRAC   = 0.10    # Anteil der Elite (Top 10%)
TOURNEY_K    = 5       # Turniergröße für Selektion

maze = Maze()


# ==========================
# Hilfsfunktionen
# ==========================

def create_individual():
    """Erzeugt ein Individuum als Liste aus Moves (0..3)."""
    return [random.randrange(4) for _ in range(STEPS)]


def simulate(ind):
    """Simuliert eine Policy und gibt die Endposition zurück."""
    pos = maze.START
    for m in ind:
        pos = maze.move(pos, m)
        if pos == maze.GOAL:
            break
    return pos


def euclidean_dist(a, b):
    return np.linalg.norm(np.array(a) - np.array(b))


# ==========================
# Fitnessfunktion
# ==========================

def fitness(ind):
    """
    Fitness orientiert sich stark an:
    - Zielerreichung + Schnelligkeit
    - Verringerung der Distanz zum Ziel
    - leichte Belohnung für neue Felder
    - Strafung für Wände und Weg vom Ziel weg
    """
    pos = maze.START
    visited = set([pos])
    score = 0.0

    best_dist = euclidean_dist(pos, maze.GOAL)

    for step, m in enumerate(ind):
        new_pos = maze.move(pos, m)
        d_old = euclidean_dist(pos, maze.GOAL)
        d_new = euclidean_dist(new_pos, maze.GOAL)
        delta = d_old - d_new  # >0: näher ans Ziel, <0: weiter weg

        # Wandkollision
        if new_pos == pos:
            score -= 5.0
        else:
            # leichtes Noveltity-Reward
            if new_pos not in visited:
                score += 1.0
                visited.add(new_pos)

            # Richtungs-Reward
            score += delta * 80.0
            if delta < 0:
                # zusätzliche Strafe, wenn man sich entfernt
                score += delta * 40.0

        best_dist = min(best_dist, d_new)
        pos = new_pos

        # Ziel erreicht: großer Bonus + Speed-Bonus
        if pos == maze.GOAL:
            score += 5000.0
            score += (STEPS - step) * 10.0
            return score

    # Wenn Ziel nicht erreicht wird: partieller Reward nach bester Distanz
    score += max(0.0, 1000.0 - best_dist * 100.0)

    return score


# ==========================
# Selektion, Crossover, Mutation
# ==========================

def evaluate_population(pop):
    """Berechnet Fitness für alle Individuen."""
    return [fitness(ind) for ind in pop]


def tournament_selection(pop, fits, k=TOURNEY_K):
    """
    Turnierselektion: k zufällige Individuen, bestes gewinnt.
    Gibt eine neue Elternliste zurück.
    """
    n = len(pop)
    parents = []
    for _ in range(n):
        candidates_idx = random.sample(range(n), k)
        best_idx = max(candidates_idx, key=lambda i: fits[i])
        parents.append(pop[best_idx][:])
    return parents


def crossover(p1, p2):
    """Einfacher 2-Punkt-Crossover."""
    cut1 = random.randint(0, STEPS // 2)
    cut2 = random.randint(STEPS // 2, STEPS)
    child = p1[:cut1] + p2[cut1:cut2] + p1[cut2:]
    return child


def mutate(ind, gen):
    """
    Adaptive Mutation:
    - Start: eher konservativ (MUT_RATE)
    - Ende: stärker, um aus lokalen Optima zu entkommen
    """
    # dynamische Rate bis max. 0.5
    dynamic_rate = MUT_RATE + (gen / max(1, GENERATIONS)) * 0.25
    rate = min(0.5, dynamic_rate)

    for i in range(STEPS):
        if random.random() < rate:
            # 50%: kompletter Move-Randomize, 50%: lokale Änderung (−1/+1)
            if random.random() < 0.5:
                ind[i] = random.randrange(4)
            else:
                ind[i] = (ind[i] + random.choice([-1, 1])) % 4
    return ind


# ==========================
# Visualisierung
# ==========================

def visualize_population(pop, gen, title_suffix=""):
    """
    Zeichnet das Maze + Trajektorien der Individuen.
    Hier: nur die besten paar Individuen, um Overdraw zu vermeiden.
    """
    plt.imshow(maze.grid, cmap="gray")

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
        plt.scatter(xs[-1], ys[-1], s=20)

    # Start/Goal hervorheben
    plt.scatter(maze.START[1], maze.START[0], s=100, marker="o")
    plt.scatter(maze.GOAL[1], maze.GOAL[0], s=100, marker="x")

    plt.title(f"Generation {gen} {title_suffix}")
    plt.pause(0.5)
    plt.clf()


# ==========================
# Hauptschleife
# ==========================

def run():
    pop = [create_individual() for _ in range(POP_SIZE)]
    plt.ion()

    best_global_fitness = float("-inf")
    best_global_ind = None

    for gen in range(GENERATIONS):
        fits = evaluate_population(pop)

        # Sortiere nach Fitness
        fitness_values = sorted(
            zip(pop, fits),
            key=lambda x: x[1],
            reverse=True
        )

        best_ind, best_fit = fitness_values[0]

        # global best updaten
        if best_fit > best_global_fitness:
            best_global_fitness = best_fit
            best_global_ind = best_ind[:]

        # Elite bestimmen
        elite_count = max(2, int(POP_SIZE * ELITE_FRAC))
        elite = [ind[:] for ind, _ in fitness_values[:elite_count]]

        # Visualisierung: nur Top 10
        top_for_vis = [ind for ind, _ in fitness_values[:min(10, POP_SIZE)]]
        visualize_population(top_for_vis, gen, title_suffix=f"(best={best_fit:.1f})")

        # Early Stop, wenn das aktuelle beste Individuum das Ziel erreicht
        if simulate(best_ind) == maze.GOAL:
            print(f"Ziel erreicht in Generation {gen}, Fitness {best_fit:.2f}")
            best_global_ind = best_ind[:]
            break

        # Eltern per Turnierselektion aus der ganzen Population
        parents = tournament_selection(pop, fits, k=TOURNEY_K)

        # Kinder erzeugen, bis Population wieder voll ist
        children = []
        while len(children) < POP_SIZE - elite_count:
            p1, p2 = random.sample(parents, 2)
            child = crossover(p1, p2)
            child = mutate(child, gen)
            children.append(child)

        pop = elite + children

    plt.ioff()

    # finale Visualisierung des global besten Pfades
    print(f"Beste gefundene Fitness: {best_global_fitness:.2f}")
    plt.figure()
    visualize_population([best_global_ind], gen, title_suffix="(Best Path)")
    plt.show()


if __name__ == "__main__":
    run()