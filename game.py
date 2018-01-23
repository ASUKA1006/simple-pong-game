import pygame
from pygame.locals import *
import sys
from time import sleep

class Ball(object):
	def __init__(self, screensize, ):
		self.screensize = screensize
		self.ball_X = int(screensize[0]*0.5)
		self.ball_Y = int(screensize[1]*0.5)
		
		self.radius = 8
		self.rect = pygame.Rect(self.ball_X-self.radius,
					 self.ball_Y-self.radius,
					 self.radius*2, self.radius*2) 
# this defines the size of pong. X and Y is the center of it.
		
		self.color = (100,100,255)
		self.direction = [1,1]
		self.speedx = 2
		self.speedy = 5
		#code task = change speed as game progresses to make it harder
		
		self.hit_edge_right = False
		self.hit_edge_left = False
		
	def update(self, player_paddle, ai_paddle):
		self.ball_X += self.direction[0]*self.speedx
		self.ball_Y += self.direction[1]*self.speedy
		
		self.rect.center = (self.ball_X, self.ball_Y)
		
		if self.rect.top <= 0:
			self.direction[1] = 1
		elif self.rect.bottom >= self.screensize[1]-1:
			self.direction[1] = -1
		#evaluate "True" after "if" code
		
		if self.rect.right >= self.screensize[0]-1:
			self.hit_edge_right = True
		elif self.rect.left <= 0:
			self.hit_edge_left = True
		#Game over
		#you win if you get to the left side of the screen like as ai's is, any loose here gets on the right. 
		#you donnot wanna loose when you win

		if self.rect.colliderect(player_paddle.rect):
			self.direction[0] = -1
		if self.rect.colliderect(ai_paddle.rect):
			self.direction[0] = 1
		
	def render(self, screen):
		pygame.draw.circle(screen, self.color, self.rect.center, self.radius, 0 )
		pygame.draw.circle(screen,(0,0,0), self.rect.center, self.radius, 1)

class CPUPaddle(object):
	def __init__(self, screensize):
		self.screensize = screensize
		self.aiPaddle_X = 30
		self.aiPaddle_Y = int(screensize[1]*0.5)
		
		self.aiColor = (163, 4, 4)
		self.aiDirection = [0,1]

		self.aiHeight = 70
		self.aiWeight = 15

		self.rect = pygame.Rect(0, self.aiPaddle_Y - int(self.aiHeight*0.5), self.aiWeight, self.aiHeight)


		self.aiSpeed = 3
	
	def update(self, ball, ):
		self.rect.center = (self.aiPaddle_X, self.aiPaddle_Y)

		if (self.rect.top < ball.rect.top - 10):
			self.aiPaddle_Y += self.aiSpeed
		elif (self.rect.top > ball.rect.bottom + 10):
			self.aiPaddle_Y -= self.aiSpeed

	def render(self, screen, ):
		pygame.draw.rect(screen, self.aiColor, self.rect, 0)
		pygame.draw.rect(screen, (0,0,0), self.rect, 1)


class PlayerPaddle(object):
	def __init__(self, screensize, ):
		self.screensize = screensize
		self.OurPaddle_X = 610
		self.OurPaddle_Y = int(screensize[1]* 0.5)

		self.OurPaddle_color = (14, 99, 0)
		self.OurDirection = 0

		self.OurHeight = 70
		self.OurWeight = 15

		self.rect = pygame.Rect(0, self.OurPaddle_Y - int(self.OurHeight*0.5), self.OurWeight, self.OurHeight)

		self.OurSpeed = 3

	def update(self):
		self.OurPaddle_Y += self.OurDirection* self.OurSpeed

		self.rect.center = (self.OurPaddle_X, self.OurPaddle_Y)

		# limit the move of player paddle_Y on the screen 0<=Y<=480
		if self.rect.top < 0:
			self.rect.top = 0
		elif self.rect.bottom > self.screensize[1] - 1:
			self.rect.bottom = self.screensize[1] -1

	def render(self, screen,):
		pygame.draw.rect(screen, self.OurPaddle_color, self.rect, 0)
		pygame.draw.rect(screen,(0,0,0), self.rect, 1)



def main():
	pygame.init()
	pygame.font.init()
	
	screensize = (640,480)
	
	screen = pygame.display.set_mode(screensize)
	pygame.display.set_caption("Hello, world")
	
	clock = pygame.time.Clock()

	font = pygame.font.Font(pygame.font.get_default_font(),48)

	ball = Ball(screensize)
	ai_paddle = CPUPaddle(screensize)
	player_paddle = PlayerPaddle(screensize)

	
	running = True

	while running:
		#limitting/reporting phase
		clock.tick(60)
		
		#event handling phase
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False

			if event.type == KEYDOWN:
				if event.key == K_UP:
					player_paddle.OurDirection = -1
				elif event.key == K_DOWN:
					player_paddle.OurDirection = 1
			
			if event.type == KEYUP:
				if event.key == K_UP or player_paddle.OurDirection == -1:
					player_paddle.OurDirection = 0
				elif event.type == K_DOWN or player_paddle.OurDirection == 1:
					player_paddle.OurDirection = 0
			#"KEYDOWN" means to push the keybord and "KEYUP" means the opposite			
				
		#updating phase
		ai_paddle.update(ball)
		player_paddle.update()
		ball.update(player_paddle, ai_paddle)

		#rendering phase		
		screen.fill((100, 100, 100))
		ai_paddle.render(screen)
		player_paddle.render(screen)
		ball.render(screen)

		if ball.hit_edge_left or ball.hit_edge_right:
			screen.fill((0,0,0))
			

		pygame.display.update()
	

		#saying win/loose, and then exit

		if ball.hit_edge_left:
			print ("You won!")
			text = font.render("WINNER",True, (255,255,255))
			running = False
			screen.blit(text,(180,250))
		elif ball.hit_edge_right:
			print ("You lose")
			text = font.render("GAME OVER",True,(255,255,255))
			running = False
			screen.blit(text,(180,250))
	
		pygame.display.flip()
		if not running:
			sleep(3)

		
	pygame.quit()

if __name__ == "__main__":
	main()
	sys.exit()
	