# Copilot Instructions for Tetris Game

## Project Overview
This workspace contains a Python implementation of the classic Tetris game using Pygame. The codebase is structured as a single-script application with game logic, rendering, and user input handling.

## Architecture
- **Single-file application**: `Tetris.py` contains the entire game implementation
- **Pygame framework**: Handles graphics, sound, and input events
- **Game loop structure**: Processes input, updates game state, renders graphics, and manages timing

## Key Components
- **Game board**: Grid-based play area for tetromino placement
- **Tetromino pieces**: Seven standard Tetris shapes with rotation and movement
- **Scoring system**: Points for lines cleared, levels, and speed increases
- **Input handling**: Keyboard controls for piece movement and rotation

## Running the Application
Execute the main script with Python:
```bash
python Tetris.py
```
- Use arrow keys for movement, space/up for rotation, down for soft drop
- Game ends when pieces reach the top; restart by running again

## Dependencies
- **Pygame**: Install via `pip install pygame`
- **Python 3.x**: Standard library for random number generation and timing

## Code Patterns
- **Game state management**: Use variables for current piece, board state, score, and level
- **Collision detection**: Check boundaries and occupied cells before piece placement
- **Line clearing**: Scan rows for completion and remove full lines, shifting above rows down
- **Piece generation**: Random selection from tetromino bag system for fair distribution

## Development Workflow
- Edit `Tetris.py` directly in VS Code
- Run via terminal: `python .\Tetris.py`
- Debug by printing game state variables or using Pygame's event logging
- Test gameplay manually by running and playing the game

## File Structure
- `Tetris.py`: Main game script containing all logic and rendering