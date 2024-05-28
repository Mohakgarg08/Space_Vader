# 🚀 Space Invaders 

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


## Scientific and Graphing Calculator
#### My project is a Scientific and Graphing Calculator that can calculate various problems. It can calculate basic calculations. Find the area of different shapes, graph polynomial and trigonometric expression. 

libraries used:
```
libraries 
  •math
  •Cmath
  •numpy
  •matplotlib
```

Reference
- https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.tight_layout.html#matplotlib.pyplot.tight_layout
- https://www.geeksforgeeks.org/plotting-sine-and-cosine-graph-using-matloplib-in-python/
- https://stackoverflow.com/questions/31556446/how-to-draw-axis-in-the-middle-of-the-figure
- https://stackoverflow.com/questions/62160148/in-python-what-does-this-do-tan-y-1np-difftan-y-0
- https://www.w3schools.com/python/ref_func_eval.asp


#### How the Program Works
##### Importing Libraries
``` python
import math
import cmath
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
```
This Snippet of code is used to import libraries that will be used in the program. 


##### Main Menu
```python
def main():

  while True:
    print("Enter (1) for Basic Calculations")
    print("Enter (2) for finding the area")
    print("Enter (3) for Graphing Calculator")

    calculator=input("What do you want to do? ")

    if calculator== "1":
      basic()
      break
    elif calculator=="2":
      area()
      break
    elif calculator=="3":
      graphing()
      break
    else:
      print("Invalid Input Please Try Agian")

main()
```
This snippet of code is the start of the program after running the program. This snippet of code is asking the user what they want to do; **Basic Calculator**, **area calculator**, or **Graphing Calculator**. Acordin to the user choice it will jump to that 

#### How to use my program?
- Open your Python program and run the script
- It will ask what the user wants to do basic calculations, finding area, or graphing calculator.
- Then it will ask you inputs according to your choice of what you wanted to do 
It will execute the given problem and return the user the answer or the graph.