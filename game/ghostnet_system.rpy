init python:
    import random

    GHOSTNET_MODULES = ["Lecteur", "Auditeur", "Réseau", "Marché noir", "Propagation"]
    GHOSTNET_TABS = ["Messages", "Mails", "Réseaux", "Photos", "Localisation", "Webcam"]

    def ghostnet_new_chunk(victim_id):
        victim = ghostnet_victims[victim_id]
        candidates = [
            {
                "source": "Messages",
                "speaker": victim["name"],
                "side": "left",
                "text": "N'en parle pas à Lena. On se voit au Blue Iris Lounge à 22h.",
                "extract": {"person": "Lena", "location": "Blue Iris Lounge", "sensitive": "secret relationnel"}
            },
            {
                "source": "Mails",
                "speaker": "Xmail",
                "side": "right",
                "text": "Relance cabinet Veld & Co : facture impayée, délai 48h.",
                "extract": {"money": "Facture impayée", "sensitive": "dette"}
            },
            {
                "source": "Réseaux",
                "speaker": victim["name"],
                "side": "left",
                "text": "Story publiée depuis Novagen Tower. #nightshift",
                "extract": {"location": "Novagen Tower"}
            },
            {
                "source": "Photos",
                "speaker": "Galerie sync",
                "side": "right",
                "text": "Photo intime détectée (miroir + plaque rue visible).",
                "extract": {"nsfw": "photo_intime", "location": "Rue Cobalt"}
            },
            {
                "source": "Localisation",
                "speaker": "GeoPing",
                "side": "right",
                "text": "07:42 domicile -> 08:31 Station Nord -> 09:02 Novagen.",
                "extract": {"location": "Routine matinale"}
            },
            {
                "source": "Webcam",
                "speaker": "Transcription micro",
                "side": "right",
                "text": "Si Joseph apprend ça, je suis ruinée.",
                "extract": {"person": "Joseph", "sensitive": "peur d'exposition"}
            },
        ]
        chunk = dict(random.choice(candidates))
        chunk["id"] = ghostnet_chunk_counter[0]
        ghostnet_chunk_counter[0] += 1
        chunk["ts"] = "{:02d}:{:02d}".format(random.randint(0, 23), random.randint(0, 59))
        chunk["tagged"] = False
        victim["chunks"].append(chunk)
        victim["last_activity"] = chunk["ts"]

    def ghostnet_tick():
        if not ghostnet_running:
            return
        vid = ghostnet_selected_victim
        ghostnet_new_chunk(vid)

        victim = ghostnet_victims[vid]
        victim["infection"] = min(100, victim["infection"] + random.randint(0, 2))
        if ghostnet_active_module in ("Auditeur", "Propagation"):
            victim["heat"] = min(100, victim["heat"] + random.randint(1, 3))
        else:
            victim["heat"] = min(100, victim["heat"] + random.randint(0, 2))

    def ghostnet_select_victim(victim_id):
        store.ghostnet_selected_victim = victim_id

    def ghostnet_set_module(module_name):
        store.ghostnet_active_module = module_name

    def ghostnet_set_tab(tab_name):
        store.ghostnet_active_tab = tab_name

    def ghostnet_extract(victim_id, chunk_id, key):
        victim = ghostnet_victims[victim_id]
        for chunk in victim["chunks"]:
            if chunk["id"] != chunk_id:
                continue
            value = chunk.get("extract", {}).get(key)
            if not value:
                return

            if key == "person":
                if value not in victim["relations"]:
                    victim["relations"].append(value)
                    victim["graph_nodes"].append({"name": value, "role": "Contact", "x": random.randint(10, 85), "y": random.randint(10, 85)})
            elif key == "location":
                victim["address"] = value
            elif key == "sensitive":
                if value not in victim["vices"]:
                    victim["vices"].append(value)
            elif key == "money":
                victim["income"] = "Risque financier détecté"
            elif key == "nsfw":
                victim["vault"] += 1

            chunk["tagged"] = True
            victim["heat"] = min(100, victim["heat"] + 2)
            break

    def ghostnet_action(victim_id, action_name):
        victim = ghostnet_victims[victim_id]
        if action_name == "webcam":
            victim["heat"] = min(100, victim["heat"] + 8)
            ghostnet_new_chunk(victim_id)
        elif action_name == "mic":
            victim["heat"] = min(100, victim["heat"] + 6)
            ghostnet_new_chunk(victim_id)
        elif action_name == "chantage":
            victim["heat"] = min(100, victim["heat"] + 10)
            victim["income"] = "+12k crédit noir estimé"
        elif action_name == "propagation":
            victim["infection"] = min(100, victim["infection"] + 6)
            victim["heat"] = min(100, victim["heat"] + 4)
        elif action_name == "cooldown":
            victim["heat"] = max(0, victim["heat"] - 12)


