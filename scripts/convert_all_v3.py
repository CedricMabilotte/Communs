#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Conversion EN MASSE grille -> evaluation v3.1, notes reprises de la grille sourcee.
Porte corrigee : un pret/des parts au nominal n'abaissent pas la porte (-> cran), seul
un maillon lucratif/commercial ou un foncier non sorti la degrade. Dry-run par defaut."""
import yaml, glob, collections, sys

S={"oui":1.0,"partiel":0.5,"non":0.0}
QMAP={"milieu":["milieu_protege","usage_non_degradant"],
      "vivant":["vivant_finalite","place_au_vivant"],
      "ouverture":["usage_interet_general","ancrage_territorial"],
      "don":["usage_non_marchand","loyer_non_rentier","travail_non_marchandise"],
      "duree":["securite_jouissance"],
      "voix":["gouvernance_collective","perennite_gouvernance"]}
MAILLON={"milieu":"lieu","vivant":"lieu","ouverture":"chaine","don":"chaine","duree":"usage","voix":"usage"}

def lab(x): return "non_etabli" if x is None else ("oui" if x==1 else ("non" if x==0 else "partiel"))

def weakest(crits, G):
    """valeur (weakest-link sur connus) + note du critere determinant."""
    known=[(S[G[c]["v"]],c) for c in crits if c in G and G[c]["v"] in S]
    if not known:
        # tout inconnu -> note du 1er critere present
        for c in crits:
            if c in G: return None, G[c]["note"]
        return None,""
    known.sort()
    val,c=known[0]
    return val, G[c]["note"]

def build_eval(grille):
    G={e["critere"]:{"v":e.get("valeur"),"note":(e.get("note") or "").strip()} for e in (grille or [])}
    def v(c): return G.get(c,{}).get("v")
    # PORTE corrigee
    if v("foncier_hors_marche")=="non":
        porte="non"
    elif v("non_lucratif_global")=="non" or v("montage_non_commercial")=="non" or v("foncier_hors_marche")=="partiel":
        porte="partiel"
    else:
        porte="oui"
    cran="pour_toujours" if v("irreversibilite")=="oui" else "a_terme"
    pnote=G.get("foncier_hors_marche",{}).get("note","")
    questions={}
    for q,crits in QMAP.items():
        if q=="voix":
            # gouvernance gate ; perennite faible tempere d'un demi-cran ; jamais bloque par tripartisme
            gov=S.get(v("gouvernance_collective")); per=S.get(v("perennite_gouvernance"))
            if gov is None: val=None
            elif per==0.0: val=min(gov,0.5)   # pérennité absente -> tempère ; partielle -> n'abaisse pas
            else: val=gov
            note=G.get("gouvernance_collective",{}).get("note","")
        elif q=="ouverture":
            val=S.get(v("usage_interet_general")); note=G.get("usage_interet_general",{}).get("note","")
        else:
            val,note=weakest(crits,G)
        d={"valeur":lab(val),"maillon":MAILLON[q],"note":note}
        if q in ("duree","voix"): d["decisive"]=True
        questions[q]=d
    return {"porte":{"valeur":porte,"cran":cran,"voie":"nature_porteur","note":pnote},"questions":questions}

# derive (identique au generateur)
UNK={"non_etabli","projete"}; BANDS={"marchand":(0,20),"en_transition":(20,40),"sorti_du_marche":(20,50),"autogere":(50,75),"usage_decommodifie":(75,90),"commun_vivant":(90,100)}
def derive(ev):
    p=ev["porte"]["valeur"]; q=ev["questions"]; v=lambda n:q[n]["valeur"]; sc=lambda n:S.get(v(n))
    susp=(p=="non_etabli") or any(v(n)=="non_etabli" for n in("voix","duree"))
    if p=="non": b="marchand"
    elif p=="partiel": b="en_transition"
    elif susp: b="sorti_du_marche"
    elif sc("voix")==1 and sc("duree")==1: b="usage_decommodifie" if sc("don")==1 else "autogere"
    else: b="sorti_du_marche"
    mil,viv=v("milieu"),v("vivant")
    badge="non_etabli" if(mil in UNK or viv in UNK) else (2 if S[mil]==1 and S[viv]==1 else(1 if S[mil]+S[viv]>=1 else 0))
    if b=="usage_decommodifie" and isinstance(badge,int) and badge>=1: b="commun_vivant"
    return b,susp,badge

write = "--write" in sys.argv
dist=collections.Counter(); susp_n=0; written=0
for f in sorted(glob.glob("lieux/*.yml")):
    d=yaml.safe_load(open(f))
    ev=build_eval(d.get("grille"))
    b,susp,badge=derive(ev); dist[b]+=1; susp_n+=1 if susp else 0
    if write and not d.get("v3_revue_sources"):  # ne pas ecraser une revue sources manuelle
        s=open(f,encoding="utf-8").read()
        # retirer un ancien bloc v3 auto s'il existe, puis re-append
        import re
        s=re.sub(r"\n# --- Évaluation v3\.1.*$","",s,flags=re.S)
        if not s.endswith("\n"): s+="\n"
        block="\n# --- Évaluation v3.1 (faisceau libéré) — convertie de la grille sourcée, 2026-06-05 ---\nv3_revue: true\n"+yaml.safe_dump({"evaluation":ev},allow_unicode=True,sort_keys=False)
        open(f,"w",encoding="utf-8").write(s+block); written+=1
print(f"distribution: {dict(dist)}  | suspendus: {susp_n}/52  | ecrits: {written}")
