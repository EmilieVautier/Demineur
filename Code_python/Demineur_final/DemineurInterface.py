# Importations
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QWidget, QGridLayout, QLabel, QPushButton
from Joueur import *
from Partie import *
from Grille import *
from Case import *
import time

class DemineurInterface(QMainWindow):
    def __init__(self, difficulte):
        """
    	Constuteur de la classe DemineurGUI quiva gérer l interface graphique
        :param difficulte: difficulté choisie par le joueur
    	:type difficulte: int
        :param Joueur: joueur de la partie en cours
    	:type Joueur: objet de la classe Joueur
        :param Partie: Partie en cours
    	:type Partie: objet de la classe Partie
        :param premier_tour: indique si il s agit du premier tour de la partie
    	:type premier_tour: boolean
        :param debut: temps marquant le début de la partie du joueur
    	:type debut: float
    	
        """ 
        super().__init__()
        self.difficulte = difficulte
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QGridLayout(self.central_widget)
        self.label = QLabel("Cliquez sur une case pour commencer la partie.")
        self.Joueur = Joueur("Joueur")
        self.Partie = Partie(self.Joueur,self.difficulte)
        self.nb_tentatives = 0
        self.premier_tour = True
        self.debut = time.time()
        
        
        # Donne le nombre de case de la grille en fonction de la difficulté
        if self.difficulte == 1:
            taille_grille = 5
        elif self.difficulte == 2:
            taille_grille = 10
        elif self.difficulte == 3:
            taille_grille = 15
        self.buttons = [[QPushButton("?") for _ in range (taille_grille)] for _ in range (taille_grille)]
        
        # Creation de la grille de boutons dans l interface graphique
        for x in range(taille_grille):
            for y in range(taille_grille):
                button = self.buttons[x][y]
                button.setFixedSize(55, 55)

                
                button.clicked.connect(lambda _, x=x, y=y: self.case_clic(x, y, Qt.LeftButton))
                button.setContextMenuPolicy(Qt.CustomContextMenu)
                button.customContextMenuRequested.connect(lambda _, x=x, y=y: self.case_clic(x, y, Qt.RightButton))
                
                self.layout.addWidget(button, x, y)
                
                      
        self.setWindowTitle("Démineur")
        
       
    def afficher_popup(self, message):
        """
    	Fonction qui permet d'afficher un popup
        :param message: Message a afficher dans le popup
    	:type message: str
    	
        """ 
        popup = QMessageBox()
        popup.setWindowTitle("Message")
        popup.setText(message)
        popup.exec_()  
        self.close()  
    
    
    
    def case_clic(self, x, y, button_type):
        """
    	Fonction qui permet de lancer une action au clic sur une case (clic gauche: ouvrir case / clic droit: marquer une case)
        :param x: Position en x de la case cliquee
    	:type x: int
        :param y: Position en y de la case cliquee
    	:type y: int
        :param button_type: Indique s il s agit d un clic droit ou un clic gauche
    	:type button_type: Qt.RightButton ou Qt.LeftButton
    	
        """ 
        
        taille_grille=self.Partie.grille.dimensions[0]
        # bouton cliqué
        selected_button = self.buttons[x][y]
        
        
        
        if button_type == Qt.RightButton:
            # Poser drapeau si clic droit et s il y a deja un drapeau remettre ?
            if selected_button.text() == 'X':
                selected_button.setText('?')
            else:   
                selected_button.setText('X')
            
        if button_type == Qt.LeftButton:
            # Ouvrir la case si clic gauche
            self.Partie.choisir_case(self.premier_tour,x,y)
            
            # Ouvrir une zone autour de la premiere case choisie au premier tour
            if self.nb_tentatives==0:
                
                self.premier_tour=False
                for i in range(taille_grille):
                    for j in range(taille_grille):
                        if self.Partie.grille.cases[i][j].est_ouverte:
                            self.buttons[i][j].setText(f'{self.Partie.grille.cases[i][j].nb_mines_voisines}')
                        
                
            # Ouverture de cases apres le premier tour 
            if self.nb_tentatives>0:
                if not self.Partie.grille.cases[x][y].est_minee:
                    selected_button.setText(f'{self.Partie.grille.cases[x][y].nb_mines_voisines}')
                # Si la case est minee 
                if self.Partie.grille.cases[x][y].est_minee:
                    # Ouvrir toutes les cases si la case ouverte est minee
                    for i in range(taille_grille):
                        for j in range(taille_grille):
                            if not self.Partie.grille.cases[i][j].est_minee:
                                
                                self.buttons[i][j].setText(f'{self.Partie.grille.cases[i][j].nb_mines_voisines}')
                            if self.Partie.grille.cases[i][j].est_minee:
                                
                                self.buttons[i][j].setText('BOOM')
                            
                    
                    
                
            
            self.nb_tentatives+=1
            
            # Gestion de la fin de la partie
            finir = self.Partie.gagner_perdre(x,y, self.debut)
            # Si gané:
            if finir == True:
                self.afficher_popup(f"Vous avez gagné!\nVotre score est de {self.Joueur.score} :)")
            # Si perdu  
            if finir == False:
                self.afficher_popup("Vous avez perdu!")
                

   