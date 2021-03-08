# Pacman-game

I want to implement a clever factor that takes control of the pacman or one of the spirits. The `Agent` class is built for this purpose. At each stage, the game engine calculates the status of all game elements, and then by calling the `getAction` method from this class and also resting the state of the ground on it, the player makes a dimensional motion. The game engine applies this process to all the existing factors (Pekman and all the spirits, respectively). Thus, one stage of the game is passed.

<img src="https://github.com/mahsawz/Pacman-game/blob/main/pacman-image.png" width="450" height="200">

Here, I implement a factor that at each stage, using the Minimax algorithm, obtains the score of all permissible moves and then selects the best one. ([adversarialAgents.py](https://github.com/mahsawz/Pacman-game/blob/main/adversarialAgents.py) -> `method minimax() in MinimaxAgent class `)

source: http://ai.berkeley.edu/project_overview.html
