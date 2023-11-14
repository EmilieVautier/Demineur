# Importations
from Controle import *


if __name__ == "__main__":
    controle = Controle()
    
    mode = input("Choisissez le mode de jeu (I pour interface / C pour console): ")
    if mode=="I":
        controle.lancer_partie_interface()
    if mode=="C":
        controle.lancer_partie_console()
        
    else:
        print("Veuillez choisir 'I' pour interface ou 'C' pour console.")

