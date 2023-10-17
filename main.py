import pygame, pygame_menu
import os, time, sys

from pygame_menu import themes
from pygame.locals import *
from player import *
from apple import Apples
from walls import Wall
from random import randrange
from typing import Tuple, Any, Optional, List

__all__ = ['main']
pygame.display.set_caption("Snake Game beta")

FPS = 120
DIFFICULTY = ['EASY']
HS_DIFFICULTY = ['EASY']
WINDOW_SIZE = (840,680)
WINDOWWIDTH = WINDOW_SIZE[0]
WINDOWHEIGHT = WINDOW_SIZE[1]
CELLSIZE = 20
CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)
assert WINDOWWIDTH % CELLSIZE == 0 #must be a multiple of cellsize
assert WINDOWHEIGHT % CELLSIZE == 0 #must be a multiple of cellsize
#               R    G    B
WHITE       = (255, 255, 255)
BLACK       = ( 0,    0,   0)
RED         = (255,   0,   0)
YELLOW      = (255, 255,   0)
GREEN       = (  0, 255,   0)
GRAY        = (185, 185, 185)
BLUE        = (  0,   0, 255)
NAVYBLUE    = ( 60,  60, 100)
ORANGE      = (255, 128,   0)
PURPLE      = (170,   0, 255)
CYAN        = (  0, 255, 255)
LIGHTRED    = (175,  20,  20)
LIGHTGREEN  = ( 20, 175,  20)
LIGHTBLUE   = ( 20,  20, 175)
LIGHTYELLOW = (175, 175,  20)
DARKGREEN   = (  0, 155,   0)
DARKGRAY    = ( 40,  40,  40)

clock: Optional['pygame.time.Clock'] = None
main_menu: Optional['pygame_menu.Menu'] = None
surface: Optional['pygame.Surface'] = None
vec = pygame.math.Vector2 # 2 for two dimensional

drawhighapple = float(10)
drawsuperhighapple = float(30)
file_name = 'easyhighscore.Ken'
file_name2 = 'highscore.Ken'
file_name3 = 'hardhighscore.Ken'
file_name4 = 'insanehighscore.Ken'
ABOUT = [f'Snake V1 Beta',
         f'Game Author: Sufyaan',]
         
         
def main():
    global clock, surface, main_menu
    global user_name
    global p_color, p_icolor

    pygame.init()
    surface = pygame.display.set_mode(WINDOW_SIZE, pygame.SCALED | pygame.RESIZABLE)
    print(surface.get_size())
    pygame.display.set_caption('Suf Snake Beta')
    clock = pygame.time.Clock()

    about_menu = pygame_menu.Menu('About', WINDOWWIDTH * 0.7, WINDOWHEIGHT * 0.75, theme=pygame_menu.themes.THEME_DEFAULT.copy())
    for m in ABOUT:
        about_menu.add.label(m, align=pygame_menu.locals.ALIGN_LEFT, font_size=20)
    about_menu.add.vertical_margin(30)
    about_menu.add.button('Return to menu', pygame_menu.events.BACK)

    high_score_menu = pygame_menu.Menu('High Scores', WINDOWWIDTH * 0.7, WINDOWHEIGHT * 0.75, theme=pygame_menu.themes.THEME_DEFAULT.copy())
    high_score_menu.add.selector('High Scores',
                                  [('1 - Easy', 'EASY'),
                                   ('2 - Medium', 'MEDIUM'),
                                   ('3 - Hard', 'HARD'),
                                   ('4 - Insane', 'INSANE')],
                                   onchange=change_hs,
                                   selector_id='change_hs')
    high_score_menu.add.button('View', show_highscores,
                               HS_DIFFICULTY)

    game_menu = pygame_menu.Menu('Snake Settings', WINDOWWIDTH * 0.5, WINDOWHEIGHT *0.65)
    user_name = game_menu.add.text_input('Name: ', default='Ken_Sensei', maxchar=20)
    game_menu.add.selector('Select Difficulty ',
                            [('1 - Easy', 'EASY'),
                             ('2 - Medium', 'MEDIUM'),
                             ('3 - Hard', 'HARD'),
                             ('4 - INSANE', 'INSANE')], 
                             onchange=change_difficulty,
                             selector_id='select_difficulty')
    p_color = game_menu.add.text_input('Outer worm color: ', default='Purple', maxchar=20)
    p_icolor = game_menu.add.text_input('Inner worm color: ', default='Black', maxchar=20)
    game_menu.add.button('Play', main_game,
                         DIFFICULTY,
                         pygame.font.Font(pygame_menu.font.FONT_FRANCHISE, 30))


    # Setting up main menu with user defined inputs
    main_menu = pygame_menu.Menu('Menu', WINDOWWIDTH * 0.3, WINDOWHEIGHT * 0.55)
    main_menu.add.button('Play', game_menu)
    main_menu.add.button('High Scores', high_score_menu)
    main_menu.add.button('About', about_menu)
    main_menu.add.button('Quit', terminate)

    while True:

        clock.tick(FPS)

        # Paint background
        main_background()

        # Application events
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.VIDEORESIZE:
                pygame.display._resize_event(event)

        # Main menu
        if main_menu.is_enabled():
            main_menu.mainloop(surface, main_background, fps_limit=FPS)

        # Flip surface
        pygame.display.flip()

