define s = Character("Spectre", what_prefix="“", what_suffix="”")

label start:
    scene black

    show screen terminal_ui

    s "Le terminal est verrouillé à l'écran. On fait tout depuis ici."
    s "Tape help pour la base, puis commence à scanner et infecter des cibles."
    s "Le vieux noyau GhostOS n'a plus de téléphone. Seulement la ligne de commande."

<<<<<<< Updated upstream
    "Le CRT vibre faiblement. Chaque commande peut augmenter le heat."
    "Essaye : prompt set \"ghost@darknet[HEAT:%heat%]:~$ \""
    "Puis : scan victim42, infect victim42 --method phish, grab victim42 --data passwords"
=======
    $ switch_channel_view("ops_feed")
    $ send_phone_message("", "22:12 // Appartement de Spectre", "ops_feed", 1)
    $ send_phone_message("NEXUS", "Rapport.", "ops_feed")
    $ send_phone_message(phone_config["phone_player_name"], "Le faux QR code dans la boutique miteuse a marché.", "ops_feed")
    $ send_phone_message(phone_config["phone_player_name"], "Identifiants siphonnés: Nora Vex.", "ops_feed")
    $ send_phone_message("NEXUS", "Confirme l'empreinte.", "ops_feed")
    $ send_phone_message(phone_config["phone_player_name"], "Token capturé: QR-8841-GH0ST.", "ops_feed")
>>>>>>> Stashed changes

    s "Tu peux rester ici autant que tu veux et expérimenter les scripts dans /scripts/."

    return
