init python:
    import re

    GHOSTNET_MODULES = ["Discussion", "Galerie", "Réseau", "Internet"]

    GHOSTNET_PROFILE_FALLBACK = {"id": "fallback", "label": "Aucune photo", "bg": "#d9d9d9", "fg": "#666666", "image": None}

    GHOSTNET_GALLERY_LIBRARY = {"romie": [], "bryonn": []}
    GHOSTNET_INLINE_IMAGE_MAP = {
        "romie_pic001.png": "images/character/romie_pic001.png",
        "bryonn_pic001.png": "images/character/bryonn_pic001.png",
    }
    GHOSTNET_INTERNET_PAGES = {}

    def ghostnet_register_internet_page(page_id, title, summary, body_lines):
        normalized_id = (page_id or "").strip().upper()
        if not normalized_id:
            return

        GHOSTNET_INTERNET_PAGES[normalized_id] = {
            "id": normalized_id,
            "title": title,
            "summary": summary,
            "body_lines": list(body_lines or []),
        }

    # Ajout de nouvelles données :
    # ghostnet_register_internet_page("WEB-XXXX", "Titre", "Résumé", ["Ligne 1", "Ligne 2"])
    ghostnet_register_internet_page(
        "WEB-0013",
        "Fiche technique : COMMUTATEUR V4",
        "Extrait d'un manuel interne sur un commutateur réseau.",
        [
            "ID validé. Chargement de l'archive réussi.",
            "Le COMMUTATEUR V4 redirige automatiquement les paquets vers des relais fantômes.",
            "Un délai anormal supérieur à 350ms indique souvent un relais compromis.",
        ],
    )
    ghostnet_register_internet_page(
        "WEB-2104",
        "Journal local : Zone 21 / Bloc 04",
        "Compte-rendu d'incidents mineurs signalés sur le réseau de proximité.",
        [
            "ID validé. Rapport récupéré.",
            "03:12 — Coupure partielle des bornes publiques pendant 7 minutes.",
            "03:41 — Reprise du trafic après redémarrage manuel du nœud principal.",
            "04:03 — Activité inhabituelle détectée sur une route secondaire.",
        ],
    )

    def ghostnet_get_dialogues(victim_id):
        return ghostnet_victims[victim_id]["dialogues"]

    def ghostnet_all_discussion_ids():
        ids = sorted(ghostnet_victims.keys())
        return [discussion_id for discussion_id in ids if ghostnet_is_discussion_unlocked(discussion_id)]

    def ghostnet_visible_discussion_ids_for_device(character_id):
        return [
            discussion_id
            for discussion_id in ghostnet_all_discussion_ids()
            if (
                ghostnet_victims[discussion_id]["device_owner"] == character_id
                or character_id in ghostnet_victims[discussion_id].get("participants", [])
            )
        ]

    def ghostnet_visible_dialogues(victim_id):
        victim = ghostnet_victims[victim_id]
        dialogues = ghostnet_get_dialogues(victim_id)
        count = min(victim["visible_count"], len(dialogues))
        return dialogues[:count]

    def ghostnet_is_discussion_unlocked(victim_id):
        victim = ghostnet_victims[victim_id]
        unlock_requirements = set(victim.get("unlock_requires", []))
        return unlock_requirements.issubset(ghostnet_unlocked_tags)

    def ghostnet_unlock_tag(tag_name):
        if tag_name:
            ghostnet_unlocked_tags.add(tag_name)

    def ghostnet_next_dialogue(victim_id):
        victim = ghostnet_victims[victim_id]
        dialogues = ghostnet_get_dialogues(victim_id)

        if victim["visible_count"] < len(dialogues):
            victim["visible_count"] += 1
            victim["last_activity"] = dialogues[victim["visible_count"] - 1]["date"]

            if victim["visible_count"] >= len(dialogues):
                ghostnet_unlock_tag(victim.get("unlock_tag"))

    def ghostnet_select_victim(victim_id):
        store.ghostnet_selected_victim = victim_id

    def ghostnet_set_module(module_name):
        store.ghostnet_active_module = module_name

    def ghostnet_set_device(character_id):
        store.ghostnet_selected_device = character_id
        visible_ids = ghostnet_visible_discussion_ids_for_device(character_id)
        if visible_ids:
            store.ghostnet_selected_victim = visible_ids[0]

    def ghostnet_unread(victim_id):
        victim = ghostnet_victims[victim_id]
        return victim["visible_count"] < len(victim["dialogues"])

    def ghostnet_gallery_for_character(character_id):
        if character_id not in ghostnet_runtime_gallery:
            ghostnet_runtime_gallery[character_id] = list(GHOSTNET_GALLERY_LIBRARY.get(character_id, []))
        return ghostnet_runtime_gallery[character_id]

    def ghostnet_profile_photo(character_id):
        gallery = ghostnet_gallery_for_character(character_id)
        if not gallery:
            return dict(GHOSTNET_PROFILE_FALLBACK)

        idx = ghostnet_profile_photo_choices.get(character_id, 0)
        idx = idx % len(gallery)
        return gallery[idx]

    def ghostnet_use_gallery_photo(character_id, photo_id):
        gallery = ghostnet_gallery_for_character(character_id)
        for idx, photo in enumerate(gallery):
            if photo["id"] == photo_id:
                ghostnet_profile_photo_choices[character_id] = idx
                return

    def ghostnet_collect_photo_from_dialogue(dialogue_chunk):
        media_image = ghostnet_dialogue_media_image(dialogue_chunk)
        speaker_id = dialogue_chunk.get("speaker_id")

        if not media_image or speaker_id not in GHOSTNET_CHARACTER_DIRECTORY or speaker_id == "system":
            return

        gallery = ghostnet_gallery_for_character(speaker_id)
        photo_id = "dlg_%s_%s_%s" % (
            speaker_id,
            dialogue_chunk.get("date", "").replace(" ", "_"),
            str(abs(hash(dialogue_chunk.get("text", ""))))[:8],
        )

        if any(photo["id"] == photo_id for photo in gallery):
            return

        gallery.append(
            {
                "id": photo_id,
                "label": "Photo %s" % dialogue_chunk.get("date", "sans date"),
                "bg": "#dcebf7",
                "fg": "#2b587b",
                "image": media_image,
            }
        )

    def ghostnet_collect_visible_dialogue_photos(character_id, victim_id):
        for chunk in ghostnet_visible_dialogues(victim_id):
            ghostnet_collect_photo_from_dialogue(chunk)

        gallery = ghostnet_gallery_for_character(character_id)
        if gallery:
            ghostnet_profile_photo_choices[character_id] = ghostnet_profile_photo_choices.get(character_id, 0) % len(gallery)

    # -------------------------------------------------------------------
    # Déclaration des images

    def ghostnet_extract_media_and_text(raw_text):
        cleaned_text = raw_text or ""
        media_image = None

        for filename in re.findall(r"\[([^\[\]]+\.png)\]", cleaned_text, flags=re.IGNORECASE):
            lower_filename = filename.lower()
            mapped_image = GHOSTNET_INLINE_IMAGE_MAP.get(lower_filename)
            if mapped_image is None:
                for character_id in GHOSTNET_CHARACTER_DIRECTORY:
                    if character_id == "system":
                        continue

                    if lower_filename.startswith(character_id + "_"):
                        candidate = "images/character/%s" % lower_filename
                        if renpy.loadable(candidate):
                            mapped_image = candidate
                            break

            if mapped_image and media_image is None:
                media_image = mapped_image
            cleaned_text = re.sub(r"\[" + re.escape(filename) + r"\]", "", cleaned_text, flags=re.IGNORECASE)

        cleaned_text = cleaned_text.strip()
        return cleaned_text, media_image

    def ghostnet_next_dialogue_and_scroll(victim_id):
        ghostnet_next_dialogue(victim_id)
        renpy.restart_interaction()

    def ghostnet_dialogue_media_image(dialogue_chunk):
        _cleaned_text, media_image = ghostnet_extract_media_and_text(dialogue_chunk.get("text", ""))
        return media_image

    def ghostnet_search_internet():
        query = (store.ghostnet_internet_query or "").strip().upper()
        page = GHOSTNET_INTERNET_PAGES.get(query)

        if page:
            store.ghostnet_internet_result_id = query
            store.ghostnet_internet_error = None
        else:
            store.ghostnet_internet_result_id = None
            store.ghostnet_internet_error = "Cette page ne donne aucun résultat."

    def ghostnet_internet_result():
        if not store.ghostnet_internet_result_id:
            return None
        return GHOSTNET_INTERNET_PAGES.get(store.ghostnet_internet_result_id)


