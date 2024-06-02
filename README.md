# 🚀 Space vaders 

> **Introduction**
>
> Welcome to **Space Invaders**! This game was created as a school project to apply our programming skills and have some fun. The game script was written by two GOATS.

## FAQ

> **Q: What is Space Invaders?**
>
> A: Space Invaders is a somewhat modern twist on the classic arcade game where you defend the Earth from waves of alien invaders.

> **Q: How do I play the game?**
>
> A: Use the arrow keys to move your spaceship and press the space bar to shoot. Collect power-ups for temporary boosts and defeat all enemies in a wave to progress.

> **Q: Who made this game?**
>
> A: The game script was written by Kabir and Mohak

> **Q: Can I play this game with a controller?**
>
> A: Currently, the game supports keyboard controls only.

> **Q: How do I collect power-ups?**
>
> A: Power-ups appear randomly on the screen. Move your spaceship over them to collect, intervals are at around 5 seconds.

> **Q: What happens when I run out of lives?**
>
> A: The game will end, and you can restart to try again for a higher score.


#### This game is a replica of `**Space Invader**` but it had been modified. So, the game can be more challenging and Fun

libraries used:
```
libraries 
  •pygame
  •random
  •sys
```

Reference
-  https://www.pygame.org/docs/

#### How the Program Works
##### Importing Libraries
``` python
import pygame
import random
import sys
```
This Snippet of code is used to import libraries that will be used in the program. 


##### Classes 
```python
class Player(pygame.sprite.Sprite):
class Enemy(pygame.sprite.Sprite):
class Finalboss(Enemy):
class Bullet(pygame.sprite.Sprite):
class Powerup(pygame.sprite.Sprite):
class ScoreText(pygame.sprite.Sprite):
class EnemyWave:
```
These lines of code are the where the diferent classes are being construted for example for the ``player`` class, ``enemy`` class. The player class is were constructes the code for the player shuch as its lives, size and etc.

#### How to use my program?
- Open your Python program 
- Depending on the software used you may have to **``pip install pygame``**  and run the script
- it will show the starting page. If **``c``** is pressed on the keybaord it will take you to the controls of the game if **``enter``** is pressed it will take you to the game.
- Then the game begins!
- **HAVE FUN !!!!!!!!!!!!!!!!!**