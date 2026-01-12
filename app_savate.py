import React, { useMemo, useState } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Search, Plus, Trash2, Download, Info } from "lucide-react";

// Barème club (outil pédagogique) – paliers 7 à 15, tranches 5 ans, 15 à 60.
const AGE_BANDS = [
  { key: "15-19", label: "15–19" },
  { key: "20-24", label: "20–24" },
  { key: "25-29", label: "25–29" },
  { key: "30-34", label: "30–34" },
  { key: "35-39", label: "35–39" },
  { key: "40-44", label: "40–44" },
  { key: "45-49", label: "45–49" },
  { key: "50-54", label: "50–54" },
  { key: "55-60", label: "55–60" },
];

const PALIER_RANGE = Array.from({ length: 9 }, (_, i) => 7 + i); // 7..15

type Sex = "M" | "F";

const SCALE_COLORS: Record<string, string> = {
  Faible: "bg-red-100 text-red-900 border-red-200",
  "Moyen-": "bg-orange-100 text-orange-900 border-orange-200",
  Moyen: "bg-amber-100 text-amber-900 border-amber-200",
  "Moyen+": "bg-yellow-100 text-yellow-900 border-yellow-200",
  Bon: "bg-green-100 text-green-900 border-green-200",
  "Très bon": "bg-emerald-100 text-emerald-900 border-emerald-200",
  Excellent: "bg-teal-100 text-teal-900 border-teal-200",
  Elite: "bg-sky-100 text-sky-900 border-sky-200",
  "Elite+": "bg-indigo-100 text-indigo-900 border-indigo-200",
};

const BAREME: Record<Sex, Record<string, Record<number, string>>> = {
  M: {
    "15-19": { 7: "Faible", 8: "Moyen-", 9: "Moyen", 10: "Moyen+", 11: "Bon", 12: "Très bon", 13: "Excellent", 14: "Elite", 15: "Elite+" },
    "20-24": { 7: "Faible", 8: "Moyen-", 9: "Moyen", 10: "Bon", 11: "Très bon", 12: "Excellent", 13: "Elite", 14: "Elite+", 15: "Elite+" },
    "25-29": { 7: "Faible", 8: "Moyen", 9: "Moyen+", 10: "Bon", 11: "Très bon", 12: "Excellent", 13: "Elite", 14: "Elite+", 15: "Elite+" },
    "30-34": { 7: "Faible", 8: "Moyen", 9: "Bon", 10: "Très bon", 11: "Excellent", 12: "Elite", 13: "Elite+", 14: "Elite+", 15: "Elite+" },
    "35-39": { 7: "Faible", 8: "Moyen+", 9: "Bon", 10: "Très bon", 11: "Excellent", 12: "Elite", 13: "Elite+", 14: "Elite+", 15: "Elite+" },
    "40-44": { 7: "Moyen-", 8: "Moyen+", 9: "Bon", 10: "Très bon", 11: "Excellent", 12: "Elite", 13: "Elite+", 14: "Elite+", 15: "Elite+" },
    "45-49": { 7: "Moyen", 8: "Bon", 9: "Très bon", 10: "Excellent", 11: "Elite", 12: "Elite+", 13: "Elite+", 14: "Elite+", 15: "Elite+" },
    "50-54": { 7: "Moyen", 8: "Bon", 9: "Très bon", 10: "Excellent", 11: "Elite", 12: "Elite+", 13: "Elite+", 14: "Elite+", 15: "Elite+" },
    "55-60": { 7: "Moyen", 8: "Bon", 9: "Très bon", 10: "Excellent", 11: "Elite", 12: "Elite+", 13: "Elite+", 14: "Elite+", 15: "Elite+" },
  },
  F: {
    "15-19": { 7: "Moyen-", 8: "Moyen", 9: "Bon", 10: "Très bon", 11: "Excellent", 12: "Elite", 13: "Elite+", 14: "Elite+", 15: "Elite+" },
    "20-24": { 7: "Moyen", 8: "Bon", 9: "Très bon", 10: "Excellent", 11: "Elite", 12: "Elite+", 13: "Elite+", 14: "Elite+", 15: "Elite+" },
    "25-29": { 7: "Moyen", 8: "Bon", 9: "Très bon", 10: "Excellent", 11: "Elite", 12: "Elite+", 13: "Elite+", 14: "Elite+", 15: "Elite+" },
    "30-34": { 7: "Moyen+", 8: "Bon", 9: "Très bon", 10: "Excellent", 11: "Elite", 12: "Elite+", 13: "Elite+", 14: "Elite+", 15: "Elite+" },
    "35-39": { 7: "Bon", 8: "Très bon", 9: "Excellent", 10: "Elite", 11: "Elite+", 12: "Elite+", 13: "Elite+", 14: "Elite+", 15: "Elite+" },
    "40-44": { 7: "Bon", 8: "Très bon", 9: "Excellent", 10: "Elite", 11: "Elite+", 12: "Elite+", 13: "Elite+", 14: "Elite+", 15: "Elite+" },
    "45-49": { 7: "Bon", 8: "Très bon", 9: "Excellent", 10: "Elite", 11: "Elite+", 12: "Elite+", 13: "Elite+", 14: "Elite+", 15: "Elite+" },
    "50-54": { 7: "Bon", 8: "Très bon", 9: "Excellent", 10: "Elite", 11: "Elite+", 12: "Elite+", 13: "Elite+", 14: "Elite+", 15: "Elite+" },
    "55-60": { 7: "Bon", 8: "Très bon", 9: "Excellent", 10: "Elite", 11: "Elite+", 12: "Elite+", 13: "Elite+", 14: "Elite+", 15: "Elite+" },
  },
};

