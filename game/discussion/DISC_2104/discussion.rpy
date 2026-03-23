init -1 python:
    JOUR_DISC_2104 = "21 avr."
    dialogue = ghostnet_dialogue_builder(JOUR_DISC_2104)

    ghostnet_register_discussion(
        discussion_id="DISC-21-04",
        name="SUIVI BOUTIQUE",
        summary="Historique d'achats et validation des paniers.",
        day=JOUR_DISC_2104,
        participants=["josef", "cassandra"],
        device_owner="josef",
        unlock_tag="TAG:PANIER_TERMINE",
        unlock_requires=["TAG:CARTE_PLATINUM"],
        unlocks_content=["Photo: Ticket caisse Bonton"],
        entries=[
            dialogue("system", "Canal restauré.", side="center"),
            dialogue("cassandra", "J'ai tout pris, même les chaussures holographiques."),
            dialogue("josef", "Parfait, récupère aussi le reçu."),
            dialogue("cassandra", "C'est fait. Je t'envoie la photo."),
            dialogue("system", "Fin de la discussion."),
        ],
    )
