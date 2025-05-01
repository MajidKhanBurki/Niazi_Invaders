# Niazi Invaders

**Niazi Invaders** is a fun little retro-style arcade game inspired by classic space shooters — but with a hilarious twist: the enemies are based on a picture of my friend **Muhammad Abdullah Niazi**.

This project was created just for fun using **Python** and **Pygame**, and it's a great intro-level example for anyone looking to learn about 2D game development in Python.

## 🎮 Gameplay

- You control a spaceship that can move left and right.
- Shoot bullets to destroy incoming enemies (aka Niazis).
- Score points for each successful hit.
- If an enemy reaches too far down, it’s **Game Over!**

## 📷 Media

The game uses custom assets like a background image, bullets, enemy sprites, and audio effects — including one featuring a friend's actual photo as the main invader.

## 🛠️ How to Run

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/niazi-invaders.git
cd niazi-invaders
```

### 2. Install dependencies

Make sure you have Python 3 installed. Then run:

```bash
pip install -r requirements.txt
```

### 3. Run the game

```bash
python main.py
```

Make sure you have all the required media files in the correct folders:

```
media/
├── audio/
│   ├── Game_Start.mp3
│   ├── Game_Over.mp3
│   └── laser.mp3
├── background/
│   └── background.png
└── icons/
    ├── bullet.png
    ├── niazi_invader.png
    └── ship.png
```

> **Note**: The game must be run from the directory where `main.py` is located and all media files are correctly placed under the `media/` folder.

## 💡 Features

- Smooth movement and collision detection
- Background music and sound effects
- Dynamic enemy behavior
- Custom artwork and sounds

## 🧑‍🎨 Author

Developed by **Majid Khan Burki** — built with love, laughs, and a a lot of caffeine.