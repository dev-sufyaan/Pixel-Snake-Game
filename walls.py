
class Wall:
    """
    Wall Class
    :param block_size: size of the grid segments
    :param bounds: Window size
    :param color: Wall color
    """
    block_size = None
    color = None
    x = 0
    y = 0
    bounds = None

    def __init__(self, block_size, bounds, color):
        super().__init__()
        self.block_size = block_size
        self.bounds = bounds
        self.color = color
        self.wall_spawned = [False, False, False, False]
        self.spawn()
    
    def spawn(self):
        """
        Wall setup
        """
        self.body = [{'x': 19, 'y': 12},{'x': 18, 'y': 12},{'x': 17, 'y': 12}]
        self.body2 = [{'x': 9, 'y': 10},{'x': 9, 'y': 11},{'x': 9, 'y': 12},{'x': 10, 'y': 10},{'x': 10, 'y': 12}]
        self.body3 = [{'x': 17, 'y': 17},{'x': 18, 'y': 17},{'x': 19, 'y': 17}]
        self.body4 = [{'x': 4, 'y': 18},{'x': 4, 'y': 19},{'x': 4, 'y': 20},{'x': 5, 'y':18},{'x': 5, 'y': 20}]

        self.all_walls = [self.body, self.body2, self.body3, self.body4]

    def draw(self, game, window, wall):
        """
        Draw the wall
        """

        wall_index = wall - 1
        if 0 <= wall_index < len(self.all_walls):
            wall_segments = self.all_walls[wall_index]
            for coord in wall_segments:
                self.x = coord['x'] * self.block_size
                self.y = coord['y'] * self.block_size
                wall_segment_rect = game.Rect(self.x, self.y, self.block_size, self.block_size)
                game.draw.rect(window, self.color, wall_segment_rect)
            self.wall_spawned[wall_index] = True

    def check_for_apples(self, apple, happle, shapple):
        """
        Check walls for apples to prevent them spawing there
        """
        for wall_segements in self.all_walls:
            for coord in wall_segements:
                if apple.x == coord['x'] * self.block_size and apple.y == coord['y'] * self.block_size:
                    print('Found apple')
                    apple.apple()
                if happle.x == coord['x'] and happle.y == coord['y']:
                    print('Found apple')
                    happle.apple()
                if shapple.x == coord['x'] and shapple.y == coord['y']:
                    print('Found apple')
                    shapple.apple()

    def check_for_snake(self, player):
        """
        Checks both walls for snake and use spawned staus to prevent premature death CAUTION: REQUIERED FOR BOTH WALLS
        """
        phead = player.body[-1]
        for i, wall_spawned in enumerate(self.wall_spawned):
            if wall_spawned:
                wall_segments = self.all_walls[i]
                for coord in wall_segments:
                    if phead[0] == coord['x'] * self.block_size and phead[1] == coord['y'] * self.block_size:
                        print (f'hit wall{i+1}')
                        return True
                    
        return False
