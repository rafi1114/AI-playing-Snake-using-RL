import pygame
from pygame.locals import *
import time #creating a time delay for the snake's movement
import random  #To generate random locations for the apple 

GRID_X, GRID_Y = 800, 800
SIZE = 40

class blockade:
    def __init__(self, surface):
        self.surface = surface
        self.image = pygame.image.load("../resources/blockade.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (SIZE, SIZE))
        self.n = random.randint(1,2) #Number of blockades
        # print("Number of blockades: ", self.n)
        self.lengths = [] #Initializing the length array
        self.x = []
        self.y = []
        for i in range(self.n):
            self.lengths.append(random.randint(2,5))
            self.x.append(random.randint(2,10)*SIZE)
            self.y.append(random.randint(3,7)*SIZE)

        # print("The Lengths of the blockades are ", self.lengths)

        # for i in range(len(self.x)):
        #     print("The starting position of x are: ", self.x[i])
        #     print("The starting position of y are: ", self.y[i])

        for i in range(self.n):
            self.case = random.randint(1, 3)
            for j in range(self.lengths[i]+1):
                if self.case == 1:
                    self.x.append(self.x[0] + j*SIZE)
                    self.y.append(self.y[0] + j*SIZE)
                if self.case == 2:
                    self.x.append(self.x[0] + j*SIZE)
                    self.y.append(self.y[0])
                if self.case == 3:
                    self.x.append(self.x[0])
                    self.y.append(self.y[0] + j*SIZE)
        # print(f"The x positions of blockade  are: ", self.x)
        # print(f"The y positions of blockade are: ", self.y)

    def blockade_length(self):
        for i in range(0, len(self.x)):
            self.surface.blit(self.image, (self.x[i], self.y[i])) #typical function for displaying the blockade

    def draw(self):
        self.blockade_length()
        pygame.display.flip() #Updates the display

                                            
                                        

class apple:
    def __init__(self, surface): #initiates the apple
        self.surface = surface #gets surface from the Game Class as input
        self.image = pygame.image.load("../resources/apple.png").convert_alpha() #imports own image here
        self.image = pygame.transform.scale(self.image, (SIZE, 35)) #reshapes the image
        self.x = random.randint(1,9)*SIZE #the x position of the first apple
        self.y = random.randint(1,6)*SIZE #the y position of the first apple


    def draw(self): #displays the apple
        self.surface.blit(self.image, (self.x, self.y)) #typical function for displaying the apple
        pygame.display.flip() #Updates the display

    def move(self): #randomly moves the apple in the game
        self.x = random.randint(1,GRID_X/SIZE - 3)*SIZE 
        self.y = random.randint(1,GRID_Y/SIZE - 3)*SIZE

class snake:
    def __init__(self, surface, block, background, length): #gets the surface, snake block, background, and length from Game Class

        #initiating all properties received from Game class

        self.surface = surface
        self.block = block
        self.background = background
        self.direction = 'down'
        self.head = pygame.image.load("../resources/head.png").convert_alpha() #imports own image here
        self.head = pygame.transform.scale(self.head, (SIZE, SIZE)) #reshapes the image
        self.dead_head = pygame.image.load("../resources/head.png").convert_alpha() #imports own image here
        self.dead_head = pygame.transform.scale(self.dead_head, (SIZE, SIZE))
        self.dead_body = pygame.image.load("../resources/head.png").convert_alpha() #imports own image here
        self.dead_body = pygame.transform.scale(self.dead_body, (SIZE, SIZE))
        self.length = length
        self.x = [200]*length
        self.y = [200]*length

    # Setting the directions 

    def move_left(self):
        self.direction = 'left'
    def move_right(self):
        self.direction = 'right'
    def move_up(self):
        self.direction = 'up'
    def move_down(self):
        self.direction = 'down'


    # Setting the snake motion where next block gets the previous block's coordinates

    def walk(self):
        for i in range(self.length-1, 0, -1): #We go backward from last block towards the head
            self.x[i]=self.x[i-1]
            self.y[i]=self.y[i-1]

        if self.direction == 'left':
            self.x[0] -= SIZE       #Coordinates are of the top corners of the blocks 
        if self.direction == 'right':
            self.x[0] += SIZE
        if self.direction == 'up':
            self.y[0] -= SIZE
        if self.direction == 'down':
            self.y[0] += SIZE    
        self.draw()

    def draw(self):    #to display the snake on the screen
        # Load the background image
        self.surface.blit(self.background, (0,0))
        self.surface.blit(self.head, (self.x[0],self.y[0]))
        for i in range(1, self.length):
            self.surface.blit(self.block, (self.x[i],self.y[i])) #show all the blocks via loop
        pygame.display.flip()
    
    def draw_dead(self):    #to display the snake on the screen
        # Load the background image
        self.surface.blit(self.background, (0,0))
        self.surface.blit(self.dead_head, (self.x[0],self.y[0]))
        for i in range(1, self.length):
            self.surface.blit(self.dead_body, (self.x[i],self.y[i])) #show all the blocks via loop
        pygame.display.flip()


    def increase_length(self):  #increase the length and this length is used in the walk function
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)
    
    def wall_crossing(self): 
        if self.x[0]< 0:
            self.x[0] = 800
        if self.y[0]< 0:
            self.y[0] = 600
        if self.x[0]> 800:
            self.x[0] = 0
        if self.y[0]> 600:
            self.y[0] = 0 


