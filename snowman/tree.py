from PPlay.gameimage import GameImage
from random import randint


class Twig:
    def __init__(self, window, branch, side):
        self.window = window
        self.branch = branch
        self.side = side
        self.angle = 200 if side == 1 else 160
        self.branch.set_position(self.branch.get_x(), self.branch.get_y() - 64)

    def update(self):
        if self.side == 1:
            self.branch.set_position(self.branch.get_x() + (2000 * self.window.delta_time()), self.branch.get_y())
            self.angle -= 270 * self.window.delta_time()
        else:
            self.branch.set_position(self.branch.get_x() - (2000 * self.window.delta_time()), self.branch.get_y())
            self.angle += 270 * self.window.delta_time()

    def draw(self):
        self.branch.draw_rotated(self.angle)

    def off_screen(self):
        return self.branch.get_x() > 300 or self.branch.get_x() < -300


class Branch:
    def __init__(self, side, x, y):
        image_paths = ('sprite/branches/right1.png',
                       'sprite/branches/left.png',
                       'sprite/branches/00.png')
        self.texture = GameImage(image_paths[side])
        self.side = side
        self.texture.set_position(x, y)

    def set_position(self, x, y):
        self.texture.set_position(x, y)

    def get_side(self):
        return self.side

    def draw(self):
        self.texture.draw()

    def draw_rotated(self, angle):
        self.texture.draw_rotated(angle)

    def get_x(self):
        return self.texture.x

    def get_y(self):
        return self.texture.y


class Tree:
    def __init__(self, window):
        self.hit_time = 0
        self.window = window
        self.descend = False

        self.last_branch_side = 'middle'
        self.flying_branches = []
        self.branches = []
        self.branches.append(Branch(2, 0, 512 - 128))
        self.last_branch = 2
        for i in range(1, 7):
            side = randint(0, 2)
            if self.branches[-1].get_side() != 2 and self.branches[-1].get_side() != side:
                side = 2
            self.branches.append(Branch(side, 0, 512 - 128 - i * 64))
            self.last_branch = side

    def draw(self):
        for branch in self.branches:
            branch.draw()
        for branch in self.flying_branches:
            branch.draw()

    def hit(self, side):
        if not self.descend:
            self.hit_time = self.window.total_time
            self.descend = True
            branch_side = self.branches[0].get_side()
            branch_side_2 = self.branches[1].get_side()
            self.flying_branches.append(Twig(self.window, self.branches.pop(0), side))
            side = randint(0, 2)
            if self.branches[-1].get_side() != 2 and self.branches[-1].get_side() != side:
                side = 2
            self.branches.append(Branch(side, 0, -64))
            self.last_branch = side
            return branch_side, branch_side_2

    def update(self):
        if self.descend and self.window.total_time - self.hit_time > 30:
            for branch in self.branches:
                branch.set_position(0, branch.get_y() + 64)
            self.descend = False
        tbd = []
        for i, branch in enumerate(self.flying_branches):
            if branch.off_screen():
                tbd.append(i)
            branch.update()
        for j in reversed(tbd):
            del self.flying_branches[j]
