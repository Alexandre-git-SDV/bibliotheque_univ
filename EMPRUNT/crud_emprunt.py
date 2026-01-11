from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey, create_engine
import os
from dotenv import load_dotenv
from datetime import date, datetime

# Charge le fichier .env
load_dotenv()

# Base ORM
Base = declarative_base()

# Import des modèles liés
from ETUDIANT.crud_etudiant import Etudiant
from LIVRE.crud_livre import Livre

# Modèle Emprunt
class Etudiant(Base):
    __tablename__ = 'etudiants'  # Nom table Postgres
    
    id = Column(Integer, primary_key=True)  # Clé primaire
    nom = Column(String)
    prenom = Column(String)
    email = Column(String)
    date_inscription = Column(Date)
    solde_amende = Column(Float)

    emprunt= relationship("Emprunt", back_populates="etudiant", cascade="delete")

# Modèle Livre
class Livre(Base):
    __tablename__ = 'livre'  # Nom table Postgres
    
    isbn = Column(Integer, primary_key=True)  # Clé primaire
    titre = Column(String)
    editeur = Column(String)
    annee = Column(Date)
    exemplaires_dispo = Column(Integer)

    emprunt= relationship("Emprunt", back_populates="livre", cascade="delete")

# Modèle Emprunt
class Emprunt(Base):
    __tablename__ = 'emprunt'  # Doit correspondre au nom réel de la table
    
    id_emprunt = Column(Integer, primary_key=True)  # Clé primaire
    date_emprunt = Column(Date, default=date.today) # format 2026-01-01
    date_retour = Column(Date)
    amende = Column(Float, default=0.0)

    id_etud = Column(Integer, ForeignKey('etudiants.id'))
    isbn = Column(Integer, ForeignKey('livre.isbn'))

    etudiant= relationship("Etudiant", back_populates="emprunt")
    livre= relationship("Livre", back_populates="emprunt")

# Fonction pour obtenir l'engine (appelée après saisie user/password)
def get_engine(user, password):
    host = os.getenv('DB_HOST')
    port = os.getenv('DB_PORT')
    dbname = os.getenv('DB_NAME')
    return create_engine(f"postgresql://{user}:{password}@{host}:{port}/{dbname}")

# Variables de session (initialisées par main.py)
Session = None
session = None

