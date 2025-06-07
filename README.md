# 🔴⚪ Smart Connect 4 – AI with Minimax & Genetic Algorithm

An advanced **AI-powered Connect Four** game built in **Python**, combining two intelligent strategies:  
- A classic **Minimax algorithm with Alpha-Beta pruning**  
- A **Genetic Algorithm-based AI agent** that evolves strategies over time.

Includes a **graphical user interface (GUI)** that supports Human vs AI, AI vs AI, and different AI vs AI strategies for comparison and experimentation.

---

## 🧩 Motivation

This project explores two different paradigms of artificial intelligence:
- **Search-based decision-making** using Minimax with Alpha-Beta pruning
- **Evolutionary computation** using Genetic Algorithms

The goal is to compare these strategies in terms of performance, decision quality, and user experience, all wrapped into a playable and visual Connect Four environment.

---

## 🧠 AI Methods Implemented

### 1. Minimax with Alpha-Beta Pruning
- Depth-limited recursive search
- Optimal decision-making based on game tree evaluation
- Efficient pruning of unnecessary branches to improve performance

### 2. Genetic Algorithm (GA)
- Chromosomes represent game-playing strategies
- Fitness function evaluates game success
- Evolution through crossover, mutation, and selection
- AI improves over generations through natural selection

---

## 🕹️ Features

- 👤 **Human vs AI**: Play against the Minimax or GA-based bot
- 🤖 **AI vs AI**: Let both agents battle and compare strategies
- 🧬 **Trainable GA Agent**: GA agent evolves and learns over time
- 🖥️ **Graphical UI**: Built using `Pygame`, offering interactive and visual feedback
- 📈 **Modular AI Selection**: Easily switch between AI strategies in code

---

## 🔧 Technologies Used

- **Python 3**
- **Pygame** – for GUI and event handling
- **NumPy** – for matrix operations and chromosome manipulation
- **Custom-built AI logic** – for both Minimax and Genetic strategies
