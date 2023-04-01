import pygame
from blur import blurSurf
from random import randint
from time import sleep
import button 

# Initialisation de pygame
pygame.init()
surf = pygame.display.set_mode((750,750))
surf.fill((255,255,255))
clock = pygame.time.Clock()

# définition de la police
police = pygame.font.SysFont("monospace" ,100)
police2 = pygame.font.SysFont("monospace" ,30)
police3 = pygame.font.SysFont("monospace" , 50)


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
            pygame.draw.line(surf, (250, 70, 70), (10, 125*(x+1) + 125*x), (740, 125*(x+1) + 125*x), 7)
            return True
            
        # Bandes verticales  
        if self.colonne_gagnante(joueur,y):
            pygame.draw.line(surf, (250, 70, 70), (125*(y+1) + 125*y, 10), (125*(y+1) + 125*y, 740), 6)
            return True

        # Bande diagonale en partant de la gauche
        if self.diagonale_bas_droite_gagnante(joueur):
            pygame.draw.line(surf, (250, 70, 70), (10, 10), (740, 740), width=10)
            return True
        
        # Bande diagonale en partant de la droite
        if self.diagonale_haut_droite_gagnante(joueur):
            pygame.draw.line(surf, (250, 70, 70), (740, 10), (10, 740), width=10)
            return True

        return False
    
    def peut_gagner(self,joueur):
        """Vérifie si un joueur peut gagner. Le joueur est représenté par un 1
        ou un 2. Renvoie les coordonnées de la case à choisir pour gagner (ou
        pour contrer une victoire). Renvoie (None,None) si aucun joueur ne peut
        gagner"""

        # La méthode est la suivante :
        #  - Sélectionne un case vide de la grille
        #  - Crée une copie de la grille
        #  - Remplis la case de la copie avec le numéro de "joueur"
        #  - vérifie si la grille est alors gagnante grâce au module précedent
        # (On part du principe que la grille n'est pas déjà gagnante)
        
        for x in range(3):
            for y in range(3):

                # On vérifie que la case est vide
                if self.get_case(x,y)==0:

                    # On crée une copie vide
                    copie_self=Grille()

                    # Pour chaque case de la grille, on copie sa valeur dans
                    # la copie de la grille
                    for a in range(3):
                        for b in range(3):
                            copie_self.set_case(a,b,self.get_case(a,b))
                    
                    if copie_self.set_case(x,y,joueur):

                        # On vérifie si la grille est alors gagnante
                        if (copie_self.ligne_gagnante(joueur,x) or
                            copie_self.colonne_gagnante(joueur,y) or
                            copie_self.diagonale_bas_droite_gagnante(joueur) or
                            copie_self.diagonale_haut_droite_gagnante(joueur)):

                            return (x,y)
        return (None,None)
                        
                
def afficher_grille(grille,surf,img_o,img_x):
    """Affiche la grille et le contenu des cases"""

    # Affiche les lignes
    for posY in range(250,751,250):
        pygame.draw.line(surf,(0,0,0),(0,posY),(750,posY),2)
    for posX in range(250,751,250):
        pygame.draw.line(surf,(0,0,0),(posX,0),(posX,750),2)

    # Récupère le contenu des cases et l'affiche
    for x in range(3):
        for y in range(3):
            case=grille.get_case(x,y)
            
            if case==1:
                surf.blit(img_o,(250*y+10,250*x+10))
            elif case==2:
                surf.blit(img_x,(250*y+10,250*x+10))

    # Actualise l'affichage
    pygame.display.flip()

