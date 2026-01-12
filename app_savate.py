# -*- coding: utf-8 -*-
# app_savate.py
# Dashboard Luc Leger (club) - Streamlit
# Saisie: prenom, age, sexe, palier | Sortie: niveau (5), interpretation assaut, specificite age, applications
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
        "20-24": {7: "Moyen", 8: "Bon", 9: "Tres bon", 10: "Excellent", 11: "Elite", 12: "
