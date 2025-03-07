# Bomb It Game

## Overview
Bomb It is a fun and interactive multiplayer game implemented in Python.<br>
Players place bombs strategically to destroy obstacles and opponents, with the last player standing declared the winner.

## Features
- **Custom Client-Server Architecture:** Custom-built client and server system for handling multiplayer communication.
- **Multiplayer Support:**: Multiple players with movement and interaction.
- **Message Protocol:** A custom message protocol for encoding and decoding data.
- **Multiple Screens:** Includes a main menu, instruction, game screen, and navigation between them.
- **Player Movement:** Real-time movement and bomb placement using keyboard controls.
- **Graphics:** Uses Pygame for dynamic graphics, animations, and event handling.

## How to Play
1. Run the program.
2. Choose between a **2-player** or **4-player** game mode.
3. Move your character to a clear block using:
   - **Arrow keys** (← ↑ → ↓) for movement.
   - **Space bar** to drop bombs (maximum 2 at a time).
4. Avoid losing all your lives — bombs explode in a **+ shape** pattern!
5. The last player standing wins the game.

## Technologies Used
- **Language:** Python
- **Graphics:** Pygame
- **Networking:** Socket programming (`socket`, `select`) for client-server communication
- **Concepts:** Object-Oriented Programming, Concurrency, Event-Driven Programming

## Setup and Usage
1. Clone the repository:
    ```bash
    git clone https://github.com/Fisher-Shira/Bomb-It-Game.git
2. Navigate to the project directory:
    ```bash
    cd Bomb-It-Game
3. Install dependencies using make:
    ```bash
    make install_requirements
    ```
- If make is not installed, you can use the following command to install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4. Start the server and clients:
    - For a 2-player game, open 3 terminals (1 for the server + 2 for players).
    - For a 4-player game, open 5 terminals (1 for the server + 4 for players).

    **Start the server** in the first terminal using make:
    ```bash
    make run_server
    ```
   **Start each client** in separate terminals using make:
    ```bash
    make run_client
    ```
- If make is not installed, you can manually start the server and clients:

    **Start the server** in the first terminal:
    ```bash
    python src/server.py
    ```
   **Start each client** in separate terminals:
    ```bash
    python src/client.py
    ```
5. To clean the environment (remove virtualenv):
    ```bash
    make clean

## Project Structure
- **`src/`**: Contains the Python code for all game components, including the server, client, and game logic.
- **`assets/`**: Stores game images and graphical assets.
- **`requirements.txt`**: Lists the required dependencies for the game.
