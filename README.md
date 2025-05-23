# Q-Learning Snake Game

The goal of this workshop is to use **Q-learning** to train an agent to play a classic game of snake.

A template is available: [Python](#) | [MATLAB](#)  
(*Replace `#` with actual links to the template files*)

Your task is to implement the missing functions and pieces of code in the file `template.m` or `template.ipynb`.
![image](https://github.com/user-attachments/assets/8240e6fd-7271-4a20-a106-8a15a940c4bc)

---

## Game Description

- The snake starts with length 1 and always moves forward.
- It can turn left or right.
- When it eats a fruit, it grows by 1 square.
- When it hits a wall or intersects itself, the game is over.

---

## State Representation

In the context of reinforcement learning, a **state** encodes:

1. The **direction to the goal** (fruit)
2. The **closest obstacles** relative to the snake’s head

### Direction to Goal

Direction is encoded using numbers corresponding to the following map:


### Obstacles

Obstacles in the **front**, **left**, and **right** are encoded as a 3-bit number.  
Each bit is set to 1 if there is an obstacle. For example:

- `000₂` = 0 → No obstacles
- `111₂` = 7 → Obstacles in all directions
- `010₂` = 2 → Obstacle in front only

There are **8 possible values** (0–7).

Example layout with encoding:


---

## Environment Setup

- There are **8 × 8 = 64 possible states**
- There are **3 possible actions**:
  - Turn left
  - Go forward
  - Turn right

---

## Learning Policy

Use the **Epsilon-Greedy** algorithm:

- With probability **epsilon**, select a random action (exploration)
- Otherwise, select the best action based on current **Q-values**

---

## Goal

Tune the following parameters for best performance:

- `episodes`
- `learning_rate`
- `discount`
- `start_exploration`
- `end_exploration`

### Final Challenge

**What is the highest score your snake can achieve?**