default ghostnet_active_module = "Discussion"
default ghostnet_selected_victim = "DISC-13-04"
default ghostnet_selected_device = "romie"
default ghostnet_unlocked_tags = set()
default ghostnet_profile_photo_choices = {
    "romie": 0,
    "bryonn": 0,
}
default ghostnet_runtime_gallery = {}
default ghostnet_lightbox_image = None
default ghostnet_internet_query = ""
default ghostnet_internet_result_id = None
default ghostnet_internet_error = None
default ghostnet_victims = ghostnet_build_victims()

screen ghostnet_avatar_preview(character_id):
    $ profile_photo = ghostnet_profile_photo(character_id)
    $ display_name = GHOSTNET_CHARACTER_DIRECTORY[character_id]["speaker"]

    frame:
        background profile_photo["bg"]
        xsize 240
        ysize 120
        xpadding 10
        ypadding 10

        hbox:
            spacing 12
            frame:
                background profile_photo["fg"]
                xsize 60
                ysize 60
                xalign 0.5
                yalign 0.5
                if profile_photo.get("image"):
                    add profile_photo["image"] fit "contain" xsize 60 ysize 60
                else:
                    text display_name[0] xalign 0.5 yalign 0.5 color "#ffffff" size 30

            vbox:
                spacing 6
                text "[display_name]" color "#173042" size 20
                text "Photo profil: [profile_photo['label']]" color "#365f7d" size 14