def partie(dif):
    pygame.display.set_caption("Partie") # titre de la fenêtre

    # Charge les images des X et des O pour après les afficher dans la grille
    img_o=pygame.transform.scale(pygame.image.load("./images/o.png"),(230,230))
    img_x=pygame.transform.scale(pygame.image.load("./images/x.png"),(230,230))

    # Permet d'arreter le programme durant le jeu si le joueur clique
    # sur "Fermer"
    run=True

    # Le joueur du début est choisi au hasard
    joueur_debut=randint(0,1)

    # Le nombre de coups joués
    nb_coups=0

    grille=Grille()
    
    while run:
        afficher_grille(grille,surf, img_o,img_x)
        
        clock.tick(30) # 30 fps

        for event in pygame.event.get():

            # Vérifie si le joueur clique sur "Fermer"
            if event.type==pygame.QUIT:
                run=False
                exit()

            # Vérifie si le joueur clique sur un bouton de souris
            if event.type == pygame.MOUSEBUTTONDOWN:

                # Vérifie que le bouton est le gauche
                if pygame.mouse.get_pressed() == (1,0,0):

                    # Récupère les coordonnées du clic et la convertit en coordonnées de cases
                    pos = pygame.mouse.get_pos()
                    y=pos[0]//250
                    x=pos[1]//250

                    # Ici, (nb_coups+joueur_debut)%2+1 est le joueur dont c'est le tour
                    if grille.set_case(x,y,(nb_coups+joueur_debut)%2+1):
                        
                        afficher_grille(grille,surf, img_o,img_x)
                        
                        if grille.victoire((nb_coups+joueur_debut)%2+1,x,y,surf):
                            # Ecran de victoire de l'humain si dif = 1 ou 2
                            # Ou l'écran de victoire d'un des deux joueurs si dif = 0
                            pygame.display.flip()

                            # "joueur %s"%(str((nb_coups+joueur_debut)%2+1),) vaut "Joueur 1" ou "Joueur 2" selon
                            # le joueur qui joue
                            run = message_victoire("joueur %s"%(str((nb_coups+joueur_debut)%2+1),),grille,dif,surf,img_o,img_x)

                            # Changer run ici permet de fermer proprement le programme si le
                            # joueur appuie sur "fermer" quand il est sur l'écran de victoire
                            
                        nb_coups+=1

        # Le tour de l'IA
        if run and dif>=1 and nb_coups%2==joueur_debut and nb_coups<9:

            # Récupère les coordonnées du coup joué pour vérifier si la grille est gagnante
            coord=tour_ia(dif, grille, nb_coups)
            afficher_grille(grille,surf, img_o,img_x)
            
            if grille.victoire(1,coord[0],coord[1],surf):
                pygame.display.flip()
                run = message_victoire("Robot",grille,dif,surf,img_o,img_x)
                    
            nb_coups+=1

        # Ecran de fin si aucun gagnant
        if run and nb_coups>=9:
            pygame.display.flip()
            run = message_victoire("Personne",grille,dif,surf,img_o,img_x)
            
    pygame.quit()

def tour_ia(dif, grille, tour):
    """Joue le tour de l'ia selon sa difficulté"""
    
    if dif==1:
        # Si la difficulté est facile, l'IA joue aléatoirement

        # Choisis une case au hasard en boucle jusqu'à ce que la case soit vide
        while True:
            x=randint(0,2)
            y=randint(0,2)
            
            if grille.get_case(x,y)==0:
                grille.set_case(x,y,1)
                return (x,y)
            
    if dif==2:
        # Si la difficulté est normale, l'IA comble les trous lorsque cela lui permet de gagner ou d'empécher
        # le joueur de gagner, et joue aléatoirement sinon (comme l'IA de niveau 2)
        x,y=grille.peut_gagner(1)

        # Si un trou existe pour l'IA, l'IA joue au niveau du trou
        if x!=None:
            grille.set_case(x,y,1)
            
        # Si aucun trou n'existe pour l'IA, on cherche les trous pour le joueur
        else:
            x,y=grille.peut_gagner(2)

            # Si un trou existe pour le joueur, l'IA joue au niveau du trou
            if x!=None:
                grille.set_case(x,y,1)

            # Si aucun trou n'existe pour le joueur, l'IA joue comme en dif facile
            else:
                return tour_ia(1,grille,tour)
        return (x,y)
    
    if dif==3:
        # Si dif est difficle, l'IA est imbattable, elle applique la méthode de l'IA normale pour combler si il
        # y a un trou et sinon elle joue d'après la méthode de https://fr.wikihow.com/gagner-au-morpion
        x,y=grille.peut_gagner(1)

        # Si un trou existe pour l'IA, l'IA joue au niveau du trou
        if x!=None:
            grille.set_case(x,y,1)

        # Si aucun trou n'existe pour l'IA, on cherche les trous pour le joueur
        else:
            x,y=grille.peut_gagner(2)

            # Si un trou existe pour le joueur, l'IA joue au niveau du trou
            if x!=None:
                grille.set_case(x,y,1)

            # Si aucun trou n'existe pour le joueur, l'IA applique la fonction tour_ia_3
            else:
                return tour_ia_3(grille, tour)
        return (x,y)

