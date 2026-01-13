# -*- coding: utf-8 -*-
# app_savate.py
# Dashboard Luc Leger (club) - Streamlit
# Lancer: streamlit run app_savate.py

from __future__ import annotations

import os
import uuid
from dataclasses import dataclass, asdict
from datetime import date
from typing import Dict, List

import pandas as pd
import streamlit as st


# -----------------------------
# BAREME CLUB (pedagogique)
# -----------------------------
BAREME: Dict[str, Dict[str, Dict[int, str]]] = {
    "M": {
        "15-19": {7: "Faible", 8: "Moyen-", 9: "Moyen", 10: "Moyen+", 11: "Bon", 12: "Tres bon", 13: "Excellent", 14: "Elite", 15: "Elite+"},
        "20-24": {7: "Faible", 8: "Moyen-", 9: "Moyen", 10: "Bon", 11: "Tres bon", 12: "Excellent", 13: "Elite", 14: "Elite+", 15: "Elite+"},
        "25-29": {7: "Faible", 8: "Moyen", 9: "Moyen+", 10: "Bon", 11: "Tres bon", 12: "Excellent", 13: "Elite", 14: "Elite+", 15: "Elite+"},
        "30-34": {7: "Faible", 8: "Moyen", 9: "Bon", 10: "Tres bon", 11: "Excellent", 12: "Elite", 13: "Elite+", 14: "Elite+", 15: "Elite+"},
        "35-39": {7: "Faible", 8: "Moyen+", 9: "Bon", 10: "Tres bon", 11: "Excellent", 12: "Elite", 13: "Elite+", 14: "Elite+", 15: "Elite+"},
        "40-44": {7: "Moyen-", 8: "Moyen+", 9: "Bon", 10: "Tres bon", 11: "Excellent", 12: "Elite", 13: "Elite+", 14: "Elite+", 15: "Elite+"},
        "45-49": {7: "Moyen", 8: "Bon", 9: "Tres bon", 10: "Excellent", 11: "Elite", 12: "Elite+", 13: "Elite+", 14: "Elite+", 15: "Elite+"},
        "50-54": {7: "Moyen", 8: "Bon", 9: "Tres bon", 10: "Excellent", 11: "Elite", 12: "Elite+", 13: "Elite+", 14: "Elite+", 15: "Elite+"},
        "55-60": {7: "Moyen", 8: "Bon", 9: "Tres bon", 10: "Excellent", 11: "Elite", 12: "Elite+", 13: "Elite+", 14: "Elite+", 15: "Elite+"},
    },
    "F": {
        "15-19": {7: "Moyen-", 8: "Moyen", 9: "Bon", 10: "Tres bon", 11: "Excellent", 12: "Elite", 13: "Elite+", 14: "Elite+", 15: "Elite+"},
        "20-24": {7: "Moyen", 8: "Bon", 9: "Tres bon", 10: "Excellent", 11: "Elite", 12: "Elite+", 13: "Elite+", 14: "Elite+", 15: "Elite+"},
        "25-29": {7: "Moyen", 8: "Bon", 9: "Tres bon", 10: "Excellent", 11: "Elite", 12: "Elite+", 13: "Elite+", 14: "Elite+", 15: "Elite+"},
        "30-34": {7: "Moyen+", 8: "Bon", 9: "Tres bon", 10: "Excellent", 11: "Elite", 12: "Elite+", 13: "Elite+", 14: "Elite+", 15: "Elite+"},
        "35-39": {7: "Bon", 8: "Tres bon", 9: "Excellent", 10: "Elite", 11: "Elite+", 12: "Elite+", 13: "Elite+", 14: "Elite+", 15: "Elite+"},
        "40-44": {7: "Bon", 8: "Tres bon", 9: "Excellent", 10: "Elite", 11: "Elite+", 12: "Elite+", 13: "Elite+", 14: "Elite+", 15: "Elite+"},
        "45-49": {7: "Bon", 8: "Tres bon", 9: "Excellent", 10: "Elite", 11: "Elite+", 12: "Elite+", 13: "Elite+", 14: "Elite+", 15: "Elite+"},
        "50-54": {7: "Bon", 8: "Tres bon", 9: "Excellent", 10: "Elite", 11: "Elite+", 12: "Elite+", 13: "Elite+", 14: "Elite+", 15: "Elite+"},
        "55-60": {7: "Bon", 8: "Tres bon", 9: "Excellent", 10: "Elite", 11: "Elite+", 12: "Elite+", 13: "Elite+", 14: "Elite+", 15: "Elite+"},
    },
}

