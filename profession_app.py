import streamlit as st
import sqlite3

# Connexion à la base de données SQLite
conn = sqlite3.connect('users.db')
c = conn.cursor()

# Supprimer des tables si elle existe
#c.execute('DROP TABLE IF EXISTS users')
#c.execute('DROP TABLE IF EXISTS user_info')

# Création de la table pour les utilisateurs
c.execute('''CREATE TABLE IF NOT EXISTS users (username TEXT, email TEXT, phone TEXT, country TEXT, province TEXT, region TEXT, language TEXT, religion TEXT, password TEXT)''')
conn.commit()

# Création de la table pour les informations personnelles
c.execute('''CREATE TABLE IF NOT EXISTS user_info (username TEXT, age INTEGER, gender TEXT, marital_status TEXT, children INTEGER, education_level TEXT, salary REAL, wakeup_time TEXT, partners INTEGER, hobbies TEXT, occupation TEXT)''')
conn.commit()

# Fonction pour vérifier la structure de la table
def check_table_structure():
    c.execute('PRAGMA table_info(users)')
    return c.fetchall()

# Fonction pour ajouter un nouvel utilisateur
def add_user(username, email, phone, country, province, region, language, religion, password):
    c.execute('INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', (username, email, phone, country, province, region, language, religion, password))
    conn.commit()

# Fonction pour vérifier les informations de connexion
def login_user(username, password):
    c.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
    return c.fetchone()

# Fonction pour ajouter des informations personnelles
def add_user_info(username, age, gender, marital_status, children, education_level, salary, wakeup_time, partners, hobbies, occupation):
    c.execute('INSERT INTO user_info VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', 
              (username, age, gender, marital_status, children, education_level, salary, wakeup_time, partners, hobbies, occupation))
    conn.commit()

# Page d'inscription
def signup_page():
    st.title("Inscription")

    username = st.text_input("Nom d'utilisateur")
    email = st.text_input("Adresse e-mail")
    phone = st.text_input("Numéro de téléphone")
    country = st.text_input("Pays")
    province = st.text_input("Province")
    region = st.text_input("Région")
    langue = ["Anglais", "Français", "Swahili", "Lingala", "Chiluba", "Kikongo", "Kinyarwanda", "Autre"];
    language = st.selectbox("Langue parlée",langue)
    religion = st.selectbox("Réligion",["Chrétien", "Musulman", "Kimbangiste", "Animiste", "Autre"])
    password = st.text_input("Mot de passe", type='password')

    if st.button("S'inscrire"):
        add_user(username, email, phone, country, province, region, language, religion, password)
        st.success("Inscription réussie ! Vous pouvez maintenant vous connecter.")
        
# Page de connexion
def login_page():
    st.title("Connexion")

    username = st.text_input("Nom d'utilisateur")
    password = st.text_input("Mot de passe", type='password')

    if st.button("Se connecter"):
        user = login_user(username, password)
        if user:
            st.success("Connexion réussie !")
            st.session_state.logged_in = True
            st.session_state.username = username
            main_page(username)
        else:
            st.error("Nom d'utilisateur ou mot de passe incorrect")

# Page principale
def main_page(username):
    st.title("Informations Personnelles")

    age = st.number_input("Âge", min_value=0)
    gender = st.selectbox("Sexe", ["Homme", "Femme"])
    marital_status = st.selectbox("État civil", ["Célibataire", "Marié(e)", "Divorcé(e)", "Veuf(ve)"])
    children = st.number_input("Nombre d'enfants", min_value=0)
    education_level = st.selectbox("Niveau d'études", ["École primaire", "Lycée", "Université", "Master", "Doctorat"])
    salary = st.number_input("Salaire", min_value=0.0)
    wakeup_time = st.number_input("Heure de réveil", min_value = 0.00, max_value = 12.00, step = 0.01)
    partners = st.number_input("Nombre de partenaires", min_value=0)
    hobbies = st.text_input("Occupations ou centres d'intérêt")

    if st.button("Soumettre"):
        # Logique pour déterminer la profession en fonction des informations fournies
        profession = determine_profession(age, gender, marital_status, children, education_level, salary, wakeup_time, partners, hobbies)
        add_user_info(username, age, gender, marital_status, children, education_level, salary, wakeup_time, partners, hobbies, profession)
        st.write(f"Votre profession est probablement : {profession}")

def determine_profession(age, gender, marital_status, children, education_level, salary, wakeup_time, partners, hobbies):
    # Logique fictive pour déterminer la profession
    if education_level == "Master" or education_level == "Doctorat":
        return "Professeur"
    elif salary > 50000:
        return "Manager"
    else:
        return "Technicien"

# Interface principale
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.sidebar.title("Menu")
    choice = st.sidebar.selectbox("Choisissez une option", ["Se connecter", "S'inscrire"])

    if choice == "S'inscrire":
        signup_page()
    else:
        login_page()
else:
    main_page(st.session_state.username)

conn.close()

