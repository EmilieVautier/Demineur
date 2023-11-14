# Importations
from Joueur import *
from Partie import *
from Grille import *
from Case import *
from PyQt5.QtWidgets import QApplication, QInputDialog
import sys
from DemineurInterface import *


class Controle:
    def __init__(self):
        pass
    def lancer_partie_console(self):
        """
     	Fonction qui permet de démarrer et jouer une partie dans la console
    	
        """ 
        nom_joueur = input("Entrez votre nom: ")
        joueur = Joueur(nom_joueur)
        print(f"Bienvenue {nom_joueur}!\nVeuillez choisir une difficulté :\n1 - Facile\n2 - Moyen\n3 - Difficile")
        difficulte = int(input("Choisissez la difficulté (1-3): "))
        
        partie = Partie(joueur, difficulte)
        
        partie.jouer_partie_console()
        
        
    def lancer_partie_interface(self):
        """
     	Fonction qui permet de démarrer et jouer une partie dans l'interface'
    	
        """ 
        app = QApplication(sys.argv)
        
        difficulte, _ = QInputDialog.getInt(None, "Choisir la difficulté", "Difficulté (1-3):", 1, 1, 3, 1)
        if 1 <= difficulte <= 3:
            
            jeu = DemineurInterface(difficulte)
            jeu.afficher_popup("Bienvenue dans le jeu démineure!\nClic droit pour poser un drapeau\nClic gauche pour ouvrir une case")
            jeu.show()
            sys.exit(app.exec_())
            