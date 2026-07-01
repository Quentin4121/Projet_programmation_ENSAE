from grid import Grid
import networkx as nx    #Cette librairie va nous aider lors de la résolution du problème en passant par les graphes
from scipy.optimize import linear_sum_assignment
from itertools import combinations  #Cette libraire sert uniquement dans la fonction qui suit (lignes 5-6) pour la résolution du problème dans le cas général.
from itertools import combinations
import numpy as np



#----------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------



class Solver:
    """
    A solver class. 

    Attributes: 
    -----------
    grid: Grid
        The grid
    pairs: list[tuple[tuple[int]]]
        A list of pairs, each being a tuple ((i1, j1), (i2, j2))
    """

    def __init__(self, grid):
        """
        Initializes the solver.

        Parameters: 
        -----------
        grid: Grid
            The grid
        """
        self.grid = grid
        self.pairs = list()

    def score(self):
        """
        Computes the score of the list of pairs in self.pairs
        """
        return "Method not implemented yet"




#----------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------




class SolverGreedy (Solver) :
    '''Voilà la classe qui devrait permettre d'obtenir des valeurs approchées (parfois de très loin!) du score optimal que l'on peut obtenir pour chaque grille.
    Sa rapidité doit être de l'ordre de 2**(n*m) opérations dans la mesure où nous nous intéressons à chaque fois à chaque case (il y en a n*m) et ses
    relations avec les cases adjacentes.'''

    def __init__(self,grid) :
        self.grid = grid
    
#----------------------------------------------------------------------------------------------------------------------------------------------------------
    
    def choix_de_paire_pour_case_donnee(grid,case) :
        '''I) Utilité -->   Cette méthode servira, étant données une case et une liste de paires , à choisir la paire contenant cette case dont le score est le plus faible.
        On peut déjà voir que l'algorithme ne rendra pas un résultat optimal car il ne prend en compte qu'une paire à la fois et pas des chemins augmentants, 
        mais il s'agit là d'une méthode de résolution naïve.'''
        '''II) Explication 6 premières lignes -->  On pourrait ne s'intéresser qu'à des cases avec lesquelles il est possible de faire au moins une paire. Mais pour 
        simplifier le calcul du score final et la recherche des cases seules, on permet à cette méthode d'être appliquée à des cases avec lesquelles il est impossible
        de faire une paire.'''

              
        z = 0          # Voir  II) Explication 6 premières lignes
        for pair in grid.all_pairs() :
            if pair [0] != case and pair[0] != case and pair[1] != case and pair[1] != case :
                z += 1                
        if z == len(grid.all_pairs()) :
            return 'On ne peut faire aucune paire avec cette case'                                       

        L = grid.all_pairs()
        Liste_des_paires_contenant_case = []     # Etant donnée la case, on prend toutes les paires qui la contiennent
        for k in range (len(L)) :
            if L[k][0] == case or L[k][1] == case :
                Liste_des_paires_contenant_case.append (L[k])
        
        x = min([grid.cost (pair) for pair in Liste_des_paires_contenant_case])  # On regarde ensuite le coût minimum de ces paires
        for paire in Liste_des_paires_contenant_case :
            if grid.cost (paire) == x :    # Et on choisit comme paire la première de la liste dont le score est égal au minimum, peu importe si elle est unique
                return paire               # Le return est dans une condition mais le minimum est nécessairement atteint donc à l'une des itérations, la condition sera remplie

