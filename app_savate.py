import streamlit as st
import pandas as pd

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Savate Coach - Analyse VMA", page_icon="🥊", layout="wide")

# --- DONNÉES DE RÉFÉRENCE (Basées sur nos grilles précédentes) ---
# Echelle : 1=Insuffisant, 2=Moyen, 3=Correct, 4=Bon, 5=Très Bon, 6=Exceptionnel

def get_level_score(age, sex, palier):
    # Ajustement de l'âge à la tranche la plus proche (5 en 5)
    age_ref = min(max(round(age / 5) * 5, 15), 60)
    
    # Grilles simplifiées pour la logique (Palier 7 à 15+)
    # Logique basée sur les tableaux fournis précédemment
    
    # Matrice simplifiée (Score de base)
    # On ajuste le score selon l'âge et le sexe dynamiquement
    base_score = 0
    
    # Logique Homme
    if sex == "Homme":
        if age_ref == 15: base_score = palier - 5 # P9=4(Bon)
        elif age_ref <= 30: base_score = palier - 6 # P10=4(Bon)
        elif age_ref <= 45: base_score = palier - 5 # P10=5(TB)
        else: base_score = palier - 4 # 50+ : P10=6(Exc)
    
    # Logique Femme (Décalage physiologique standard)
    else:
        if age_ref == 15: base_score = palier - 4 # P9=5(TB)
        elif age_ref <= 30: base_score = palier - 6 # P10=4(TB) mais ajusté
        elif age_ref <= 45: base_score = palier - 4 
        else: base_score = palier - 3

    # Plafonnement des scores entre 1 et 6
    if base_score < 1: base_score = 1
    if base_score > 6: base_score = 6
    
    levels = {
        1: "Insuffisant", 2: "Moyen", 3: "Correct", 
        4: "Bon", 5: "Très Bon", 6: "Exceptionnel"
    }
    return levels[base_score], base_score

# --- INTERPRÉTATION DU COACH ---
def get_advice(score, age):
    advice = {}
    
    # 1. Interprétation Assaut
    if score <= 2:
        advice['assaut'] = "⚠️ **Danger :** Risque d'asphyxie dès le 2ème round. Le tireur sera lucide 1 minute, puis subira le combat."
    elif score == 3:
        advice['assaut'] = "🆗 **Juste :** Tiendra la distance mais manquera de 'jus' pour finir fort. Doit boxer à l'économie."
    elif score == 4:
        advice['assaut'] = "✅ **Solide :** Capable de maintenir un rythme soutenu. Peut imposer un pressing modéré."
    else:
        advice['assaut'] = "🚀 **Arme Fatale :** Le cardio est une arme. Peut étouffer l'adversaire, travailler en volume et accélérer à la fin."

    # 2. Spécificité Age
    if age < 18:
        advice['age_spec'] = "En pleine croissance. Profiter de ce cardio pour travailler la **technique en mouvement** (décalages)."
    elif 18 <= age <= 35:
        advice['age_spec'] = "L'âge de la performance pure. Il faut convertir ce cardio en **puissance-endurance**."
    else:
        advice['age_spec'] = "Conservation et gestion. Attention aux tendons. Privilégier la **récupération active**."

    # 3. Applications / Entraînement
    if score <= 3:
        advice['drill'] = "🏃 **Priorité Foncier :** Footing 45min + 30/30 (2 séries de 6min) chaque semaine."
    elif score <= 5:
        advice['drill'] = "🥊 **Spécifique Boxe :** Leçons de gants avec changements de rythme. Travail de fractionné au sac (10s fort / 20s souple)."
    else:
        advice['drill'] = "⚡ **Explosivité :** Le coffre est là. Travailler les sprints courts, la pliométrie et la vitesse de réaction."

    return advice

# --- INTERFACE UTILISATEUR ---

st.title("🥊 Savate Coach - Dashboard VMA")
st.markdown("### Analyseur de performance Luc Léger pour la compétition")

# Zone de Saisie (Sidebar)
st.sidebar.header("Profil du Tireur")
prenom = st.sidebar.text_input("Prénom", "Alex")
age = st.sidebar.number_input("Âge", min_value=15, max_value=60, value=23, step=1)
sexe = st.sidebar.radio("Sexe", ["Homme", "Femme"])
palier = st.sidebar.slider("Palier Luc Léger atteint", 7.0, 15.0, 10.0, 0.5)

# Calculs
niveau_txt, score_num = get_level_score(age, sexe, palier)
conseils = get_advice(score_num, age)
vma_estimee = palier * 0.5 + 8.0 # Approximation simple VMA = 8 + 0.5*Palier (dépend des variantes, ici standard)

# Affichage Principal
col1, col2 = st.columns([1, 2])

with col1:
    st.image("https://cdn-icons-png.flaticon.com/512/1474/1474560.png", width=100) # Icone Boxe
    st.metric(label="VMA Estimée", value=f"{vma_estimee} km/h")
    
    # Code couleur dynamique
    color = "red"
    if score_num >= 3: color = "orange"
    if score_num >= 4: color = "green"
    if score_num == 6: color = "blue"
    
    st.markdown(f"""
    <div style="background-color:{color}; padding:10px; border-radius:10px; color:white; text-align:center;">
        <h3>Niveau</h3>
        <h2>{niveau_txt}</h2>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.header(f"Analyse pour {prenom}")
    
    st.subheader("🥊 Interprétation Assaut")
    st.info(conseils['assaut'])
    
    st.subheader(f"🧠 Spécificité Catégorie ({age} ans)")
    st.write(conseils['age_spec'])
    
    st.subheader("🏋️ Applications & Travail à fournir")
    st.success(conseils['drill'])

st.divider()
st.caption("Outil généré pour le coaching de Savate Boxe Française - Basé sur les grilles de performance VMA.")
