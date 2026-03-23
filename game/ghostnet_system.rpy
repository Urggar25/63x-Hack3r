init python:
    GHOSTNET_MODULES = ["Lecteur", "Réseau", "Archives"]

    GHOSTNET_PROFILE_OPTIONS = [
        {"label": "Portrait Bleu", "bg": "#d8e9f8", "fg": "#1f4d72"},
        {"label": "Portrait Cyan", "bg": "#d9f3f6", "fg": "#1f5f67"},
        {"label": "Portrait Ardoise", "bg": "#e5e8ef", "fg": "#3f4f6b"},
    ]

    def ghostnet_get_dialogues(victim_id):
        return ghostnet_victims[victim_id]["dialogues"]

    def ghostnet_visible_dialogues(victim_id):
        victim = ghostnet_victims[victim_id]
        dialogues = ghostnet_get_dialogues(victim_id)
        count = min(victim["visible_count"], len(dialogues))
        return dialogues[:count]

    def ghostnet_next_dialogue(victim_id):
        victim = ghostnet_victims[victim_id]
        dialogues = ghostnet_get_dialogues(victim_id)
        if victim["visible_count"] < len(dialogues):
            victim["visible_count"] += 1
            victim["last_activity"] = dialogues[victim["visible_count"] - 1]["date"]

    def ghostnet_select_victim(victim_id):
        store.ghostnet_selected_victim = victim_id

    def ghostnet_set_module(module_name):
        store.ghostnet_active_module = module_name

    def ghostnet_cycle_avatar(character_id):
        current = ghostnet_avatar_choices.get(character_id, 0)
        ghostnet_avatar_choices[character_id] = (current + 1) % len(GHOSTNET_PROFILE_OPTIONS)

    def ghostnet_avatar_style(character_id):
        idx = ghostnet_avatar_choices.get(character_id, 0)
        return GHOSTNET_PROFILE_OPTIONS[idx]


default ghostnet_active_module = "Lecteur"
default ghostnet_selected_victim = "DISC-13-04"
default ghostnet_avatar_choices = {
    "josef": 0,
    "cassandra": 1,
}
default ghostnet_victims = ghostnet_build_victims()

screen ghostnet_avatar_preview(character_id):
    $ style_data = ghostnet_avatar_style(character_id)
    $ display_name = GHOSTNET_CHARACTER_DIRECTORY[character_id]["speaker"]

    frame:
        background style_data["bg"]
        xsize 240
        ysize 120
        xpadding 10
        ypadding 10

        hbox:
            spacing 12
            frame:
                background style_data["fg"]
                xsize 60
                ysize 60
                xalign 0.5
                yalign 0.5
                text display_name[0] xalign 0.5 yalign 0.5 color "#ffffff" size 30

            vbox:
                spacing 6
                text "[display_name]" color "#173042" size 20
                text "[style_data['label']]" color "#365f7d" size 14
                textbutton "Changer l'image":
                    action Function(ghostnet_cycle_avatar, character_id)
                    text_size 14
                    xpadding 10
                    ypadding 4

screen ghostnet_v2_ui():
    tag menu
    modal True

    $ victim = ghostnet_victims[ghostnet_selected_victim]
    $ visible_dialogues = ghostnet_visible_dialogues(ghostnet_selected_victim)
    $ all_loaded = victim["visible_count"] >= len(victim["dialogues"])

    if not all_loaded:
        key "dismiss" action Function(ghostnet_next_dialogue, ghostnet_selected_victim)

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
            text "| GHOSTNET / DISCUSSIONS" color "#28465d" size 24
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
            text "Lecture séquentielle" color "#173042" size 20

    hbox:
        xfill True
        yfill True
        spacing 14
        xpos 14
        ypos 94

        frame:
            background "#eaf3fa"
            xmaximum 640
            yfill True
            xpadding 14
            ypadding 12

            vbox:
                spacing 12
                text "[victim['name']]" color "#153247" size 38
                text "ID conversation : [victim['id']]" color "#507086" size 17
                text "[victim['summary']]" color "#2d5168" size 17

                text "Profils participants" color "#1a3a52" size 28
                for participant in victim["participants"]:
                    use ghostnet_avatar_preview(participant)

                frame:
                    background "#d4e4f2"
                    xfill True
                    xpadding 10
                    ypadding 8
                    vbox:
                        spacing 4
                        text "Ajout de dialogues :" color "#1b3b51" size 18
                        text "• Les messages sont stockés dans game/discussion/DISC_XXXX/discussion.rpy." color "#1b3b51" size 15
                        text "• Utilisez une variable de jour + dialogue('personnage', 'texte')." color "#1b3b51" size 15
                        text "• Un clic du joueur affiche le dialogue suivant en séquence." color "#1b3b51" size 15

        frame:
            background "#f1f7fc"
            xfill True
            yfill True
            xpadding 14
            ypadding 12

            vbox:
                spacing 8
                text "DISCUSSIONS" color "#1c3a51" size 36
                text "Début de l'enregistrement" color "#4f7894" size 20

                viewport:
                    draggable True
                    mousewheel True
                    scrollbars "vertical"
                    yfill True
                    xfill True

                    vbox:
                        spacing 10
                        for chunk in visible_dialogues:
                            if chunk["side"] == "center":
                                text "[chunk['text']]" color "#5c819d" size 24 xalign 0.5
                            else:
                                $ style_data = ghostnet_avatar_style(chunk["speaker_id"])
                                hbox:
                                    spacing 8
                                    if chunk["side"] == "right":
                                        null width 180
                                    frame:
                                        background style_data["bg"]
                                        xsize 84
                                        ysize 84
                                        text chunk["speaker"][0] color "#ffffff" size 36 xalign 0.5 yalign 0.5
                                    frame:
                                        background ("#ffffff" if chunk["side"] == "left" else "#d2e6f6")
                                        xmaximum 760
                                        xpadding 12
                                        ypadding 8
                                        vbox:
                                            spacing 2
                                            text "[chunk['speaker']]   [chunk['date']]" color "#32536a" size 15
                                            text "[chunk['text']]" color "#112c40" size 21
                                    if chunk["side"] == "left":
                                        null width 180

                frame:
                    background "#d4e4f2"
                    xfill True
                    xpadding 10
                    ypadding 8
                    hbox:
                        spacing 15
                        text "Dernière activité : [victim['last_activity']]" color "#1b3b51" size 16
                        if not all_loaded:
                            text "Cliquez pour afficher le dialogue suivant." color "#315976" size 16
                        else:
                            text "Tous les messages sont affichés." color "#315976" size 16
                        textbutton "Quitter simulation" action Return()

label ghostnet_demo:
    call screen ghostnet_v2_ui
    return