#----------------------------------------------------------------------------------------------------------------------------------------------------------

    def choix_gluton_des_paires (grid) : 
        '''Cette méthode servira à choisir les paires que l'on va prendre en tant que paires pour notre score final. On commence par regarder l'ensemble des
        paires possibles. On regarde la première case de la première paire, on sélectionne la paire contenant cette case ayant le coût le plus faible
        et on enlève toutes les paires contenant cette case des paires possibles. On recommence, car la première paire aura changé.'''

        L = grid.all_pairs()
        Liste_paires_choisies0 = []
        for k in range (len(grid.all_pairs())) :

            if L == [] : 
                break

            if L != [] : 
                # On sélectionne les deux paires au coût le moins cher contenant respectivement la premiere et la deuxième case de la première paire possible
                Liste_paires_choisies0.append(SolverGreedy.choix_de_paire_pour_case_donnee(grid,L[0][0]))
                Liste_paires_choisies0.append(SolverGreedy.choix_de_paire_pour_case_donnee(grid,L[0][1]))
                L.pop(0)

        # Ne reste plus qu'à supprimer les doublons dans la liste des paires choisies le double Liste_paires_choisies0.append juste au-dessus pourrait avoir été appliqué à la même paire
        Liste_paires_choisies1 = []
        for element in Liste_paires_choisies0 :
            if element not in Liste_paires_choisies1 :
                Liste_paires_choisies1.append(element)

        return Liste_paires_choisies1 
       
#----------------------------------------------------------------------------------------------------------------------------------------------------------
    
    def choix_glouton_des_cases_seules (grid) :
        '''La méthode précédente servait à choisir les paires de cases. Il faut maintenant récupérer toutes les cases qui n'ont pas eu la chance 
        d'être prises dans une paire. Cela concerne les cases avec lesquelles il est impossible de faire une paire et les cases qui étaient présentes
        dans grid.all_pairs mais qui ne sont au final dans aucune paire.'''

        Liste_cases_prises_dans_une_paire = []
        for Case0,Case1 in SolverGreedy.choix_gluton_des_paires(grid) :
            if Case0 not in Liste_cases_prises_dans_une_paire :
                Liste_cases_prises_dans_une_paire.append(Case0) 
            if Case1 not in Liste_cases_prises_dans_une_paire :
                Liste_cases_prises_dans_une_paire.append(Case1)
       
        Cases_seules = []
        for i in range (grid.n) :
            for j in range (grid.m) :
                if (SolverGreedy.choix_de_paire_pour_case_donnee(grid,(i,j)) == 'On ne peut faire aucune paire avec cette case' and grid.color != 4) or ((i,j) not in Liste_cases_prises_dans_une_paire) :
                    if (i,j) not in Cases_seules :
                        Cases_seules.append ((i,j))

        return Cases_seules 
    
#----------------------------------------------------------------------------------------------------------------------------------------------------------

    def score_final_glouton (grid) :
        '''Cette dernière méthode va permettre de calculer le score final avec notre algorithme glouton. Il ne s'agit pas nécessairement d'un résultat optimal.
        La première boucle compte le score qui est dû aux paires que l'on a choisies. La seconde compte le score dû aux cases seules.'''

        score_final = 0
        for pair in SolverGreedy.choix_gluton_des_paires(grid) : 
            score_final = score_final+grid.cost(pair)
        for k in range (len(SolverGreedy.choix_glouton_des_cases_seules(grid))) :
            i = SolverGreedy.choix_glouton_des_cases_seules(grid)[k][0]
            j = SolverGreedy.choix_glouton_des_cases_seules(grid)[k][1]
            score_final = score_final+grid.value[i][j]

        return score_final


#----------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------



class SolverMatching:
    '''Cette classe est celle qui devrait nous permettre de résoudre le problème de manière opitmale avec le plus haut degré de confiance en le résultat. Elle 
    utilise la bibliothèque networkx qui sert à résoudre des problèmes tournant autour des graphes. Le lecteur avisé trouvera une autre classe appelée
    SolverMatching_sans_networkx avec laquelle nous cherchons à résoudre le problème sans utiliser cette librairie.'''

    def __init__(self,grid):
        self.grid = grid