def change_difficulty(value: Tuple[Any, int], difficulty: str) -> None:
    """
    Change difficulty of the game.
    :param value: Tuple containing the data of the selected object
    :param difficulty: Optional parameter passed as argument to add_selector
    """
    selected, index = value
    print(f'Selected difficulty: "{selected}" ({difficulty}) at index {index}')
    DIFFICULTY[0] = difficulty

def change_hs(value: Tuple[Any, int], difficulty_scores: str) -> None:
    """
    Change difficulty of the game.
    :param value: Tuple containing the data of the selected object
    :param difficulty: Optional parameter passed as argument to add_selector
    """
    selected, index = value
    print(f'Selected HS difficulty: "{selected}" ({difficulty_scores}) at index {index}')
    HS_DIFFICULTY[0] = difficulty_scores


def terminate():
    pygame.quit()
    sys.exit()

def main_game(difficulty: List, font: pygame.font.Font):
    """
    Main game function.
    :param difficulty: Difficulty of the game
    :param font: Pygame font
    """
    assert isinstance(difficulty, list)
    difficulty = difficulty[0]
    assert isinstance(difficulty, str)
    
    #define constants
    block_size = 20
    bounds = WINDOW_SIZE
    bg_color = BLACK

    # Define globals
    global main_menu
    global clock
    global user_name
    global p_color
    global p_icolor
    global P1
    global W1
    global W2
    global W3
    global W4

    #define objects
    P1 = Player(block_size, bounds, p_color.get_value(), p_icolor.get_value())
    AP1 = Apples(block_size, bounds, RED, last_apple_spawn_times={'high': time.time(), 'super_high': time.time()})
    AP2 = Apples(block_size, bounds, CYAN, last_apple_spawn_times={'high': time.time(), 'super_high': time.time()})
    AP3 = Apples(block_size, bounds, YELLOW, last_apple_spawn_times={'high': time.time(), 'super_high': time.time()})
    W1 = Wall(block_size, bounds, BLUE)
    W2 = Wall(block_size, bounds, GREEN)
    W3 = Wall(block_size, bounds, YELLOW)
    W4 = Wall(block_size, bounds, BLUE)

    # Reset main menu and disable
    # You also can set another menu, like a 'pause menu', or just use the same
    # main_menu as the menu that will check all your input.
    main_menu.disable()
    main_menu.full_reset()

    frame = 0

    key_map = {
        pygame.K_LEFT: Direction.LEFT,
        pygame.K_a: Direction.LEFT,
        pygame.K_RIGHT: Direction.RIGHT,
        pygame.K_d: Direction.RIGHT,
        pygame.K_UP: Direction.UP,
        pygame.K_w: Direction.UP,
        pygame.K_DOWN: Direction.DOWN,
        pygame.K_s: Direction.DOWN
    }

    drawGrid()

    while True:

        # increment frame
        frame += 1

        

        # Application events
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                terminate()
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    main_menu.enable()

                    # Quit this function, then skip to loop of main-menu on line 223
                    return
        keys = pygame.key.get_pressed()
        for key in key_map:
            if keys[key]:
                P1.steer(key_map[key])
                if difficulty == 'EASY':
                    P1.move(key_map[key])
                last_key_pressed = key_map[key]
                break

        # Pass events to main_menu
        if main_menu.is_enabled():
            main_menu.update(events)
            main_menu.draw(surface)

        # Continue playing
        surface.fill(bg_color)
        drawGrid()

        text = font.render(str(round(clock.get_fps(),2)), True, GREEN)
        surface.blit(text, (0, 0))

        P1.draw(pygame, surface)
        if difficulty != 'EASY':
            if frame > 60:
                P1.move(last_key_pressed)
        P1.check_for_apple(AP1)
        
        AP1.draw(pygame, surface)

        if time.time() - AP2.last_apple_spawn_times['high'] > drawhighapple:
            AP2.draw(pygame, surface)
            P1.check_for_happle(AP2, difficulty) == True
        if time.time() - AP3.last_apple_spawn_times['super_high'] > drawsuperhighapple:
            AP3.draw(pygame, surface)
            P1.check_for_shapple(AP3, difficulty)

        W1.check_for_apples(AP1, AP2, AP3) #The definintion only needs to be called once it checks all walls
        
        for pscore in range(P1.score):
            pscore = P1.score
            if difficulty == 'EASY':
                high_score = P1.score
                file_name = 'easyhighscore.neonzz'
                if pscore >= int(29):
                    W1.draw(pygame, surface, wall = 1)
                    if W1.check_for_snake(P1) == True:
                        print('SNAKE')
                        main_menu.enable()
                        set_high_score(file_name, user_name.get_value(), high_score)
                        showGameOverScreen()
                        return
                if pscore >= int(39):
                    W2.draw(pygame, surface, wall = 2)
                    if W2.check_for_snake(P1) == True:
                        main_menu.enable()
                        set_high_score(file_name, user_name.get_value(), high_score)
                        showGameOverScreen()
                        return
                if pscore >= int(49):
                    W3.draw(pygame, surface, wall = 3)
                    if W3.check_for_snake(P1) == True:
                        main_menu.enable()
                        high_score = P1.score
                        set_high_score(file_name, user_name.get_value(), high_score)
                        showGameOverScreen()
                        return
                if pscore >= int(59):
                    W4.draw(pygame, surface, wall = 4)
                    if W4.check_for_snake(P1) == True:
                        main_menu.enable()
                        high_score = P1.score
                        set_high_score(file_name, user_name.get_value(), high_score)
                        showGameOverScreen()
                        return
            if difficulty == 'MEDIUM':
                high_score = P1.score
                file_name = file_name2
                if pscore >= int(24):
                    W1.draw(pygame, surface)
                    if W1.check_for_snake(P1) == True:
                        main_menu.enable()
                        set_high_score(file_name, user_name.get_value(), high_score)
                        showGameOverScreen()
                        return
                if pscore >= int(34):
                    W2.nextwall(pygame, surface)
                    if W2.check_for_snake(P1) == True:
                        main_menu.enable()
                        high_score = P1.score
                        set_high_score(file_name, user_name.get_value(), high_score)
                        showGameOverScreen()
                        return
                if pscore >= int(44):
                    W3.thirdwall(pygame, surface)
                    if W3.check_for_snake(P1) == True:
                        main_menu.enable()
                        high_score = P1.score
                        set_high_score(file_name, user_name.get_value(), high_score)
                        showGameOverScreen()
                        return
                if pscore >= int(54):
                    W4.fourthwall(pygame, surface)
                    if W4.check_for_snake(P1) == True:
                        main_menu.enable()
                        high_score = P1.score
                        set_high_score(file_name, user_name.get_value(), high_score)
                        showGameOverScreen()
                        return
            elif difficulty == 'HARD':
                high_score = P1.score
                file_name = file_name3
                if pscore >= int(14):
                    W1.draw(pygame, surface)
                    if W1.check_for_snake(P1) == True:
                        main_menu.enable()
                        set_high_score(file_name, user_name.get_value(), high_score)
                        showGameOverScreen()
                        return
                if pscore >= int(24):
                    W2.nextwall(pygame, surface)
                    if W2.check_for_snake(P1) == True:
                        main_menu.enable()
                        high_score = P1.score
                        set_high_score(file_name, user_name.get_value(), high_score)
                        showGameOverScreen()
                        return
                if pscore >= int(34):
                    W3.thirdwall(pygame, surface)
                    if W3.check_for_snake(P1) == True:
                        main_menu.enable()
                        high_score = P1.score
                        set_high_score(file_name, user_name.get_value(), high_score)
                        showGameOverScreen()
                        return
                if pscore >= int(44):
                    W4.fourthwall(pygame, surface)
                    if W4.check_for_snake(P1) == True:
                        main_menu.enable()
                        high_score = P1.score
                        set_high_score(file_name, user_name.get_value(), high_score)
                        showGameOverScreen()
                        return
            elif difficulty == 'INSANE':
                high_score = P1.score
                file_name = file_name4
                if pscore >= int(4):
                    W1.draw(pygame, surface)
                    if W1.check_for_snake(P1) == True:
                        main_menu.enable()
                        set_high_score(file_name, user_name.get_value(), high_score)
                        showGameOverScreen()
                        return
                if pscore >= int(9):
                    W2.nextwall(pygame, surface)
                    if W2.check_for_snake(P1) == True:
                        high_score = P1.score
                        set_high_score(file_name, user_name.get_value(), high_score)
                        showGameOverScreen()
                        return
                if pscore >= int(19):
                    W3.thirdwall(pygame, surface)
                    if W3.check_for_snake(P1) == True:
                        main_menu.enable()
                        high_score = P1.score
                        set_high_score(file_name, user_name.get_value(), high_score)
                        showGameOverScreen()
                        return
                if pscore >= int(29):
                    W4.fourthwall(pygame, surface)
                    if W4.check_for_snake(P1) == True:
                        main_menu.enable()
                        high_score = P1.score
                        set_high_score(file_name, user_name.get_value(), high_score)
                        showGameOverScreen()
                        return

        if P1.check_bounds() == True or P1.check_tail_collision() == True:
            main_menu.enable()
            if difficulty == 'EASY':
                high_score = P1.score
                file_name = 'easyhighscore.neonzz'
            if difficulty == 'MEDIUM':
                high_score = P1.score
                file_name = file_name2
            elif difficulty == 'HARD':
                high_score = P1.score
                file_name = file_name3
            elif difficulty == 'INSANE':
                high_score = P1.score
                file_name = file_name4
            set_high_score(file_name, user_name.get_value(), high_score)
            showGameOverScreen()
            return
        f = pygame.font.SysFont("Verdana", 20)
        scoreSurf = f.render('Score: %s' % (P1.score), True, WHITE)
        scoreRect = scoreSurf.get_rect()
        scoreRect.topleft = (WINDOWWIDTH - 120, 10)
        surface.blit(scoreSurf, scoreRect)

        pygame.display.flip()

        clock.tick(15)
    
