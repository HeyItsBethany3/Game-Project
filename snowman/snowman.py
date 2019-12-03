from PPlay.gameimage import GameImage


class Snowman:
    def __init__(self, Tree, side):
        self.side = side
        self.Tree = Tree
        self.sprites = (GameImage('sprite/snowman/1.png', 0, 512 - 150),
                        GameImage('sprite/snowman/1.png', 0, 512 - 150),
                        GameImage('sprite/snowman/4.png', 0, 512 - 150),
                        GameImage('sprite/snowman/4.png', 0, 512 - 150))
        self.knock = False
        self.current_sprite = 0
        self.time_punch = 0

    def get_side(self):
        return 1 if self.side == 'left' else 0

    def hit(self, side):
        if self.side != side:
            if self.current_sprite == 0:
                self.current_sprite = 2
            else:
                self.current_sprite = 0
            self.knock = True
            self.time_punch = self.Tree.total_time
        else:
            self.knock = True
            self.time_punch = self.Tree.total_time
        self.side = side

    def draw(self):
        self.sprites[self.current_sprite].draw()

    def update(self):
        if self.knock:
            if self.Tree.total_time - self.time_punch > 5:
                if self.side == 'left':
                    self.current_sprite = 1
                else:
                    self.current_sprite = 3
            if self.Tree.total_time - self.time_punch > 50:
                self.knock = False
                if self.side == 'left':
                    self.current_sprite = 0
                else:
                    self.current_sprite = 2
