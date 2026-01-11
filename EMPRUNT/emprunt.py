from EMPRUNT.crud_emprunt import (
    create_emprunt,
    display_emprunts,
    emprunt_by_id,
    update_amende,
    emprunts_par_date_emprunt,
    emprunt_par_date_retour,
    livres_non_retournes,
    delete_emprunt,
)
import EMPRUNT.crud_emprunt as emprunt_mod

def menu_crud():
    try:
        print("\n=== MENU CRUD EMPRUNT ===")
        print("1: Créer un emprunt")
        print("2: Afficher tous les emprunts")
        print("3: Avoir un emprunt par ID")
        print("4: Mettre à jour l'amende d'un emprunt")
        print("5: Rechercher les emprunts par date d'emprunt")
        print("6: Rechercher les emprunts par date de retour")
        print("7: Afficher les livres non retournés")
        print("8: Supprimer un emprunt")
        print("0: Quitter")
        return input("Choix (0-8): ")
 
    except Exception as e:
        print(f"Erreur dans le menu: {e}")
        return None
 
# BOUCLE PRINCIPALE
try:
    while True:
        choix = menu_crud()

        if choix is None:
            continue

        match choix:
            case "1":
                create_emprunt(emprunt_mod.session)

            case "2":
                display_emprunts()

            case "3":
                emprunt_by_id(emprunt_mod.session)

            case "4":
                update_amende(emprunt_mod.session)

            case "5":
                emprunts_par_date_emprunt(emprunt_mod.session)

            case "6":
                emprunt_par_date_retour(emprunt_mod.session)

            case "7":
                livres_non_retournes(emprunt_mod.session)

            case "8":
                delete_emprunt(emprunt_mod.session)

            case "0":  # Fermeture du Code
                print("Au revoir !")
                break

            case _:
                print("---------------------------------------------------")
                print("Choix invalide. Veuillez réessayer.")
                print("---------------------------------------------------")
 
except Exception as e:
    print(f"Erreur dans la boucle principale: {e}")
finally:
    try:
        # Fermeuture de la session
        if emprunt_mod.session is not None:
            emprunt_mod.session.close()
    except Exception:
        pass