LEVEL5_COLORS = {
    "Insuffisant": "#fee2e2",
    "Moyen": "#ffedd5",
    "Bon": "#dcfce7",
    "Très Bon": "#bbf7d0",
    "Excellent": "#cffafe",
}


def clamp(n: int, lo: int, hi: int) -> int:
    return max(lo, min(hi, n))


def age_band(age: int) -> str:
    a = clamp(age, 15, 60)
    start = ((a - 15) // 5) * 5 + 15
    end = start + 4
    return f"{start}-{end}"


def level_raw(sex: str, age: int, palier: int) -> str:
    sex = "M" if sex == "M" else "F"
    band = age_band(age)
    p = clamp(palier, 7, 15)
    return BAREME.get(sex, {}).get(band, {}).get(p, "-")


def to_level5(raw: str) -> str:
    if raw == "Faible":
        return "Insuffisant"
    if raw in ("Moyen-", "Moyen", "Moyen+"):
        return "Moyen"
    if raw == "Bon":
        return "Bon"
    if raw == "Tres bon":
        return "Très Bon"
    if raw in ("Excellent", "Elite", "Elite+"):
        return "Excellent"
    return "-"


def level_for(sex: str, age: int, palier: int) -> str:
    return to_level5(level_raw(sex, age, palier))


def interpret_for_assaut(level5: str) -> Dict[str, str]:
    if level5 == "Insuffisant":
        return {
            "Synthese": "Endurance insuffisante pour soutenir plusieurs reprises a intensite assaut.",
            "Point de vigilance": "Baisse rapide de lucidite (distance, garde) des la 1re-2e reprise.",
            "Priorite de travail": "Construire une base aerobie et stabiliser la technique a faible intensite.",
        }
    if level5 == "Moyen":
        return {
            "Synthese": "Base cardio correcte pour l'entrainement, limite sur des assauts enchaines.",
            "Point de vigilance": "Degradation en fin de reprise: deplacements moins frequents, relances plus rares.",
            "Priorite de travail": "Developper l'intermittent et la tolerance aux changements de rythme.",
        }
    if level5 == "Bon":
        return {
            "Synthese": "Bon niveau pour l'assaut: volume de travail stable et capacite a relancer.",
            "Point de vigilance": "Risque principal: surcharge si recuperation et progressivite sont negligees.",
            "Priorite de travail": "Specifique savate (intermittent + déplacements + relances structurées).",
        }
    if level5 == "Très Bon":
        return {
            "Synthese": "Très bon moteur: enchainement de reprises et relances frequentes possibles.",
            "Point de vigilance": "Risque: partir trop vite (sur-regime) plutot qu'une limite cardio.",
            "Priorite de travail": "Affutage, qualite des relances, lactique court en controle, tactique.",
        }
    if level5 == "Excellent":
        return {
            "Synthese": "Excellent moteur cardio: pression et repetition d'efforts a haute frequence possibles.",
            "Point de vigilance": "Risque: surcharge (tendons, mollets) si volumes et intensites mal pilotes.",
            "Priorite de travail": "Qualite > volume, spécificité assaut, récupération premium.",
        }
    return {"Synthese": "Niveau non determine.", "Point de vigilance": "-", "Priorite de travail": "-"}


def age_specific_notes(age: int) -> Dict[str, str]:
    if age <= 19:
        return {
            "Titre": "Spécificité 15-19 ans",
            "Note": "Priorité a la progressivite: technique propre, déplacements, developpement aérobie. Éviter la surcharge lactique, privilégier des formats courts et ludiques.",
        }
    if age <= 34:
        return {
            "Titre": "Spécificité 20-34 ans",
            "Note": "Fenêtre idéale pour développer la VMA et la tolérance a l'intensité. Monter progressivement la densité (intermittent, circuits spécifiques assaut).",
        }
    if age <= 44:
        return {
            "Titre": "Spécificité 35-44 ans",
            "Note": "Accent sur la récupération et la régularité. Maintenir la VMA via intermittents courts et renforcer l'économie des déplacements.",
        }
    return {
        "Titre": "Spécificité 45-60 ans",
        "Note": "Priorité: prévention (tendons, mollets, ischios), échauffement long, montée en charge progressive. Intermittent court maîtrisé et endurance fondamentale régulière.",
    }


def suggested_work(level5: str) -> List[Dict[str, str]]:
    base = [
        {"Code": "EF", "Application": "Endurance fondamentale", "Detail": "20 a 45 min en aisance respiratoire, 1 a 2 fois par semaine."},
        {"Code": "TECH", "Application": "Technique basse intensité", "Detail": "Rounds techniques (shadow, cibles) sans fatigue excessive."},
    ]
    intermittent = [
        {"Code": "30/30", "Application": "Intermittent 30/30", "Detail": "2 x (6 a 10 répétitions) a intensité élevée, récupération 3 a 4 min entre blocs."},
        {"Code": "15/15", "Application": "Intermittent 15/15", "Detail": "2 x (10 a 20 répétitions), axe relance et déplacements."},
        {"Code": "ASSAUT", "Application": "Intermittent spécifique assaut", "Detail": "6 x (1 min assaut actif / 1 min léger) avec consignes tactiques."},
        {"Code": "DEPL", "Application": "Déplacements", "Detail": "Ateliers d'appuis (avant/arrière, latéral, pivots), 2 a 3 blocs de 4 min."},
        {"Code": "REL", "Application": "Relances", "Detail": "10 a 15 s explosif / 45 a 50 s récup, 8 a 12 répétitions."},
    ]
    recovery = [{"Code": "REC", "Application": "Récupération", "Detail": "Marche, mobilité, sommeil, hydratation, 1 a 2 jours faciles par semaine."}]

    if level5 == "Insuffisant":
        return base + [intermittent[0]] + recovery
    if level5 == "Moyen":
        return base + intermittent + recovery
    if level5 == "Bon":
        return base + intermittent + recovery
    if level5 == "Très Bon":
        return intermittent[2:] + [{"Code": "LACT", "Application": "Lactique court", "Detail": "4 a 6 x (30 a 45 s dur / 2 a 3 min récup) en contrôle."}] + recovery
    if level5 == "Excellent":
        return intermittent[2:] + [{"Code": "QUAL", "Application": "Qualité > volume", "Detail": "Séances plus courtes, intensité ciblée, exigence forte sur la récupération."}] + recovery
    return []


@dataclass
class Athlete:
    id: str
    prenom: str
    age: int
    sexe: str
    palier: int


# -----------------------------
# UI
# -----------------------------
st.set_page_config(page_title="Dashboard Luc Leger - CBF", layout="wide")

st.markdown(
    """
<style>
/* Header sobre uni + marge basse */
.header {
  padding: 12px 16px;
  border-radius: 16px;
  color: white;
  background: #0f172a;
  border: 1px solid #1f2937;
  margin-bottom: 12px;
}
.small { color: rgba(255,255,255,0.85); }

/* Section avec bandeau integre */
.section {
  border-radius: 16px;
  border: 1px solid #e5e7eb;
  background: #ffffff;
  overflow: hidden;
  box-shadow: 0 1px 2px rgba(15, 23, 42, 0.06);
}
.section-header {
  padding: 10px 16px;
  font-weight: 900;
  font-size: 15px;
  color: #0f172a;
  border-bottom: 1px solid #e5e7eb;
}
.section-header.saisie { background: #f1f5f9; }
.section-header.liste  { background: #f8fafc; }
.section-header.analyse{ background: #eef2f7; }

.section-body { padding: 16px; }

/* KPI cards */
.kpi { padding: 14px; border-radius: 14px; border: 1px solid #e5e7eb; background: white; }

/* Pills */
.pill {
  display:inline-block;
  padding: 4px 10px;
  border-radius: 999px;
  border:1px solid #e5e7eb;
  font-size: 12px;
  font-weight: 800;
  background: #f1f5f9;
}
</style>
""",
    unsafe_allow_html=True,
)

# Header + logo
col_logo, col_title = st.columns([1, 7], vertical_alignment="center")
with col_logo:
    if os.path.exists("Logo Rond.png"):
        st.image("Logo Rond.png", width=72)
    else:
        st.markdown("<div class='pill'>Logo manquant: Logo Rond.png</div>", unsafe_allow_html=True)

with col_title:
    st.markdown(
        """
<div class="header">
  <div style="font-size:24px; font-weight:900;">Tableau de bord - Test Luc Leger</div>
  <div class="small" style="margin-top:6px;">
    Saisie des résultats, niveau automatique (5 niveaux), Interprétation assaut, Spécificité âge et applications pour les tireurs.
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

if "athletes" not in st.session_state:
    st.session_state.athletes: List[Athlete] = []

df = (
    pd.DataFrame([asdict(a) for a in st.session_state.athletes])
    if st.session_state.athletes
    else pd.DataFrame(columns=["id", "prenom", "age", "sexe", "palier"])
)

total = len(df)
nb_m = int((df["sexe"] == "M").sum()) if total else 0
nb_f = int((df["sexe"] == "F").sum()) if total else 0
avg_palier = float(df["palier"].mean()) if total else None
avg_palier_str = f"{avg_palier:.1f}" if avg_palier is not None else "-"

k1, k2, k3, k4 = st.columns(4)
k1.markdown(f"<div class='kpi'><div style='color:#0f172a;font-weight:900;'>Participants</div><div style='font-size:26px;font-weight:900;'>{total}</div></div>", unsafe_allow_html=True)
k2.markdown(f"<div class='kpi'><div style='color:#0f172a;font-weight:900;'>Masculin</div><div style='font-size:26px;font-weight:900;'>{nb_m}</div></div>", unsafe_allow_html=True)
k3.markdown(f"<div class='kpi'><div style='color:#0f172a;font-weight:900;'>Féminin</div><div style='font-size:26px;font-weight:900;'>{nb_f}</div></div>", unsafe_allow_html=True)
k4.markdown(f"<div class='kpi'><div style='color:#0f172a;font-weight:900;'>Palier moyen</div><div style='font-size:26px;font-weight:900;'>{avg_palier_str}</div></div>", unsafe_allow_html=True)

st.write("")

left, right = st.columns([1, 2], gap="large")

with left:
    st.markdown("<div class='section'>", unsafe_allow_html=True)
    st.markdown("<div class='section-header saisie'>Saisie d'un résultat</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-body'>", unsafe_allow_html=True)

    prenom = st.text_input("Prénom", placeholder="Ex: Lina")
    age = st.number_input("Âge", min_value=15, max_value=60, value=15, step=1)
    sexe = st.selectbox("Sexe", options=["M", "F"], format_func=lambda x: "Masculin" if x == "M" else "Féminin")
    palier = st.number_input("Palier atteint", min_value=7, max_value=15, value=7, step=1)

    if st.button("Évaluer", use_container_width=True, type="primary"):
        if prenom.strip():
            st.session_state.athletes.insert(
                0,
                Athlete(
                    id=str(uuid.uuid4()),
                    prenom=prenom.strip(),
                    age=int(age),
                    sexe=sexe,
                    palier=int(palier),
                ),
            )
            st.success("Résultat ajouté.")
            st.rerun()
        else:
            st.error("Le prénom est requis.")

    st.markdown("</div></div>", unsafe_allow_html=True)

with right:
    st.markdown("<div class='section'>", unsafe_allow_html=True)
    st.markdown("<div class='section-header liste'>Liste des tireurs</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-body'>", unsafe_allow_html=True)

    query = st.text_input("Recherche", placeholder="Filtrer: prénom, âge, sexe, palier...")
    if total:
        view = df.copy()
        if query.strip():
            q = query.strip().lower()
            mask = (
                view["prenom"].astype(str).str.lower().str.contains(q)
                | view["age"].astype(str).str.contains(q)
                | view["sexe"].astype(str).str.lower().str.contains(q)
                | view["palier"].astype(str).str.contains(q)
            )
            view = view[mask]

        view["niveau"] = view.apply(lambda r: level_for(str(r["sexe"]), int(r["age"]), int(r["palier"])), axis=1)

        view_display = view[["prenom", "age", "sexe", "palier", "niveau"]].rename(
            columns={"prenom": "Prénom", "age": "Âge", "sexe": "Sexe", "palier": "Palier", "niveau": "Niveau"}
        )
        st.dataframe(view_display, use_container_width=True, hide_index=True)

        csv = view_display.to_csv(index=False).encode("utf-8")
        st.download_button(
            "Exporter CSV",
            data=csv,
            file_name=f"luc-leger_cbf_{date.today().isoformat()}.csv",
            mime="text/csv",
            use_container_width=True,
        )

        st.markdown("</div></div>", unsafe_allow_html=True)

        st.write("")

        st.markdown("<div class='section'>", unsafe_allow_html=True)
        st.markdown("<div class='section-header analyse'>Analyse (tireur sélectionné)</div>", unsafe_allow_html=True)
        st.markdown("<div class='section-body'>", unsafe_allow_html=True)

        if len(view) > 0:
            selected_row = view.iloc[0]
            sel_prenom = str(selected_row["prenom"])
            sel_age = int(selected_row["age"])
            sel_sexe = str(selected_row["sexe"])
            sel_palier = int(selected_row["palier"])

            lvl5 = level_for(sel_sexe, sel_age, sel_palier)
            band = age_band(sel_age)

            pill_bg = LEVEL5_COLORS.get(lvl5, "#e5e7eb")
            st.markdown(
                f"""
<div style="display:flex; flex-wrap:wrap; gap:8px; align-items:center;">
  <span class="pill">{sel_prenom}</span>
  <span class="pill">{sel_age} ans</span>
  <span class="pill">Tranche {band}</span>
  <span class="pill">Sexe {'Masculin' if sel_sexe=='M' else 'Féminin'}</span>
  <span class="pill">Palier {sel_palier}</span>
  <span class="pill" style="background:{pill_bg}; margin-left:auto;">Niveau: {lvl5}</span>
</div>
""",
                unsafe_allow_html=True,
            )

            tab1, tab2, tab3 = st.tabs(["Interprétation assaut", "Spécificité âge", "Applications (tireur)"])

            with tab1:
                info = interpret_for_assaut(lvl5)
                c1, c2, c3 = st.columns(3)
                c1.markdown("<div class='section'><div class='section-header analyse'>Synthèse</div><div class='section-body'>", unsafe_allow_html=True)
                c1.write(info["Synthese"])
                c1.markdown("</div></div>", unsafe_allow_html=True)

                c2.markdown("<div class='section'><div class='section-header liste'>Point de vigilance</div><div class='section-body'>", unsafe_allow_html=True)
                c2.write(info["Point de vigilance"])
                c2.markdown("</div></div>", unsafe_allow_html=True)

                c3.markdown("<div class='section'><div class='section-header saisie'>Priorité de travail</div><div class='section-body'>", unsafe_allow_html=True)
                c3.write(info["Priorite de travail"])
                c3.markdown("</div></div>", unsafe_allow_html=True)

            with tab2:
                note = age_specific_notes(sel_age)
                st.write(f"**{note['Titre']}**")
                st.write(note["Note"])

            with tab3:
                work = suggested_work(lvl5)
                if not work:
                    st.info("Aucune recommandation disponible.")
                else:
                    st.dataframe(pd.DataFrame(work), use_container_width=True, hide_index=True)

        st.markdown("</div></div>", unsafe_allow_html=True)

    else:
        st.info("Ajoute au moins un tireur pour afficher la liste et l'analyse.")
        st.markdown("</div></div>", unsafe_allow_html=True)

st.caption("Barème club - Luc Leger (15-60 ans, paliers 7-15). Outil d'aide a la decision pour l'entrainement en Savate.")
