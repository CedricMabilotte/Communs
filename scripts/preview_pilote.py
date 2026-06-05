#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Aperçu HTML autonome du PILOTE v3.1 (3 fiches revues sur sources + méthode). Rien de publié."""
import html
S={"oui":1.0,"partiel":0.5,"non":0.0}; UNK={"non_etabli","projete"}
BANDS={"marchand":(0,20),"en_transition":(20,40),"sorti_du_marche":(20,50),"autogere":(50,75),"usage_decommodifie":(75,90),"commun_vivant":(90,100)}
LBL={"marchand":"marchand","en_transition":"en transition","sorti_du_marche":"sorti du marché","autogere":"autogéré","usage_decommodifie":"usage libéré","commun_vivant":"commun vivant"}
SYM={"oui":"●","partiel":"◐","non":"○","non_etabli":"non établi","projete":"projeté"}
def derive(ev):
    porte=ev["porte"]["valeur"]; q=ev["questions"]; v=lambda n:q[n]["valeur"]; sc=lambda n:S.get(v(n))
    susp=(porte=="non_etabli") or any(v(n)=="non_etabli" for n in("voix","duree"))
    if porte=="non": band="marchand"
    elif porte=="partiel": band="en_transition"
    elif susp: band="sorti_du_marche"
    elif sc("voix")==1 and sc("duree")==1: band="usage_decommodifie" if sc("don")==1 else "autogere"
    else: band="sorti_du_marche"
    mil,viv=v("milieu"),v("vivant")
    badge="non_etabli" if(mil in UNK or viv in UNK) else (2 if S[mil]==1 and S[viv]==1 else(1 if S[mil]+S[viv]>=1 else 0))
    if band=="usage_decommodifie" and isinstance(badge,int) and badge>=1: band="commun_vivant"
    chemin=("voix","duree","don","ouverture"); rank=lambda n:(0 if n in("voix","duree") and v(n)=="non_etabli" else 1,9 if v(n) in UNK else S[v(n)])
    pf=min(chemin,key=rank); lo,hi=BANDS[band]
    if susp: num=None
    elif band=="sorti_du_marche": num=round(lo+(hi-lo)*(((1.0 if porte=="oui" else .5)+(sc("ouverture") or 0)+(sc("duree") or 0))/3))
    elif band=="autogere": num=round(lo+(hi-lo)*(sc("don") or 0))
    elif band=="usage_decommodifie": num=round(lo+(hi-lo)*(1.0 if badge!="non_etabli" and badge>=1 else .3))
    else: num=round((lo+hi)/2)
    return band,susp,pf,badge,num

