# Importations
from Joueur import *
from Case import *
from Grille import *
import random
import time

class Partie:
    def __init__(self, joueur, difficulte):
        """
    	Constructeur de la classe Partie
        :param joueur: joueur de la partie en cours
    	:type joueur: objet de la classe Joueur
        :param grille: grille de la partie en cours
    	:type grille: objet de la classe Grille
        :param en_cours: indique si la partie est en cours
    	:type en_cours: boolean
        :param difficulte: difficulté choisie par le joueur
    	:type difficulte: int
        :param nb_tentatives: nombre de tentative du joueur
    	:type nb_tentatives: int
        :param x_choisi: coordonnees x de la case choisi par le joueur
    	:type x_choisi: int
        :param y_choisi: coordonnees y de la case choisi par le joueur
    	:type y_choisi: int
    	
        """ 
        self.joueur = joueur
        self.grille = Grille(difficulte)
        self.en_cours = True
        self.nb_tentatives = 0
        self.x_choisi = None
        self.y_choisi = None
    
    
    
    
    def score(self, debut):
        """
    	Fonction qui calcule le score du joueur en fonction de la durée et de la difficulté choisie par le joueur
        :param debut: temps marquant le début de la partie du joueur
    	:type debut: float
    	
        """ 
        fin = time.time()
        self.joueur.score = round((10000**self.grille.difficulte-round(fin - debut)))
    
    def afficher_grille(self):
        """
    	Fonction qui permet d afficher la grille dans la console
    	
        """ 
        for ligne in self.grille.cases:
            for case in ligne:
                if case.est_ouverte:
                    print(case.nb_mines_voisines, end=' ')
                if case.est_marquee and case.est_ouverte==False:
                    print('X', end=' ')
                if case.est_ouverte==False and case.est_marquee==False:
                    print('?', end=' ')
            print()
            
    def choisir_drapeau(self,x,y):
        """
    	Fonction qui permet de placer un drapeau sur une case de la grille
    	
        """ 
        
        case_a_marquer = self.grille.cases[x][y]
        case_a_marquer.poser_drapeau()
        
    
    def gagner_perdre(self,x,y,debut):
        """
    	Fonction qui détermine si le joueur à gagner ou perdu le jeu 
        :param case_a_ouvrir: case que le joueur à decidé d'ouvrir au dernier tour'
    	:type case_a_ouvrir: objet de la classe case
        :param debut: temps marquant le début de la partie du joueur
    	:type debut: float
        :return: indique si le jeu est terminé (False si perdu / True si gagné)
        turntype: boolean
    	
        """ 
        case_a_ouvrir = self.grille.cases[x][y]
        # Vérifier si le joueur a gagné ou perdu.
        if case_a_ouvrir.est_minee:
            
            return False
        
        nb_cases_non_minees_ouvertes = sum(case.est_ouverte and not case.est_minee for ligne in self.grille.cases for case in ligne)
       
        if nb_cases_non_minees_ouvertes == len(self.grille.cases) * len(self.grille.cases[0]) - self.grille.nb_mines:
            self.score(debut)
            return True
            
        else:
            return None
            
    
    
    def choisir_case(self, premier_tour,x,y):
        """
    	Fonction qui permet de choisir une case de la grille et de l ouvrir
        :param premier_tour: indique si il s agit du premier tour de la partie
    	:type premier_tour: boolean
    	
        """ 
        case_a_ouvrir = self.grille.cases[x][y]

        # Si c'est le premier tour et que la case est minée, échanger la mine avec une autre case.
        if premier_tour and case_a_ouvrir.est_minee:
            while True:
                x2, y2 = random.randint(0, self.grille.dimensions[0] - 1), random.randint(0, self.grille.dimensions[1] - 1)
                if not self.grille.cases[x2][y2].est_minee:
                    case_a_ouvrir.est_minee = False
                    self.grille.cases[x2][y2].est_minee = True
                    break

        # Compter le nombre de mines voisines et ouvrir la case.
        if not case_a_ouvrir.est_ouverte:
            case_a_ouvrir.compter_mines_voisines(self.grille)
            case_a_ouvrir.ouvrir_case()
        else:
            pass

        # Si c'est le premier tour, ouvrir une zone non minée autour de la case.
        if premier_tour:
            zone_size = random.randint(1, self.grille.dimensions[0] * self.grille.dimensions[1] // 2)
            for _ in range(zone_size):
                self.grille.ouvrir_zone(x, y)

            self.grille.placer_mines(self.grille.nb_mines)
            for x in range(self.grille.dimensions[0]):
                for y in range(self.grille.dimensions[1]):
                    case = self.grille.cases[x][y]
                    if case.est_ouverte:
                        case.compter_mines_voisines(self.grille)
            premier_tour = False

        # Ouvrir case
        
        case_a_ouvrir.ouvrir_case()

        return premier_tour
    
    def jouer_partie_console(self):
        """
    	Fonction qui permet de jouer une partie dans la console
    	
        """ 
        premier_tour = True
        debut = time.time()
        while self.en_cours:
            

            self.afficher_grille()
            
            # Demander si le joueur veux poser un drapeau
            while self.nb_tentatives > 0:
                choix = input("Voulez-vous poser un drapeau ? (O/N) ")
                
                if choix == 'O':
                    x, y = map(int, input("Entrez les coordonnées de la case à marquer (ligne colonne): ").split())
                    
                    self.choisir_drapeau(x,y)
                    
                    case_a_marquer = self.grille.cases[x][y]
                    
                    self.afficher_grille()
                    if case_a_marquer.est_ouverte:
                        print ("Cette case est déjà ouverte, inutile de la marquer!")
                elif choix == 'N':
                    print(f"On continue {self.joueur.nom}!")
                    break
                else:
                    print("Répondez avec 'O' pour Oui ou 'N' pour Non.")
            
            # Demander au joueur d'entrer les coordonnées de la case à ouvrir.
            x, y = map(int, input("Entrez les coordonnées de la case à ouvrir (ligne colonne): ").split())
            self.x_choisi = x
            self.y_choisi = y
            if self.grille.cases[x][y].est_ouverte:
                print("la case est deja ouverte")
            premier_tour = self.choisir_case(premier_tour,self.x_choisi,self.y_choisi)
            
            # Verifier si la partie est terminée
            finir = self.gagner_perdre(self.x_choisi,self.y_choisi, debut)
            if finir == True:
                
                print(f"Vous avez gagné {self.joueur.nom}!\nVotre score est de {self.joueur.score} :)")
                break
            
            if finir == False:
                self.grille.ouvrir_toutes_les_cases()
                print(f"BOOOOM!!!!!!!\nVous avez perdu {self.joueur.nom}! :(")
                break
            else:
                pass

            self.nb_tentatives += 1
