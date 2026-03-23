init -1 python:
    JOUR_DISC_1304 = "13 avr."
    dialogue = ghostnet_dialogue_builder(JOUR_DISC_1304)

    ghostnet_register_discussion(
        discussion_id="DISC-13-04",
        name="SESSION ENTRANTE",
        summary="Conversation interceptée. Défilement manuel en mode lecture.",
        day=JOUR_DISC_1304,
        participants=["romie", "bryonn"],
        device_owner="romie",
        unlock_tag="TAG:CARTE_PLATINUM",
        unlocks_discussions=["DISC-21-04"],
        unlocks_content=["Dossier achats Bonton"],
        entries=[
            dialogue("romie", "Putain Bryonn je suis dég."),
            dialogue("romie", "J’ai vu le QR code réduction 60% sur le nouveau top asymétrique en vitrine (le noir avec les découpes sur les côtés)."),
            dialogue("romie", "Je l’ai scanné direct, j’étais sûre que ça allait marcher, la pub disait « valable aujourd’hui seulement pour les 500 premières »."),
            dialogue("romie", "Et rien. Le code a buggé, le caissier m’a regardée comme si j’étais une fraudeuse."),
            dialogue("romie", "J’ai dû le payer plein pot. 89 crédits. Pour un bout de tissu."),
            dialogue("bryonn", "Sérieux ? Encore un de ces codes foireux…"),
            dialogue("bryonn", "Ils font exprès pour qu’on scanne et qu’ils trackent nos achats."),
            dialogue("bryonn", "T’as quand même essayé en cabine ?"),
            dialogue("romie", "Ouais… et franchement, il me va trop bien."),
            dialogue("romie", "Les découpes tombent pile où il faut, ça dégage les hanches et le dos."),
            dialogue("romie", "Avec la jupe réglementaire grise en dessous c’est hyper… provocant."),
            dialogue("romie", "Je me suis sentie un peu trop exposée devant le miroir, mais j’ai kiffé."),
            dialogue("romie", "Dommage que t’étais pas là pour voir."),
            dialogue("romie", "[envoie photo] Regarde ça."),
            dialogue("romie", "Je me suis dit « si la réduction marchait pas, au moins je vais le prendre pour le porter ce soir quand tu rentres »."),
            dialogue("romie", "Mais là je suis crevée et un peu vénère."),
            dialogue("romie", "Tu finis à quelle heure ? J’ai envie qu’on se pose, que tu me déshabilles lentement… histoire de me consoler de ces 89 crédits volés."),
            dialogue("bryonn", "Merde Romie… cette photo."),
            dialogue("bryonn", "Je finis dans 45 min."),
            dialogue("bryonn", "Rentre direct, garde-le sur toi."),
            dialogue("bryonn", "Je m’occupe du reste."),
            dialogue("system", "Session close."),
        ],
    )