# --- 3 fiches REVUES sur sources (étape D faite à la main pour le pilote) ---
FICHES=[
 {"nom":"La Marinie","lieu":"Causse-et-Diège (12)","porteur":"Fonds de dotation Antidote → association Les Communs de la Marinie (bail emphytéotique 99 ans)",
  "ev":{"porte":{"valeur":"oui","cran":"pour_toujours"},"questions":{
   "milieu":{"valeur":"non_etabli","note":"Clauses environnementales du bail non documentées."},
   "vivant":{"valeur":"partiel","note":"Céréales anciennes, agriculture paysanne ; rien d'agi délibérément pour le vivant non-humain."},
   "ouverture":{"valeur":"oui","note":"Agriculture, fournil, savonnerie, activités culturelles ouvertes au-delà des membres."},
   "don":{"valeur":"partiel","note":"Mise en commun ; redevance modique ; régime d'accès aux fruits non documenté."},
   "duree":{"valeur":"oui","note":"Bail emphytéotique 99 ans."},
   "voix":{"valeur":"oui","note":"Les usager·es décident (asso Les Communs de la Marinie) ; transmission pérenne partiellement formalisée."}}}},
 {"nom":"Domaine du Rayol","lieu":"Rayol-Canadel-sur-Mer (83)","porteur":"Conservatoire du littoral (domaine propre, inaliénable) → association gestionnaire",
  "ev":{"porte":{"valeur":"oui","cran":"pour_toujours"},"questions":{
   "milieu":{"valeur":"oui","note":"Domaine propre du Conservatoire, géré en jardin botanique de conservation."},
   "vivant":{"valeur":"oui","note":"Espace côtier des Maures sauvegardé ; vocation de protection du vivant."},
   "ouverture":{"valeur":"oui","note":"Ouvert au public, ~95 000 visiteur·es/an, pédagogie de l'environnement."},
   "don":{"valeur":"non","note":"Accès payant (billet) ; gestion par équipe salariée."},
   "duree":{"valeur":"partiel","note":"Convention d'objectifs renouvelée ; gestionnaires, non une communauté d'usagers qui « reste »."},
   "voix":{"valeur":"partiel","note":"Association gestionnaire sous convention publique ; pas une autogestion des usager·es."}}}},
 {"nom":"Terres du Larzac","lieu":"Plateau du Larzac (12)","porteur":"Propriété de l'État → SCTL (bail emphytéotique 99 ans) → baux longs aux paysan·nes",
  "ev":{"porte":{"valeur":"oui","cran":"pour_toujours"},"questions":{
   "milieu":{"valeur":"non","note":"Baux longs non assortis d'une protection environnementale opposable documentée."},
   "vivant":{"valeur":"non_etabli","note":"Vaste espace agropastoral ; place au vivant non documentée par les sources."},
   "ouverture":{"valeur":"oui","note":"Office foncier qui réinstalle des paysan·nes (+~20 %) ; intérêt général manifeste."},
   "don":{"valeur":"partiel","note":"Office foncier sans recherche de rente ; régime d'accès aux fruits non documenté."},
   "duree":{"valeur":"oui","note":"Baux longs sécurisant la jouissance ; emphytéose 99 ans en amont (échéance 2083)."},
   "voix":{"valeur":"oui","note":"Les associé·es de la SCTL sont les usager·es ; fonctionnement continu depuis 1985."}}}},
]
QORDER=[("milieu","Le milieu"),("vivant","Le vivant"),("ouverture","L'ouverture"),("don","Le don"),("duree","La durée"),("voix","La voix")]
def badge_html(b):
    return {0:"<span class='b0'>pas de badge</span>",1:"🌿 <b>Sanctuaire</b>",2:"🌿🌿 <b>Sanctuaire</b>","non_etabli":"<span class='b0'>badge non évalué</span>"}[b]
cards=""
for f in FICHES:
    band,susp,pf,badge,num=derive(f["ev"])
    note = "suspendue — palier atteint : "+LBL[band] if susp else f"<b>{num}</b> / 100"
    rows=""
    for k,lab in QORDER:
        qq=f["ev"]["questions"][k]; val=qq["valeur"]; sym=SYM[val]
        cls="ok" if val=="oui" else("mid" if val=="partiel" else("na" if val in UNK else "no"))
        rows+=f"<tr><td>{lab}</td><td class='sym {cls}'>{sym}</td><td class='nt'>{html.escape(qq['note'])}</td></tr>"
    p=f["ev"]["porte"]
    cards+=f"""<div class="card">
      <div class="hd"><h2>{html.escape(f['nom'])}</h2><span class="loc">{html.escape(f['lieu'])}</span></div>
      <div class="porteur">{html.escape(f['porteur'])}</div>
      <div class="score"><span class="band band-{band}">{LBL[band]}</span>
        <span class="num">libération {note}</span> · <span class="badge">{badge_html(badge)}</span></div>
      <table class="q"><tr><th>la porte</th><td class="sym ok">●</td><td class="nt">Sortie du marché — {p['cran'].replace('_',' ')} (préalable franchi).</td></tr>{rows}</table>
      <div class="pf">Point faible nommé : <b>{pf}</b>.</div>
      <div class="dr">Vous représentez ce lieu ? <b>Droit de réponse</b> : correction sur pièce, levée d'un « non établi » sur témoignage, réponse libre sans retouche. Contact avant toute publication.</div>
    </div>"""