def create_emprunt(session):
    try:
        id_etud = input("Entrez l'ID de l'étudiant : ")
        # vérifie si le user existe
        check_user = session.query(Etudiant).get(id_etud)
        if not check_user:
                # crée une boucle tant que l'ID n'est pas correct ou si l'utilisateur veut quitter
                print("User non trouvé.")
                check = False
                while not check:
                    id_emprunt = int(input("Veuillez entrer l'ID d'un user existant ou '-1' pour quitter : "))
                    if id_emprunt == -1:
                        return False
                    check_user = session.query(Etudiant).get(id_emprunt)
                    if check_user:
                        check = True
                    else:
                        print("User non trouvé.")
 
        # Check le livre existant
        isbn = input("Entrez l'ISBN du livre : ")
        check_livre = session.query(Livre).get(isbn)
        if not check_livre:
                # crée une boucle tant que l'ISBN n'est pas correct ou si l'utilisateur veut quitter
                print("Livre non trouvé.")
                check = False
                while not check:
                    isbn = input("Veuillez entrer l'ISBN d'un livre existant ou 'q' pour quitter : ")
                    if isbn.lower() == 'q':
                        return
                    check_livre = session.query(Livre).get(isbn)
                    if check_livre:
                        check = True
                    else:
                        print("Livre non trouvé.")
 
 
        # Check la date d'emprunt
        date_emprunt = input("Entrez la date d'emprunt (YYYY-MM-DD) : ")
        if not check_date_format(date_emprunt):
            # crée une boucle tant que la date n'est pas correcte ou si l'utilisateur veut quitter
            check = False
            while not check:
                date_emprunt = input("Format de date invalide. Veuillez entrer une date au format YYYY-MM-DD ou 'q' pour quitter : ")
                if date_emprunt.lower() == 'q':
                    return
                if check_date_format(date_emprunt):
                    check = True
 
        # Check la date de retour
        date_retour = input("Entrez la date de retour (YYYY-MM-DD) ou laissez vide : ")
        # si aucun date de retour alors None par défaut
        if date_retour == '' :
            date_retour = None
       
        elif date_retour!='' and not check_date_format(date_retour):
            check = False
            while not check:
                # crée une boucle tant que la date n'est pas correcte ou si l'utilisateur veut quitter
                date_retour = input("Format de date invalide. Veuillez entrer une date au format YYYY-MM-DD ou 'q' pour quitter : ")
                if date_retour.lower() == 'q':
                    return
                if check_date_format(date_retour):
                    check = True
 
        # Check l'amende
        amende = input("Entrez l'amende (0.0 si aucune) : ")
        # si aucune amende alors 0.0 par défaut
        if amende == None or amende =='':
            amende = 0.0
 
        elif not check_float_input(float(amende), 1000.0):
                    # crée une boucle tant que l'amende n'est pas correcte ou si l'utilisateur veut quitter
                    check = False
                    while not check:
                        amende = float(input("Valeur invalide. Veuillez entrer une amende entre 0.0 et 1000.0 ou '-1' pour quitter : "))
                        if amende== -1:
                            return False
                        if check_float_input(amende, 1000.0):
 
                            check = True
 
        emprunt = Emprunt(id_etud=id_etud,
                         isbn=isbn,
                         date_emprunt=date_emprunt,
                         date_retour=date_retour,
                         amende=float(amende))
       
        # ajout de l'emprunt si tout est ok
        session.add(emprunt)
        session.commit()
 
        # affichage de l'emprunt créé
        print(f' Emprunt créé avec ID: {emprunt.id_emprunt} ')
        new = session.query(Emprunt).get(emprunt.id_emprunt)
        if new:
            print(f' Emprunt ID: {new.id_emprunt}, Étudiant ID: {new.id_etud}, Livre ISBN: {new.isbn}, date emprunt: {new.date_emprunt}, date retour: {new.date_retour}, amende: {new.amende} ')
        else:
            print("Erreur lors de la création de l'emprunt.")
    except Exception as e:
        # Annulation en cas d'erreur et affichage du message d'erreur
        session.rollback()
        print(f"Erreur lors de la création de l'emprunt: {e}")
 
 
#  fonction pour vérifier le format de la date
def check_date_format(date_text):
    try:
        datetime.strptime(date_text, '%Y-%m-%d')
        return True
    except ValueError:
        return False
 
def emprunts_par_date_emprunt(session):
    try:
        date_emprunt = input("Entrez la date d'emprunt (YYYY-MM-DD) : ")
        # vérifie le format de la date
        if not check_date_format(date_emprunt):
            check = False
            while not check:
                date_emprunt = input("Format de date invalide. Veuillez entrer une date au format YYYY-MM-DD ou 'q' pour quitter : ")
                if date_emprunt.lower() == 'q':
                    return
                if check_date_format(date_emprunt):
                    check = True
 
        # Recherche des emprunts par rapport à la date saisie
        liste = session.query(Emprunt).filter_by(date_emprunt=date_emprunt).all()
        # affichage des résultats
        if liste:
            print(f"La liste des emprunts pour la date {date_emprunt}:")
            for el in liste:
                print(f" Emprunt ID: {el.id_emprunt}, Date emprunt: {el.date_emprunt}, Étudiant ID: {el.id_etud},Etudiant nom : {el.etudiant.nom} , Livre ISBN: {el.isbn}, Livre titre: {el.livre.titre}, ammende: {el.amende} ")
        else:
            # message si aucun emprunt trouvé
            print(f"Aucun emprunt trouvé pour la date {date_emprunt}.")
    except Exception as e:
        print(f"Erreur lors de la recherche des emprunts par date: {e}")
 
# emprunts_par_date_emprunt(session)
 
