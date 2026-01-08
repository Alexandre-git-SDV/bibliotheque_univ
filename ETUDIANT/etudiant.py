import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from LIVRE.crud_livre import Livre, create_livre, read_livre, update_livre
from ETUDIANT.crud_etudiant import Etudiant, create_etu, read_etu, delete_etu, update_etu
import LIVRE.crud_livre as crud_livre
import ETUDIANT.crud_etudiant as crud_etudiant

def menu_etudiant():
    while True:
        print("\n=== Menu Étudiant ===")
        choix = input("Choisissez une option: ")
        
        match choix:
            case '1':
                print("1. Voir tous les livres disponibles")
                livres = crud_livre.session.query(Livre).all()  # Comme SELECT *
                for livre in livres:
                    print(f"\n{livre.titre} {livre.editeur} (ISBN: {livre.isbn}, année : {livre.annee})")
            case '2':
                print("2. Voir les emprunt d'un étudiant")
                
            case '3':
                print("3. Voir les livres en retard d'un étudiant")
            case '4':
                print("4. Créer un emprunt pour un étudiant")
            case '5':
                print("5. Quitter")
            case '6':
                print("6. Quitter")
                break
            case _:
                print("Choix invalide, réessayez.")
                break