def tour_ia_3(grille, tour):
    """Joue de manière à toujours gagner, part du principe que l'IA complète les trous avant d'utiliser cette
    fonction. Si l'IA ne joue pas de coups personnalisé, elle jouera aléatoirement.
    Voir https://fr.wikihow.com/gagner-au-morpion pour avoir la méthode"""
    
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
    """Affiche un message de victoire avec le nom du gagnant (En entrée, gagnant est soit 'Joueur 1' soit
    'Joueur 2' soit 'Robot' soit 'Personne')"""
    
    sleep(.5)  # Pour éviter d'appuyer sur le bouton sans s'en rendre compte
    rect = pygame.Rect(130,0,490,750) # création d'une copie partielle de l'écran 
    sub = surf.subsurface(rect)       # -----------------------------------------
    surf.blit(blurSurf(sub,5),(130,0)) # Floute la copie de l'écran faite ci-dessus et l'affiche sur la fenêtre principale (pour l'esthétique)
    pygame.draw.line(surf, (36, 36, 36), (130, 0), (130, 750))
    pygame.draw.line(surf, (36, 36, 36), (620, 0), (620, 750))
    run=True
    while run:
        if run:
            replay_img = pygame.image.load("./images/New_game_Button.png").convert_alpha()
            replay_button = button.Button(258, 400, replay_img, 0.4)
            menu_img = pygame.image.load("./images/Menu_Button.png").convert_alpha()
            menu_button = button.Button(258, 500, menu_img, 0.4)

            # Si il y a égalité affiche "Aucun gagnant"
            if gagnant=="Personne":
                image_texte1 = police.render ("Aucun", 1 , (222, 109, 44))
                image_texte2 = police.render ("gagnant", 1 , (222, 109, 44))
                surf.blit(image_texte1, (225,125))
                surf.blit(image_texte2, (170,208))

            else:
                image_texte1 = police.render ("Victoire", 1 , (42, 201, 71))
                image_texte2 = police.render ("du", 1 , (42, 201, 71))
                image_texte3 = police.render (gagnant, 1, (42, 201, 71))
                surf.blit(image_texte1, (135,100))
                surf.blit(image_texte2, (325,183))
                if gagnant=="Robot":
                    surf.blit(image_texte3, (225,266))
                else:
                    surf.blit(image_texte3, (135,266)) 
            pygame.display.flip()

            
            
            if replay_button.draw(surf):  # Un appui sur le bouton replay (affiché à l'écran) relance une partie
                surf.fill((255,255,255))
                partie(dif) # Relance une partie
            
            
            
            for event in pygame.event.get(): 
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN: # Un appui sur la touche "Entrée" relance une partie
                        surf.fill((255,255,255))
                        partie(dif)
                if event.type==pygame.QUIT:
                    run = False
                    exit()
            
            if menu_button.draw(surf):
                run = False
                sleep(0.2)
                menu.main_menu()
                
    return run

