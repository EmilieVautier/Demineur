import random
import time

class Joueur:
    def __init__(self, nom):
        """
    	Constructeur de la classe Joueur
    	:param nom: nom du joueur
    	:type nom: string
    	
        """
        self.nom = nom
        self.score = 0
        

class Case:
    def __init__(self, x, y):
        """
    	Constructeur de la classe Case
    	:param x: coordonnées en x de la case dans la grille
    	:type x: int
    	:param y: coordonnées en y de la case dans la grille
    	:type y: int
    	
        """
        self.x = x
        self.y = y
        self.est_ouverte = False
        self.est_minee = False
        self.est_marquee = False
        self.nb_mines_voisines = 0

    def ouvrir_case(self):
        """
    	Fonction qui permet d ouvrir une case
    	
        """
        if not self.est_ouverte:
            self.est_ouverte = True

    def poser_drapeau(self):
        """
    	Fonction qui permet de poser un drapeau
    	
        """
        if not self.est_ouverte:
            self.est_marquee = True
            
    def compter_mines_voisines(self, grille):
        """
    	Compter les mines voisines à la case choisie
    	:param grille: la grille qui contient la case
    	:type grille: objet de la classe Grille
    	
        """
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                nx, ny = self.x + dx, self.y + dy
                if 0 <= nx < len(grille.cases) and 0 <= ny < len(grille.cases[0]):
                    if grille.cases[nx][ny].est_minee:
                        self.nb_mines_voisines += 1


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
    

class Partie:
    def __init__(self, joueur, difficulte):
        """
    	Constructeur de la classe Partie
        :param joueur: joueur de la partie en cours
    	:type joueur: objet de la classe Joueur
        :param difficulte: difficulté choisie par le joueur
    	:type difficulte: int
    	
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
        self.joueur.score = round((10000**self.grille.difficulte/round(fin - debut)))
    
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
            
    def choisir_drapeau(self):
        """
    	Fonction qui permet de placer un drapeau sur une case de la grille
    	
        """ 
        # Demander si le joueur veux poser un drapeau
        nom = self.joueur.nom
        while self.nb_tentatives > 0:
            choix = input("Voulez-vous poser un drapeau ? (O/N) ")
            
            if choix == 'O':
                x, y = map(int, input("Entrez les coordonnées de la case à marquer (x y): ").split())
                case_a_marquer = self.grille.cases[x][y]
                case_a_marquer.poser_drapeau()
                self.afficher_grille()
                if case_a_marquer.est_ouverte:
                    print ("Cette case est déjà ouverte, inutile de la marquer!")
            elif choix == 'N':
                print(f"On continue {nom}!")
                break
            else:
                print("Répondez avec 'O' pour Oui ou 'N' pour Non.")
    
    def gagner_perdre(self,case_a_ouvrir,debut):
        """
    	Fonction qui détermine si le joueur à gagner ou perdu le jeu
        :param case_a_ouvrir: case que le joueur à decidé d'ouvrir au dernier tour'
    	:type case_a_ouvrir: objet de la classe case
        :param debut: temps marquant le début de la partie du joueur
    	:type debut: float
        :return: indique si le jeu est terminé
        turntype: boolean
    	
        """ 
        nom = self.joueur.nom
        # Vérifier si le joueur a gagné ou perdu.
        if case_a_ouvrir.est_minee:
            self.grille.ouvrir_toutes_les_cases()
            print(f"BOOOOM!!!!!!!\nVous avez perdu {nom}! :(")
            return True
        else:
            nb_cases_non_minees_ouvertes = sum(case.est_ouverte and not case.est_minee for ligne in self.grille.cases for case in ligne)
            if nb_cases_non_minees_ouvertes == len(self.grille.cases) * len(self.grille.cases[0]) - self.grille.nb_mines:
                self.score(debut)
                
                print(f"Vous avez gagné {nom}!\nVotre score est de {self.joueur.score} :)")
                return True
    
    
    def choisir_case(self, premier_tour):
        """
    	Fonction qui permet de choisir une case de la grille et de l ouvrir
        :param premier_tour: indique si il s agit du premier tour de la partie
    	:type premier_tour: boolean
    	
        """ 
        # Demander au joueur d'entrer les coordonnées de la case à ouvrir.
        x, y = map(int, input("Entrez les coordonnées de la case à ouvrir (x y): ").split())
        self.x_choisi = x
        self.y_choisi = y
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
            print("Cette case est déjà ouverte!")

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
    
    def jouer_partie(self):
        """
    	Fonction qui permet de jouer une partie
    	
        """ 
        premier_tour = True
        while self.en_cours:
            debut = time.time()

            self.afficher_grille()
            self.choisir_drapeau()

            premier_tour = self.choisir_case(premier_tour)

            finir = self.gagner_perdre(self.grille.cases[self.x_choisi][self.y_choisi], debut)
            if finir == True:
                break

            self.nb_tentatives += 1
     
        

class Controle:
    def __init__(self):
        """
    	Constructeur de la classe Controle permettant de controler le lancement du jeu
        
        """ 
        pass

    def lancer_partie(self):
        """
    	Fonction qui permet de démarrer et jouer une partie
    	
        """ 
        nom_joueur = input("Entrez votre nom: ")
        joueur = Joueur(nom_joueur)
        print(f"Bienvenue {nom_joueur}!\nVeuillez choisir une difficulté :\n1 - Facile\n2 - Moyen\n3 - Difficile")
        difficulte = int(input("Choisissez la difficulté (1-3): "))
        
        partie = Partie(joueur, difficulte)
        
        partie.jouer_partie()


if __name__ == "__main__":
    controle = Controle()
    controle.lancer_partie()