function clamp(n: number, min: number, max: number) {
  return Math.max(min, Math.min(max, n));
}

function getAgeBand(age: number) {
  const a = clamp(age, 15, 60);
  const start = Math.floor((a - 15) / 5) * 5 + 15;
  const end = start + 4;
  return `${start}-${end}`;
}

function levelFor(sex: Sex, age: number, palier: number) {
  const band = getAgeBand(age);
  const p = clamp(palier, 7, 15);
  return BAREME[sex]?.[band]?.[p] ?? "—";
}

// Interprétation club pour l'assaut (Savate) – guidance opérationnelle
function interpretForAssaut(level: string) {
  // Intention : orienter le coach, pas médical.
  switch (level) {
    case "Faible":
      return {
        verdict: "Endurance insuffisante pour soutenir plusieurs reprises à intensité assaut.",
        risk: "Risque de chute de lucidité (distance / garde) dès la 1re–2e reprise.",
        focus: "Construire une base aérobie + maîtrise technique à faible intensité.",
      };
    case "Moyen-":
    case "Moyen":
      return {
        verdict: "Base cardio correcte pour entraînement, limite pour assauts enchaînés.",
        risk: "Dégradation en fin de reprise, baisse de fréquence de déplacements.",
        focus: "Développer VMA/intermittent et tolérance à l'effort.",
      };
    case "Moyen+":
      return {
        verdict: "Profil exploitable en assaut club, à condition d'une gestion du rythme.",
        risk: "Peut subir les accélérations adverses (changements de rythme).",
        focus: "Intermittent court + travail de relance + stratégie d'économie.",
      };
    case "Bon":
      return {
        verdict: "Bon niveau pour assaut : capacité à tenir le volume et relancer.",
        risk: "Principal risque : surcharge si la récup est négligée.",
        focus: "Spécifique savate (intermittent + déplacements + enchaînements).",
      };
    case "Très bon":
    case "Excellent":
      return {
        verdict: "Très bon moteur : enchaînement de reprises, relances fréquentes possibles.",
        risk: "Risque : partir trop vite (sur-régime) plutôt que limite cardio.",
        focus: "Affûtage, qualité des relances, lactique court, gestion tactique.",
      };
    case "Elite":
    case "Elite+":
      return {
        verdict: "Très haut niveau cardio : gros potentiel de pression et répétition d'efforts.",
        risk: "Risque : blessure/surcharge si volumes mal pilotés.",
        focus: "Spécificité assaut (vitesse, lucidité, relances), récupération premium.",
      };
    default:
      return {
        verdict: "Niveau non déterminé.",
        risk: "—",
        focus: "—",
      };
  }
}

