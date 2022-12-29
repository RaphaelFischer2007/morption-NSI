import pygame
from blur import blurSurf
from random import randint
from PIL import Image, ImageFilter
from time import sleep
import button 

# Initialisation de pygame
pygame.init()
surf = pygame.display.set_mode((750,750))
surf.fill((255,255,255))
clock = pygame.time.Clock()
police = pygame.font.SysFont("monospace" ,100)

class Grille:
    """Grille 3x3 de morpion sous forme de liste de liste basée sur un système de coordonnée comme ceci :
[[00,01,02],
 [10,11,12],
 [20,21,22]]

sous la forme xy

Dans les cases, les 0 représentent des cases vides, les 1 représentent des X et les 2 des O"""

    def __init__(self):
        """Constructeur"""
        self.grille=[[0,0,0],[0,0,0],[0,0,0]]
       
    def get_case(self,x,y):
        """Récupère le contenu de la case de coordonnée xy"""
        return self.grille[x][y]

    def set_case(self,x,y,valeur):
        """vérifie que la case de coordonnée xy est vide et remplace le contenu par valeur (1 ou 2)
        renvoie True si la modification a été effectuée"""
        if self.get_case(x,y)==0:
            self.grille[x][y]=valeur
            return True
        return False
    
    def ligne_gagnante(self,joueur,numero_ligne):
        """Vérifie si la ligne 'numero_ligne' est gagnante pour le joueur 'joueur' et renvoie True si oui (non sinon)"""
        return self.grille[numero_ligne]==[joueur,joueur,joueur]

    def colonne_gagnante(self,joueur,numero_colonne):
        """Vérifie si la colonne 'numero_colonne' est gagnante pour le joueur 'joueur' et renvoie True si oui (non sinon)"""
        return [self.grille[j][numero_colonne] for j in range(3)]==[joueur,joueur,joueur]

    def diagonale_bas_droite_gagnante(self, joueur):
        """Vérifie si la diagonale \ est gagnante pour le joueur 'joueur' et renvoie True si oui (non sinon)"""
        return [self.grille[j][j] for j in range(3)]==[joueur,joueur,joueur]

    def diagonale_haut_droite_gagnante(self, joueur):
        """Vérifie si la diagonale / est gagnante pour le joueur 'joueur' et renvoie True si oui (non sinon)"""
        return [self.grille[2-j][j] for j in range(3)]==[joueur,joueur,joueur]
        
    def victoire(self,joueur,x,y,surf):
        """Vérifie si le joueur 'joueur' a gagné à partir de ce qu'il vient de jouer (coordonnées x, y).
        Si oui trace une ligne rouge sur la bande gagnante et renvoie un booléen."""

        # Bandes horizontales
        if self.ligne_gagnante(joueur,x):
            pygame.draw.line(surf, (250, 70, 70), (10, 125*(x+1) + 125*x), (740, 125*(x+1) + 125*x), 10)
            return True
            
        # Bandes verticales  
        if self.colonne_gagnante(joueur,y):
            pygame.draw.line(surf, (250, 70, 70), (125*(y+1) + 125*y, 10), (125*(y+1) + 125*y, 740), 10)
            return True

        # Bande diagonale en partant de la gauche
        if self.diagonale_bas_droite_gagnante(joueur):
            pygame.draw.line(surf, (250, 70, 70), (10, 10), (740, 740), 10)
            return True
        
        # Bande diagonale en partant de la droite
        if self.diagonale_haut_droite_gagnante(joueur):
            pygame.draw.line(surf, (250, 70, 70), (740, 10), (10, 740), 10)
            return True

        return False
    
    def peut_gagner(self,joueur):
        """Vérifie si un joueur peut gagner. Le joueur est représenté par un 1 ou un 2.
        Renvoie les coordonnées de la case à choisir pour gagner (ou pour contrer une victoire)"""

        for x in range(3):
            for y in range(3):
                if self.get_case(x,y)==0:
                    copie_self=Grille()
                    for a in range(3):
                        for b in range(3):
                            copie_self.set_case(a,b,self.get_case(a,b))
                    if copie_self.set_case(x,y,joueur):
                        if (copie_self.ligne_gagnante(joueur,x) or
                            copie_self.colonne_gagnante(joueur,y) or
                            copie_self.diagonale_bas_droite_gagnante(joueur) or
                            copie_self.diagonale_haut_droite_gagnante(joueur)):

                            return (x,y)
        return (None,None)
                        
                
def afficher_grille(grille,surf,img_o,img_x): 
    for posY in range(250,751,250):
        pygame.draw.line(surf,(0,0,0),(0,posY),(750,posY),2)
    for posX in range(250,751,250):
        pygame.draw.line(surf,(0,0,0),(posX,0),(posX,750),2)
    for x in range(3):
        for y in range(3):
            case=grille.get_case(x,y)
            if case==1:
                surf.blit(img_o,(250*y+10,250*x+10))
            elif case==2:
                surf.blit(img_x,(250*y+10,250*x+10))
    pygame.display.flip()

