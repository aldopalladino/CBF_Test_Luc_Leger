# -*- coding: utf-8 -*-
# app_savate.py
# Dashboard Luc Leger (club) - Streamlit
# Saisie: prenom, age, sexe, palier | Sortie: niveau, interpretation assaut, specificite age, applications
# Lancer: streamlit run app_savate.py

from __future__ import annotations

import uuid
from dataclasses import dataclass, asdict
from datetime import date
from typing import Dict, List

import pandas as pd
import streamlit as st


# -----------------------------
# Bareme club (outil pedagogique)
# Paliers 7 a 15, tranches 5 ans, ages 15 a 60
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

LEVEL_COLORS = {
    "Faible": "#fecaca",
    "Moyen-": "#fed7aa",
    "Moyen": "#fde68a",
    "Moyen+": "#fef08a",
    "Bon": "#bbf7d0",
    "Tres bon": "#86efac",
    "Excellent": "#99f6e4",
    "Elite": "#bae6fd",
    "Elite+": "#c7d2fe",
}


def clamp(n: int, lo: int, hi: int) -> int:
    return max(lo, min(hi, n))


def age_band(age: int) -> str:
    a = clamp(age, 15, 60)
    start = ((a - 15) // 5) * 5 + 15
    end = start + 4
    return f"{start}-{end}"


def level_for(sex: str, age: int, palier: int) -> str:
    sex = "M" if sex == "M" else "F"
    band = age_band(age)
    p = clamp(palier, 7, 15)
    return BAREME.get(sex, {}).get(band, {}).get(p, "—")


def interpret_for_assaut(level: str) -> Dict[str, str]:
    if level == "Faible":
        return {
            "Synthese": "Endurance insuffisante pour soutenir plusieurs reprises a intensite assaut.",
            "Point de vigilance": "Risque de chute de lucidite (distance / garde) des la 1re-2e reprise.",
            "Priorite de travail": "Construire une base aerobie + maitrise technique a faible intensite.",
        }
    if level in ("Moyen-", "Moyen"):
        return {
            "Synthese": "Base cardio correcte pour entrainement, limite pour assauts enchaines.",
            "Point de vigilance": "Degradation en fin de reprise, baisse de frequence de deplacements.",
            "Priorite de travail": "Developper VMA/intermittent et tolerance a l'effort.",
        }
    if level == "Moyen+":
        return {
            "Synthese": "Profil exploitable en assaut club, a condition d'une gestion du rythme.",
            "Point de vigilance": "Peut subir les accelerations adverses (changements de rythme).",
            "Priorite de travail": "Intermittent court + travail de relance + strategie d'economie.",
        }
    if level == "Bon":
        return {
            "Synthese": "Bon niveau pour assaut : capacite a tenir le volume et relancer.",
            "Point de vigilance": "Principal risque : surcharge si la recup est negligee.",
            "Priorite de travail": "Specifique savate (intermittent + deplacements + enchainements).",
        }
    if level in ("Tres bon", "Excellent"):
        return {
            "Synthese": "Tres bon moteur : enchainement de reprises, relances frequentes possibles.",
            "Point de vigilance": "Risque : partir trop vite (sur-regime) plutot que limite cardio.",
            "Priorite de travail": "Affutage, qualite des relances, lactique court, gestion tactique.",
        }
    if level in ("Elite", "Elite+"):
        return {
            "Synthese": "Tres haut niveau cardio : gros potentiel de pression et repetition d'efforts.",
            "Point de vigilance": "Risque : blessure/surcharge si volumes mal pilotes.",
            "Priorite de travail": "Specificite assaut (vitesse, lucidite, relances), recuperation premium.",
        }
    return {"Synthese": "Niveau non determine.", "Point de vigilance": "—", "Priorite de travail": "—"}


def age_specific_notes(age: int) -> Dict[str, str]:
    if age <= 19:
        return {
            "Titre": "Specificite 15-19 ans",
            "Note": "Priorite a la progressivite : technique propre, deplacements, et developpement aerobie. Eviter la surcharge lactique, privilegier des formats ludiques et courts.",
        }
    if age <= 34:
        return {
            "Titre": "Specificite 20-34 ans",
            "Note": "Fenetre ideale pour developper la VMA et la tolerance a l'intensite. Monter progressivement la densite (intermittent, circuits specifiques assaut).",
        }
    if age <= 44:
        return {
            "Titre": "Specificite 35-44 ans",
            "Note": "Accent sur la recuperation et la regularite. Maintenir la VMA via intermittents courts, et renforcer l'economie de course/deplacements.",
        }
    return {
        "Titre": "Specificite 45-60 ans",
        "Note": "Priorite : prevention (tendons, mollets, ischios), echauffement long, montee en charge progressive. Intermittent court maitrise, et endurance fondamentale reguliere.",
    }


def suggested_work(level: str) -> List[Dict[str, str]]:
    base = [
        {"Code": "EF", "Application": "Endurance fondamentale", "Detail": "20-45 min en aisance respiratoire, 1-2x/sem."},
        {"Code": "TECH", "Application": "Technique basse intensite", "Detail": "Rounds techniques (shadow, cibles) sans fatigue excessive."},
    ]
    vma_short = [
        {"Code": "30/30", "Application": "Intermittent 30/30", "Detail": "2x(6-10 repetitions) a intensite elevee, recup 3-4 min entre blocs."},
        {"Code": "15/15", "Application": "Intermittent 15/15", "Detail": "2x(10-20 repetitions), focalise relance/deplacements."},
    ]
    specific = [
        {"Code": "ASSAUT", "Application": "Intermittent specifique assaut", "Detail": "Ex: 6x(1 min assaut actif / 1 min leger) + consignes tactiques."},
        {"Code": "DEPL", "Application": "Deplacements", "Detail": "Ateliers d'appuis: avant/arriere, lateral, pivots, 2-3 blocs de 4 min."},
        {"Code": "REL", "Application": "Relances", "Detail": "Series courtes: 10-15 s explosif / 45-50 s recup, 8-12 reps."},
    ]
    recovery = [{"Code": "REC", "Application": "Recuperation", "Detail": "Marche, mobilite, sommeil, hydratation, 1-2 jours faciles/sem."}]

    if level == "Faible":
        return base + [vma_short[0]] + recovery
    if level in ("Moyen-", "Moyen"):
        return base + vma_short + [specific[1]] + recovery
    if level == "Moyen+":
        return base + vma_short + specific + recovery
    if level == "Bon":
        return base + vma_short + specific + recovery
    if level in ("Tres bon", "Excellent"):
        return specific + [{"Code": "LACT", "Application": "Lactique court", "Detail": "4-6x(30-45 s dur / 2-3 min recup) en controle."}] + recovery
    if level in ("Elite", "Elite+"):
        return specific + [{"Code": "QUAL", "Application": "Qualite > volume", "Detail": "Seances courtes, intensite ciblee, forte exigence de recuperation."}] + recovery
    return []


@dataclass
class Athlete:
    id: str
    prenom: str
    age: int
    sexe: str  # "M" | "F"
    palier: int


st.set_page_config(page_title="Dashboard Luc Leger - CBF", layout="wide")

st.markdown(
    """
<style>
.kpi { padding: 14px; border-radius: 14px; border: 1px solid #e5e7eb; background: white; }
.level-pill { display:inline-block; padding: 4px 10px; border-radius:999px; border:1px solid #e5e7eb; font-size: 12px; font-weight:600; }
.header { padding: 16px; border-radius: 18px; color: white;
  background: linear-gradient(90deg, #dc2626 0%, #2563eb 50%, #0f172a 100%); }
.small { color: rgba(255,255,255,0.9); }
</style>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
<div class="header">
  <div style="display:flex; align-items:center; gap:14px;">
    <div>
      <div style="font-size:26px; font-weight:700;">Tableau de bord - Test Luc Leger</div>
      <div class="small" style="margin-top:4px;">Saisie des resultats, niveau automatique, interpretation assaut, specificite age et applications pour les tireurs.</div>
    </div>
  </div>
</div>
""",
    unsafe_allow_html=True,
)

if "athletes" not in st.session_state:
    st.session_state.athletes: List[Athlete] = []

df = pd.DataFrame([asdict(a) for a in st.session_state.athletes]) if st.session_state.athletes else pd.DataFrame(columns=["id", "prenom", "age", "sexe", "palier"])
total = len(df)
m = int((df["sexe"] == "M").sum()) if total else 0
f = int((df["sexe"] == "F").sum()) if total else 0
avg_palier = float(df["palier"].mean()) if total else None

k1, k2, k3, k4 = st.columns(4)
k1.markdown(f"<div class='kpi'><div style='color:#64748b;'>Participants</div><div style='font-size:26px;font-weight:700;'>{total}</div></div>", unsafe_allow_html=True)
k2.markdown(f"<div class='kpi'><div style='color:#64748b;'>Masculin</div><div style='font-size:26px;font-weight:700;'>{m}</div></div>", unsafe_allow_html=True)
k3.markdown(f"<div class='kpi'><div style='color:#64748b;'>Feminin</div><div style='font-size:26px;font-weight:700;'>{f}</div></div>", unsafe_allow_html=True)
k4.markdown(
    f"<div class='kpi'><div style='color:#64748b;'>Palier moyen</div><div style='font-size:26px;font-weight:700;'>{avg_palier:.1f if avg_palier is not None else '—'}</div></div>",
    unsafe_allow_html=True,
)

st.write("")

left, right = st.columns([1, 2], gap="large")

with left:
    st.subheader("Saisie d'un resultat")

    prenom = st.text_input("Prenom", placeholder="Ex: Lina")
    age = st.number_input("Age", min_value=15, max_value=60, value=15, step=1)
    sexe = st.selectbox("Sexe", options=["M", "F"], format_func=lambda x: "Masculin" if x == "M" else "Feminin")
    palier = st.number_input("Palier atteint", min_value=7, max_value=15, value=7, step=1)

    if st.button("Ajouter", use_container_width=True, type="primary"):
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
            st.success("Ajoute.")
        else:
            st.error("Le prenom est requis.")

    st.divider()
    st.caption("Le niveau est calcule via un bareme club (pedagogique). Outil d'aide a la decision pour l'entrainement en Savate.")

with right:
    st.subheader("Liste des tireurs")
    query = st.text_input("Recherche", placeholder="Filtrer: prenom, age, sexe, palier...")

    if total:
        view = df.copy()
        if query.strip():
            q = query.strip().lower()
            mask = (
                view["prenom"].str.lower().str.contains(q)
                | view["age"].astype(str).str.contains(q)
                | view["sexe"].astype(str).str.lower().str.contains(q)
                | view["palier"].astype(str).str.contains(q)
            )
            view = view[mask]

        view["niveau"] = view.apply(lambda r: level_for(r["sexe"], int(r["age"]), int(r["palier"])), axis=1)
        view_display = view[["prenom", "age", "sexe", "palier", "niveau"]].rename(
            columns={"prenom": "Prenom", "age": "Age", "sexe": "Sexe", "palier": "Palier", "niveau": "Niveau"}
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

        st.divider()

        if len(view) > 0:
            selected_row = view.iloc[0]
            sel_prenom = str(selected_row["prenom"])
            sel_age = int(selected_row["age"])
            sel_sexe = str(selected_row["sexe"])
            sel_palier = int(selected_row["palier"])

            lvl = level_for(sel_sexe, sel_age, sel_palier)
            band = age_band(sel_age)

            color = LEVEL_COLORS.get(lvl, "#e5e7eb")
            st.markdown(
                f"""
<div style="display:flex; flex-wrap:wrap; gap:8px; align-items:center;">
  <span class="level-pill" style="background:#f1f5f9;">{sel_prenom}</span>
  <span class="level-pill" style="background:#f1f5f9;">{sel_age} ans</span>
  <span class="level-pill" style="background:#f1f5f9;">Tranche {band}</span>
  <span class="level-pill" style="background:#f1f5f9;">Sexe {'Masculin' if sel_sexe=='M' else 'Feminin'}</span>
  <span class="level-pill" style="background:#f1f5f9;">Palier {sel_palier}</span>
  <span class="level-pill" style="background:{color}; margin-left:auto;">Niveau: {lvl}</span>
</div>
""",
                unsafe_allow_html=True,
            )

            tab1, tab2, tab3 = st.tabs(["Interpretation assaut", "Specificite age", "Applications (tireur)"])

            with tab1:
                info = interpret_for_assaut(lvl)
                c1, c2, c3 = st.columns(3)
                c1.metric("Synthese", "")
                c1.write(info["Synthese"])
                c2.metric("Point de vigilance", "")
                c2.write(info["Point de vigilance"])
                c3.metric("Priorite de travail", "")
                c3.write(info["Priorite de travail"])

            with tab2:
                note = age_specific_notes(sel_age)
                st.write(f"**{note['Titre']}**")
                st.write(note["Note"])

            with tab3:
                work = suggested_work(lvl)
                if not work:
                    st.info("Aucune recommandation disponible.")
                else:
                    wdf = pd.DataFrame(work)
                    st.dataframe(wdf, use_container_width=True, hide_index=True)

            st.divider()
            st.caption("Astuce: pour selectionner un tireur precisement, remplace la selection automatique par une liste deroulante sur l'ID ou le prenom.")
    else:
        st.info("Ajoute au moins un tireur pour afficher la liste et l'analyse.")
