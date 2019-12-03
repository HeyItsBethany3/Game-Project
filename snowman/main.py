from PPlay.window import Window
from PPlay.gameimage import GameImage
from tree import Tree
from snowman import Snowman
from scorer import Scorer
from highscoremanager import ScoreManager

window = Window(512, 512)
window.set_title('SnowMan')

background = GameImage('sprite/scenario/scenarionew.gif')
menu_bg = GameImage('sprite/scenario/start.png')
start_button = GameImage('sprite/scenario/button.png')
game_over = GameImage('sprite/scenario/GAMEOVER.png')
score_manager = ScoreManager()

keyboard = window.get_keyboard()

tree = Tree(window)
snowie = Snowman(window, 'left')
scorer = Scorer(window)

keyboard_pressed = False
record_checked = False

game_state = 2  #  2 IN-MENU, 0 PLAYING, 1 GAME-OVER 

while True:
#if in play mode    
    if game_state == 0:
        if keyboard.key_pressed('left') or keyboard.key_pressed('right'):
            if not keyboard_pressed:
                side = 1 if keyboard.key_pressed('left') else 0
                snowie_side = 'left' if keyboard.key_pressed('left') else 'right'

                hit_side_1, hit_side_2 = tree.hit(side)
                snowie.hit(snowie_side)
                scorer.points_calc()

                if side == hit_side_1 or side == hit_side_2:
                    game_state = 1

            keyboard_pressed = True
        else:
            keyboard_pressed = False
        background.draw()
        tree.update()
        tree.draw()
        snowie.update()
        snowie.draw()
        scorer.update()
        if not scorer.snowie_alive():
            game_state = 1
        scorer.draw()

# setting new high record after gameover
    elif game_state == 1:
        if not record_checked:
            if scorer.get_points() > score_manager.get_records():
                score_manager.set_new_record(scorer.get_points())
            record_checked = True

        background.draw()
        tree.draw()
        game_over.draw()

#showing scores on gameover menu
        window.draw_text(str(score_manager.get_records()), 260, 205, color=(20, 200, 50), font_file='font.TTF',
                         size=30)#highest records
        window.draw_text(str(scorer.get_points()), 260, 240, color=(20, 200, 50), font_file='font.TTF',
                         size=30)#last score
#start new game
        if keyboard.key_pressed('enter'):
            game_state = 0
            tree = Tree(window)
            snowie = Snowman(window, 'left')
            scorer = Scorer(window)
            record_checked = False
#menu before clicking enter
    elif game_state == 2:
        menu_bg.draw()
        start_button.draw()
        window.draw_text(str(score_manager.get_records()), 512 - 56, 274, color=(20, 200, 50), font_file='font.TTF', size=30)
        if keyboard.key_pressed('enter'):
            game_state = 0
    window.update()