function ageSpecificNotes(age: number) {
  if (age <= 19) {
    return {
      title: "Spécificité 15–19 ans",
      note:
        "Priorité à la progressivité : technique propre, déplacements, et développement aérobie. Éviter la surcharge lactique, privilégier des formats ludiques et courts.",
    };
  }
  if (age <= 34) {
    return {
      title: "Spécificité 20–34 ans",
      note:
        "Fenêtre idéale pour développer la VMA et la tolérance à l'intensité. Monter progressivement la densité (intermittent, circuits spécifiques assaut).",
    };
  }
  if (age <= 44) {
    return {
      title: "Spécificité 35–44 ans",
      note:
        "Accent sur la récupération et la régularité. Maintenir la VMA via intermittents courts, et renforcer l'économie de course/déplacements.",
    };
  }
  return {
    title: "Spécificité 45–60 ans",
    note:
      "Priorité : prévention (tendons, mollets, ischios), échauffement long, montée en charge progressive. Intermittent court maîtrisé, et endurance fondamentale régulière.",
  };
}

function suggestedWork(level: string, age: number) {
  // Propositions d'applications (exercices) pour les tireurs
  const base = [
    { k: "EF", t: "Endurance fondamentale", d: "20–45 min en aisance respiratoire, 1–2×/sem." },
    { k: "TECH", t: "Technique basse intensité", d: "Rounds techniques (shadow, cibles) sans fatigue excessive." },
  ];

  const vmaShort = [
    { k: "30/30", t: "Intermittent 30/30", d: "2×(6–10 répétitions) à intensité élevée, récup 3–4 min entre blocs." },
    { k: "15/15", t: "Intermittent 15/15", d: "2×(10–20 répétitions), focalisé relance/déplacements." },
  ];

  const specific = [
    { k: "ASSAUT", t: "Intermittent spécifique assaut", d: "Ex: 6×(1 min assaut actif / 1 min léger) + consignes tactiques." },
    { k: "DEPL", t: "Déplacements", d: "Ateliers d'appuis: avant/arrière, latéral, pivots, 2–3 blocs de 4 min." },
    { k: "REL", t: "Relances", d: "Séries courtes: 10–15 s explosif / 45–50 s récup, 8–12 reps." },
  ];

  const recovery = [
    { k: "REC", t: "Récupération", d: "Marche, mobilité, sommeil, hydratation, 1–2 jours faciles/sem." },
  ];

  if (level === "Faible") return [...base, vmaShort[0], recovery[0]];
  if (level === "Moyen-" || level === "Moyen") return [...base, ...vmaShort, specific[1], recovery[0]];
  if (level === "Moyen+") return [...base, ...vmaShort, ...specific, recovery[0]];
  if (level === "Bon") return [...base, ...vmaShort, ...specific, recovery[0]];
  if (level === "Très bon" || level === "Excellent") return [...specific, { k: "LACT", t: "Lactique court", d: "4–6×(30–45 s dur / 2–3 min récup) en contrôle." }, recovery[0]];
  if (level === "Elite" || level === "Elite+") return [...specific, { k: "QUAL", t: "Qualité > volume", d: "Séances courtes, intensité ciblée, forte exigence de récupération." }, recovery[0]];
  return [];
}

type Athlete = {
  id: string;
  prenom: string;
  age: number;
  sex: Sex;
  palier: number;
};

function uid() {
  return Math.random().toString(16).slice(2) + Date.now().toString(16);
}

function toCSV(rows: Athlete[]) {
  const header = ["prenom", "age", "sexe", "palier"].join(",");
  const lines = rows.map((r) => [r.prenom, r.age, r.sex, r.palier].join(","));
  return [header, ...lines].join("\n");
}