#----------------------------------------------------------------------------------------------------------------------------------------------------------

    def graphe_biparti (self) :
        '''Cette méthode crée un graphe biparti qui représentera le problème sous forme de graphe, comme expliqué dans l'énoncé. 
        On renvoie également la liste des noeuds qui seront sur la gauche de notre graphe (les noeuds pairs)'''

        G = nx.Graph()    # On initialise un graphe vide
        côté_gauche = []
        for Case0,Case1 in self.grid.all_pairs() :
            G.add_edge(Case0, Case1) # On ajoute les arêtes entre les points, qui correspondent exactement aux paires possibles (donc que l'on trouve dans la fonction all_pairs)
            G.add_node(Case0, bipartite = (Case0[0]+Case0[1])%2)
            G.add_node(Case1, bipartite = (Case1[0]+Case1[1])%2)

            if (Case0[0]+Case0[1])%2 == 0 :
                côté_gauche.append(Case0)
            else :
                côté_gauche.append(Case1)
  
        return G,côté_gauche
    
#----------------------------------------------------------------------------------------------------------------------------------------------------------

    def liste_des_paires_choisies(self) :
        ''' I) Explications -->   La méthode précédente permet de ramener le problème à un problème identique ne concernant que des graphes connexes. 
        On peut maintenant amorcer la résolution en cherchant les ensembles de paires minimisant le score pour chaque composante connexe.
        La fonction algorithms.bipartite.maximum_matching renvoie un dictionnaire des paires qu'il faut prendre pour avoir un maximum
        de paires. Si l'ensemble des paires pour maximiser le nombre de paires est {  ((1,2),(1,3))  ;  ((4,8),(5,8))  ,  ((10,6),(10,7))} alors
        la fonction renvoie le dictionnaire { (1,2):(1,3) , (4,8):(5,8) , (10,6):(10,7) , (1,3):(1,2) , (5,8):(4,8) , (10,7):(10,6) } à l'ordre près 
        pour chaque moitié du dictionnaire. C'est-à-dire qu'étant donné un ensemble de paires, dans la première moitié du dico on retrouvera 
        les paires ((i,j),(k,l)) sous la forme (i,j):(k,l) et dans la deuxième moitié on retrouvera son symétrique (k,l):(i,j). '''
     
        # La fonction nx.bipartite.maximum_matching prend en argument un graphe biparti et une liste de sommets qui sont tous du même côté
        return nx.bipartite.maximum_matching(SolverMatching.graphe_biparti(self)[0],SolverMatching.graphe_biparti(self)[1])
        
    
#----------------------------------------------------------------------------------------------------------------------------------------------------------
    
    def solution_optimale (self) :
        '''Cette méthode est celle qui nous permettra enfin de résoudre le problème dans le cas où toutes les paires ont la même valeur. 
        Dans ce cas, il s'agit de récupérer la liste des paires optimales grâce aux méthodes précédentes et de compter le nombre de cases 
        de notre grille qui ne sont dans aucune paire ET qui ne sont pas noires, car une paire à une valeur de 0 pour notre score final.'''
        
        Listes_des_cases_utilisees = []   # On crée la liste de toutes les cases qui seront prises dans une paire
        for pair in SolverMatching.liste_des_paires_choisies(self) : # pair parcourt les clés du dico
            if pair not in Listes_des_cases_utilisees :
                Listes_des_cases_utilisees.append (pair)
                
        Nombre_de_cases_seules = 0         
        for k in range (self.grid.n) :        # Pour chaque case de la grille, si elle n'est pas dans une paire et qu'elle n'est pas noire, elle sera comptée en case seule
            for i in range (self.grid.m) :
                if (k,i) not in Listes_des_cases_utilisees and self.grid.color [k][i] != 4 :
                    Nombre_de_cases_seules+=1
                    
        return Nombre_de_cases_seules



#----------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------



class SolverMatching_sans_networkx :
    '''Cette classe doit servir à résoudre le problème dans le cas où la grille ne comporte que des 1 sans avoir 
    recours à la librairie networkx'''
    def ___inti__ (self,grid) :
        self.grid = grid

