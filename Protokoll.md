# Projektbericht: Maze Navigation mittels Genetischem Algorithmus

## Ziel des Projekts
Es wird ein genetischer Algorithmus entwickelt, der einen Agenten dazu bringt, ein zufällig generiertes Labyrinth vom Startpunkt zum Zielpunkt zu durchlaufen. Der Agent hat keine Kenntnis über die Struktur des Labyrinths und optimiert sein Verhalten rein über die Generationen hinweg.

## Motivation
Genetische Algorithmen eignen sich hervorragend für Probleme,
- bei denen keine analytische Lösung existiert,
- die eine große Suchraumkomplexität besitzen,
- und bei denen Heuristiken nötig sind, um gute Lösungen zu finden.

Ein Labyrinth erfüllt all diese Punkte:
Der Agent kennt zu Beginn weder die beste Route noch die optimale Bewegungsstrategie. Kompetitives Lernen über Fitnessbewertung und Mutation soll ihn dazu bringen, zielgerichtete Wege zu entwickeln.

---

## Aufbau des Systems

### Erzeugung des Labyrinths
Das Labyrinth wird mit einem Depth-First-Search (DFS) erzeugt:
- Start in Zelle (1,1)
- Wände bestehen aus `1`, freie Felder aus `0`

### Agentenrepräsentation
Jedes Individuum ist eine Liste von Aktionen:
0 == Rechts
1 == Unten
2 == links
3 == Hoch

Länge: `(Beispielsweise) 150 Schritte`

### Populationsparameter
| Parameter        | Wert |
|-----------------|-----:|
| Population       | 500 Individuen |
| Generationen     | 200 |
| Mutationsrate    | dynamisch (0.1 → max. 0.5) |
| Elitismus Anteil | 20 % |
| Turnierselektion | k = 8 |

---

## Fitnessfunktion
Ziele der Fitness:
- **Annäherung an das Ziel**
- **Exploration neuer Zellen**
- **Schnelles Finden des Ziels**
- **Vermeidung ineffizienten Verhaltens also zb besuchte Felder nochmal zu besuchen**

Bewertungsbestandteile:

| Verhalten                              |                 Effekt |
|---------------------------------------|-----------------------:|
| Wand getroffen                        |                     −5 |
| Neues Feld betreten                   |                    +20 |
| Zielannäherung             | +20 × ÄnderungDistance |
| Vom Ziel entfernen                    |  −10 × ÄnderungDistanz |
| Bereits besuchte Zelle       |                    −20 |
| Ziel erreicht                         |                  +1000 |
| Restliche Schritte nach Zielerreichung|        +10 pro Schritt |
| Exploration        |     +10 pro neues Feld |

Begründung:
- Frühe Generationen sollen viele Wege ausprobieren → Exploration

---

## Genetische Operatoren

### Selektion
Turnierselektion mit k=8 → starke Selektionsdrift zugunsten fitter Individuen.

### Crossover
Drei-Segment-Crossover: `[p1] + [p2] + [p1]`  

### Mutation
Mutation erhöht sich mit Generationenanzahl:
- Anfangs mehr Stabilität
- Gegen Ende mehr Variation zur Feinjustierung
→ evtl noch aus lokalen maxima entkommen

---

## Visualisierung
Für die Top-10 jeder Generation wird der Pfad eingezeichnet:
- Maze als Gitter
- Start und Ziel dargestellt
- Pfadverläufe verglichen (besten 10 werden dargestellt)



## Ergebnisse

Fitness steigt über Generationen typischerweise stark an.

Paramteter beeinflussen Ergebnis stark.

---

## Fazit
Dieses Projekt zeigt, dass genetische Algorithmen komplexe Navigationsaufgaben effizient lösen können.  
Wesentliche Erkenntnisse:

- Exploration in frühen Generationen essenziell
- Fitness muss sorgfältig austariert werden
- Elitismus schützt nur die Genotypen, nicht die Fitnessentwicklung


---

## Kernnutzen
- Veranschaulicht evolutive Optimierung in Umgebungen ohne globale Information
