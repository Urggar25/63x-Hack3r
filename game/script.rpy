define s = Character("Spectre", what_prefix="“", what_suffix="”")

label start:
    scene black

    show screen terminal_ui
    show screen ghost_net_ui

    s "Le terminal est verrouillé à l'écran. On fait tout depuis ici."
    s "Tape help pour la base, puis victims pour ouvrir Ghost Net. Raccourci direct: V."
    s "Le CRT vibre faiblement. Chaque commande peut augmenter le heat."
    "Essaye : prompt set \"ghost@darknet[HEAT:%heat%]:~$ \""
    "Puis : scan victim42, infect victim42 --method phish, grab victim42 --data passwords."

    s "Tu peux rester ici autant que tu veux et expérimenter les scripts dans /scripts/."

    return
