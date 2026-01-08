from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey, create_engine
import os
from dotenv import load_dotenv

# Charge le fichier .env
load_dotenv()

# Base pour modèles ORM
Base = declarative_base()
 
# Modèle Etudiant (comme ta table)
class Etudiant(Base):
    __tablename__ = 'etudiants'  # Nom table Postgres
    
    id = Column(Integer, primary_key=True)  # Clé primaire
    nom = Column(String)
    prenom = Column(String)
    email = Column(String)
    date_inscription = Column(Date)
    solde_amende = Column(Float)

# Fonction pour obtenir la session (appelée après que user/password soient définis)
def get_engine(user, password):
    host = os.getenv('DB_HOST')
    port = os.getenv('DB_PORT')
    dbname = os.getenv('DB_NAME')
    return create_engine(f"postgresql://{user}:{password}@{host}:{port}/{dbname}")

# Variable globale pour la session (sera initialisée plus tard)
Session = None
session = None

def create_etu(session, nom, prenom, email, date_inscription, solde_amende):
    etu = Etudiant(nom=nom,
                   prenom=prenom,
                   email=email,
                   date_inscription=date_inscription,
                   solde_amende=solde_amende)
    session.add(etu)
    session.commit()
    return etu.id

def read_etu(session, nom):
    print(f"Recherche de l'étudiant avec le nom : {nom}")
    return session.query(Etudiant).filter_by(nom=nom).first()

def update_etu(session, id_etud, nouveau_prenom, nouveau_solde):
    etu = session.query(Etudiant).get(id_etud)
    if etu:
        etu.prenom = nouveau_prenom
        etu.solde_amende = nouveau_solde
        session.commit()
        print(f"Étudiant ID={id_etud} mis à jour : prénom={nouveau_prenom}, solde_amende={nouveau_solde}")
        return True
    return False

def delete_etu(session, id_etud):
    etu = read_etu(session, id_etud)
    if etu:
        session.delete(etu)
        session.commit()
        return True
    return False

# update_etu(session, '26', 'Alexandre', 0)
# read_etu(session, 'Gouraud')

