from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey, create_engine
import os
from dotenv import load_dotenv

# Charge le fichier .env
load_dotenv()

# Base pour modèles ORM
Base = declarative_base()

class Livre(Base):
    __tablename__ = 'livre'  # Nom table Postgres
    
    isbn = Column(Integer, primary_key=True)  # Clé primaire
    titre = Column(String)
    editeur = Column(String)
    annee = Column(Date)
    exemplaires_dispo = Column(Integer)

# Fonction pour obtenir la session (appelée après que user/password soient définis)
def get_engine(user, password):
    host = os.getenv('DB_HOST')
    port = os.getenv('DB_PORT')
    dbname = os.getenv('DB_NAME')
    return create_engine(f"postgresql://{user}:{password}@{host}:{port}/{dbname}")

# Variable globale pour la session (sera initialisée plus tard)
Session = None
session = None

def create_livre(session, isbn, titre, editeur, annee, exemplaires_dispo):
    livre = Livre(isbn=isbn,
                  titre=titre,
                  editeur=editeur,
                  annee=annee,
                  exemplaires_dispo=exemplaires_dispo)
    session.add(livre)
    session.commit()
    return livre.isbn

def read_livre(session, isbn):
    print(f"Recherche du livre avec l'ISBN : {isbn}")
    return session.query(Livre).filter_by(isbn=isbn).first()

def update_livre(session, isbn, nouveau_titre, nouveau_exemplaires_dispo):
    livre = session.query(Livre).get(isbn)
    if livre:
        livre.titre = nouveau_titre
        livre.exemplaires_dispo = nouveau_exemplaires_dispo
        session.commit()
        print(f"Livre ISBN={isbn} mis à jour : titre={nouveau_titre}, exemplaires_dispo={nouveau_exemplaires_dispo}")
        return True
    return False