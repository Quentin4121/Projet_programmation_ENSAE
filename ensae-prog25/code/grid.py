"""
This is the grid module. It contains the Grid class and its associated methods.
"""

import numpy as np
import matplotlib.pyplot as plt



class Grid():
    """
    A class representing the grid. 

    Attributes: 
    -----------
    n: int
        Number of lines in the grid
    m: int
        Number of columns in the grid
    color: list[list[int]]
        The color of each grid cell: value[i][j] is the value in the cell (i, j), i.e., in the i-th line and j-th column. 
        Note: lines are numbered 0..n-1 and columns are numbered 0..m-1.
    value: list[list[int]]
        The value of each grid cell: value[i][j] is the value in the cell (i, j), i.e., in the i-th line and j-th column. 
        Note: lines are numbered 0..n-1 and columns are numbered 0..m-1.
    colors_list: list[char]
        The mapping between the value of self.color[i][j] and the corresponding color
    """

#----------------------------------------------------------------------------------------------------------------------------------------------------------    

    def __init__(self, n, m, color=[], value=[]):
        """
        Initializes the grid.

        Parameters: 
        -----------
        n: int
            Number of lines in the grid
        m: int
            Number of columns in the grid
        color: list[list[int]]
            The grid cells colors. Default is empty (then the grid is created with each cell having color 0, i.e., white).
        value: list[list[int]]
            The grid cells values. Default is empty (then the grid is created with each cell having value 1).
        
        The object created has an attribute colors_list: list[char], which is the mapping between the value of self.color[i][j] and the corresponding color
        """
        self.n = n
        self.m = m
        if not color:
            color = [[0 for j in range(m)] for i in range(n)]            
        self.color = color
        if not value:
            value = [[1 for j in range(m)] for i in range(n)]            
        self.value = value
        self.colors_list = ['w', 'r', 'b', 'g', 'k']
        

#----------------------------------------------------------------------------------------------------------------------------------------------------------

    '''def __str__(self): 
        """
        Prints the grid as text.
        """
        output = f"The grid is {self.n} x {self.m}. It has the following colors:\n"
        for i in range(self.n): 
            output += f"{[self.colors_list[self.color[i][j]] for j in range(self.m)]}\n"
        output += f"and the following values:\n"
        for i in range(self.n): 
            output += f"{self.value[i]}\n"
        return output'''

#----------------------------------------------------------------------------------------------------------------------------------------------------------

    def __repr__(self): 
        """
        Returns a representation of the grid with number of rows and columns.
        """
        return f"<grid.Grid: n={self.n}, m={self.m}>"

#----------------------------------------------------------------------------------------------------------------------------------------------------------

    def is_forbidden(self, i, j):
        """
        Returns True if the cell (i, j) is black and False otherwise
        """
        if self.color [int(i)][int(j)] == 4 :
            return True 
        else : 
            return False
        
#----------------------------------------------------------------------------------------------------------------------------------------------------------
        
    def color_friendly (self, pair) : 
        '''Cette méthode servira à savoir si les couleurs de deux cases adjacentes sont compatibles'''
        i1,j1,i2,j2 = pair[0][0], pair[0][1],pair[1][0], pair[1][1],
        if self.color [i1][j1] == 4 or self.color [i2][j2] == 4 :    # Cette ligne traite tous les cas de paire dont l'une des cases est noire
            return False
        
        if self.color [i1][j1] == 0 or self.color [i2][j2] == 0 :    # Cette ligne traite ensuite tous les cas de paire avec une case blanche
            return True
        
        if self.color [i1][j1] == 2 or self.color [i1][j1] == 1 : 
            if self.color [i2][j2] == 2 or self.color [i2][j2] == 1: # Cas d'une case bleue ou rouge (compatible avec seulement rouge ou bleu)
                return True
        
        if self.color [i1][j1] == 3 and self.color [i2][j2] == 3 :  # Ne reste que les cas de case verte
            return True
        # Contre-intuitif mais on a bien traité tous les cas !!!!!!!!
        return False

#----------------------------------------------------------------------------------------------------------------------------------------------------------

    def cost(self, pair):
        """
        Returns the cost of a pair
 
        Parameters: 
        -----------
        pair: tuple[tuple[int]]
            A pair in the format ((i1, j1), (i2, j2))

        Output: 
        -----------
        cost: int
            the cost of the pair defined as the absolute value of the difference between their values
        """
        i0,j0,i1,j1 = pair[0][0],pair[0][1],pair[1][0],pair[1][1]
        return abs (self.value [i0][j0]-self.value[i1][j1])
            
