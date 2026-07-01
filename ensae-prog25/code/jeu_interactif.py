import pygame 
from pygame.locals import *
import numpy as np
from pygame.font import*
import jeu_interactif_constantes as jc

# On affiche la grille et les chiffres
jc.affichage_de_la_grille()
jc.affichage_des_chiffres()


# Initialisation de la boucle de jeu à partir de la constante continuer présente dans jeu_interactif_constantes
while jc.continuer  :
    
    # Création des événements
    for event in pygame.event.get () :

        # Possibilité de fermer la fenêtre
        if event.type == QUIT: 
            jc.continuer = 0

        # Les interactions
        if event.type == MOUSEBUTTONDOWN :

            # Quand il y a un clic : une case est choisie et on récupère les coordonnées de la souris
            x = event.pos [0]
            y = event.pos [1]
            colonne , ligne = int(np.floor(x/jc.largeur_case)) , int(np.floor(y/jc.hauteur_case))
            
            # Si la case choisie n'est ni noire, ni orange, ni marron, ni rose alors elle est valide et devient orange et on joue un bruit amusant
            if jc.grid.color[ligne][colonne] != 4 :
                jc.fenetre.blit(jc.case_orange.subsurface(0, 0, jc.largeur_case, jc.hauteur_case), (colonne*jc.largeur_case,ligne*jc.hauteur_case))
                jc.listes_cases_choisies.append((ligne,colonne))
                jc.son.play()

            # Si une case avait déjà été choisie, alors le choix de la deuxième forme peut-être une paire, il faut agir en conséquence
            if len(jc.listes_cases_choisies) == 2 :
                i0 = jc.listes_cases_choisies[0][0]
                j0 = jc.listes_cases_choisies[0][1]
                i1 = jc.listes_cases_choisies[1][0]
                j1 = jc.listes_cases_choisies[1][1]
                
                # Si les deux cases choisies ne forment pas une paire, on revient au point de départ 
                if jc.paire_légale((i0,j0),(i1,j1)) == False :
                    
                    jc.fenetre.blit(jc.cases[jc.grid.color[i0][j0]].subsurface(0, 0,jc.largeur_case, jc.hauteur_case), (j0*jc.largeur_case,i0*jc.hauteur_case))
                    jc.fenetre.blit(jc.cases[jc.grid.color[i1][j1]].subsurface(0, 0, jc.largeur_case, jc.hauteur_case), (j1*jc.largeur_case,i1*jc.hauteur_case))
                    
                    print('Veuillez choisir une paire de cases compatibles.')

                # Si elles forment une paire, alors les deux cases deviennent roses et c'est au tour de l'algorithme
                else : 
                    jc.grid.color[i0][j0] = 4
                    jc.grid.color[i1][j1] = 4
                    jc.fenetre.blit(jc.case_rose.subsurface(0, 0, jc.largeur_case, jc.hauteur_case), (j0*jc.largeur_case,i0*jc.hauteur_case))
                    jc.fenetre.blit(jc.case_rose.subsurface(0, 0, jc.largeur_case, jc.hauteur_case), (j1*jc.largeur_case,i1*jc.hauteur_case))

                    # On affiche le nouveau score en cachant l'ancien par un rectangle noir et on affiche le nouveau
                    jc.score += jc.grid.cost (((i0,j0),(i1,j1)))
                    jc.fenetre.blit(jc.case_noire.subsurface(0, 0, 300, 100), (100,700))
                    jc.affichage_du_score(jc.score)
                    
                    # Si l'algorithme ne peut pas jouer parce qu'il n'y a plus de paire possible alors on arête le jeu
                    if jc.choix_algorithmique_de_la_paire_suivante() == False:
                        jc.continuer = 0

                    # Sinon il joue et ses cases deviennent marron et on affiche de nouveau le score  
                    else :
                        algo0 = jc.choix_algorithmique_de_la_paire_suivante()[0]
                        algo1 = jc.choix_algorithmique_de_la_paire_suivante()[1]
                        jc.grid.color[algo0[0]][algo0[1]] = 4
                        jc.grid.color[algo1[0]][algo1[1]] = 4
                        jc.fenetre.blit(jc.case_marron.subsurface(0, 0, jc.largeur_case, jc.hauteur_case), (algo0[1]*jc.largeur_case,algo0[0]*jc.hauteur_case))
                        jc.fenetre.blit(jc.case_marron.subsurface(0, 0, jc.largeur_case, jc.hauteur_case), (algo1[1]*jc.largeur_case,algo1[0]*jc.hauteur_case))
                        jc.score += jc.grid.cost ((algo0,algo1))
                        jc.fenetre.blit(jc.case_noire.subsurface(0, 0, 300, 100), (100,700))
                        jc.affichage_du_score(jc.score)
                        jc.explosion.play()
                
                # Si deux cases avaient été choisies à la suite, alors quoi qu'il se soit passé, on réinitialise cette liste pour recommencer le choix de deux cases.
                jc.listes_cases_choisies = []
                
    # On actualise pour que tous les changements soient affichés et on affiche de nouveaux les chiffres au cas où une case a été choisie mais pas validée dans une paire, superposition oblige
    jc.affichage_des_chiffres()
    pygame.display.flip()
    
    # Si après les coups qui ont été joués, il n'y a plus aucune possibilité, on arête le jeu
    if jc.grid.all_pairs() == [] :
        jc.continuer = 0

    # Messages de fin
    if not jc.continuer :
        print ('Fin du jeu monsieur Loiseau')
        print('Votre score est de ' , jc.score_grille(jc.score))
        
# On ferme la fenêtre quand le jeu est fini
pygame.quit()
