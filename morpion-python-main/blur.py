import pygame

def blurSurf(surface, amt):
    """
    Fonction permettant de floutter la fenêtre par une valeur donnée (amt)
    amt = 1 --> pas de flou
    """
    if amt < 1.0:
        raise ValueError("Arg 'amt' must be greater than 1.0, passed in value is %s"%amt) # la valeur doit être supérieur à 1
    scale = 1.0/float(amt)
    surf_size = surface.get_size() # accède à la taille de la fenêtre à flouter
    scale_size = (int(surf_size[0]*scale), int(surf_size[1]*scale)) 
    surf = pygame.transform.smoothscale(surface, scale_size) # permet de floutter
    surf = pygame.transform.smoothscale(surf, surf_size) # permet de floutter
    return surf # renvoie la surface flouttée