#----------------------------------------------------------------------------------------------------------------------------------------------------------

    def score_de_paires (self,L) :
        '''Cette fonction est une fonction de calcul du score comme il y en a tant dans ce fichier'''
        Utilisées = []
        score = 0
        for Case0,Case1 in L :
            if Case0 not in Utilisées : 
                Utilisées.append (Case0)
            if Case1 not in Utilisées :
                Utilisées.append(Case1)
        
        for i in range (self.grid.n) :
            for j in range (self.grid.m) :
                if (i,j) not in Utilisées and self.grid.color[i][j] !=4 :
                    score += 1
    
        return score
    
#----------------------------------------------------------------------------------------------------------------------------------------------------------

    def verifier_repetitions (liste) :
        '''Cette méthode sert à faire moins d'opérations. Dans notre raisonnement, on teste toutes les combinaisons possibles 
        de paires à partir des parties de grid.all_pairs mais certaines parties contiennent plusieurs paires contenant une même 
        case. Ceci est une combinaison impossible donc il ne sert à rien d'en calculer le score.'''

        for k in range (len(liste)) :
            for i in range (k+1,len(liste)) :
                if (liste[i][0] == liste[k][0]) or (liste[i][0] == liste[k][1]) or (liste[i][1] == liste[k][0]) or (liste[i][1] == liste[k][1]) : 
                    return False
        return True

#----------------------------------------------------------------------------------------------------------------------------------------------------------

    def calcul_du_score (self):
        '''Cette méthode calcule le score final de notre grille. On prend toutes les parties non vides de grid.all_pairs
        et on en calcule le score si c'est une combinaison de paires valides (i.e. telle qu'une case est au plus présente dans une seule paire).'''

        # On initialise une variable qui nous servira de minimum, au départ elle prend la valeur la plus grande possible (lignes 290-293)
        x = 0
        for i in range (self.grid.n) :
            for j in range (self.grid.m) :
                x += self.grid.value[i][j]
        
        def liste_parties_a_r_elements(L,r):
            '''Cette fonction prend en argument une liste L et un entier r et renvoie la liste des sous-listes de L à r éléments'''
            return list(combinations(L, r))
        
        for k in range (1,len(self.grid.all_pairs())) :
            L = liste_parties_a_r_elements(self.grid.all_pairs(),k)

            for j in range (len(liste_parties_a_r_elements(self.grid.all_pairs(),k))) :
                if SolverOptimal_glouton.verifier_repetitions(L[j]) == True : # Si la combinaison de paires est valide, on calcule le score
                    
                    if SolverMatching_sans_networkx.score_d_une_combinaison_de_paires(self,list(L[j])) < x :
                        x = SolverMatching_sans_networkx.score_d_une_combinaison_de_paires(self,list(L[j]))
                
        return x
    



#----------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------




class SolverOptimal_glouton:
    def __init__(self, grid):
        self.grid = grid
    
#----------------------------------------------------------------------------------------------------------------------------------------------------------

    def score_d_une_combinaison_de_paires (self,Liste) :
        '''Cette méthode prend en argument une combinaison possibles de paires sous forme de liste et renvoie le score associé'''

        # On cherche les cases qui sont appariées dans une paire 
        score = 0
        Cases_appariées = []
        for j in range (len(Liste)) :
            for case in Liste[j]: 
                if case not in Cases_appariées :
                    Cases_appariées.append(case)
                
        # On ajoute au score la valeur des cases qui ne sont dans aucune paire
        for i in range (self.grid.n) :
            for j in range (self.grid.m) :
                if (i,j) not in Cases_appariées :
                    if self.grid.color [i][j] != 4 :
                        score += self.grid.value [i][j]
                        
        # On ajoute au score le coût des paires choisies
        for pair in Liste :
            score += self.grid.cost (pair)
            
        return score 

