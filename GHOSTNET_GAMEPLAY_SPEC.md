# GHOSTNET — Spécification complète du nouveau gameplay (inspiration Orwell)

## 0) Vision produit et principe directeur

**Objectif** : remplacer entièrement le gameplay terminal par une expérience d'analyse de surveillance visuelle, froide et systémique, structurée autour d'un **profil cible à gauche** et d'un **flux de données à droite**, dans une esthétique bleu/gris clinique.

**Promesse joueur** :
- « Je n'exécute plus des commandes ; j'observe, j'extrais, je relie, puis j'exploite. »
- Le cœur du jeu devient la lecture active des traces numériques (datachunks), la constitution de graphe social, et l'orchestration de pressions/propagation.

**Nom système validé** : **GHOSTNET**.

---

## 1) Interface principale (layout Orwell-like 100 %)

## 1.1 Composition globale écran

- **Top bar horizontale (hauteur ~8-10%)**
  - Date du jour simulée + horloge de session.
  - Indicateurs statut système (enregistrement, latence, chiffrement, alerte).
  - Modules onglets (style badges anguleux) :
    1. **Lecteur**
    2. **Auditeur**
    3. **Réseau**
    4. **Marché noir**
    5. **Propagation**

- **Corps écran en 2 colonnes (hauteur ~90%)**
  - **Colonne gauche fixe (35-40%)** : Fiche Victime + bloc Relations.
  - **Colonne droite flexible (60-65%)** : DISCUSSIONS / DATASTREAM avec timeline et onglets de source.

- **Direction artistique UI**
  - Palette : bleu glacier, gris acier, blanc froid, accents cyan.
  - Contraste faible-moyen, lisibilité élevée, typo sans-serif technique.
  - Pas d'effet CRT, pas de vert terminal, pas de bruit retro.

## 1.2 Panneau gauche — Fiche Victime

### A. Header identité
- Nom complet (ex. **CASSANDRA WATERGATE**) en capitales.
- ID interne GHOSTNET (ex. GH-447-21-9).
- Niveau de certitude des données (% complétude du profil).

### B. Carte d'identité enrichie
- **Photo principale** (source volée : galerie / webcam / réseau social), affichage carré.
- Champs auto-remplissables:
  - Date de naissance (ou intervalle estimé)
  - Adresse approximative
  - Profession
  - Situation relationnelle
  - Revenus estimés
  - Vulnérabilités détectées (tags comportementaux)

### C. Infection et exposition technique
- **Barre d'infection globale 0-100%**.
- Sous-barres:
  - Mail
  - Réseaux sociaux
  - Webcam
  - Micro
  - Géolocalisation
- Chaque sous-barre influence le type de datachunks reçus.

### D. Heat / Risque de détection
- Jauge rouge/orange persistante.
- États:
  1. Bas : cible passive
  2. Moyen : comportements prudents
  3. Élevé : nettoyage, changement mdp, rupture de routine
  4. Critique : suspicion active / contre-mesures

### E. RELATIONS (graphe interactif)
- Graphe en arbre/réseau avec portraits miniatures hexagonaux.
- Lignes bleues de liens (familial, intime, pro, criminel, financier).
- Interactions:
  - Drag & drop pour relier des nœuds
  - Zoom/pan
  - Clic nœud = ouvrir fiche contact
  - Survol lien = source de preuve + degré de confiance

## 1.3 Panneau droit — DISCUSSIONS / DATASTREAM

### A. Barre d'onglets source
1. Messages
2. Mails
3. Réseaux sociaux
4. Photos/Vidéos
5. Localisation
6. Webcam Live

### B. Fil chronologique live
- Entrées sous forme de bulles/cartes timestampées.
- Alternance interlocuteurs (gauche/droite) avec avatar cible/contact.
- Types de datachunks mélangés:
  - SMS/DM
  - Email
  - Story/post
  - Audio transcrit
  - Photo/vidéo
  - Ping de géoloc

### C. Datachunk interactif (mécanique Orwellienne)
- Le joueur peut:
  - surligner un mot
  - cliquer une entité (nom, lieu, date, montant)
  - extraire la preuve
  - tagger et classer
- Résultat instantané:
  - mise à jour profil gauche
  - ajout/renforcement d'un lien dans RELATIONS
  - ajout au dossier d'exploitation (chantage, vente, propagation)

## 1.4 Modules top bar (équivalent Lecteur/Auditeur/Initié)

### 1) Lecteur
- Vue par défaut du datastream.
- Outils d'annotation, extraction, tags.

### 2) Auditeur
- Accès webcam/micro live.
- Boutons : écouter, enregistrer, couper, snapshot.
- Flux avec artefacts (compression, drops, interférences).

### 3) Réseau
- Graphe macro multi-victimes (10-15+ cibles).
- Filtres : intime, financier, hiérarchie, géographique.

### 4) Marché noir
- Inventaire de contenus exploitables.
- Évaluation dynamique valeur/risque.
- Vente instantanée ou lot anonymisé.

### 5) Propagation
- Création de vecteurs (QR frauduleux, faux login, lien appât).
- Templates par contexte (banque, RH, livraison, romance).

