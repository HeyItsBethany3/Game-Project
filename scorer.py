import pygame


class Scorer:
    
    health = 100
    points = 0
    multiplier = 1
    life_loss_rate = 3.3
        
    def __init__(self, window):
        self.window = window
        
    def add_points(self):
        self.points += 1


    def snowflake_calc(self):
        self.points += 5
        self.health += 10 # why does health increase?
        self.life_loss_rate += 0.4 ** self.life_loss_rate # confused - v small increase?
        if self.health > 100:
            self.health = 100

    def update(self, x):
        self.x = x
        self.health -= self.life_loss_rate * x/360

    def snowie_alive(self):
        return self.health > 0 # confused  - returns boolean? True if health positive?

    def get_points(self):
        return self.points

    # shows health bar
    def draw(self):
        # why are the tuples 3D?
        pygame.draw.rect(self.window.get_screen(), (105, 105, 105), (512 / 2 - 66, 8, 132, 34), 0)  # 2px gray border
        pygame.draw.rect(self.window.get_screen(), (255, 0, 0), (512 / 2 - 64, 10, 128, 30), 0)  # Red bar
        pygame.draw.rect(self.window.get_screen(), (0, 255, 0), (512 / 2 - 64, 10,  self.health / 100 * 128, 30), 0) # Green bar
        self.window.draw_text('points: {}'.format(self.points), 512 / 2 - 64, 12, color=(0, 0, 255), font_file='font.TTF', size=24)