def show_highscores(difficulty_scores: List, Font = pygame.font.Font):

    assert isinstance(difficulty_scores, list)
    difficulty_scores = difficulty_scores[0]
    assert isinstance(difficulty_scores, str)

    surface.fill(BLACK)
    global main_menu  
    
    main_menu.disable()
    main_menu.full_reset()

    frame = 0

    mousex = 0
    mousey = 0

    while True:

        frame += 1

        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    main_menu.enable()
                    
                    
                    return
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
            

        if main_menu.is_enabled():
            main_menu.update(event)
        
        if difficulty_scores == 'EASY':
            scores = get_high_scores(file_name)
        elif difficulty_scores == 'MEDIUM':
            scores = get_high_scores(file_name2)
        elif difficulty_scores == 'HARD':
            scores = get_high_scores(file_name3)
        elif difficulty_scores == 'INSANE':
            scores = get_high_scores(file_name4)

        surface.fill(BLACK)
        firstfont = pygame.font.Font('freesansbold.ttf', 30)
        bigfont = pygame.font.Font('freesansbold.ttf', 36)
        surface.fill(BLACK)
        hsstring = "%s HIGH SCORES" % difficulty_scores
        highScoreText = bigfont.render(hsstring, 1, GREEN) #Create the text
        highScoreTextRect = highScoreText.get_rect()
        highScoreTextRect.midtop = (WINDOWWIDTH / 2, 10)
                    
        
        firstscoretext = firstfont.render("1st: " + scores.get('high')[0] + " - " + scores.get('high')[1], 1, GREEN) #Create the text
        firstscoretextrect = firstscoretext.get_rect()
        firstscoretextrect.midtop = (WINDOWWIDTH / 2, firstscoretextrect.height + 10 + 25)
        #draw the next highest score
        secondfont = pygame.font.Font('freesansbold.ttf', 26)
        secondscoretext = secondfont.render("2nd: " + scores.get('mid')[0] + " - " + scores.get('mid')[1], 1, GREEN) #Create the text
        secondscoretextrect = secondscoretext.get_rect()
        secondscoretextrect.midtop = (WINDOWWIDTH / 2, secondscoretextrect.height + 40 + 35)
        thirdfont = pygame.font.Font('freesansbold.ttf', 20)
        thirdscoretext = thirdfont.render("3rd: " + scores.get('low')[0] + " - " + scores.get('low')[1], 1, GREEN) #Create the text
        thirdscoretextrect = thirdscoretext.get_rect()
        thirdscoretextrect.midtop = (WINDOWWIDTH / 2, secondscoretextrect.height + 80 + 35)
        back_font = Font('freesansbold.ttf', 20)
        back_to_game = back_font.render('Main Menu', 5, GREEN)
        back_to_game_rect = back_to_game.get_rect()
        back_to_game_rect.bottomleft = (0,460)
        surface.blit(firstscoretext, firstscoretextrect)
        surface.blit(secondscoretext, secondscoretextrect)
        surface.blit(thirdscoretext, thirdscoretextrect)
        surface.blit(highScoreText, highScoreTextRect)
        surface.blit(back_to_game, back_to_game_rect)
        pygame.display.update()
        
        if back_to_game_rect.collidepoint( (mousex, mousey) ):
            main_menu.enable()

            return

        clock.tick(60)
        pygame.display.flip()


