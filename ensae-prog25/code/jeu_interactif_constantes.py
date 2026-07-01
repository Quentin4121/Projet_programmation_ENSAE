from grid import Grid
from solver import SolverHongrois
import pygame 
from pygame.locals import *
import numpy as np

# On initialise pygame, le module de texte et le module de son
pygame.init()
pygame.font.init()
pygame.mixer.init()

# On récupère une grille dont le choix est laissé au joueur
numéro_grille = str(input('Quelle grille voulez-vous ?')) 
data_path = "../input/"
file_name = data_path + "grid"+numéro_grille+".in"
grid = Grid.grid_from_file(file_name)
n = grid.n
m = grid.m

# Les variables absolument nécessaires à la boucle
score = 0
listes_cases_choisies = []
continuer = 1

# Ici commence la création de la grille. On ouvre une fen^tre 1250X800 et on la divise pour que toutes les cases rentrent dans la grille
largeur_case = 1250/m
hauteur_case = 700/n
largeur_fenetre = 1250
hauteur_fenetre = 800

# On ouvre la fenêtre
fenetre =  pygame.display.set_mode((largeur_fenetre,hauteur_fenetre))

# On crée tous les éléments de la grille en les important depuis le fichier code
fond = pygame.image.load("fond_base.png").convert()
case_blanche = pygame.image.load("fond_blanc.png").convert()
case_bleue = pygame.image.load("fond_bleu.png").convert()
case_noire = pygame.image.load("fond_noir.png").convert()
case_rouge = pygame.image.load("fond_rouge.png").convert()
case_verte = pygame.image.load("fond_vert.png").convert()
case_orange = pygame.image.load("fond_orange.png").convert_alpha()
case_rose = pygame.image.load("fond_rose.png").convert_alpha()
case_marron = pygame.image.load("fond_marron.png").convert_alpha()
cases = [case_blanche,case_rouge,case_bleue,case_verte,case_noire]

# Deux petits sons qui rajouteront du piment à la partie
son = pygame.mixer.Sound("bruitage.wav")
explosion = pygame.mixer.Sound("explosion.wav")


def affichage_de_la_grille () :
    for i in range (n) :
        for j in range (m) :
            # On affiche des cases de couleur
            case = cases[grid.color[i][j]].subsurface(0, 0, largeur_case, hauteur_case)
            fenetre.blit(case, (j*largeur_case,i*hauteur_case))


def affichage_des_chiffres () :
    # On affiche les chiffres sous forme de texte
    for i in range (n) :
        for j in range (m) :
            if grid.color [i][j] < 4 :
                font = pygame.font.Font(None, int(np.ceil(1000/(n+m))) ) 
                text = font.render(str(grid.value[i][j]), True, (0,0,0))
                fenetre.blit(text, ((j+0.35)*largeur_case,(i+0.35)*hauteur_case)) 


def affichage_du_score (score) :
    score_str = 'Score = ' + str(score) 
    font = pygame.font.Font(None, int(np.ceil(1000/(n+m))) ) 
    text = font.render(score_str , True, (255,255,255))
    fenetre.blit(text, ((100,725))) 
    return 


def score_grille (score) :
    for i in range (n) :
        for j in range (m) :
            if grid.color [i][j] != 4 :
                score += grid.value [i][j]
    return score


def liste_des_voisines_compatibles (i,j) :
    '''Cette fonction prend en argument les coordonnées d'une case et renvoie la liste des cases avec lesquelles on peut former une paire.
    C'est-à-dire une case adjacente et de couleur compatible.'''

    Liste_des_voisines = []
    
    if i != n-1 :
        if grid.color_friendly(((i,j),(i+1,j))) == True :
            Liste_des_voisines.append ((i+1,j))

    if i != 0 :
        if grid.color_friendly(((i,j),(i-1,j))) == True :
            Liste_des_voisines.append ((i-1 , j))
        
    if j != m-1 :
        if grid.color_friendly(((i , j),(i , j+1))) == True :
            Liste_des_voisines.append ((i , j+1))

    if j != 0 :
        if grid.color_friendly(((i , j),(i , j-1))) == True :
            Liste_des_voisines.append ((i , j-1))
    return Liste_des_voisines


def choix_possible (x,y) :
    '''Etant données deux cases, '''
    choix_possible = True
    if  (grid.color[x][y] >= 4) :
        choix_possible = False

    return choix_possible


def paire_légale (Case0,Case1) :
    '''True si une paire est conforme aux règle, False sinon'''
    if (grid.color[Case0[0]][Case0[1]] < 4) and (grid.color[Case1[0]][Case1[1]] < 4) : 
        if Case1 in liste_des_voisines_compatibles(Case0[0],Case0[1]) :
            return True 
   
    return False


def choix_algorithmique_de_la_paire_suivante () :
    '''Cette fonction renvoie la paire choisie par l'algorithme. Quand le joueur choisit une paire, les deux cases prennent la valeur 4 
    cette fonction applique le SolverHongroid à la grille dans laquelle les deux valeurs des cases sont devenues 4. Il choisit ensuite 
    de jouer la paire qui contribue le plus faiblement au score total.'''
    Résolution = SolverHongrois(grid)
    paires = Résolution.résolution_optimale_avec_algorithme_optimal()[1]
    if not paires :
        return False 
    else :
        Liste_des_coûts = [grid.cost((i,j)) for i,j in paires]
        x = min(Liste_des_coûts)
        i = Liste_des_coûts.index (x)
        return paires[i] 
    