class Menu():
    """Classe permettant la création d'un menu. Prend un paramètre niveau à l'instation (0 de base)"""
    def __init__(self, niveau=0):
        """Création d'une variable niveau permettant de gérér la difficulté du jeu (de 0 à 3)"""
        self.niveau = niveau
    def main_menu(self):
        """Menu principal du jeu comportant trois rubriques : Play (pour lancer une parite) ; Options (pour régler la difficulté du jeu) et Credits (noms du binome ayant travaillé sur le jeu)"""  
        pygame.display.set_caption("Main Menu")  # titre de la fenêtre 
        run = True
        # permet de transformer un texte de format str dans une forme affichable par pygame
        titre_txt = police.render ("Morpion", 1 , (0))
        # charge les images des boutons
        play_img = pygame.image.load("./images/Play_Button.png").convert_alpha()
        options_img = pygame.image.load("./images/Options_Button.png").convert_alpha()
        credits_img = pygame.image.load("./images/bouton_credits.png").convert_alpha()
        # permet de créer des boutons avec pygame en utilisant la class bouton du fichier button.py
        play_button = button.Button(258, 275, play_img, 0.4) 
        options_button = button.Button(258, 400, options_img, 0.4)
        credits_button = button.Button(258, 525, credits_img, 0.4)
        while run:
            surf.fill((112, 112, 112)) # rempli la surface pygame avec un fond d'écran gris
            surf.blit(titre_txt, (165,80))
            for event in pygame.event.get(): # si le bouton quitter est pressé, permet de sortir du programme
                if event.type==pygame.QUIT:
                    run = False
                    exit()
            if play_button.draw(surf):  # Un appui sur le bouton Play (affiché à l'écran) relance une partie
                surf.fill((255,255,255))
                partie(self.niveau)  # création d'une partie
            if options_button.draw(surf): # Un appui sur le bouton Options (affiché à l'écran) ouvre la fenêtre options
                run = False
                menu.options() # ouverture de la fenêtre options
            if credits_button.draw(surf): # Un appui sur le bouton Credits (affiché à l'écran) ouvre la fenêtre des crédits
                run = False
                menu.credits() # ouverture de la fenêtre options
            pygame.display.flip()
    
    def selec_niveau(self, niv, l_button, actif_img, pos_x, pos_y):
        """Fonction permettant de sélectionner le niveau de difficulté du jeu.
        Celle-ci prend en paramètre le niveau de difficulté désiré, une liste des boutons qui doivent être affichés, une image actif_img permettant
        de renseigner l'utilisateur du niveau de difficulté actuellement sélectionné, et finalement la position (pos_x, pos_y) de celle-ci sur l'écran"""
        l = list(l_button) # crée une copie de la liste l_button
        l.pop(niv) # retire le bouton  associé au niveau de difficulté actuellement sélectionné de la liste l
        for element in l: # affiche les 3 autres boutons et gère le click
            if element[0].draw(surf): # permet d'afficher le bouton et de détecter s'il a été pressé
                self.niveau = element[1] # dans ce cas le niveau de difficulté prend la valeur correspondant au bouton
        actif_button= button.Button(pos_x, pos_y, actif_img, 0.4) 
        actif_button.draw(surf) # affiche bouton actif
                
    def options(self):
        """Affiche la fenêtre options. Celle-ci permet de régler le niveau de difficulté du jeu.
        4 niveaux de difficulté:
        0 --> Joueur contre joueur
        1 --> Joueur contre IA facile
        2 --> Joueur contre IA moyenne
        3 --> Joueur contre IA difficile"""
        pygame.display.set_caption("Options") # titre de la fenêtre
        run = True
        # permet de transformer un texte de format str dans une forme affichable par pygame
        titre_txt = police.render ("Difficulté", 1 , (0))
        joueur_txt = police2.render ("joueur", 1 , (0))
        contre_txt = police2.render ("VS", 1 , (250,0,0)) 
        ia_txt = police2.render ("IA", 1 , (0))
        simple_txt = police2.render ("simple", 1 , (50, 168, 82))
        moyenne_txt = police2.render ("moyenne", 1 , (232, 155, 23))
        difficile_txt = police2.render ("difficile", 1 , (250,0,0))
        # charge les images des boutons
        dif0g_img = pygame.image.load("./images/dif0(grey).png").convert_alpha()
        dif1g_img = pygame.image.load("./images/dif1(grey).png").convert_alpha()
        dif2g_img = pygame.image.load("./images/dif2(grey).png").convert_alpha()
        dif3g_img = pygame.image.load("./images/dif3(grey).png").convert_alpha()
        actif_img = pygame.image.load("./images/dif_actif.png").convert_alpha()
        back_img = pygame.image.load("./images/Back_Button.png").convert_alpha()
        # permet de créer des boutons avec pygame en utilisant la class bouton du fichier button.py
        dif0_button = button.Button(100, 200, dif0g_img, 0.4)
        dif1_button = button.Button(260, 200, dif1g_img, 0.4)
        dif2_button = button.Button(420, 200, dif2g_img, 0.4)
        dif3_button = button.Button(580, 200, dif3g_img, 0.4)
        back_button = button.Button(258, 600, back_img, 0.4)
        # liste de tuple comportant un bouton et le niveau de difficulté qui leur est associé (permet d'optimiser le programme)
        l_button = [(dif0_button,0),(dif1_button,1),(dif2_button,2),(dif3_button,3)]
        while run:
            surf.fill((112, 112, 112)) # Fond d'écran gris
            # Affiche le texte chargé ci-dessus sur l'écran
            surf.blit(titre_txt, (75,50))
            surf.blit(joueur_txt, (85,300)) # 0
            surf.blit(joueur_txt, (245,300)) # 1
            surf.blit(joueur_txt, (405,300)) # 2
            surf.blit(joueur_txt, (570,300)) # 3
            surf.blit(contre_txt, (115,330)) # 0
            surf.blit(contre_txt, (275,330)) # 1
            surf.blit(contre_txt, (435,330)) # 2
            surf.blit(contre_txt, (600,330)) # 3
            surf.blit(joueur_txt, (85,360)) # 0
            surf.blit(ia_txt, (275,360)) # 1
            surf.blit(ia_txt, (435,360)) # 2
            surf.blit(ia_txt, (600,360)) # 3
            surf.blit(simple_txt, (245,390)) # 1
            surf.blit(moyenne_txt, (395,390)) # 2
            surf.blit(difficile_txt, (545,390)) # 3

            if self.niveau == 0: # permet d'afficher l'ensemble des boutons lorsque que le niveau de difficulté est de 0 (Joueur contre joueur)
                self.selec_niveau(0, l_button, actif_img, 100, 200)

            if self.niveau == 1: # permet d'afficher l'ensemble des boutons lorsque que le niveau de difficulté est de 1 (IA facile)
                self.selec_niveau(1, l_button, actif_img, 260, 200)

            if self.niveau == 2: # permet d'afficher l'ensemble des boutons lorsque que le niveau de difficulté est de 2 (IA moyenne)
                self.selec_niveau(2, l_button, actif_img, 420, 200)
        
            if self.niveau == 3: # permet d'afficher l'ensemble des boutons lorsque que le niveau de difficulté est de 3 (IA difficile)
                self.selec_niveau(3, l_button, actif_img, 580, 200)
            
            if back_button.draw(surf): # Affiche un bouton permmettant de revenir au menu principal
                run = False
                menu.main_menu()
            
            for event in pygame.event.get(): # si le bouton quitter est pressé, permet de sortir du programme
                if event.type==pygame.QUIT:
                    run = False
                    exit()   
            pygame.display.flip() # permet de raffraichir la page
    
    def credits(self):
        """Affiche la fenêtre crédits"""
        pygame.display.set_caption("Crédits") # Titre de la fenêtre
        run = True
        # charge l'image du bouton
        back_img = pygame.image.load("./images/Back_Button.png").convert_alpha()
        # permet de créer un bouton avec pygame en utilisant la class bouton du fichier button.py
        back_button = button.Button(258, 600, back_img, 0.4)
        # permet de transformer un texte de format str dans une forme affichable par pygame
        titre_txt = police.render ("Crédits", 1 , (0))
        realise_txt = police3.render("Réalisé par :", 1, (0))
        raphael_txt  = police3.render("Raphaël FISCHER", 1, (50, 168, 82))
        dorian_txt  = police3.render("Dorian COURCELLE", 1, (50, 168, 82))
        while run:
            surf.fill((112, 112, 112)) # Fond d'écran gris
            
            # Affiche le texte chargé ci-dessus sur l'écran
            surf.blit(titre_txt, (165,80))
            surf.blit(realise_txt, (180,220))
            surf.blit(raphael_txt, (150,290))
            surf.blit(dorian_txt, (140,360))

            for event in pygame.event.get(): # si le bouton quitter est pressé, permet de sortir du programme
                if event.type==pygame.QUIT:
                    run = False
                    exit()
            if back_button.draw(surf): # Affiche un bouton permmettant de revenir au menu principal
                run = False
                menu.main_menu()
            
            pygame.display.flip() # permet de raffraichir la page

# Programme principal
menu = Menu() # instansiation
menu.main_menu() # lancement du jeu
pygame.quit() # quitte pygame