def emprunt_par_date_retour(session):
    try:
        # vérifie le format de la date
        date_retour = input("Entrez la date de retour (YYYY-MM-DD) : ")
        if not check_date_format(date_retour):
            check = False
            while not check:
                date_retour = input("Format de date invalide. Veuillez entrer une date au format YYYY-MM-DD ou 'q' pour quitter : ")
                if date_retour.lower() == 'q':
                    return
                if check_date_format(date_retour):
                    check = True
 
        # Recherche des emprunts par rapport à la date saisie
        liste = session.query(Emprunt).filter_by(date_retour=date_retour).all()
        if liste:
            # affichage des résultats
            print(f"La liste des emprunts pour la date de retour {date_retour}:")
            for el in liste:
               
                print(f" Emprunt ID: {el.id_emprunt}, Étudiant ID: {el.id_etud},Etudiant nom : {el.etudiant.nom} , Livre ISBN: {el.isbn}, Livre titre: {el.livre.titre}, ammende: {el.amende} ")
        else:
            # message si aucun emprunt trouvé
            print(f"Aucun emprunt trouvé pour la date de retour {date_retour}.")
    except Exception as e:
        print(f"Erreur lors de la recherche par date de retour: {e}")
 
# emprunt_par_date_retour(session)
 
def livres_non_retournes(session):
    try:
        # Recherche des emprunts où la date de retour est None
        liste = session.query(Emprunt).filter_by(date_retour=None).all()
        if liste:
            print(f" Livres non retournés :")
            for el in liste:
                print(f"{el.id_emprunt}, Date retour: {el.date_retour}, Étudiant ID: {el.id_etud},Etudiant nom : {el.etudiant.nom} , Livre ISBN: {el.isbn}, Livre titre: {el.livre.titre}, ammende: {el.amende} ")
        else:
            # message si tous les livres ont été retournés
            print("Tous les livres ont été retournés.")
    except Exception as e:
        print(f"Erreur lors de la recherche des livres non retournés: {e}")
 
# livres_non_retournes(session)
 
def display_emprunts():
    try:
        # Affiche tous les emprunts
        emprunts = session.query(Emprunt).all()
        if emprunts:
            print("Liste de tous les emprunts :")
            for emprunt in emprunts :
                print(f" Emprunt ID: {emprunt.id_emprunt}, Étudiant ID: {emprunt.id_etud},Etudiant nom : {emprunt.etudiant.nom} , Livre ISBN: {emprunt.isbn}, Livre titre: {emprunt.livre.titre}, ammende: {emprunt.amende} ")
        else:
            # message si aucun emprunt trouvé
            print("Aucun emprunt trouvé.")
    except Exception as e:
        print(f"Erreur lors de l'affichage des emprunts: {e}")

# fonction pour vérifier la validité d'un float 
def check_float_input(float, limit):
    try:
        val = float
        if val <= 0 or val > limit:
            return False
        return True
    except ValueError:
        return False
 
def emprunt_by_id(session):
    try:
        id_emprunt = input("Entrez l'ID à chercher : ")
        # vérifie un emprunt existant
        emprunt = session.query(Emprunt).get(id_emprunt)
        if not emprunt:
            # crée une boucle tant que l'ID n'est pas correct ou si l'utilisateur veut quitter
            print("Emprunt non trouvé.")
            check = False
            while not check:
                id_emprunt = input("Veuillez entrer un ID d'emprunt valide ou 'q' pour quitter : ")
                if id_emprunt.lower() == 'q':
                    return False
                emprunt = session.query(Emprunt).get(id_emprunt)
                if emprunt:
                    check = True
                else:
                    print("Emprunt non trouvé.")
 
        else:
            # affichage de l'emprunt trouvé
            print("Emprunt trouvé :")
            print(f' Emprunt ID: {emprunt.id_emprunt}, Étudiant ID: {emprunt.id_etud},Etudiant nom : {emprunt.etudiant.nom} , Livre ISBN: {emprunt.isbn}, Livre titre: {emprunt.livre.titre}, ammende: {emprunt.amende} ')
    except Exception as e:
        print(f"Erreur lors de la recherche de l'emprunt par ID: {e}")
 
