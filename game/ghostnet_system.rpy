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
                "text": "Toujours pas remboursée du bug promo de ce soir, ça me rend folle.",
                "extract": {"sensitive": "frustration achat"}
            },
            {
                "source": "Messages",
                "speaker": "Bryonn",
                "side": "right",
                "text": "Rentre tranquille, je livre mon dernier colis et j'arrive.",
                "extract": {"person": "Bryonn"}
            },
            {
                "source": "Localisation",
                "speaker": "GeoPing",
                "side": "left",
                "text": "Sortie NeoWear Bloc 9 -> arrêt tram ligne B.",
                "extract": {"location": "NeoWear Bloc 9"}
            },
            {
                "source": "Messages",
                "speaker": victim["name"],
                "side": "right",
                "text": "Le QR 60% était un fake... 89 crédits perdus pour rien.",
                "extract": {"money": "89 crédits"}
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

    def ghostnet_reveal_followup(victim_id):
        victim = ghostnet_victims[victim_id]
        if victim.get("followup_revealed"):
            return

        followup_chunks = [
            {"id": ghostnet_chunk_counter[0] + 0, "source": "Messages", "speaker": "Romie Guillet", "side": "left", "ts": "19:43", "text": "Regarde la photo cabine. Le top tombe super bien.", "extract": {"nsfw": "selfie cabine", "location": "NeoWear Bloc 9"}, "tagged": False},
            {"id": ghostnet_chunk_counter[0] + 1, "source": "Photos", "speaker": "Flux média", "side": "right", "ts": "19:43", "text": "Photo jointe affichée dans le flux (cabine NeoWear, lumière froide).", "extract": {"location": "NeoWear Bloc 9"}, "tagged": False},
            {"id": ghostnet_chunk_counter[0] + 2, "source": "Messages", "speaker": "Romie Guillet", "side": "left", "ts": "19:44", "text": "Je voulais le garder pour ce soir quand tu rentres.", "extract": {"person": "Bryonn"}, "tagged": False},
            {"id": ghostnet_chunk_counter[0] + 3, "source": "Messages", "speaker": "Romie Guillet", "side": "left", "ts": "19:44", "text": "Là je suis juste crevée et vénère de la promo cassée.", "extract": {"sensitive": "fatigue"}, "tagged": False},
            {"id": ghostnet_chunk_counter[0] + 4, "source": "Messages", "speaker": "Romie Guillet", "side": "left", "ts": "19:45", "text": "Tu finis à quelle heure ?", "extract": {}, "tagged": False},
            {"id": ghostnet_chunk_counter[0] + 5, "source": "Messages", "speaker": "Bryonn", "side": "right", "ts": "19:45", "text": "Dans 45 min. Rentre direct.", "extract": {"person": "Bryonn"}, "tagged": False},
            {"id": ghostnet_chunk_counter[0] + 6, "source": "Messages", "speaker": "Bryonn", "side": "right", "ts": "19:46", "text": "Garde le top, on se pose tranquille.", "extract": {}, "tagged": False},
            {"id": ghostnet_chunk_counter[0] + 7, "source": "Messages", "speaker": "Système", "side": "right", "ts": "19:46", "text": "Capture terminée : conversation chiffrée ensuite.", "extract": {}, "tagged": False},
        ]
        ghostnet_chunk_counter[0] += len(followup_chunks)
        victim["chunks"].extend(followup_chunks)
        victim["followup_revealed"] = True
        victim["heat"] = min(100, victim["heat"] + 3)
        victim["last_activity"] = "19:46"


default ghostnet_running = False
default ghostnet_active_module = "Lecteur"
default ghostnet_active_tab = "Messages"
default ghostnet_selected_victim = "romie"
default ghostnet_chunk_counter = [3]
default ghostnet_victims = {
    "romie": {
        "name": "ROMIE GUILLET",
        "dob": "Inconnu (24 ans estimés)",
        "address": "Inconnue",
        "job": "Inconnu",
        "relation": "Inconnue",
        "income": "Inconnu",
        "vices": [],
        "infection": 17,
        "heat": 22,
        "mail": 8,
        "social": 14,
        "webcam": 4,
        "mic": 7,
        "geo": 19,
        "relations": [],
        "graph_nodes": [
            {"name": "Romie", "role": "Cible", "x": 48, "y": 55},
        ],
        "vault": 0,
        "followup_revealed": False,
        "last_activity": "19:42",
        "chunks": [
            {
                "id": 0,
                "source": "Messages",
                "speaker": "Romie Guillet",
                "side": "left",
                "ts": "19:42",
                "text": "Putain Bryonn je suis dég. J'ai scanné un QR -60% au NeoWear et ça a buggué. J'ai payé 89 crédits plein pot.",
                "extract": {"person": "Bryonn", "location": "NeoWear Bloc 9", "money": "89 crédits"},
                "tagged": False,
            },
            {
                "id": 1,
                "source": "Messages",
                "speaker": "Bryonn",
                "side": "right",
                "ts": "19:42",
                "text": "Encore un faux code promo... Ils trackent tout. T'as quand même essayé l'outfit ?",
                "extract": {"person": "Bryonn"},
                "tagged": False,
            },
            {
                "id": 2,
                "source": "Messages",
                "speaker": "Romie Guillet",
                "side": "left",
                "ts": "19:42",
                "text": "Oui, et il rend super bien. Dommage que la promo n'ait pas marché.",
                "extract": {"sensitive": "outfit essayé"},
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
            text "23 mars 2026" color "#173042" size 28
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
                        if not victim.get("followup_revealed", False):
                            textbutton "Lire la suite (8 messages)":
                                action Function(ghostnet_reveal_followup, ghostnet_selected_victim)
                        textbutton "Quitter simulation" action Return()

label ghostnet_demo:
    call screen ghostnet_v2_ui
    return