default ghostnet_running = True
default ghostnet_active_module = "Lecteur"
default ghostnet_active_tab = "Messages"
default ghostnet_selected_victim = "cassandra"
default ghostnet_chunk_counter = [1]
default ghostnet_victims = {
    "cassandra": {
        "name": "CASSANDRA WATERGATE",
        "dob": "13 septembre 1992",
        "address": "District Arcadia, Mégalopole 7",
        "job": "Avocate corporate",
        "relation": "En couple avec Josef Langley",
        "income": "7 400 crédits/mois (estimé)",
        "vices": ["sexting", "dette"],
        "infection": 58,
        "heat": 34,
        "mail": 66,
        "social": 73,
        "webcam": 45,
        "mic": 54,
        "geo": 80,
        "relations": ["Josef Langley", "Nina Maternova", "Juliet Kerrington"],
        "graph_nodes": [
            {"name": "Cassandra", "role": "Cible", "x": 48, "y": 55},
            {"name": "Josef", "role": "Relation", "x": 20, "y": 25},
            {"name": "Nina", "role": "Amie", "x": 75, "y": 24},
            {"name": "Juliet", "role": "Collègue", "x": 23, "y": 80},
            {"name": "Abraham", "role": "Client", "x": 78, "y": 79},
        ],
        "vault": 2,
        "last_activity": "09:11",
        "chunks": [
            {
                "id": 0,
                "source": "Messages",
                "speaker": "Cassandra Watergate",
                "side": "left",
                "ts": "09:11",
                "text": "Coucou Jossi :) La carte platinum est sur ton bureau.",
                "extract": {"person": "Josef", "sensitive": "intimité financière"},
                "tagged": False,
            }
        ],
    }
}

