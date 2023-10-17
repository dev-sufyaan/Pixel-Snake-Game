import random, time
from typing import Tuple

class Apples:
    """
    Apples class
    :param block_size: size of the grid segments
    :param color: Apple color
    :param bounds: Window size
    :param last_apple_spawn_times: Tuple for apple spawn delays
    """
    block_size = None
    color = None
    x = 0; 
    y = 0; 
    bounds = None
    last_apple_spawn_times = None
    
    def __init__(self, block_size: int, bounds: Tuple[int, int], color: Tuple[int, int, int], last_apple_spawn_times:Tuple[str, float]):
        super().__init__()
        self.block_size = block_size
        self.bounds = bounds
        self.color = color
        self.last_apple_spawn_times = last_apple_spawn_times
        self.apple()
        
    def draw(self, game, window):
        """
        Draw all the Apples
        """
        game.draw.rect(window, self.color, (self.x, self.y, self.block_size, self.block_size))

    def apple(self):
        """
        Draw Apple
        """
        self.x, self.y = self.random_position() 
       
    def random_position(self) -> Tuple[int, int]:
        """
        Generate a random position for the apple that is within the bounds of the game
        and not on the edge of the screen.
        """
        blocks_in_x = (self.bounds[0]) // self.block_size; #32
        blocks_in_y = (self.bounds[1]) // self.block_size; #24
        
        x = random.randint(0, blocks_in_x - 1) * self.block_size #max 620
        y = random.randint(0, blocks_in_y - 1) * self.block_size #max 460
        
        if (time.time() - self.last_apple_spawn_times['high']) > float(10):
            self.last_apple_spawn_times['high'] = time.time()
        if (time.time() - self.last_apple_spawn_times['super_high']) > float(30):
            
            self.last_apple_spawn_times['super_high'] = time.time()
        
        # stop the apple from spawning on the edges
        if x == 0:
            print('move apple(edges)')
            x += self.block_size
        if x == 820:
            print('move apple(edges)')
            x -= self.block_size
        if y == 0:
            print('move apple(edges)')
            y += self.block_size
        if y == 660:
            print('move apple(edges)')
            y -= self.block_size
        return (x,y)