def delete_emprunt(session):
    try:
        # Suppression d'un emprunt par ID
        id_emprunt = input("Entrez l'ID de l'emprunt à supprimer : ")
        emprunt = session.query(Emprunt).get(id_emprunt)
        done= False
        while not done:
            # vérifie un emprunt existant
            if not emprunt:
                print("Emprunt non trouvé.")
                check = False
                # crée une boucle tant que l'ID n'est pas correct ou si l'utilisateur veut quitter
                while not check:
                    id_emprunt = input("Veuillez entrer un ID d'emprunt existant ou 'q' pour quitter : ")
                    if id_emprunt.lower() == 'q':
                        return False
                    emprunt = session.query(Emprunt).get(id_emprunt)
                    if emprunt:
                        check = True
                    else:
                        print("Emprunt non trouvé.")
       
            else:
                # affichage d'un message de confirmation et suppression de l'emprunt
                print("Emprunt trouvé.")
                session.delete(emprunt)
                session.commit()
                print(f' Emprunt ID: {id_emprunt} supprimé avec succès. ')
                done= True
               
    except Exception as e:
        session.rollback()
        print(f"Erreur lors de la suppression de l'emprunt: {e}")
 
def update_amende(session):
    try:
        id_emprunt = input("Entrez l'ID de l'emprunt à mettre à jour : ")
        # vérifie un emprunt existant
        emprunt = session.query(Emprunt).get(id_emprunt)
        done= False
        while not done:
            if not emprunt:
                # crée une boucle tant que l'ID n'est pas correct ou si l'utilisateur veut quitter
                print("Emprunt non trouvé.")
                check = False
                while not check:
                    id_emprunt = input("Veuillez entrer un ID d'emprunt valide ou 'q' pour quitter : ")
                    if id_emprunt.lower() == 'q':
                        return False
                    emprunt = session.query(Emprunt).get(id_emprunt)
                    if emprunt:
                        check = True
                    else:
                        print("Emprunt non trouvé.")
       
            else:
                # affichage de l'emprunt trouvé et mise à jour de l'amende
                print("Emprunt trouvé.")
                nouvelle_amende = float(input("Entrez la nouvelle amende (0.0 - 1000.0) : "))
 
                if not check_float_input(nouvelle_amende, 1000.0):
                    check = False
                    while not check:
                        # crée une boucle tant que l'amende n'est pas correcte ou si l'utilisateur veut quitter
                        nouvelle_amende = float(input("Valeur invalide. Veuillez entrer une amende entre 0.0 et 1000.0 ou '-1' pour quitter : "))
                        if nouvelle_amende== -1:
                            return False
                        if check_float_input(nouvelle_amende, 1000.0):
                            check = True

                # mise à jour de l'amende dans la base de données
                emprunt.amende = nouvelle_amende
                session.commit()
 
                updated = session.query(Emprunt).get(emprunt.id_emprunt)
                if updated:
                    print(f' Nouvelle valeur:')
                    print(f' Emprunt ID: {updated.id_emprunt}, amende: {updated.amende} ')
                else:
                    print("Erreur lors de la mise à jour de l'amende de l'emprunt.")
                done= True
               
    except Exception as e:
        session.rollback()
        print(f"Erreur lors de la mise à jour de l'amende: {e}")
        
        
def emprunt_par_id_etudiant(session):
    try:
        id_etud = input("Entrez l'ID de l'étudiant : ")
        # Check user existant
        check_user = session.query(Etudiant).get(id_etud)
        if not check_user:
                # crée une boucle tant que l'ID n'est pas correct ou si l'utilisateur veut quitter
                print("User non trouvé.")
                check = False
                while not check:
                    id_etud = int(input("Veuillez entrer l'ID d'un user existant ou '-1' pour quitter : "))
                    if id_etud == -1:
                        return False
                    check_user = session.query(Etudiant).get(id_etud)
                    if check_user:
                        check = True
                    else:
                        print("User non trouvé.")

        # Recherche des emprunts par rapport à l'ID étudiant
        liste = session.query(Emprunt).filter_by(id_etud=id_etud).all()
        if liste:
            print(f"La liste des emprunts pour l'étudiant ID {id_etud}:")
            for el in liste:
               
                print(f" Emprunt ID: {el.id_emprunt}, Étudiant ID: {el.id_etud},Etudiant nom : {el.etudiant.nom} , Livre ISBN: {el.isbn}, Livre titre: {el.livre.titre}, ammende: {el.amende} ")
        else:
            # message si aucun emprunt trouvé
            print(f"Aucun emprunt trouvé pour l'étudiant ID {id_etud}.")
    except Exception as e:
        print(f"Erreur lors de la recherche par ID étudiant: {e}")