def partie(dif):
    img_o=pygame.transform.scale(pygame.image.load("o.png"),(230,230))
    img_x=pygame.transform.scale(pygame.image.load("x.png"),(230,230))
    run=True
    joueur_debut=randint(0,1)
    nb_coups=0
    grille=Grille()
    while run:
        clock.tick(30) # 30 fps
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed() == (1,0,0):
                    pos = pygame.mouse.get_pos()
                    y=pos[0]//250
                    x=pos[1]//250
                    if grille.set_case(x,y,(nb_coups+joueur_debut)%2+1):
                        afficher_grille(grille,surf, img_o,img_x)
                        if grille.victoire((nb_coups+joueur_debut)%2+1,x,y,surf): # Ecran de victoire de l'humain si dif = 1 ou 2 / Ecran de victoire d'un des deux joueurs si dif = 0
                            pygame.display.flip()
                            sleep(0.4)
                            run=message_victoire("joueur %s"%(str((nb_coups+joueur_debut)%2+1),),grille,dif,surf,img_o,img_x)

                        nb_coups+=1
        
        if run and dif>=1 and nb_coups%2==joueur_debut and nb_coups<9:
            coord=tour_ia(dif, grille, nb_coups)
            if grille.victoire(1,coord[0],coord[1],surf):
                run = message_victoire("Robot",grille,dif,surf,img_o,img_x)
                    
            nb_coups+=1
        if run and nb_coups>=9:  # Ecran de fin si aucun gagnant
            run = message_victoire("Personne",grille,dif,surf,img_o,img_x)

        afficher_grille(grille,surf, img_o,img_x)
        

    pygame.quit()

def tour_ia(dif, grille, tour):
    if dif==1:
        while True:
            x=randint(0,2)
            y=randint(0,2)
            if grille.get_case(x,y)==0:
                grille.set_case(x,y,1)
                return (x,y)
    if dif==2:
        x,y=grille.peut_gagner(1)
        if x!=None:
            grille.set_case(x,y,1)
        else:
            x,y=grille.peut_gagner(2)
            if x!=None:
                grille.set_case(x,y,1)
            else:
                return tour_ia(1,grille,tour)
        return (x,y)
    
    if dif==3:
        x,y=grille.peut_gagner(1)
        if x!=None:
            grille.set_case(x,y,1)
        else:
            x,y=grille.peut_gagner(2)
            if x!=None:
                grille.set_case(x,y,1)
            else:
                return tour_ia_3(grille, tour)
        return (x,y)

def tour_ia_3(grille, tour):
    if tour==0:
        grille.set_case(0,0,1)
        return (0,0)
    elif tour==2:
        if grille.get_case(1,1)==2:
            grille.set_case(2,2,1)
            return (2,2)
        elif grille.get_case(2,0)==0 and grille.get_case(1,0)==0:
            grille.set_case(2,0,1)
            return (2,0)
        else:
            grille.set_case(0,2,1)
            return (0,2)
    elif tour==4:
        if grille.get_case(2,0)==1:
            if grille.get_case(0,1)==2 or grille.get_case(0,2)==2:
                grille.set_case(2,2,1)
                return (2,2)
            else:
                grille.set_case(0,2,1)
                return (0,2)
        else:
            if grille.get_case(1,0)==2 or grille.get_case(2,0)==2:
                grille.set_case(2,2,1)
                return (2,2)
            else:
                grille.set_case(2,0,1)
                return (2,0)
    elif tour==1:
        if grille.get_case(0,0)==2 or grille.get_case(2,0)==2 or grille.get_case(0,2)==2 or grille.get_case(2,2)==2:
            grille.set_case(1,1,1)
            return(1,1)
        else:
            grille.set_case(0,0,1)
            return(0,0)
    return tour_ia(1,grille,tour)
            

def message_victoire(gagnant,grille,dif,surf,img_o,img_x):
    afficher_grille(grille,surf, img_o,img_x)
    surf.blit(blurSurf(surf,5),(0,0)) # Remplace la surface actuelle par une surface floutée
    sleep(.2) # Pour éviter d'appuyer sur le bouton sans s'en rendre compte
    
    run=True
    while run:
        try:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    run=False
        except:
            run=False

        if run:
            replay_img = pygame.image.load('replay.png').convert_alpha()
            replay_button = button.Button(250, 166, replay_img, 0.2)
            
            if gagnant=="Personne":
                image_texte1 = police.render ("Aucun", 1 , (255,0,0))
                image_texte2 = police.render ("gagnant", 1 , (255,0,0))
                surf.blit(image_texte1, (250,250))
                surf.blit(image_texte2, (200,333))

            else:
                image_texte1 = police.render ("Victoire", 1 , (255,0,0))
                image_texte2 = police.render ("du", 1 , (255,0,0))
                image_texte3 = police.render (gagnant, 1, (255,0,0))
                surf.blit(image_texte1, (175,250))
                surf.blit(image_texte2, (325,333))
                if gagnant=="Robot":
                    surf.blit(image_texte3, (250,416))
                else:
                    surf.blit(image_texte3, (175,416))
            pygame.display.flip()
            
            if replay_button.draw(surf):  # Si click sur bouton replay
                surf.fill((255,255,255))
                partie(dif) # Relance une partie
                
    return run

dif = 0 # Niveau de difficulté
partie(dif)
