def worlds(level):
    """
    The function `worlds` returns a tuple containing a 2D list representing a game world and a tuple
    representing the starting position of the player character, based on the input level.
    
    :param level: The level parameter is used to determine which world to generate. If level is 1, it
    will generate the first world. If level is 2, it will generate the second world
    :return: a tuple containing the world grid and the starting position for the player.
    """
    world = []
    start = (0, 0)

    if level == 1:
        world = [
            [6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,6,0,0,5],
            [0,0,0,0,0,0,0,0,6,0,2,0,0,2,2,2],
            [0,0,0,6,0,0,2,2,4,4,4,4,4,1,1,1],
            [0,0,0,3,2,2,1,1,0,0,0,0,0,1,1,1],
            [2,2,2,2,1,1,1,1,1,1,1,1,1,1,1,1],
        ]

        start = (60, 420)
    elif level == 2:
        world = [
            [6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,6,0,0,0],
            [0,0,0,6,0,0,6,0,0,6,0,0,0,0,0,5],
            [2,4,4,2,4,4,2,4,4,2,4,4,2,4,4,2],
            [1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        ]

        start = (0, 360)
    
    return (world, start)

def total():
    """
    The function "total" calculates the total number of levels in a game by incrementing the level count
    until there are no more worlds.
    :return: the value of the variable "count".
    """
    level = 1
    count = 0

    while level:
        if not worlds(level)[0]:
            level = 0
        else:
            level += 1
            count += 1
    
    return count