#----------------------------------------------------------------------------------------------------------------------------------------------------------

    def verifier_repetitions (liste) :
        '''Cette méthode sert à faire moins d'opérations. Dans notre raisonnement, on teste toutes les combinaisons possibles 
        de paires à partir des parties de grid.all_pairs mais certaines parties contiennent plusieurs paires contenant une même 
        case. Ceci est une combinaison impossible donc il ne sert à rien d'en calculer le score.'''

        for k in range (len(liste)) :
            for i in range (k+1,len(liste)) :
                if (liste[i][0] == liste[k][0]) or (liste[i][0] == liste[k][1]) or (liste[i][1] == liste[k][0]) or (liste[i][1] == liste[k][1]) : 
                    return False
        return True

#----------------------------------------------------------------------------------------------------------------------------------------------------------

    def calcul_du_score (self):
        '''Cette méthode calcule le score final de notre grille. On prend toutes les parties non vides de grid.all_pairs
        et on en calcule le score si c'est une combinaison de paires valides (i.e. telle qu'une case est au plus présente dans une seule paire).'''

        # On initialise une variable qui nous servira de minimum, au départ elle prend la valeur la plus grande possible (lignes 290-293)
        x = 0
        for i in range (self.grid.n) :
            for j in range (self.grid.m) :
                x += self.grid.value[i][j]
        
        def liste_parties_a_r_elements(L,r):
            '''Cette fonction prend en argument une liste L et un entier r et renvoie la liste des sous-listes de L à r éléments'''
            return list(combinations(L, r))
        
        for k in range (1,len(self.grid.all_pairs())) :
            L = liste_parties_a_r_elements(self.grid.all_pairs(),k)

            for j in range (len(liste_parties_a_r_elements(self.grid.all_pairs(),k))) :
                if SolverOptimal_glouton.verifier_repetitions(L[j]) == True : # Si la combinaison de paires est valide, on calcule le score
                    
                    if SolverOptimal_glouton.score_d_une_combinaison_de_paires(self,list(L[j])) < x :
                        x = SolverOptimal_glouton.score_d_une_combinaison_de_paires(self,list(L[j]))
                
        return x   




#----------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------




class SolverHongrois:
    def __init__(self, grille:Grid):
        self.grille = grille  # Stocke la grille donnée
        self.n = grille.n  # Nombre de lignes
        self.m = grille.m  # Nombre de colonnes
        self.cellules_paires = []  # Liste des cellules de type 'paire'
        self.cellules_impaires = []  # Liste des cellules de type 'impaire'
        self.paires_trouvees = []  # Liste des paires optimales
        self.matrice_de_cout= None

#----------------------------------------------------------------------------------------------------------------------------------------------------------

    def construire_matrice(self):
        '''Construit la matrice de coût en classant les cellules paires et impaires'''
              
        # Classification des cellules en cellules paires et impaires
        for i in range(self.n):
            for j in range(self.m):
                if (i + j) % 2 == 0:
                    self.cellules_paires.append((i, j))
                else:
                    self.cellules_impaires.append((i, j))
        
        nb_paires = len(self.cellules_paires)
        nb_impaires = len(self.cellules_impaires)

        # Initialisation de la matrice de coût avec des valeurs infinies
        self.matrice_de_cout = np.full((nb_paires, nb_impaires), np.inf)  

        # Remplissage de la matrice des coûts
        for i, paire in enumerate(self.cellules_paires):
            for j, impaire in enumerate(self.cellules_impaires):

                # On met le coût d'une paire pour les paires
                if (paire, impaire) in self.grille.all_pairs() or (impaire, paire) in self.grille.all_pairs():
                    self.matrice_de_cout[i, j] = self.grille.cost((paire, impaire))
                else:
                    # Sinon, on calcule le coût en fonction des valeurs des cellules
                    valeur_paire = self.grille.value[paire[0]][paire[1]]
                    valeur_impaire = self.grille.value[impaire[0]][impaire[1]]
                    
                    # Ajustement si l'une des cellules est noire
                    if self.grille.color[paire[0]][paire[1]] == 4:
                        valeur_paire = 0
                    if self.grille.color[impaire[0]][impaire[1]] == 4:
                        valeur_impaire = 0
                    
                    # Somme des valeurs des deux cellules
                    self.matrice_de_cout[i, j] = valeur_paire + valeur_impaire
        return self.cellules_paires,self.cellules_impaires
        
