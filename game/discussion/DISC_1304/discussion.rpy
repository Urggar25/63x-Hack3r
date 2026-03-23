init -1 python:
    JOUR_DISC_1304 = "13 avr."
    dialogue = ghostnet_dialogue_builder(JOUR_DISC_1304)

    ghostnet_register_discussion(
        discussion_id="DISC-13-04",
        name="SESSION ENTRANTE",
        summary="Conversation interceptée. Défilement manuel en mode lecture.",
        day=JOUR_DISC_1304,
        participants=["josef", "cassandra"],
        device_owner="josef",
        unlock_tag="TAG:CARTE_PLATINUM",
        unlocks_discussions=["DISC-21-04"],
        unlocks_content=["Dossier achats Bonton"],
        entries=[
            dialogue("josef", "Salut, toi."),
            dialogue("cassandra", "Coucou jossi :)"),
            dialogue("josef", "Ma carte de crédit a disparu. J'imagine que tu l'as prise ?"),
            dialogue("cassandra", "euuh... bien vu Sherlock !"),
            dialogue("cassandra", "Je suis en train d'acheter tout Bonton avec cette carte platinum que j'ai prise sur ton bureau...."),
            dialogue("cassandra", "tu ne peux plus m'arrêter !!"),
            dialogue("josef", "Tu as de la chance, tes folies ne me dérangent pas, tant que tu passes prendre du vin pour le dîner."),
            dialogue("system", "Session close."),
        ],
    )
