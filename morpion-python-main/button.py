import pygame


class Button():
	""" Classe permettant la création d'un bouton"""
	def __init__(self, x, y, image, scale):
		"""Initialisation du bouton avec ses coordonnées, l'image qui sera affichée pour le représenter, et une échelle permettant de régler sa taille"""
		width = image.get_width()  # largeur de l'image
		height = image.get_height()  # hauteur de l'image
		self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale))) # charge l'image dans pygame
		self.rect = self.image.get_rect() # copie l'image
		self.rect.topleft = (x, y)
		self.clicked = False # variable renseignant si le bouton a été pressé

	def draw(self, surface):
		""" Fonction permmettant d'afficher le bouton, renvoie True s'il est pressé"""
		action = False
		# obtient les positions de la souris sur l'écran
		pos = pygame.mouse.get_pos()

		# vérifie si la souris est au-dessus du bouton et si elle est entrain de cliquer
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				self.clicked = True
				action = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		# affiche le bouton sur l'écran
		surface.blit(self.image, (self.rect.x, self.rect.y))

		return action