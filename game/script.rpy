define s = Character("Spectre", what_prefix="“", what_suffix="”")

label start:
    scene black
    $ terminal_mode = False

    s "Bienvenue dans GHOSTNET."
    s "Le terminal a été retiré : toute l'opération passe par l'interface de discussions."
    s "Les dialogues sont désormais séquentiels, longs et déterministes."
    s "Clique pour faire défiler chaque message dans l'ordre exact de la conversation."
    s "Tu peux choisir l'image de profil de chaque personnage à gauche."

    call screen ghostnet_v2_ui

    s "Session terminée."
    return
