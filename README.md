# Pygame-CE Game

**Author:** Muhammed Emir Akgül

This project is a Top-Down-Shooter developed using [Pygame-CE](https://pygame-ce.org/) for the Game-Logic and [Tiled](https://www.mapeditor.org/) for the own custom designed map. The player controls a character that can move, sprint, and shoot.

## Demonstration on YouTube
[***HERE THE LINK TO VIDEO***]

## Controls

- **Move:** `W`, `A`, `S`, `D`  
- **Sprint:** `Shift` (hold)  
- **Shoot:** Left click  

# Play the Game - Step by Step installation

### Requirements

- [Python 3.10](https://www.python.org/downloads/) or higher
- Pygame-CE
- Pytmx
- [Git](https://git-scm.com/install/)
## Windows

#### Installing Pygame-CE

1. Open Command Prompt (CMD) or PowerShell. (Windows Key + R, then type CMD)
2. Install Pygame-CE and Pytmx using pip (just copy paste it and press enter):

```bash
pip install pygame-ce
```
```bash
pip install pytmx
```
If this doesnt work, try this:
```bash
python -m pip install pygame-ce
```
```bash
python -m pip install pytmx
```
3. Test if installation was successful

```bash
python -m pygame.examples.aliens
```
4. Now Install/Clone this Repository

```bash
git clone https://github.com/29cmtruedamage/Shooter-Game-Project.git
```
5. Finally, start the game
   
```bash
python -m main
```
## MacOS

#### Installing Pygame-CE

1. Open Terminal
2. Install Pygame-CE and Pytmx using pip3 (just copy paste it and press enter):

```bash
pip3 install pygame-ce
```
```bash
pip3 install pytmx
```
If this doesnt work, try this:
```bash
python3 -m pip3 install pygame-ce
```
```bash
python3 -m pip3 install pytmx
```
3. Test if installation was successful

```bash
python3 -m pygame.examples.aliens
```
4. Now Install/Clone this Repository

```bash
git clone https://github.com/29cmtruedamage/Shooter-Game-Project.git
```
5. Finally, start the game
   
```bash
python3 -m main
```


## Project Sourcecode Structure

Shooter-Game-Project/

├── main.py          

├── characters.py

├── sprites.py

├── spritegroups.py

├── globals.py

├── init.py