screen ghostnet_v2_ui():
    tag menu
    modal True

    timer 6.0 action Function(ghostnet_tick) repeat True

    $ victim = ghostnet_victims[ghostnet_selected_victim]
    $ filtered_chunks = [c for c in victim["chunks"] if c["source"] == ghostnet_active_tab or ghostnet_active_tab == "Messages"]

    add Solid("#d5e7f2")

    frame:
        background "#9db5c8"
        xfill True
        ysize 82
        xpadding 18
        ypadding 10

        hbox:
            xfill True
            spacing 16
            text "23 mars 2030" color "#173042" size 28
            text "| GHOSTNET / THE EYE" color "#28465d" size 24
            null width 30
            for module in GHOSTNET_MODULES:
                textbutton module:
                    action Function(ghostnet_set_module, module)
                    background ("#1e3e56" if ghostnet_active_module == module else "#4f6c80")
                    text_color "#e8f4ff"
                    text_size 18
                    xpadding 14
                    ypadding 7
            null
            text "HEAT GLOBAL [victim['heat']]%" color "#7c1a1a" size 20

    hbox:
        xfill True
        yfill True
        spacing 14
        xpos 14
        ypos 94

        frame:
            background "#eaf3fa"
            xmaximum 620
            yfill True
            xpadding 14
            ypadding 12

            vbox:
                spacing 10
                text "[victim['name']]" color "#153247" size 42
                text "ID-GHOSTNET: GH-647-24-612" color "#507086" size 17

                hbox:
                    spacing 12
                    frame:
                        background "#c5d9ea"
                        xsize 220
                        ysize 220
                        text "PHOTO\nGLITCH" xalign 0.5 yalign 0.5 color "#21455f" size 30 text_align 0.5

                    vbox:
                        spacing 6
                        text "Date de naissance : [victim['dob']]" color "#1f3b51" size 18
                        text "Adresse : [victim['address']]" color "#1f3b51" size 18
                        text "Profession : [victim['job']]" color "#1f3b51" size 18
                        text "Relation : [victim['relation']]" color "#1f3b51" size 18
                        text "Revenus : [victim['income']]" color "#1f3b51" size 18
                        text "Vices : [', '.join(victim['vices'])]" color "#7f2338" size 18

                text "INFECTION [victim['infection']]%" color "#20435d" size 20
                bar value StaticValue(victim["infection"], 100) xmaximum 560
                text "Mail [victim['mail']] | Réseaux [victim['social']] | Webcam [victim['webcam']] | Mic [victim['mic']] | Géoloc [victim['geo']]" color "#355870" size 16

                text "HEAT / RISQUE [victim['heat']]%" color "#7d1d2e" size 20
                bar value StaticValue(victim["heat"], 100) xmaximum 560

                hbox:
                    spacing 8
                    textbutton "Activer Webcam":
                        action Function(ghostnet_action, ghostnet_selected_victim, "webcam")
                    textbutton "Activer Mic":
                        action Function(ghostnet_action, ghostnet_selected_victim, "mic")
                    textbutton "Générer chantage":
                        action Function(ghostnet_action, ghostnet_selected_victim, "chantage")
                    textbutton "Propagation":
                        action Function(ghostnet_action, ghostnet_selected_victim, "propagation")
                    textbutton "Cooldown":
                        action Function(ghostnet_action, ghostnet_selected_victim, "cooldown")

                text "RELATIONS" color "#1a3a52" size 32
                fixed:
                    xmaximum 580
                    ysize 250
                    add Solid("#dbe9f4")
                    for i, node in enumerate(victim["graph_nodes"]):
                        frame:
                            background ("#315a77" if i == 0 else "#6b8fa7")
                            xpos int(node["x"] * 5.5)
                            ypos int(node["y"] * 2.5)
                            xpadding 8
                            ypadding 4
                            text "[node['name']]" color "#edf6ff" size 14

        frame:
            background "#f1f7fc"
            xfill True
            yfill True
            xpadding 14
            ypadding 12

            vbox:
                spacing 8
                text "DISCUSSIONS / DATASTREAM" color "#1c3a51" size 36
                hbox:
                    spacing 6
                    for tab in GHOSTNET_TABS:
                        textbutton tab:
                            action Function(ghostnet_set_tab, tab)
                            background ("#2b506b" if ghostnet_active_tab == tab else "#9eb5c7")
                            text_color ("#ecf6ff" if ghostnet_active_tab == tab else "#27475f")
                            text_size 16
                            xpadding 8
                            ypadding 5

                viewport:
                    draggable True
                    mousewheel True
                    scrollbars "vertical"
                    yfill True
                    xfill True

                    vbox:
                        spacing 10
                        for chunk in victim["chunks"]:
                            if chunk["source"] == ghostnet_active_tab or ghostnet_active_tab == "Messages":
                                frame:
                                    background ("#e5f0f8" if chunk["side"] == "left" else "#d2e6f6")
                                    xfill True
                                    xpadding 10
                                    ypadding 8

                                    vbox:
                                        spacing 4
                                        text "[chunk['speaker']] • [chunk['ts']] • [chunk['source']]" color "#32536a" size 15
                                        text "[chunk['text']]" color "#112c40" size 20
                                        if chunk["tagged"]:
                                            text "TAGGÉ ✔" color "#175737" size 15
                                        hbox:
                                            spacing 4
                                            if "person" in chunk.get("extract", {}):
                                                textbutton "Extraire personne":
                                                    action Function(ghostnet_extract, ghostnet_selected_victim, chunk["id"], "person")
                                            if "location" in chunk.get("extract", {}):
                                                textbutton "Extraire lieu":
                                                    action Function(ghostnet_extract, ghostnet_selected_victim, chunk["id"], "location")
                                            if "sensitive" in chunk.get("extract", {}):
                                                textbutton "Tag sensible":
                                                    action Function(ghostnet_extract, ghostnet_selected_victim, chunk["id"], "sensitive")
                                            if "money" in chunk.get("extract", {}):
                                                textbutton "Tag dette":
                                                    action Function(ghostnet_extract, ghostnet_selected_victim, chunk["id"], "money")
                                            if "nsfw" in chunk.get("extract", {}):
                                                textbutton "Ajouter NSFW Vault":
                                                    action Function(ghostnet_extract, ghostnet_selected_victim, chunk["id"], "nsfw")

                frame:
                    background "#d4e4f2"
                    xfill True
                    xpadding 10
                    ypadding 8
                    hbox:
                        spacing 15
                        text "Victime active : [victim['name']]" color "#1b3b51" size 16
                        text "Dernière activité : [victim['last_activity']]" color "#1b3b51" size 16
                        text "NSFW Vault : [victim['vault']] éléments" color "#5d1f36" size 16
                        textbutton "Quitter simulation" action Return()

label ghostnet_demo:
    call screen ghostnet_v2_ui
    return
