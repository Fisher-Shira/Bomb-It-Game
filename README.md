# Bomb It Game

## Overview
This is a Bomb It Game! implemented in Python.<br>
This is a fun and interactive game where players place bombs and aim to destroy obstacles and other players.

## Features
- **Custom Client-Server Architecture:** Custom-built client and server system for handling multiplayer communication.
- **Multiplayer support:**: Multiple players with movement and interaction.
- **Message Protocol:** A custom message protocol for encoding and decoding data.
- **Multiple Screens:** Includes a main menu, instruction, game screen, and navigation between them.
- **Player Movement:** Real-time movement and bomb placement using keyboard controls.
- **Graphics:** Uses Pygame for dynamic graphics, animations, and event handling.

## How to Play
1. Run the program.
2. Choose 2/4 Players (according to the open terminals number).
3. Control the player movement to a clear block using the **left**, **right**, **up** and **down** arrow keys.
4. Press the **space** bar to drop a bomb (maximum 2 at the same time).
5. Avoid losing all your lives by staying clear of bombs and explosions (+ shape explosion).
6. The last player remaining after all others have lost their lives wins the game.

## Technologies Used
- **Language:** Python
- **Graphics:** Pygame
- **Socket Programming:** socket (client-server communication), select (monitoring and managing socket events)
- **Concepts:** Classes, Networking, Concurrency, Event-Driven Programming

## Installation
1. Setup and Usage:
    ```bash
    git clone https://github.com/Fisher-Shira/Bomb-It-Game.git
    ```
2. Navigate to the project directory:
    ```bash
    cd Bomb-It-Game
    ```
3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4. Open 3 terminals for 2 players / 5 terminals for 4 players and execute the following commands in each:
    **Terminal 1**
    ```bash
    python .\src\server.py
    ```
    **Terminal 2 - 5**
    ```bash
    python .\src\client.py
    ```

## Project Structure
- **`src/`**: Contains the pythn code for all game components, including the server, client, and game logic.
- **`Images/`**: Folder inside src folder that cintain game images.
- **requirements.txt**: Requirements file
