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