export default function DashboardLucLeger() {
  const [prenom, setPrenom] = useState("");
  const [age, setAge] = useState<string>("");
  const [sex, setSex] = useState<Sex>("M");
  const [palier, setPalier] = useState<string>("");
  const [items, setItems] = useState<Athlete[]>([]);
  const [query, setQuery] = useState("");

  const canAdd = useMemo(() => {
    const a = Number(age);
    const p = Number(palier);
    return prenom.trim().length > 0 && Number.isFinite(a) && Number.isFinite(p);
  }, [prenom, age, palier]);

  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase();
    if (!q) return items;
    return items.filter((x) =>
      [x.prenom, String(x.age), x.sex, String(x.palier)].some((v) =>
        String(v).toLowerCase().includes(q)
      )
    );
  }, [items, query]);

  const selected = filtered[0];

  function add() {
    if (!canAdd) return;
    const a = clamp(Number(age), 15, 60);
    const p = clamp(Number(palier), 7, 15);
    setItems((prev) => [
      { id: uid(), prenom: prenom.trim(), age: a, sex, palier: p },
      ...prev,
    ]);
    setPrenom("");
    setAge("");
    setPalier("");
  }

  function remove(id: string) {
    setItems((prev) => prev.filter((x) => x.id !== id));
  }

  function exportCSV() {
    const blob = new Blob([toCSV(items)], { type: "text/csv;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `luc-leger_cbfmontmorency_${new Date().toISOString().slice(0, 10)}.csv`;
    a.click();
    URL.revokeObjectURL(url);
  }

  const insights = useMemo(() => {
    if (!selected) return null;
    const band = getAgeBand(selected.age);
    const lvl = levelFor(selected.sex, selected.age, selected.palier);
    const assaut = interpretForAssaut(lvl);
    const ageNote = ageSpecificNotes(selected.age);
    const work = suggestedWork(lvl, selected.age);
    return { band, lvl, assaut, ageNote, work };
  }, [selected]);

  const kpis = useMemo(() => {
    const total = items.length;
    const m = items.filter((x) => x.sex === "M").length;
    const f = items.filter((x) => x.sex === "F").length;
    const avgPalier = total
      ? (items.reduce((s, x) => s + x.palier, 0) / total).toFixed(1)
      : "—";
    return { total, m, f, avgPalier };
  }, [items]);

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-50 to-white p-6">
      <div className="mx-auto max-w-6xl space-y-6">
        <header className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between bg-gradient-to-r from-red-600 via-blue-600 to-slate-900 text-white rounded-2xl p-5">
          <div className="flex items-center gap-4">
            <img
              src="/Logo Rond.png"
              alt="Logo CBF Montmorency"
              className="h-16 w-16 rounded-full bg-white p-1"
            />
            <div>
              <h1 className="text-2xl md:text-3xl font-semibold tracking-tight">Tableau de bord – Test Luc Léger</h1>
              <p className="text-sm text-white/90 mt-1">
                Saisie des résultats, niveau automatique, interprétation assaut et recommandations d'entraînement.
              </p>
            </div>
          </div>
          <div className="flex gap-2">
            <Button variant="outline" onClick={exportCSV} disabled={!items.length}>
              <Download className="h-4 w-4 mr-2" /> Export CSV
            </Button>
          </div>
        </header>

        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <Card className="rounded-2xl shadow-sm border-t-4 border-blue-600">
            <CardContent className="p-4">
              <div className="text-sm text-slate-600">Participants</div>
              <div className="text-2xl font-semibold mt-1">{kpis.total}</div>
            </CardContent>
          </Card>
          <Card className="rounded-2xl shadow-sm border-t-4 border-blue-600">
            <CardContent className="p-4">
              <div className="text-sm text-slate-600">Masculin</div>
              <div className="text-2xl font-semibold mt-1">{kpis.m}</div>
            </CardContent>
          </Card>
          <Card className="rounded-2xl shadow-sm border-t-4 border-blue-600">
            <CardContent className="p-4">
              <div className="text-sm text-slate-600">Féminin</div>
              <div className="text-2xl font-semibold mt-1">{kpis.f}</div>
            </CardContent>
          </Card>
          <Card className="rounded-2xl shadow-sm border-t-4 border-blue-600">
            <CardContent className="p-4">
              <div className="text-sm text-slate-600">Palier moyen</div>
              <div className="text-2xl font-semibold mt-1">{kpis.avgPalier}</div>
            </CardContent>
          </Card>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <Card className="rounded-2xl shadow-sm lg:col-span-1 border-t-4 border-red-600">
            <CardContent className="p-5 space-y-4">
              <div className="flex items-center gap-2">
                <Plus className="h-4 w-4" />
                <h2 className="font-semibold">Saisie d'un résultat</h2>
              </div>

              <div className="space-y-2">
                <Label>Prénom</Label>
                <Input value={prenom} onChange={(e) => setPrenom(e.target.value)} placeholder="Ex: Lina" />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div className="space-y-2">
                  <Label>Âge</Label>
                  <Input
                    value={age}
                    onChange={(e) => setAge(e.target.value.replace(/[^0-9]/g, ""))}
                    placeholder="15–60"
                  />
                </div>
                <div className="space-y-2">
                  <Label>Palier atteint</Label>
                  <Input
                    value={palier}
                    onChange={(e) => setPalier(e.target.value.replace(/[^0-9]/g, ""))}
                    placeholder="7–15"
                  />
                </div>
              </div>

              <div className="space-y-2">
                <Label>Sexe</Label>
                <Select value={sex} onValueChange={(v) => setSex(v as Sex)}>
                  <SelectTrigger>
                    <SelectValue placeholder="Sélectionner" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="M">Masculin</SelectItem>
                    <SelectItem value="F">Féminin</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <Button className="w-full" onClick={add} disabled={!canAdd}>
                Ajouter
              </Button>

              <Separator />

              <div className="flex items-center gap-2">
                <Search className="h-4 w-4" />
                <Label>Recherche</Label>
              </div>
              <Input value={query} onChange={(e) => setQuery(e.target.value)} placeholder="Filtrer: prénom, âge, sexe, palier…" />

              <div className="text-xs text-slate-600 flex items-start gap-2">
                <Info className="h-4 w-4 mt-0.5" />
                <p>
                  Le niveau est calculé via un barème club (pédagogique). Utilisez-le pour orienter le travail, pas comme un diagnostic.
                </p>
              </div>
            </CardContent>
          </Card>

          <Card className="rounded-2xl shadow-sm lg:col-span-2 border-t-4 border-slate-800">
            <CardContent className="p-5">
              <div className="flex items-center justify-between gap-4">
                <h2 className="font-semibold">Liste des tireurs</h2>
                <div className="text-sm text-slate-600">Clique sur un tireur (la 1ère ligne affichée est analysée ci-dessous).</div>
              </div>

              <div className="mt-4 overflow-auto border rounded-xl">
                <table className="w-full text-sm">
                  <thead className="bg-slate-50">
                    <tr>
                      <th className="text-left p-3">Prénom</th>
                      <th className="text-left p-3">Âge</th>
                      <th className="text-left p-3">Sexe</th>
                      <th className="text-left p-3">Palier</th>
                      <th className="text-left p-3">Niveau</th>
                      <th className="p-3"></th>
                    </tr>
                  </thead>
                  <tbody>
                    {filtered.map((x) => {
                      const lvl = levelFor(x.sex, x.age, x.palier);
                      return (
                        <tr key={x.id} className="border-t hover:bg-slate-50">
                          <td className="p-3 font-medium">{x.prenom}</td>
                          <td className="p-3">{x.age}</td>
                          <td className="p-3">{x.sex === "M" ? "M" : "F"}</td>
                          <td className="p-3">{x.palier}</td>
                          <td className="p-3">
                            <span className={`inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs ${SCALE_COLORS[lvl] ?? "bg-slate-100 text-slate-900 border-slate-200"}`}>
                              {lvl}
                            </span>
                          </td>
                          <td className="p-3 text-right">
                            <Button variant="ghost" size="icon" onClick={() => remove(x.id)} aria-label="Supprimer">
                              <Trash2 className="h-4 w-4" />
                            </Button>
                          </td>
                        </tr>
                      );
                    })}
                    {!filtered.length && (
                      <tr>
                        <td colSpan={6} className="p-6 text-center text-slate-600">
                          Aucun enregistrement.
                        </td>
                      </tr>
                    )}
                  </tbody>
                </table>
              </div>

              <Separator className="my-6" />

              <h2 className="font-semibold">Analyse (tireur sélectionné)</h2>
              {!selected ? (
                <p className="text-sm text-slate-600 mt-2">Ajoute un tireur pour afficher l'analyse.</p>
              ) : (
                <div className="mt-4">
                  <div className="flex flex-wrap items-center gap-2">
                    <Badge variant="secondary">{selected.prenom}</Badge>
                    <Badge variant="outline">{selected.age} ans</Badge>
                    <Badge variant="outline">Tranche {insights?.band.replace("-", "–")}</Badge>
                    <Badge variant="outline">Sexe {selected.sex === "M" ? "Masculin" : "Féminin"}</Badge>
                    <Badge variant="outline">Palier {selected.palier}</Badge>
                    <span className={`ml-auto inline-flex items-center rounded-full border px-3 py-1 text-sm ${SCALE_COLORS[insights?.lvl ?? ""] ?? "bg-slate-100 text-slate-900 border-slate-200"}`}>
                      Niveau: {insights?.lvl}
                    </span>
                  </div>

                  <Tabs defaultValue="assaut" className="mt-5">
                    <TabsList className="bg-slate-100 rounded-xl p-1">
                      <TabsTrigger value="assaut" className="data-[state=active]:bg-red-600 data-[state=active]:text-white">Interprétation assaut</TabsTrigger>
                      <TabsTrigger value="age" className="data-[state=active]:bg-blue-600 data-[state=active]:text-white">Spécificité âge</TabsTrigger>
                      <TabsTrigger value="work" className="data-[state=active]:bg-slate-800 data-[state=active]:text-white">Applications (tireur)</TabsTrigger>
                    </TabsList>

                    <TabsContent value="assaut" className="mt-4">
                      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                        <Card className="rounded-2xl shadow-sm border-t-4 border-blue-600">
                          <CardContent className="p-4">
                            <div className="text-sm text-slate-600">Synthèse</div>
                            <div className="mt-2 font-medium">{insights?.assaut.verdict}</div>
                          </CardContent>
                        </Card>
                        <Card className="rounded-2xl shadow-sm border-t-4 border-blue-600">
                          <CardContent className="p-4">
                            <div className="text-sm text-slate-600">Point de vigilance</div>
                            <div className="mt-2 font-medium">{insights?.assaut.risk}</div>
                          </CardContent>
                        </Card>
                        <Card className="rounded-2xl shadow-sm border-t-4 border-blue-600">
                          <CardContent className="p-4">
                            <div className="text-sm text-slate-600">Priorité de travail</div>
                            <div className="mt-2 font-medium">{insights?.assaut.focus}</div>
                          </CardContent>
                        </Card>
                      </div>
                    </TabsContent>

                    <TabsContent value="age" className="mt-4">
                      <Card className="rounded-2xl shadow-sm border-t-4 border-blue-600">
                        <CardContent className="p-5">
                          <div className="text-sm text-slate-600">{insights?.ageNote.title}</div>
                          <div className="mt-2 font-medium">{insights?.ageNote.note}</div>
                        </CardContent>
                      </Card>
                    </TabsContent>

                    <TabsContent value="work" className="mt-4">
                      <Card className="rounded-2xl shadow-sm border-t-4 border-blue-600">
                        <CardContent className="p-5">
                          <div className="text-sm text-slate-600">Applications à fournir au tireur</div>
                          <div className="mt-3 grid grid-cols-1 md:grid-cols-2 gap-3">
                            {insights?.work.map((w) => (
                              <div key={w.k} className="border rounded-xl p-4">
                                <div className="font-medium">{w.t}</div>
                                <div className="text-sm text-slate-600 mt-1">{w.d}</div>
                              </div>
                            ))}
                          </div>
                          <div className="text-xs text-slate-500 mt-4">
                            Conseil: adapter les volumes selon la charge globale (savate + muscu + fatigue) et privilégier la régularité.
                          </div>
                        </CardContent>
                      </Card>
                    </TabsContent>
                  </Tabs>
                </div>
              )}
            </CardContent>
          </Card>
        </div>

        <footer className="text-xs text-slate-500 pt-4 border-t mt-4">
          Barème club – Luc Léger (15–60 ans, paliers 7–15). Outil d'aide à la décision pour l'entraînement en Savate.
        </footer>
      </div>
    </div>
  );
}
