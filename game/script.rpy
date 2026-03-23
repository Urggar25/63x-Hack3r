define s = Character("Spectre", what_prefix="“", what_suffix="”")

label start:
    scene black

    show screen terminal_ui

    s "Le terminal est verrouillé à l'écran. On fait tout depuis ici."
    s "Tape help pour la base, puis commence à scanner et infecter des cibles."
    s "Le vieux noyau GhostOS n'a plus de téléphone. Seulement la ligne de commande."

    "Le CRT vibre faiblement. Chaque commande peut augmenter le heat."
    "Essaye : prompt set \"ghost@darknet[HEAT:%heat%]:~$ \""
    "Puis : scan victim42, infect victim42 --method phish, grab victim42 --data passwords"

    s "Tu peux rester ici autant que tu veux et expérimenter les scripts dans /scripts/."

    return
