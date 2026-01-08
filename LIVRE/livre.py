import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from LIVRE.crud_livre import Livre, create_livre, read_livre, update_livre
from ETUDIANT.crud_etudiant import Etudiant, create_etu, read_etu, delete_etu, update_etu
import LIVRE.crud_livre as crud_livre
import ETUDIANT.crud_etudiant as crud_etudiant

def menu_bibliothecaire():
    while True:
        print("\n=== Menu Bibliothécaire ===")
        choix = input("Choisissez une option (1-13): ")
        print("\n1. Voir tous les étudiants")
        print("\n2. Voir tous les livres")
        print("\n3. Voir tous les emprunts")
        print("\n4. Ajouter un étudiant")
        print("\n5. Ajouter un livre")
        print("\n6. Ajouter un emprunt")
        print("\n7. Mettre à jour le titre du livre")
        print("\n8. Mettre à jour le solde d'amende d'un étudiant")
        print("\n9. Supprimer un étudiant")
        print("\n10. Chercher un étudiant par ID")
        print("\n11. Supprimer un livre")
        print("\n12. Supprimer un emprunt")
        print("\n13. Quitter")
        
        match choix:
            case '1':  # Voir tous les étudiants
                print("1. Voir tous les étudiants")
                etudiants = crud_etudiant.session.query(Etudiant).all()
                print("ORM -- SUCCESS! Étudiants :")
                for etu in etudiants:
                    print(f"\n {etu.prenom} {etu.nom} (ID: {etu.id}, email : {etu.email})")
            case '2':  # Voir tous les livres
                print("2. Voir tous les livres")
                livres = crud_livre.session.query(Livre).all()  # Comme SELECT *
                for livre in livres:
                    print(f"\n{livre.titre} {livre.editeur} (ISBN: {livre.isbn}, année : {livre.annee})")
            case '3':  # Voir tous les emprunts
                print("3. Voir tous les emprunts")
            case '4':  # Ajouter un étudiant
                print("4. Ajouter un étudiant")
                nom = input("Nom: ").upper()
                prenom = input("Prénom: ")
                email = input("Email: ")
                from datetime import date
                date_inscription = date.today()
                solde_amende = 0.0
                id_new = create_etu(crud_etudiant.session, nom, prenom, email, date_inscription, solde_amende)
                print(f"Créé ID={id_new}")
            case '5':  # Ajouter un livre
                print("5. Ajouter un livre")
                isbn = input("ISBN: ")
                titre = input("Titre: ")
                editeur = input("Éditeur: ")
                annee = input("Année: ")
                exemplaires_dispo = int(input("Exemplaires disponibles: "))
                id_new = create_livre(crud_livre.session, isbn, titre, editeur, annee, exemplaires_dispo)
                print(f"Créé ISBN={id_new}")
            case '6':  # Ajouter un emprunt
                print("6. Ajouter un emprunt")
            case '7':  # Mettre à jour le titre du livre
                print("7. Mettre à Jour le Titre du livre")
                isbn = input("ISBN du livre à modifier: ")
                l = crud_livre.session.query(Livre).get(isbn)
                new_titre = input("Nouveau titre: ")
                new_exemplaires_dispo = int(input("Nouveaux exemplaires disponibles: "))
                if update_livre(crud_livre.session, isbn, new_titre, new_exemplaires_dispo):
                    print(f"Livre ISBN={isbn} mis à jour : titre={new_titre}, exemplaires_dispo={new_exemplaires_dispo}")
                else:
                    print("ID inexistant")
            case '8':  # Mettre à jour le solde d'amende d'un étudiant
                print("8. Mettre à Jour le solde d'amende d'un étudiant")
                id_etud = int(input("ID de l'étudiant: "))
                nouveau_prenom = input("Nouveau prénom: ")
                nouveau_solde = float(input("Nouveau solde d'amende: "))
                if update_etu(crud_etudiant.session, id_etud, nouveau_prenom, nouveau_solde):
                    print(f"Étudiant mis à jour")
                else:
                    print("ID inexistant")
            case '9':  # Supprimer un étudiant
                print("9. Supprimer un étudiant")
            case '10':  # Chercher un étudiant par ID
                print("10. Chercher un étudiant par ID")
                id = int(input("ID à chercher: "))
                e = crud_etudiant.session.query(Etudiant).get(id)
                if e:
                    print(f" {e.prenom} {e.nom} (ID={e.id})")
                else:
                    print(" Non trouvé")
            case '11':  # Supprimer un livre
                print("11. Supprimer un livre")
                nom = input("Nom à supprimer: ").upper()
                if delete_etu(crud_etudiant.session, nom):
                    print("Supprimé")
                else:
                    print(" Non trouvé")
            case '12':  # Supprimer un emprunt
                print("12. Supprimer un emprunt")
            case '13':  # Quitter
                print("13. Quitter")
                break
            case _:
                print("Choix invalide, réessayez.")
                break