---

## 2) Boucle de gameplay complète (minute par minute)

## 2.1 Macro-boucle (10-20 min)
1. Préparer une infection (Propagation).
2. Activer une nouvelle cible (fiche vide).
3. Recevoir datachunks en flux.
4. Extraire/tagger preuves.
5. Ouvrir opportunités (chantage/vente/propagation).
6. Gérer Heat.
7. Étendre réseau.

## 2.2 Micro-boucle (1-3 min)
- **0:00-0:30** : arrivée d'un chunk (message ambigu + photo).
- **0:30-1:00** : extraction d'un nom + lieu + mot-clé sensible.
- **1:00-1:30** : profil et graphe se mettent à jour.
- **1:30-2:00** : décision exploitation (vault / menace / pivot contact).
- **2:00-3:00** : réaction monde (heat+, changement comportement cible).

## 2.3 Rythme d'arrivée des données
- Intervalle standard : 30-60 sec réelles.
- Accélération si:
  - infection forte,
  - période active cible,
  - caméra/micro activés.
- Ralentissement si:
  - heat élevé,
  - cible en mode prudent,
  - source temporairement coupée.

---

## 3) Intégration de l'ancien contenu (phishing, RAT, live spying, NSFW)

## 3.1 Ce qui remplace le terminal
- **Ancien**: commandes textuelles de hack.
- **Nouveau**: actions UI contextualisées (boutons, drag/drop, sélection).

| Ancien système | Nouveau mapping GHOSTNET |
|---|---|
| Commande de scan | Carte victime auto-init après infection |
| Commande RAT | Sous-barres d'infection + permissions exploitables |
| Dump messages | Datachunks timeline en direct |
| Commande webcam/mic | Module Auditeur avec flux live |
| Exfiltration dossier | Drag vers NSFW Vault / Marché noir |

## 3.2 Phishing & infection
- Écran Opérations minimaliste.
- Éditeur template appât (visuel simple bloc par bloc).
- Simulateur de taux de clic selon crédibilité.
- Infection réussie => création fiche cible dans GHOSTNET.

## 3.3 RAT / espionnage live
- Permissions progressives (mail -> socials -> cam/mic).
- Activation live consomme « bruit réseau » et augmente Heat.
- Enregistrements découpés en extraits taggables.

## 3.4 Contenu NSFW (au cœur du loop)
- Photos/vidéos/logs sexting intégrés au datastream natif.
- Actions dédiées:
  - Agrandir
  - Classer dans **NSFW Vault**
  - Associer à personne/lieu/date
  - Ajouter à paquet d'exploitation

---

## 4) Système d'analyse et tagging (cœur du gameplay)

## 4.1 Typologie d'entités extractibles
- Personnes
- Lieux
- Dates/heures
- Transactions/argent
- Événements
- Vulnérabilités comportementales
- Contenus compromettants

## 4.2 Règles de transformation automatique
- Nom inconnu taggé -> création nœud relation (confiance faible).
- Nom répété (>=3 chunks) -> confiance moyenne + priorité enquête.
- Lieu + horodatage concordants -> routine cible enrichie.
- Mots sensibles (dette, adultère, substance, fraude, sexting) -> score chantage +1.

## 4.3 Suggestions IA in-game
- « Cette personne apparaît dans 7 discussions. Lier à Cible ? »
- « Ce numéro semble être un contact intime. »
- « Ce média correspond au même décor que preuve #A21. »

---

## 5) Actions possibles sur une fiche victime

## 5.1 Actions d'observation
- Ouvrir historique complet.
- Filtrer par source.
- Activer surveillance live webcam.
- Activer écoute micro.
- Marquer routine géographique.

## 5.2 Actions d'analyse
- Extraire entité (surlignage/clic).
- Ajouter/retirer tag.
- Créer lien dans graphe.
- Fusionner doublons de contacts.
- Élever baisse du niveau de confiance d'une preuve.

## 5.3 Actions d'exploitation
- Générer message de menace auto.
- Rédiger message manuel via identité compromise.
- Créer paquet de chantage (preuves + deadline + montant).
- Vendre lot au Marché noir.
- Lancer infection latérale d'un contact.

## 5.4 Actions de gestion du risque
- Pause collecte active.
- Dégrader fréquence d'extraction.
- Purger traces locales.
- Attendre baisse heat avant action offensive.

---

## 6) Exemples de datachunks

## 6.1 Messages (chat)
- « Tu supprimes les photos d'hier ? Mon mari rentre à 19h. »
- « J'ai encore déplacé 2 800€ du compte pro, on fait comment ? »

**Extraction possible**
- Personne: mari
- Heure: 19h
- Argent: 2 800€
- Tag: infidélité potentielle / fraude financière

## 6.2 Mails
- Objet: « Relance cabinet Veld & Co — échéance impayée »
- Corps: « Sans règlement sous 48h, procédure engagée. »

**Extraction possible**
- Entité pro: Veld & Co
- Échéance: 48h
- Tag: dette / pression légale