#----------------------------------------------------------------------------------------------------------------------------------------------------------

    def all_pairs(self):
        """
        Returns a list of all pairs of cells that can be taken together. 

        Outputs a list of tuples of tuples [(c1, c2), (c1', c2'), ...] where each cell c1 etc. is itself a tuple (i, j)
        """
        liste_paires_valables=[]
        # Les trois listes qui suivent servent à créer une liste de toutes les paires qui existent. Pour chaque case, on forme deux paires : une avec la case à sa droite et une avec la case en dessous d'elle.
        liste_paires_verticales = [((i,j),(i+1,j)) for i in range (self.n-1) for j in range (self.m) ]  # on prend les n-1 potentielles paires d'une colonne
        liste_paires_horizontales = [((i,j),(i,j+1)) for j in range (self.m-1) for i in range (self.n) ] # on prend les m-1 potentielles paires d'une ligne
        liste_paires_potentielles = liste_paires_horizontales + liste_paires_verticales
        
        for pair in liste_paires_potentielles : 
            if self.color_friendly (pair) == True : 
                liste_paires_valables.append (pair)


        return liste_paires_valables
    
#----------------------------------------------------------------------------------------------------------------------------------------------------------

    @classmethod
    def grid_from_file(cls, file_name, read_values=True): 
        """
        Creates a grid object from class Grid, initialized with the information from the file file_name.
        
        Parameters: 
        -----------
        file_name: str
            Name of the file to load. The file must be of the format: 
            - first line contains "n m" 
            - next n lines contain m integers that represent the colors of the corresponding cell
            - next n lines [optional] contain m integers that represent the values of the corresponding cell
        read_values: bool
            Indicates whether to read values after having read the colors. Requires that the file has 2n+1 lines

        Output: 
        -------
        grid: Grid
            The grid
        """
        with open(file_name, "r") as file:
            n, m = map(int, file.readline().split())
            color = [[] for i_line in range(n)]
            for i_line in range(n):
                line_color = list(map(int, file.readline().split()))
                if len(line_color) != m: 
                    raise Exception("Format incorrect")
                for j in range(m):
                    if line_color[j] not in range(5):
                        raise Exception("Invalid color")
                color[i_line] = line_color

            if read_values:
                value = [[] for i_line in range(n)]
                for i_line in range(n):
                    line_value = list(map(int, file.readline().split()))
                    if len(line_value) != m: 
                        raise Exception("Format incorrect")
                    value[i_line] = line_value
            else:
                value = []

            grid = Grid(n, m, color, value)
        return grid

#----------------------------------------------------------------------------------------------------------------------------------------------------------

    def plot(self): 
        """
        Plots a visual representation of the grid.
        """ 

        # On prépare la représentation en associant aux chiffres des couleurs de la grille leur équivalent RGB
        lignes, colonnes = self.n, self.m
        colors = self.color
        for i in range(lignes):
            for j in range(colonnes):
                colors[i][j]=[(255,255,255),(255,0,0),(0,0,255),(0,255,0),(0,0,0)][self.color[i][j]]

        # On crée la grille et les traits qui séparent les cellules
        figure, axe = plt.subplots()
        axe.set_xticks(np.arange(colonnes + 1) - 0.5, minor=True)
        axe.set_yticks(np.arange(lignes + 1) - 0.5, minor=True)
        axe.grid(which="minor", color="black", linestyle='-', linewidth=1)

        # On supprime les axes et les étiquettes
        axe.tick_params(which="both", bottom=False, left=False, labelbottom=False, labelleft=False)

        # On affiche les couleurs sous forme d'images
        axe.imshow(colors, extent=[-0.5, colonnes-0.5, -0.5, lignes-0.5])

        # Ne reste plus qu'à afficher les valeurs dans les cellules
        for i in range(lignes):
            for j in range(colonnes):
                axe.text(j, i, str(self.value[i][j]), ha='center', va='center', color='black', fontsize=12)

        # On affiche le tout
        plt.show()


#----------------------------------------------------------------------------------------------------------------------------------------------------------  
#----------------------------------------------------------------------------------------------------------------------------------------------------------  
#----------------------------------------------------------------------------------------------------------------------------------------------------------  
#----------------------------------------------------------------------------------------------------------------------------------------------------------  
#----------------------------------------------------------------------------------------------------------------------------------------------------------  