def drawGrid():
    for x in range(0, WINDOWWIDTH, CELLSIZE):
        pygame.draw.line(surface, DARKGRAY, (x, 0), (x, WINDOWHEIGHT))
    for y in range(0, WINDOWHEIGHT, CELLSIZE):
        pygame.draw.line(surface, DARKGRAY, (0, y), (WINDOWWIDTH, y))

def showGameOverScreen():
    gameOverFont = pygame.font.Font('freesansbold.ttf', 150)
    gameSurf = gameOverFont.render('Game', True, WHITE)
    overSurf = gameOverFont.render('Over', True, WHITE)
    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()
    gameRect.midtop = (WINDOWWIDTH / 2, 10)
    overRect.midtop = (WINDOWWIDTH / 2, gameRect.height + 10 + 25)

    surface.blit(gameSurf, gameRect)
    surface.blit(overSurf, overRect)
    pygame.display.update()
    pygame.time.wait(500)

    main_menu.disable()
    main_menu.full_reset()
    while True:

        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                exit()
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    main_menu.enable()

                    # Quit this function, then skip to loop of main-menu on line 223
                    return
        if main_menu.is_enabled():
            main_menu.update(events)
            main_menu.draw(surface)
            

def get_high_scores(file_name):
    content = "" #Used to store content from the file

    #Check if the file exists, if it does exist...
    if os.path.isfile(file_name):
        #We open the file and save its contents to the content variable
        #When we open a file using with, the file is automatically closed after we
        #are finished, so we don't need to wory about closing it. If you're not accessing
        #a file in this way, you must remember to close it after use
        with open(file_name, 'r') as content_file:
            content = content_file.read()
    #If it doesn't exist, we create the file and populate it with default values
    else:
        f = open(file_name, 'w')
        content = "high::0,mid::0,low::0" #We also set content with the default values to avoid any errors in future code
        f.write(content) #write the contents to file
        f.close() #close the file
        

    content_list = content.split(',') #Split the content into different parts by splitting at every ','

    to_return = {} #create an empty dictionary that will be populated and then returned

    for element in content_list: #For each element in list 
        l = element.split(':') #Split the element into the title name and score sections, which are stored as a list in the variable l
        #use the first variable in the list l as the key in the dictionary to_return, which references a 
        #list containing the second and third values
        to_return[l[0]] = [l[1], l[2]] 

    return to_return #return the dictionary


