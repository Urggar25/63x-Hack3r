init -1 python:
    JOUR_DISC_2404 = "24 avr."
    dialogue = ghostnet_dialogue_builder(JOUR_DISC_2404)

    ghostnet_register_discussion(
        discussion_id="DISC-24-04",
        name="FLUX PERSONNEL",
        summary="Messages retrouvés sur l'appareil de Romie.",
        day=JOUR_DISC_2404,
        participants=["romie", "bryonn"],
        device_owner="romie",
        unlock_tag="TAG:RESEAU_CASSANDRA",
        entries=[
            dialogue("romie", "On garde cette discussion sur mon appareil."),
            dialogue("bryonn", "Parfait, je vois bien que tu as plusieurs boîtes actives."),
            dialogue("romie", "La galerie est prête aussi, au cas où."),
            dialogue("system", "Synchronisation réseau terminée.", side="center"),
        ],
    )