class Game: #most important
    def __init__(self): 
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption("Snake Game by Rafi Bin Dastagir")

        #self.play_bg_music()

        self.surface = pygame.display.set_mode((GRID_X, GRID_Y)) #this surface is used by snake and apple too

        block = pygame.image.load("../resources/body.png").convert_alpha() #imports block for snake, apple
        block = pygame.transform.scale(block, (SIZE,SIZE))

        self.background = pygame.image.load("../resources/bg2.jpg").convert() #imports background, used by snake too
        self.background = pygame.transform.scale(self.background, (GRID_X, GRID_Y))

        self.border = pygame.image.load("../resources/border.png").convert_alpha() #imports background, used by snake too
        self.border = pygame.transform.scale(self.border, (GRID_X+100, GRID_Y+100))


        self.length = 1
        self.block = block
        self.snake = snake(self.surface, self.block, self.background, self.length) #This is how we pass the details through Snake
        self.snake.draw() #Draw the snake
        self.apple = apple(self.surface) #passing details to apple
        self.apple.draw() #Draw the apple
        self.blockade = blockade(self.surface)
        self.blockade.draw() 
        self.reward = 0
        self.score = self.count_score()
        self.frame_iteration = 0



    def is_collision(self, x1, y1, x2, y2): #Any collision detection

        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True
        return False 
    
    def count_score(self):
        score = self.snake.length-1
        return score
    
    def display_score(self, episode): #display the score
        font = pygame.font.SysFont('arial', 50, bold=True)
        score = font.render(f"Score: {self.snake.length-1}", True, (255,255,255))
        self.surface.blit(score, (280,20))
        episode = font.render(f"Episode: {episode}", True, (255,255,255))
        self.surface.blit(episode, (20,20))
    
    def play_bg_music(self):  #play bg music continuously
        pygame.mixer.music.load("../resources/music.mp3")
        pygame.mixer.music.play()

    def bad_collision(self, headx, heady):
        #Snake colliding with Itself
        for i in range(2, self.snake.length):
            if self.is_collision(headx, heady, self.snake.x[i], self.snake.y[i]):
                return True
        # # Snake colliding with Blockade
        # for i in range(len(self.blockade.x)):    
        #     if self.is_collision(headx, heady, self.blockade.x[i], self.blockade.y[i]):
        #         return True
            
        if headx + SIZE > GRID_X or headx < 0 or heady + SIZE > GRID_Y or heady < 0:
            self.show_border()
            return True
        else:
            return False
        
    def show_border(self):
        self.surface.blit(self.border, (-50,-50))
        pygame.display.flip()
        
# Snake colliding with Apple    
    def eat_apple(self):
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            sound1 = pygame.mixer.Sound("../resources/yay.wav")
            pygame.mixer.Sound.play(sound1)
            self.reward = 100
            self.snake.increase_length()
            self.apple.move()


    def location(self):
        direction = self.snake.direction
        snkx, snky = self.snake.x[0], self.snake.y[0]
        appx, appy = self.apple.x, self.apple.y
        return direction, snkx, snky, appx, appy

    def play(self, episode):
        self.snake.walk()
        #self.blockade.draw()
        self.apple.draw()
        self.location()
        
        self.display_score(episode)
        pygame.display.flip()


        
        #Apple colliding with Blockade
        for i in range(len(self.blockade.x)):
            if self.is_collision(self.blockade.x[i], self.blockade.y[i], self.apple.x, self.apple.y):
                self.apple.move()
        
        #Apple colliding with Snake's Body Parts
        for i in range(1, self.snake.length):
            if self.is_collision(self.snake.x[i], self.snake.y[i], self.apple.x, self.apple.y):
                self.apple.move() 

        if self.bad_collision(self.snake.x[0], self.snake.y[0]) or self.frame_iteration > 500*self.snake.length:
            sound2 = pygame.mixer.Sound("../resources/noo.mp3")
            pygame.mixer.Sound.play(sound2)
            raise "Colision detected"
                            
    def show_game_over(self):
        self.background = pygame.image.load("../resources/bg2.jpg").convert()
        self.background = pygame.transform.scale(self.background, (800, 600))
        self.surface.blit(self.background, (0,0)) 
        font = pygame.font.SysFont('impact', 40)
        line1 = font.render(f"Game OVER! Your Score is: {self.snake.length}", True, (255,155,0))
        self.surface.blit(line1, (150,200))
        line2 = font.render("To play the game again, hit ENTER!", True, (255,255,255))
        self.surface.blit(line2, (100,300))
        line3 = font.render("To exit press ESCAPE!", True, (255,255,255))
        self.surface.blit(line3, (200,350))
        pygame.display.flip()

        pygame.mixer.music.pause()
    
    def reset(self):
        self.snake = snake(self.surface, self.block, self.background, 1)
        self.apple = apple(self.surface)
        self.blockade = blockade(self.surface)
        self.score = 0
        self.frame_iteration = 0
        self.reward = 0


    def run(self, action, episode):
        self.frame_iteration += 1
        done = False
        self.reward = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        if done == False:
            if action == 0 and self.snake.direction != 'right': #Cant go behind the body
                self.snake.move_left()
            if action == 1 and self.snake.direction != 'left':
                self.snake.move_right()
            if action == 2 and self.snake.direction != 'down':
                self.snake.move_up()
            if action == 3 and self.snake.direction != 'up':
                self.snake.move_down()
        try:
            if not done:
                self.score = self.count_score()
                self.reward = -0.1
                self.eat_apple()
                self.play(episode)
        except Exception as e:
            done = True
            self.score = self.count_score()
            self.reward = -100

        time.sleep(0.1)
    
        return self.reward, done, self.score

if __name__ == '__main__':
    game = Game()
    game.run()