def write_high_scores(file_name, scores):
    f = open(file_name, 'w') #open the file for writing
    to_write = "" #create an empty string to store the data we will write to our file
    #cycle through the different scores, writing the values in the correct format and adding them to the string 
    for name in ('high', 'mid', 'low'): 
        to_write += name
        to_write += ':'
        to_write += str(scores.get(name)[0])
        to_write += ':'
        to_write += str(scores.get(name)[1])
        to_write += ','

    print(to_write)
    to_write = to_write[:-1] #Remove the last character from the two_write string - this is an unnecessary comma created by our loop
    f.write(to_write) #write the string to the file
    f.close() #close the file

#Updates the high score file with a new score, placing it in the relevant location (i.e. highest, next highest etc.)
#Depending on the score
def set_high_score(file_name, player_name, score):
    scores = get_high_scores(file_name) #get a dictionary of the current high scores

    #If we have a new high score, update the values in the dictionary
    if (int(score) >= int(scores.get('high')[1])): 
        scores['high'][0] = player_name
        scores['high'][1] = score
    #Else if we have a new next highest score, update this value
    elif (int(score) >= int(scores.get('mid')[1])):
        scores['mid'][0] = player_name
        scores['mid'][1] = score
    #Else if our score is lower than anyone elses, update this value.
    elif (int(score) >= int(scores.get('low')[1])):
        scores['low'][0] = player_name
        scores['low'][1] = score

    write_high_scores(file_name, scores)
    print(scores)
    pygame.display.update()

def main_background() -> None:
    """
    Function used by menus, draw on background while menu is active.
    """
    global surface
    surface.fill((128, 0, 128))

if __name__ == '__main__':
    main()