#----------------------------------------------------------------------------------------------------------------------------------------------------------

    def calcul_du_score(self):
        '''Calcule le score total en tenant compte des cellules non appariées'''
        score = 0 

        # Ajout du coût des paires trouvées
        for paire in self.paires_trouvees:
            cellule_paire, cellule_impaire = paire
            i = self.cellules_paires.index(cellule_paire)
            j = self.cellules_impaires.index(cellule_impaire)
            score += self.matrice_de_cout[i, j]
            
        cellules_utilisees = {cellule for paire in self.paires_trouvees for cellule in paire}
        
        # Ajout du coût des cellules non appariées
        for cellule in self.cellules_paires + self.cellules_impaires:
            i, j = cellule
            if cellule not in cellules_utilisees and self.grille.color[i][j] != 4:
                score += self.grille.value[i][j] 

        return score 

#----------------------------------------------------------------------------------------------------------------------------------------------------------

    def adjacence (Case0,Case1) :
        '''Renvoie True si deux cases sont adjacentes, False sinon'''
        i0 = Case0[0]
        j0 = Case0[1]
        i1 = Case1[0]
        j1 = Case1[1]

        adjacentes = False 
        if (i0 == i1+1 or i0 == i1-1) and j0 == j1 :
            adjacentes = True
        if (j0 == j1+1 or j0 == j1-1) and i0 == i1 :
            adjacentes = True
        
        return adjacentes

#----------------------------------------------------------------------------------------------------------------------------------------------------------

    def résolution_optimale_avec_algorithme_optimal(self):
        '''Résout le problème d'affectation avec l'algorithme hongrois. La fonction linear_sum_assignment renvoie deux listes de nombres.
        Pour tout k, on prend le k-ième élément de la première liste et de la deuxième liste, et on forme les cases correspondants à la 
        k-ième ligne et la k-ième colonne de la matrice de coûts. Une paire de cases non-adjacentes pour scipy doit être interprétée comme 
        deux cases que l'on n'assigne à aucune paire et qui donc contribuent au score de la somme de leurs valeurs, soit le coût de la paire 
        rentré dans la matrice.'''

        self.construire_matrice()

        # Coeurs de l'algorithme hongrois
        lignes, colonnes = linear_sum_assignment(self.matrice_de_cout)

        # Filtrage des paires valides
        self.paires_trouvees = []
        for i, j in zip(lignes, colonnes):            
            
            if self.matrice_de_cout[i, j] != np.inf :
                if SolverHongrois.adjacence(self.cellules_paires[i], self.cellules_impaires[j]) == True and self.grille.color_friendly((self.cellules_paires[i], self.cellules_impaires[j])) == True:
                    self.paires_trouvees.append((self.cellules_paires[i], self.cellules_impaires[j]))
        
        # Retourne les paires et le score optimal
        return int(self.calcul_du_score()), self.paires_trouvees
    



#---------------------------------------------------------------FIN----------------------------------------------------------------------------------------
#----------------------------------------------Quentin Brisemur et Ermance Lancrenon----------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------

'''

data_path = "../input/"
data_path2 = "../input-test/"
file_name = data_path + "grid01.in"
file_name2 = data_path2 + "grid_test_1_0.in"
grid = Grid.grid_from_file(file_name)
grid2 = Grid.grid_from_file(file_name2)

a = SolverHongrois(grid2)
print (a.résolution_optimale_avec_algorithme_optimal())
'''