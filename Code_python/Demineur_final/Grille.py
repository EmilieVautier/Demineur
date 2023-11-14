# Importations
from Case import *
import random

class Grille:
    def __init__(self, difficulte):
        """
    	Constructeur de la classe Grille
    	:param difficulte: la difficulté du jeu (de 1 à 3) qui va définir la taille de la grille, le nombre de mine présente et le nombre de drapeau utilisable
    	:type difficulte: int
    	
        """
        self.difficulte = difficulte
     
        if difficulte == 1:
            self.dimensions = (5, 5)
            self.nb_mines = 5
            self.nb_drapeaux = 5
        elif difficulte == 2:
            self.dimensions = (10, 10)
            self.nb_mines = 20
            self.nb_drapeaux = 20
        elif difficulte == 3:
            self.dimensions = (15, 15)
            self.nb_mines = 40
            self.nb_drapeaux = 40

        # Initialiser la grille avec des cases vides.
        self.cases = [[Case(x, y) for y in range(self.dimensions[1])] for x in range(self.dimensions[0])]

    # Placer les mines de manière aléatoire.
    def placer_mines(self,nb_mines):
        """
    	Fonction qui va permettre de placer les mines dans la grille aléatoirement
    	:param nb_mines: nombre de mine à placer dans la grille
    	:type nb_mines: int
    	
        """
        for _ in range(self.nb_mines):
            K = 0
            while K==0:
                x, y = random.randint(0, self.dimensions[0] - 1), random.randint(0, self.dimensions[1] - 1)
                case = self.cases[x][y]
                if case.est_minee==False and case.est_ouverte==False:
                    case.est_minee = True
                    K += 1
                    break
                
                
    def ouvrir_toutes_les_cases(self):
        """
     	Fonction qui va permettre d ouvrir toutes les cases losqu'on perd en cliquant sur une mine'
    	
        """
        for ligne in self.cases:
            for case in ligne:
                if case.est_minee:
                    print('O', end=' ')
                else:
                    print('+', end=' ')
            print()
            
    def ouvrir_zone(self, x, y):
        """
     	Fonction qui va permettre d ouvrir une zone aléatoire autour de la première case ouverte lors de la partie au premier tour
     	:param x: coordonnées en x de la première case ouverte par le joueur
     	:type x: int
        :param y: coordonnées en y de la première case ouverte par le joueur
     	:type y: int
    	
        """
        directions = [(dx, dy) for dx in [-1, 0, 1] for dy in [-1, 0, 1]]
        for dx, dy in directions:
            
            alea = random.randint(0,self.dimensions[0]//2)
            if alea == 0 :
                break
            for k in range (alea):
                nx, ny = x + dx, y + dy
                
                if 0 <= nx < self.dimensions[0] and 0 <= ny < self.dimensions[1]:
                    case = self.cases[nx][ny]
                    if not case.est_minee and not case.est_ouverte:
                         
                        case.ouvrir_case()
                        break
                    random.shuffle(directions)
                    dx , dy = dx+directions[0][0] , dy+directions[0][1]
