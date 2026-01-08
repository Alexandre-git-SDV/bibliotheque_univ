# 📚 Application de gestion de bibliothèque (Console)

## I. Présentation du projet

Cette application est une **application console de gestion de bibliothèque**, développée en **Python**.
Elle permet de gérer :

* les **étudiants**
* les **livres**
* les **emprunts de livres**

L’application se connecte à une **base de données PostgreSQL** et offre à l’utilisateur la possibilité d’effectuer des opérations **CRUD** (*Create, Read, Update, Delete*) à travers un **menu interactif en ligne de commande**.

### 🔐 Gestion des rôles

Les opérations accessibles varient selon le rôle de la personne connectée :

* **Postgres (Administrateur)**
  Accès total à la base de données et à l’ensemble des tables avec tous les droits administrateur.

* **Bibliothécaire**
  Accès à la base de données avec des droits limités aux opérations suivantes :

  * `SELECT`
  * `INSERT`
  * `UPDATE`

* **Étudiant**
  Accès restreint à la base de données avec uniquement des droits de lecture (`SELECT`) sur la table **emprunt**.

### 🔒 Sécurité des données

Le projet utilise un fichier **`.env`** afin de stocker les informations sensibles telles que :

* le nom d’utilisateur administrateur,
* le mot de passe,
* le chemin d’accès à la base de données.

Cela permet de garantir la **confidentialité** des données et d’éviter leur exposition dans le code source.

---

## II. Architecture du projet

L’architecture du projet est divisée en **quatre parties distinctes**, assurant une bonne séparation des responsabilités.

### A. Accès à la base de données

Cette couche utilise des **variables d’environnement** pour récupérer les informations de connexion à la base de données **PostgreSQL**.
La bibliothèque **psycopg2** est utilisée afin d’établir la connexion entre l’application Python et la base de données.

---

### B. Couche ORM

La couche ORM repose sur **SQLAlchemy** et permet de définir les tables de la base de données sous forme de **classes Python**.

Chaque classe correspond à une table et doit respecter :

* le nom des attributs,
* les types de données,
* les contraintes (clé primaire, clé étrangère, unicité, etc.).

Ces modèles sont ensuite utilisés pour la création et la manipulation des opérations **CRUD**.

---

### C. Logique métier (fonctions CRUD)

La logique métier est responsable de la gestion des opérations **CRUD**.

Elle fonctionne de la manière suivante :

1. Création d’une **session** avec la base de données.
2. Utilisation des modèles ORM pour exécuter les requêtes.
3. Gestion des transactions (`commit`, `rollback`) et des erreurs.

Cette couche assure la cohérence des données et centralise les règles métier.

---

### D. Interface utilisateur (console de gestion)

L’interface utilisateur est une **interface en ligne de commande** qui permet à l’utilisateur de sélectionner les actions via un menu interactif.

Des mécanismes de **gestion des erreurs** ont été implémentés dans la logique métier afin de :

* détecter les saisies invalides (ex. texte à la place d’une date),
* éviter les interruptions ou crashs de l’application,
* garantir une expérience utilisateur stable.

---

## 🛠️ Technologies utilisées

* **Python**
* **PostgreSQL**
* **psycopg2**
* **SQLAlchemy**
* **dotenv**

Dis-moi 👍
