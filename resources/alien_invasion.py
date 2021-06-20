#importing pygame module
import pygame

#defining class for ship which contains shop's property
class Ship:
    def __init__(self, window, x, y):
        self.x = x
        self.window = window
        self.y = y

    #this function is used to draw the ship 
    def draw(self):
        self.window.screen.blit(pygame.image.load('resources/ship.png'),(self.x ,self.y))

    #checking collision of ship with aliens
    def checkCollision(self, window):
        for alien in window.aliens:
            if((alien.y + 32 > self.y and self.x >= alien.x and self.x <= alien.x + 32) or (alien.y + 32 > self.y and self.x + 32 >= alien.x and self.x + 32 <= alien.x + 32) or(alien.y + 32 > self.y and self.x + 64 >= alien.x and self.x +64 <= alien.x + 32)):
                window.lost = True
                window.ship_distroyed = True

#defining a class for alien which contains its property
class Alien:
    def __init__(self,window ,x, y):
        self.x = x
        self.window = window
        self.y = y
        #here size is 32 because image of alien is of 32pixcel
        self.size = 32

    #this function is used to draw the alien 
    def draw(self):
        self.window.screen.blit(pygame.image.load('resources/alien.png'),(self.x,self.y))
        self.y += self.window.alien_speed

    #this function will check the collision taking place or not
    def checkCollision(self, window):
        for bullet in window.bullets:
            if (bullet.x > self.x  and bullet.x < self.x + self.size and bullet.y < self.y + self.size ): 
                window.bullets.remove(bullet)
                window.aliens.remove(self)

#defining alien_fleet class to produce an alien_fleet 
class Alien_Fleet:
    def __init__(self, window):
        margin = 30  
        width = 50 

        #this loop will make alien fleet according to the dimensions of the window 
        # here giving range three agruments "start, stop, step" to arrange the fleet
        for x in range(margin, window.width - margin, width):
            for y in range(margin, int(window.height / 2), width):
                window.aliens.append(Alien(window, x, y))
                #print(x,y)


#defining bullet class which has its property        
class Bullet:
    def __init__(self, window, x,y):
        #here i add 32 because ship is of 64 pixcel so +32 will make appear bullet to be fired from top-center
        self.x =x + 32
        self.y = y
        self.window = window

    #this function is used to draw the bullets and move it 
    def draw(self):
        pygame.draw.rect(self.window.screen, (254,52,110), pygame.Rect(self.x , self.y, 2, 4))
        self.y -= self.window.bullet_speed

    #this function will delete the bullet as it is going to negative Y axis
    def update(self):
        for bullet in self.window.bullets:
            if bullet.y < 0:
                self.window.bullets.remove(bullet)

#defining window(display) class 
class Window:
    
    def __init__(self,width,height):
        pygame.init()
        #seting a two variables for height and width of window
        self.width = width
        self.height = height
        #creating lists for alien and bullet
        self.aliens = []
        self.bullets = []
        #seting window with some width and height using pygame
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        #this bool will help us to display "you died" when alien enter the ship territory
        self.lost = False
        #this bool helps to run and stop the main game loop
        self.running = True
        #seting a variable for number of alien_fleet
        self.num_of_fleet = 0
        #seting alien speed
        self.alien_speed = 0
        #seting bullet speed
        self.bullet_speed = 0
        #seting ship speed
        self.ship_speed = 0
        #seting bool for ship distruction
        self.ship_distroyed = False

        #passing argument to the class "Ship" and "Alien_Fleet" and making its instance
        ship = Ship(self, width/2, height -84)

        #the main game loop
        while self.running:

            #calling a function when all the aliens are destroyed
            if len(self.aliens) == 0:
                if self.num_of_fleet == 5:
                    self.displayText("VICTORY ACHIEVED",height)
                else:
                    alien_fleet = Alien_Fleet(self)
                    self.alien_speed += 0.1
                    self.num_of_fleet += 1
                    self.bullet_speed += 2
                    self.ship_speed += 1.5

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    #using SPACE buttom pressed event to create bullets
                    if event.key == pygame.K_SPACE and not self.lost:
                        self.bullets.append(Bullet(self, ship.x, ship.y))

            #using get_pressed() function to move ship
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_q]:
                self.running = False
            if pressed[pygame.K_LEFT]:  
                if ship.x > 20:
                    ship.x -= self.ship_speed
                else: 
                    ship.x = 20  
            elif pressed[pygame.K_RIGHT]:  
                if ship.x < width - 84:
                    ship.x += self.ship_speed
                else: 
                    ship.x = width - 84

            #using flip() function to regularly update the screen
            pygame.display.flip()
            #self.clock.tick(500)
            #self.screen.fill((0, 0, 0))

            #giving a background image
            self.screen.blit(pygame.image.load("resources/BG.png"), (0,0))

            #giving caption
            pygame.display.set_caption("Alien Invasion")

            #loop which will display every alien on the screen and will checkcollision
            for alien in self.aliens:
                alien.draw()
                alien.checkCollision(self)
                if (alien.y + 32 > height):
                    self.lost = True
                    self.displayText("YOU DIED",height)

            #loop which will fire bullet from the bullets list and will check delete that bullet when it enters the negative Y axis
            for bullet in self.bullets:
                bullet.draw()
                bullet.update()

            #will remove the ship if alien enters the ship's territory
            if not self.lost:
                ship.draw()
                ship.checkCollision(self)
            
            #display when ship touches alien
            if self.ship_distroyed:
                self.displayText("!!Ship Destroyed!!",self.height)

    #this function is used to display the winning or lossing text
    def displayText(self, text,height):
        self.height = height
        pygame.font.init()
        font = pygame.font.SysFont('Arial', 50)
        textsurface = font.render(text, False, (255, 0, 0))
        self.screen.blit(textsurface, (60, self.height/2))


window = Window(600, 600)