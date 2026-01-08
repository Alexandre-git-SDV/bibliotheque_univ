import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from LIVRE.crud_livre import Livre, create_livre, read_livre, update_livre
from ETUDIANT.crud_etudiant import Etudiant, create_etu, read_etu, delete_etu, update_etu
import LIVRE.crud_livre as crud_livre
import ETUDIANT.crud_etudiant as crud_etudiant
import EMPRUNT.crud_emprunt as crud_emprunt
import EMPRUNT.crud_emprunt as crud_emprunt

def menu_etudiant():
    while True:
        print("\n=== Menu Étudiant ===")
        print("\n1. Voir tous les livres disponibles")
        print("2. Voir les emprunts d'un étudiant")
        print("3. Créer un emprunt pour un étudiant")
        print("4. Quitter")
        choix = input("\nChoisissez une option (1-4): ")
        
        match choix:
            case '1':
                print("1. Voir tous les livres disponibles")
                livres = crud_livre.session.query(Livre).all()  # Comme SELECT *
                for livre in livres:
                    print(f"\n{livre.titre} {livre.editeur} (année : {livre.annee})")
            case '2':
                print("2. Voir les emprunt d'un étudiant")
                id_etud = input("ID de l'étudiant: ")
                emprunts = crud_emprunt.session.query(crud_emprunt.Emprunt).filter_by(id_etud=id_etud).all()
                if emprunts:
                    for emp in emprunts:
                        print(f" Emprunt ID: {emp.id_emprunt}, ISBN: {emp.isbn}, date emprunt: {emp.date_emprunt}, date retour: {emp.date_retour}, amende: {emp.amende}")
                else:
                    print("Aucun emprunt trouvé pour cet étudiant.")
            case '3':
                print("3. Créer un emprunt pour un étudiant")
                crud_emprunt.create_emprunt(crud_emprunt.session)
            case '4':
                print("4. Quitter")
                break
            case _:
                print("Choix invalide, réessayez.")
                break