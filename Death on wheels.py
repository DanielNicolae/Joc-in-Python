import pygame
import time
import random

pygame.init() # initializare

display_width = 800 # variabila pentru latime ecran
display_height = 600 # variabila pentru inaltime ecran

black = (0,0,0) # setare culori
white = (255,255,255)
red = (255,0,0)
green=(0,255,0)
block_color = (53,115,255)
bright_green=(0,200,0)
bright_red=(200,0,0)
car_width = 128 # dimensiuni masina
car_height=80
gameDisplay = pygame.display.set_mode((display_width,display_height)) # setare rezolutie ecran
pygame.display.set_caption('Death on wheels') # titlu joc
clock = pygame.time.Clock() # variabila pentru timp
icon = pygame.image.load('32.png') # incarca iconul
carImg = pygame.image.load('racecar.png') # incarca imaginea pentru masina controlata
Car=pygame.image.load('car3.png') # incarca imaginea pentru celelalte masini din joc
pygame.display.set_icon(icon) # schimba iconul
def quitgame(): # functie pentru iesire din joc
    pygame.quit()
    quit()
class Background(pygame.sprite.Sprite): # clasa pentru schimbare fundal
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
def things_dodged(count): # functie pentru afisarea punctajului
    font = pygame.font.SysFont(None, 25)
    text = font.render("Dodged: "+str(count), True, black)
    gameDisplay.blit(text,(0,0))
def Cars(carx,cary): # functie pentru afisarea masinilor, din sens opus, pe ecran
    gameDisplay.blit(Car,(carx,cary))
def car(x,y): # functie pentru afisarea masinii controlate pe ecran
    gameDisplay.blit(carImg,(x,y))
def text_objects(text, font): # functie pentru afisare text pe butoane
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()
def title(text, font):# functie pentru afisare titlu
    textSurface = font.render(text, True, red)
    return textSurface, textSurface.get_rect()
def message_display(text): # functie pentru afisare mesaj
    largeText = pygame.font.Font('freesansbold.ttf',115)
    TextSurf, TextRect = title(text, largeText)
    TextRect.center = ((display_width/2),(display_height/2))
    gameDisplay.blit(TextSurf, TextRect)

    pygame.display.update() # update ecran

    time.sleep(2) # asteapte 2 milisecunde

    game_loop() # chemare functie game_loop

def button(msg,x,y,w,h,ic,ac,action=None): # functie pentru butoane
    mouse = pygame.mouse.get_pos() # detecteaza pozitia mouseului
    click = pygame.mouse.get_pressed() # detecteaza daca ai apasat clic stanga
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac,(x,y,w,h))

        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(gameDisplay, ic,(x,y,w,h))

    smallText = pygame.font.SysFont("comicsansms",20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    gameDisplay.blit(textSurf, textRect)

def crash(): # functie pentru detectare coliziune
    message_display('You crashed!') # afisare mesaj

def game_intro(): #functie pentru pagina de intro

    intro = True

    while intro: # bucla while
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        fundal = Background('intro.png', [0, 0]) # setare fundal
        gameDisplay.blit(fundal.image, fundal.rect)
        largeText = pygame.font.Font('freesansbold.ttf',90) # setare text
        TextSurf, TextRect = title("Death on wheels", largeText) # setare titlu
        TextRect.center = ((display_width/2),(display_height/2)) # pozitionare
        gameDisplay.blit(TextSurf, TextRect)
        pygame.draw.rect(gameDisplay, green,(150,450,100,50)) # setare buton verde
        pygame.draw.rect(gameDisplay, red,(550,450,100,50)) # setare buton rosu
        button("GO!", 150, 450, 100, 50, green, bright_green, game_loop) # afisare buton GO!
        button("Quit", 550, 450, 100, 50, red, bright_red, quitgame) # afisare buton Quit

        pygame.display.update() # update ecran
        clock.tick(15) # asteapta 15 milisecunde

def game_loop(): # functie principala
    x = (display_width * 0.45) # coordonatele pentru afisarea masinii controlate
    y = (display_height * 0.8)

    x_change = 0 # variabile pentru schimbarea pozitiei masinii
    y_change=0
    carx = display_width # variabila pentru pozitia de start pe axa X a masinii ce trebuie evitata
    cary = random.randrange(car_height, display_height) # variabila ce genereaza un nr. aleatoriu, intre nr. ce reprezinta inaltimea masinii si inaltimea ecranului
    thing_speed = 9 # variabila pentru setarea vitezei masinii controlate
    thingCount = 1 # variabila pentru setarea punctajului

    dodged = 0 # variabila pentru nr. de masini evitate

    gameExit = False

    while not gameExit: # bucla while

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN: # daca apasam tasta
                if event.key == pygame.K_DOWN: # sageata jos
                    y_change = 10              # masina se va deplasa pe Y cu 10 pixeli
                if event.key == pygame.K_UP: # sageata sus
                    y_change = -10           # masina se va deplasa pe Y cu -10 pixeli
                if event.key == pygame.K_RIGHT: # sageata dreapta
                    x_change = 10              # masina se va deplasa pe X cu 10 pixeli
                if event.key == pygame.K_LEFT: # sageata dreapta
                    x_change = -10             # masina se va deplasa pe X cu -10 pixeli
            if event.type == pygame.KEYUP:     # daca ridicam degetul de pe tasta
                if event.key == pygame.K_DOWN or event.key == pygame.K_UP or event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT: # oricare dintre sageti
                    y_change = 0 # pozitia masinii nu se schimba
                    x_change=0

        x += x_change # pozitia pe X a masinii se schimba cu x_change
        y+=y_change   # pozitia pe Y a masinii se schimba cu y_change
        BackGround = Background('road2.png', [0, 0]) # afisare fundal
        gameDisplay.blit(BackGround.image, BackGround.rect)

        Cars(carx, cary) # masinile din sens opus, de coordonate (carx,cary)
        carx-=thing_speed # se deplaseaza pe X cu - valoarea lui thing_speed (viteza)
        

        car(x,y) # masina controlata, de coordonate (x,y)
        things_dodged(dodged) # chemare functie pentru masini evitate

        if x > display_width - car_width or x < 0: # detectare coliziune cu marginea ecranului pe X
            crash() # chemare functie pentru coliziune
        if y+car_height > display_height or y < 0: # detectare coliziune cu marginea ecranului pe Y
            crash() # chemare functie pentru coliziune

        if carx+car_width<x:# daca masina din sens opus trece de masina controlata de noi
                     
            if carx<0: # daca masina din sens opus trece da 0 pe axa X
                carx=display_width # atunci masina isi reia pozitia pe axa X, la capatul ecranului
                cary=random.randrange(car_height+50,display_height-100)  # intr-un loc aleatoriu
                thing_speed += 1 # viteza masinii din sens opus creste
                dodged += 1 # punctajul creste cu 1

        if x+car_width > carx: # daca masina controlata de noi se intersecteaza cu masina din sens opus, pe axa X
            if x<carx+car_width: # sau daca se ciocneste de spatele masinii
                if y>cary and y<cary+car_height or y+car_height>cary and y+car_height<cary+car_height: # verifica daca masina se intersecteaza pe axa Y cu masina din sens opus
                    crash() # daca da, rezulta crash
                
        pygame.display.update() # update ecran
        clock.tick(60) # se asteapta 60 de milisecunde

game_intro() # chemare functie game_intro
game_loop() # chemare functie game_loop
pygame.quit()
quit() # oprire program
