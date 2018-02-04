import pygame
from pygame.locals import *
import sys
from time import sleep
from random import random

max_speed_y = 8

def sign(x):
	return (1, -1)[x < 0]

class Ball(object):
	def __init__(self, screensize, ):
		self.screensize = screensize
		self.position = [int(screensize[0]*0.5), int(screensize[1]*0.5)]
		
		# this defines the size of pong. X and Y is the center of it.
		self.radius = 8
		self.rect = pygame.Rect(self.position[0]-self.radius,
					 self.position[1]-self.radius,
					 self.radius*2, self.radius*2) 
		
		self.color = (100,100,255)
		self.vector = [-2,5]
		
		self.hit_edge_right = False
		self.hit_edge_left = False
		
	def update(self, player_paddle, ai_paddle):
		self.position[0] += self.vector[0]
		self.position[1] += self.vector[1]
		
		self.rect.center = (self.position[0], self.position[1])
		
		if self.rect.colliderect(player_paddle.rect):
			self.vector[0] = -abs(self.vector[0])
			self.vector[1] += player_paddle.vector[1]
		if self.rect.colliderect(ai_paddle.rect):
			self.vector[0] = abs(self.vector[0])
			self.vector[1] += ai_paddle.vector[1]
		self.vector[1] = sign(self.vector[1]) * min(abs(self.vector[1]), max_speed_y)

		if self.rect.top <= 0:
			self.vector[1] = abs(self.vector[1])
		elif self.rect.bottom >= self.screensize[1]-1:
			self.vector[1] = -abs(self.vector[1])
		
		#Game over
		#you win if you get to the left side of the screen like as ai's is, any loose here gets on the right. 
		#you donnot wanna loose when you win
		if self.rect.right >= self.screensize[0]-1:
			self.hit_edge_right = True
		elif self.rect.left <= 0:
			self.hit_edge_left = True
		
	def render(self, screen):
		pygame.draw.circle(screen, self.color, self.rect.center, self.radius, 0)
		pygame.draw.circle(screen,(0,0,0), self.rect.center, self.radius, 1)

class CPUPaddle(object):
	def __init__(self, screensize,):
		self.screensize = screensize
		
		self.aiColor = (163, 4, 4)
		ball = Ball(screensize)
		self.vector = [0,max_speed_y]

		self.aiHeight = 70
		self.aiWeight = 15

		self.rect = pygame.Rect(30, int(screensize[1]*0.5) - int(self.aiHeight*0.5), self.aiWeight, self.aiHeight)

	def update(self, ball):

		# the chance that we delay switching the direction of the AI
		delay_chance = 0.8
		if random() > delay_chance:
			if self.rect.bottom < ball.rect.top:
				self.vector[1] = max_speed_y + 0.5
			elif self.rect.top > ball.rect.bottom:
				self.vector[1] = -(max_speed_y + 0.5)
			else:
				# only move by the difference in position between the paddle/ball
				diff = ball.rect.center[1] - self.rect.center[1]
				if abs(diff) <= max_speed_y:
					self.vector[1] = diff

		self.rect.move_ip(self.vector[0], self.vector[1])

		if self.rect.bottom > self.screensize[1]:
			self.rect.bottom = self.screensize[1]
		elif self.rect.top < 0:
			self.rect.top = 0	

	def render(self, screen, ):
		pygame.draw.rect(screen, self.aiColor, self.rect, 0)
		pygame.draw.rect(screen, (0,0,0), self.rect, 1)


class PlayerPaddle(object):
	def __init__(self, screensize, ):
		self.screensize = screensize
		self.position = [610, int(screensize[1]* 0.5)]

		self.OurPaddle_color = (14, 99, 0)
		self.vector = [0,0]

		self.OurHeight = 70
		self.OurWeight = 15

		self.rect = pygame.Rect(0, self.position[1] - int(self.OurHeight*0.5), self.OurWeight, self.OurHeight)

		self.OurSpeed = 5

	def update(self):
		self.position[1] += self.vector[1]

		self.rect.center = (self.position[0], self.position[1])

		# limit the move of player on the screen 0<=Y<=screensize_y
		if self.rect.top < 0:
			self.rect.top = 0
			self.position[1] = self.rect.center[1]
		elif self.rect.bottom > self.screensize[1]:
			self.rect.bottom = self.screensize[1]
			self.position[1] = self.rect.center[1]

	def render(self, screen,):
		pygame.draw.rect(screen, self.OurPaddle_color, self.rect, 0)
		pygame.draw.rect(screen,(0,0,0), self.rect, 1)


def main():
	screensize = (640,480)

	pygame.init()
	pygame.font.init()
	
	screen = pygame.display.set_mode(screensize)
	pygame.display.set_caption("Hello, world")
	
	clock = pygame.time.Clock()

	font = pygame.font.Font(pygame.font.get_default_font(),48)
	small_font = pygame.font.Font(pygame.font.get_default_font(),22)

	ball = Ball(screensize)
	ai_paddle = CPUPaddle(screensize)
	player_paddle = PlayerPaddle(screensize)

	Menu = True
	
	while Menu:
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				quit()
				
			if event.type == KEYDOWN:
				if event.key == K_SPACE:
					Menu = False
				if event.key == K_a:
					pygame.quit()
					quit()

		screen.fill((1,5,38))
		#add the "START?" screen
		text1 = font.render("PONG START?",True,(255,7,7))
		screen.blit(text1,(170,100))
		#add the button screen
		text2 = small_font.render("press SPACE to play and A to quit",True,(22,91,45))
		screen.blit(text2,(160,250))

		pygame.display.update()
		clock.tick(15)

	
	running = True

	# keeps track of which of up/down is currently held
	pressed = { 
				"up"  : False, 
				"down": False
			  }

	while running:
		
		#limitting/reporting phase
		clock.tick(60)
		
		#event handling phase
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False

			if event.type == KEYDOWN:
				if event.key == K_UP:
					pressed["up"] = True
				elif event.key == K_DOWN:
					pressed["down"] = True
			
			if event.type == KEYUP:
				if event.key == K_UP:
					pressed["up"] = False
				elif event.key == K_DOWN:
					pressed["down"] = False

		if pressed["up"] and pressed["down"]:
			player_paddle.vector[1] = 0
		elif pressed["up"]:
			player_paddle.vector[1] = -player_paddle.OurSpeed
		elif pressed["down"]:
			player_paddle.vector[1] = player_paddle.OurSpeed
		else:
			player_paddle.vector[1] = 0

		#updating
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
	