HTML=f"""<!doctype html><html lang="fr"><meta charset="utf-8"><title>Pilote v3.1 — aperçu</title>
<style>
body{{font-family:Georgia,serif;max-width:820px;margin:24px auto;padding:0 16px;color:#1d2421;line-height:1.5}}
h1{{font-size:1.6rem}} .intro{{background:#f4f1ea;border-left:4px solid #6b8f71;padding:12px 16px;border-radius:6px;font-size:.96rem}}
.card{{border:1px solid #d8d3c6;border-radius:10px;padding:18px 20px;margin:22px 0;box-shadow:0 1px 3px rgba(0,0,0,.05)}}
.hd{{display:flex;align-items:baseline;justify-content:space-between;border-bottom:1px solid #eee;padding-bottom:6px}}
.hd h2{{margin:0;font-size:1.3rem}} .loc{{color:#777;font-size:.85rem}}
.porteur{{font-size:.85rem;color:#555;margin:6px 0 10px}}
.score{{margin:8px 0 12px;font-size:1rem}} .num{{color:#333}}
.band{{display:inline-block;padding:2px 10px;border-radius:12px;font-size:.8rem;font-weight:bold;color:#fff;margin-right:6px}}
.band-autogere{{background:#3d7a4e}} .band-sorti_du_marche{{background:#b08a3e}} .band-en_transition{{background:#a86a4a}} .band-marchand{{background:#9a9a9a}} .band-usage_decommodifie{{background:#2f6e8f}} .band-commun_vivant{{background:#274}}
.badge{{font-size:.95rem}} .b0{{color:#999;font-size:.85rem}}
table.q{{width:100%;border-collapse:collapse;margin:8px 0;font-size:.9rem}}
table.q td,table.q th{{padding:5px 8px;border-bottom:1px solid #f0ece2;vertical-align:top;text-align:left}}
table.q th{{font-weight:bold;width:90px}}
.sym{{text-align:center;width:38px;font-size:1.1rem}} .sym.ok{{color:#3d7a4e}} .sym.mid{{color:#b08a3e}} .sym.no{{color:#b04a4a}} .sym.na{{color:#999;font-size:.75rem}}
.nt{{color:#555;font-size:.85rem}} .pf{{margin-top:6px;font-weight:bold}}
.dr{{margin-top:10px;font-size:.8rem;color:#666;background:#faf8f3;padding:8px 10px;border-radius:6px}}
</style>
<h1>Pilote — « Le faisceau libéré » v3.1 <span style="font-weight:normal;font-size:1rem;color:#999">(aperçu interne, non publié)</span></h1>
<div class="intro"><b>Comment lire.</b> Une <b>porte</b> (sortir du marché) puis <b>six questions</b> du lieu vers le groupe ; une <b>échelle de libération</b> (marchand → sorti du marché → autogéré → usage libéré → commun vivant) lue au point faible <i>du chemin</i> ; un <b>badge « Sanctuaire »</b> écologique <i>à côté</i> de la note, jamais dedans. On note <b>un degré de sortie du marché, pas un lieu</b> ; ce qu'on ne peut établir reste « non établi », jamais deviné. Trois fiches <b>revues sur sources</b> ci-dessous.</div>
{cards}
<p style="font-size:.8rem;color:#999;margin-top:30px">Aperçu autonome — chiffres calculés par <code>derive.py</code>, évaluations revues à la main sur les grilles sourcées. Le reste du corpus (52 lieux) reste en v2 tant qu'il n'est pas re-collecté. Rien n'est déployé.</p>
</html>"""
open("apercu/pilote-v3.1.html","w").write(HTML)
for f in FICHES:
    b,s,pf,bd,n=derive(f["ev"]); print(f"{f['nom']:20} -> {LBL[b]:16} note={'susp' if s else n} badge={bd} pf={pf}")
print("\nAperçu écrit : apercu/pilote-v3.1.html")