screen ghostnet_v2_ui():
    tag menu
    modal True

    $ visible_ids = ghostnet_visible_discussion_ids_for_device(ghostnet_selected_device)

    if visible_ids and ghostnet_selected_victim not in visible_ids:
        $ ghostnet_selected_victim = visible_ids[0]

    if ghostnet_selected_victim in ghostnet_victims:
        $ _ghostnet_sync = ghostnet_collect_visible_dialogue_photos(ghostnet_selected_device, ghostnet_selected_victim)

    $ victim = ghostnet_victims[ghostnet_selected_victim] if visible_ids else None
    $ visible_dialogues = ghostnet_visible_dialogues(ghostnet_selected_victim) if victim else []
    $ all_loaded = victim and victim["visible_count"] >= len(victim["dialogues"])

    if ghostnet_active_module == "Discussion" and victim and not all_loaded:
        key "dismiss" action [
            Function(ghostnet_next_dialogue_and_scroll, ghostnet_selected_victim),
        ]

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
                    action [
                        Function(ghostnet_set_module, module),
                        SetScreenVariable("dialogue_scroll", ui.adjustment(value=1.0, range=1.0)),
                    ]
                    background ("#1e3e56" if ghostnet_active_module == module else "#4f6c80")
                    text_color "#e8f4ff"
                    text_size 18
                    xpadding 14
                    ypadding 7
            null
            text "Appareil actif : [GHOSTNET_CHARACTER_DIRECTORY[ghostnet_selected_device]['speaker']]" color "#173042" size 20

    hbox:
        xfill True
        yfill True
        spacing 14
        xpos 14
        ypos 94

        frame:
            background "#eaf3fa"
            xmaximum 680
            yfill True
            xpadding 14
            ypadding 12

            vbox:
                spacing 12

                if ghostnet_active_module == "Discussion":
                    text "Discussions ouvrables" color "#153247" size 38
                    text "Les discussions non lues apparaissent en rouge." color "#507086" size 17

                    viewport:
                        draggable True
                        mousewheel True
                        scrollbars "vertical"
                        ymaximum 490
                        xfill True

                        vbox:
                            spacing 8
                            for discussion_id in visible_ids:
                                $ item = ghostnet_victims[discussion_id]
                                $ unread = ghostnet_unread(discussion_id)
                                button:
                                    action [
                                        Function(ghostnet_select_victim, discussion_id),
                                        SetScreenVariable("dialogue_scroll", ui.adjustment(value=1.0, range=1.0)),
                                    ]
                                    background ("#c7dff1" if ghostnet_selected_victim == discussion_id else "#dcebf7")
                                    xfill True
                                    xpadding 10
                                    ypadding 10
                                    vbox:
                                        spacing 3
                                        text "[item['id']] — [item['name']]" color ("#b01e1e" if unread else "#1d3f57") size 20
                                        text "[item['summary']]" color "#355d78" size 15
                                        text "Dernière activité : [item['last_activity']]" color "#476f8c" size 14

                    if victim:
                        text "Profils participants" color "#1a3a52" size 26
                        for participant in victim["participants"]:
                            use ghostnet_avatar_preview(participant)

                elif ghostnet_active_module == "Galerie":
                    $ gallery = ghostnet_gallery_for_character(ghostnet_selected_device)
                    $ owner_name = GHOSTNET_CHARACTER_DIRECTORY[ghostnet_selected_device]["speaker"]
                    text "Galerie" color "#153247" size 38
                    text "Photos collectées pour [owner_name]." color "#507086" size 17
                    text "Chaque photo envoyée en discussion est ajoutée automatiquement ici." color "#507086" size 16
                    text "Cliquez sur une photo pour l'appliquer en photo de profil des discussions." color "#507086" size 16

                    if not gallery:
                        text "Aucune photo collectée." color "#32536a" size 20
                    else:
                        for photo in gallery:
                            frame:
                                background photo["bg"]
                                xfill True
                                xpadding 10
                                ypadding 10
                                hbox:
                                    spacing 10
                                    button:
                                        action SetVariable("ghostnet_lightbox_image", photo.get("image"))
                                        background photo["fg"]
                                        xsize 120
                                        ysize 80
                                        if photo.get("image"):
                                            add photo["image"] fit "contain" xsize 120 ysize 80
                                        else:
                                            text owner_name[0] color "#ffffff" size 24 xalign 0.5 yalign 0.5
                                    vbox:
                                        spacing 4
                                        text "[photo['label']]" color "#1d3f57" size 19
                                        if ghostnet_profile_photo(ghostnet_selected_device)["id"] == photo["id"]:
                                            text "Photo de profil active" color "#2c5b77" size 14
                                        else:
                                            textbutton "Appliquer cette photo":
                                                action [
                                                    Function(ghostnet_use_gallery_photo, ghostnet_selected_device, photo["id"]),
                                                    SetScreenVariable("dialogue_scroll", ui.adjustment(value=1.0, range=1.0)),
                                                ]
                                                background "#2e5a78"
                                                text_color "#eef7ff"
                                                text_size 14
                                                xpadding 10
                                                ypadding 4

                else:
                    if ghostnet_active_module == "Réseau":
                        text "Réseau" color "#153247" size 38
                        text "Choisissez l'appareil à inspecter." color "#507086" size 17

                        for character_id, character_data in GHOSTNET_CHARACTER_DIRECTORY.items():
                            if character_id == "system":
                                continue

                            $ available = len(ghostnet_visible_discussion_ids_for_device(character_id))
                            button:
                                action Function(ghostnet_set_device, character_id)
                                background ("#c7dff1" if ghostnet_selected_device == character_id else "#dcebf7")
                                xfill True
                                xpadding 10
                                ypadding 10
                                vbox:
                                    spacing 3
                                    text "[character_data['speaker']]" color "#1d3f57" size 21
                                    text "Appareil : [character_data['device_name']]" color "#355d78" size 15
                                    text "Discussions accessibles : [available]" color "#476f8c" size 14
                                    $ tags_for_character = sorted({ghostnet_victims[d]["unlock_tag"] for d in ghostnet_visible_discussion_ids_for_device(character_id) if ghostnet_victims[d].get("unlock_tag") and ghostnet_victims[d]["unlock_tag"] in ghostnet_unlocked_tags})
                                    if tags_for_character:
                                        text "Tags débloqués : [', '.join(tags_for_character)]" color "#476f8c" size 14
                    else:
                        text "Internet" color "#153247" size 38
                        text "Rechercher une page par ID (ex: WEB-0013)." color "#507086" size 17

                        frame:
                            background "#dcebf7"
                            xfill True
                            xpadding 10
                            ypadding 10
                            vbox:
                                spacing 8
                                input value VariableInputValue("ghostnet_internet_query", length=20) color "#133149" size 22
                                hbox:
                                    spacing 10
                                    textbutton "Rechercher":
                                        action Function(ghostnet_search_internet)
                                        background "#2e5a78"
                                        text_color "#eef7ff"
                                        text_size 16
                                        xpadding 12
                                        ypadding 6
                                    textbutton "Effacer":
                                        action [
                                            SetVariable("ghostnet_internet_query", ""),
                                            SetVariable("ghostnet_internet_result_id", None),
                                            SetVariable("ghostnet_internet_error", None),
                                        ]
                                        background "#56758b"
                                        text_color "#eef7ff"
                                        text_size 16
                                        xpadding 12
                                        ypadding 6
                                text "IDs disponibles pour la démo : [', '.join(sorted(GHOSTNET_INTERNET_PAGES.keys()))]" color "#355d78" size 14

        frame:
            background "#f1f7fc"
            xfill True
            yfill True
            xpadding 14
            ypadding 12

            vbox:
                spacing 8

                if ghostnet_active_module == "Discussion":
                    text "Discussion" color "#1c3a51" size 36

                    if not victim:
                        text "Aucune discussion disponible pour cet appareil." color "#4f7894" size 20
                    else:
                        text "[victim['name']]" color "#4f7894" size 24
                        text "Début de l'enregistrement" color "#4f7894" size 20

                        viewport:
                            draggable True
                            mousewheel True
                            scrollbars "vertical"
                            yfill True
                            xfill True
                            yinitial 1.0

                            vbox:
                                spacing 10
                                for chunk in visible_dialogues:
                                    if chunk["side"] == "center":
                                        text "[chunk['text']]" color "#5c819d" size 24 xalign 0.5
                                    else:
                                        $ clean_text, media_image = ghostnet_extract_media_and_text(chunk["text"])
                                        $ photo = ghostnet_profile_photo(chunk["speaker_id"])
                                        hbox:
                                            spacing 8
                                            if chunk["side"] == "right":
                                                null width 180
                                            frame:
                                                background photo["fg"]
                                                xsize 84
                                                ysize 84
                                                if photo.get("image"):
                                                    add photo["image"] fit "contain" xsize 84 ysize 84
                                                else:
                                                    text chunk["speaker"][0] color "#ffffff" size 36 xalign 0.5 yalign 0.5
                                            frame:
                                                background ("#ffffff" if chunk["side"] == "left" else "#d2e6f6")
                                                xmaximum 760
                                                xpadding 12
                                                ypadding 8
                                                vbox:
                                                    spacing 2
                                                    text "[chunk['speaker']]   [chunk['date']]" color "#32536a" size 15
                                                    if clean_text:
                                                        text "[clean_text]" color "#112c40" size 21
                                                    if media_image:
                                                        null height 4
                                                        button:
                                                            action SetVariable("ghostnet_lightbox_image", media_image)
                                                            background "#ecf4fb"
                                                            xsize 360
                                                            ysize 240
                                                            add media_image fit "contain" xsize 360 ysize 240
                                            if chunk["side"] == "left":
                                                null width 180
                                null height 85

                        frame:
                            background "#d4e4f2"
                            xfill True
                            xpadding 10
                            ypadding 8
                            vbox:
                                spacing 5
                                text "Dernière activité : [victim['last_activity']]" color "#1b3b51" size 16
                                if not all_loaded:
                                    text "Cliquez pour afficher le dialogue suivant." color "#315976" size 16
                                else:
                                    text "Tous les messages sont affichés." color "#315976" size 16
                                    if victim.get("unlock_tag"):
                                        text "Tag débloqué : [victim['unlock_tag']]" color "#315976" size 16
                                    if victim.get("unlocks_discussions"):
                                        text "Nouvelles discussions : [', '.join(victim['unlocks_discussions'])]" color "#315976" size 16
                                    if victim.get("unlocks_content"):
                                        text "Nouveaux contenus : [', '.join(victim['unlocks_content'])]" color "#315976" size 16

                elif ghostnet_active_module == "Galerie":
                    $ current_profile = ghostnet_profile_photo(ghostnet_selected_device)
                    text "Profil appliqué" color "#1c3a51" size 36
                    frame:
                        background current_profile["bg"]
                        xfill True
                        xpadding 12
                        ypadding 12
                        vbox:
                            spacing 5
                            text "Photo active : [current_profile['label']]" color "#24455f" size 22
                            text "Cette photo est utilisée dans les discussions de ce personnage." color "#3b607b" size 16
                            if current_profile.get("image"):
                                frame:
                                    background "#d7e8f6"
                                    xsize 320
                                    ysize 220
                                    add current_profile["image"] fit "contain" xsize 320 ysize 220

                elif ghostnet_active_module == "Réseau":
                    text "État du réseau" color "#1c3a51" size 36
                    text "Tags débloqués" color "#4f7894" size 20
                    if ghostnet_unlocked_tags:
                        for tag in sorted(ghostnet_unlocked_tags):
                            text "• [tag]" color "#2d5168" size 18
                    else:
                        text "Aucun tag débloqué." color "#2d5168" size 18
                else:
                    $ internet_page = ghostnet_internet_result()
                    text "Navigateur GHOSTNET" color "#1c3a51" size 36
                    if ghostnet_internet_error:
                        frame:
                            background "#f6dede"
                            xfill True
                            xpadding 12
                            ypadding 10
                            text "[ghostnet_internet_error]" color "#7c2020" size 21
                    elif internet_page:
                        frame:
                            background "#d7e8f6"
                            xfill True
                            xpadding 12
                            ypadding 10
                            vbox:
                                spacing 6
                                text "Résultat : [internet_page['id']]" color "#21455f" size 18
                                text "[internet_page['title']]" color "#16374d" size 28
                                text "[internet_page['summary']]" color "#315976" size 18
                        viewport:
                            draggable True
                            mousewheel True
                            scrollbars "vertical"
                            yfill True
                            xfill True
                            frame:
                                background "#ffffff"
                                xfill True
                                xpadding 12
                                ypadding 12
                                vbox:
                                    spacing 10
                                    for line in internet_page["body_lines"]:
                                        text "[line]" color "#112c40" size 20
                    else:
                        text "Aucune page chargée. Saisissez un ID puis cliquez sur Rechercher." color "#32536a" size 19

    if ghostnet_lightbox_image:
        frame:
            background "#000c"
            xfill True
            yfill True
            button:
                action SetVariable("ghostnet_lightbox_image", None)
                background None
                xfill True
                yfill True

            frame:
                background "#10283a"
                xalign 0.5
                yalign 0.5
                xsize 980
                ysize 680
                xpadding 14
                ypadding 14
                vbox:
                    spacing 10
                    add ghostnet_lightbox_image fit "contain" xsize 952 ysize 610
                    textbutton "Fermer":
                        action SetVariable("ghostnet_lightbox_image", None)
                        xalign 1.0
                        background "#2e5a78"
                        text_color "#eef7ff"
                        text_size 16
                        xpadding 12
                        ypadding 6

label ghostnet_demo:
    call screen ghostnet_v2_ui
    return
