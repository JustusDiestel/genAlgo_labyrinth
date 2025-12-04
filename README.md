# Genetischer Algorithmus – Maze Navigation

Dieses Projekt implementiert einen genetischen Algorithmus (GA), der lernt, ein Labyrinth autonom zu lösen.
Dabei entwickeln sich über Generationen hinweg Pfade, die vom Startpunkt zum Ziel führen.


![Maze Beispiel](Bildschirmfoto 2025-12-04 um 11.04.26.png)
---

## Funktionsweise

Jedes Individuum (Chromosom) steht für einen **Bewegungsplan** aus diskreten Aktionen:
- 0 = oben
- 1 = rechts
- 2 = unten
- 3 = links

Der genetische Algorithmus optimiert die Sequenzen durch:
- **Fitness-Selektion**
- **Crossover**
- **Mutation**
- **Elitismus / Turnierselektion**

Das Ziel: möglichst schnell und ohne unnötige Umwege den Goal-Point erreichen.

---

## Fitness-Funktion

Berücksichtigt werden unter anderem:
- Distanzverringerung zum Ziel
- Belohnung für neu entdeckte Felder
- Strafe für Wände und Backtracking
- Zusätzliche Belohnung bei Zielerreichung

---

## Maze-Generierung

Das Labyrinth wird zufällig per DFS generiert und anschließend durch zusätzliche "Tunnels" ergänzt,
um **mehrere Lösungen** zu ermöglichen und lokale Minima zu reduzieren.

---

## Ausführung

Starten des Trainings:

```bash
python ga.py
```

Während der Laufzeit wird die aktuelle Population visuell dargestellt.
Das Endergebnis wird nach Abschluss in einem Plot angezeigt.

---

## Einstellungen & Parameter

Die wichtigsten Parameter befinden sich in `ga.py`:

| Parameter | Bedeutung |
|----------|-----------|
| POP_SIZE | Größe der Population |
| STEPS | Anzahl an Aktionen pro Individuum |
| GENERATIONS | Trainingsgenerationen |
| MUT_RATE | Mutationsrate |
| Fitness-Gewichte | Anpassung von Exploration/Exploitation |

---

## Fortschritt

- Ziel: Robuste Navigation in komplexeren Mazes
- Visualisierung und Metriken für Konvergenzanalyse geplant