## 6.3 Réseaux sociaux
- Story géotaggée: « Blue Iris Lounge »
- DM: « N'en parle pas à Lena stp. »

**Extraction possible**
- Lieu: Blue Iris Lounge
- Personne: Lena
- Tag: secret relationnel

## 6.4 Photo/Vidéo
- Selfie intime + reflet plaque rue dans miroir.

**Extraction possible**
- Média compromettant -> NSFW Vault
- Lieu probable via plaque/rue
- Corrélation temporelle avec logs de chat

## 6.5 Localisation
- 07:42 domicile -> 08:31 station Nord -> 09:02 siège Novagen.

**Extraction possible**
- Routine matinale
- Employeur probable: Novagen

## 6.6 Webcam/Micro live
- Audio: dispute « si Joseph apprend ça, je suis ruinée ».

**Extraction possible**
- Personne: Joseph
- Mot-clé: ruinée
- Tag: peur d'exposition / levier chantage

---

## 7) Heat, conséquences et contre-jeu

## 7.1 Ce qui augmente le Heat
- Activation webcam/mic prolongée.
- Extraction massive en peu de temps.
- Envoi de messages depuis appareil compromis.
- Propagation trop agressive sur proches directs.

## 7.2 Effets gameplay par paliers
- **Heat 0-30** : flux normal.
- **Heat 31-60** : latence, bruit de données, premières incohérences.
- **Heat 61-80** : cibles méfiantes, comptes privés, changements routines.
- **Heat 81-100** : risque de burn opérationnel, pertes d'accès, enquête.

## 7.3 Contre-mesures joueur
- Dormance tactique.
- Pivot sur autre cible du réseau.
- Réduction collecte live.
- Exploitation indirecte via contact tiers.

---

## 8) Progression, campagne et fins

## 8.1 Courbe de progression (15-25h)
- Acte 1 : prise en main GHOSTNET, petites cibles, faibles enjeux.
- Acte 2 : réseau dense, choix moraux, profits vs exposition.
- Acte 3 : polarisation stratégique (révolution / domination / fuite).

## 8.2 Mode infini
- Génération procédurale de nouvelles cibles.
- Événements dynamiques (fuites massives, crackdown, panne infra).
- Meta-objectifs score (influence, fortune, invisibilité).

## 8.3 Fins multiples
- Architecte de révolte.
- Empereur du chantage.
- Capture et exposition publique.
- Dissociation/paranoïa du joueur (fin psychologique).

---

## 9) Recommandations visuelles (fidèles Orwell + cyberpunk 2030)

## 9.1 Fidélité Orwell stricte
- Grands aplats bleu/gris.
- Cartes/bulles nettes et orthogonales.
- Iconographie institutionnelle (dossier, audit, terminal de contrôle).
- Photo portrait stylisée (glitch léger, low poly optionnel).

## 9.2 Couche cyberpunk 2030 (subtile)
- Micro-animations de scanline **très discrètes** (non-CRT).
- Reflets holo doux sur certains overlays.
- Effets de compression visuelle lors de surcharge réseau.
- Accent néon cyan uniquement pour états interactifs critiques.

## 9.3 Feedback état système
- Heat haut: UI plus instable (micro lag, blur transitoire, audio oppressant).
- Corrélations trouvées: impulsion lumineuse dans graphe.
- Nouvel élément critique: flash encadré + son sec notification.

---

## 10) Spécification UX des interactions clés

## 10.1 Sélection / extraction
- Clic simple: sélectionner chunk.
- Double clic: ouvrir détail.
- Drag sélection texte: créer entité/tag.
- Glisser média: déplacer vers vault ou marché.

## 10.2 Graphe relations
- Clic nœud: focus fiche.
- Drag nœud vers nœud: proposition de lien (avec justification).
- Molette: zoom progressif.
- Shift+drag: déplacement viewport.

## 10.3 Files d'actions rapides (raccourcis)
- `A` annoter
- `L` lier
- `V` vault
- `M` marché
- `P` propager
- `R` masquer activité (réduction risque court terme)

---

## 11) Backlog de modules (implémentation gameplay)

## M1 — Shell GHOSTNET UI
- Layout top + gauche + droite.
- Système d'onglets modules.

## M2 — Datachunk Engine
- Ingestion multi-source simulée.
- Timeline temps réel.

## M3 — Tagging & Entity Resolver
- Extraction entités + confiance.
- Auto-remplissage profil + liens graphe.

## M4 — Heat & Detection
- Modèle de risque + événements de réaction cibles.

## M5 — Exploitation Suite
- Chantage, Vault, Marché noir, propagation latérale.

## M6 — Progression & Endings
- Arc campagne + fins + mode infini.

---

## 12) Résumé exécutable design

Le nouveau **GHOSTNET** supprime totalement la fantasy terminal au profit d'un gameplay de surveillance analytique en temps réel :
1. infecter,
2. observer,
3. extraire,
4. relier,
5. exploiter,
6. contenir le risque.

L'identité visuelle reste pleinement Orwellienne (profil à gauche, discussions à droite, graphe relationnel clinique), avec une couche cyberpunk 2030 mesurée pour moderniser sans casser la lisibilité.
