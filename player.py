from collections import deque
from typing import Tuple

class Direction(Tuple[int, int]):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

class Player:
    """
    Player class
    :param block_size: size of the grid segments
    :param color: User defined outer player color
    :param incolor: User defined inner player color
    :param bounds: Window size
    """
    length = None
    direction = None
    body = None
    block_size = None
    color = None
    incolor = None
    bounds = None

    def __init__(self, block_size: int, bounds: Tuple[int, int], color: Tuple[int, int, int], incolor: Tuple[int, int, int]):
        super().__init__()
        self.block_size = block_size
        self.bounds = bounds
        self.color = color
        self.incolor = incolor
        self.score = int(0)

        self.next_head_lookup = {
        Direction.UP: (0, -block_size),
        Direction.DOWN: (0, block_size),
        Direction.LEFT: (-block_size, 0),
        Direction.RIGHT: (block_size, 0) 
    }

        self.respawn()

    def respawn(self):
        """
        Snake setup
        """
        self.length = 3
        self.body = deque([[20,20],[20,40],[20,60]])
        self.direction = Direction.DOWN

    def draw(self, game, window, ):
        """
        Draw all segments of the snake
        """
        for segment in self.body:
            wormsegmentrect = (segment[0], segment[1], self.block_size, self.block_size)
            game.draw.rect(window, self.color, wormsegmentrect)
            innersegmentrect = (segment[0] + 4, segment[1] + 4, self.block_size - 8, self.block_size - 8)
            game.draw.rect(window, self.incolor, innersegmentrect)

    def steer(self, direction: Direction):
        """
        Set direction 
        """
        if direction != self.direction and direction[0] + self.direction[0] != 0 and direction[1] + self.direction[1] != 0:
            self.direction = direction
        
    def move(self, direction: Direction):
        """
        Snake movement using direction EMUM
        """
        curr_head = self.body[-1]
        
        next_head_offset = self.next_head_lookup[direction]
        next_head = (curr_head[0] + next_head_offset[0], curr_head[1] + next_head_offset[1])
        
        self.body.append(next_head)

        if self.length < len(self.body):
            self.body.popleft()

    def eat(self):
        """
        Eating food makes snake bigger
        """
        self.length += 1
    
    def check_for_apple(self, apple):
        """
        Checks for normal apples and increments score
        """
        head = self.body[-1]

        if head[0] == apple.x and head[1] == apple.y:
            self.eat()
            self.score += 1
            apple.apple()
    
    def check_for_happle(self, happle, difficulty: str):
        """
        Checks for high apples score moved to main to prevent bug
        """
        head = self.body[-1]
        if head[0] == happle.x and head[1] == happle.y:
            self.eat()
            if difficulty == 'EASY' or 'MEDIUM':
                self.score += 2
            else:
                self.score += 1
            happle.apple()
            return True
        return False
    
    def check_for_shapple(self, shapple, difficulty: str):
        """
        Checks for super high apples score moved to main to prevent bug
        """
        head = self.body[-1]
        if head[0] == shapple.x and head[1] == shapple.y:
            self.eat()
            if difficulty == 'EASY' or 'MEDIUM':
                self.score += 5
            else:
                self.score += 2
            shapple.apple()
            return True
        return False


    def check_tail_collision(self):
        """
        Cannibal detection
        """
        head = self.body[-1]
        has_eaten_tail = False

        for i in range(len(self.body) - 1): 
            segment = self.body[i]
            if head[0] == segment[0] and head[1] == segment[1]:
                has_eaten_tail = True
        return has_eaten_tail
    
    def check_bounds(self):
        """
        The edge kills
        """
        head = self.body[-1]
        if head[0] >= self.bounds[0]:
            print('check bounds')
            return True
        if head[1] >= self.bounds[1]:
            print('check bounds')
            return True

        if head[0] < 0:
            return True
        if head[1] < 0:
            return True  

        return False
    