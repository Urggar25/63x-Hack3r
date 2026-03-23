define s = Character("Spectre", what_prefix="“", what_suffix="”")

label start:
    scene black
    $ terminal_mode = False

    s "Bienvenue dans GHOSTNET."
    s "Des messages bug s'affichent partout à l'écran... parfait."
    s "Quelqu'un vient de scanner mon faux QR-Code."
    s "Enfin une cible qui va me faire gagner un peu d'argent."
    s "Le terminal a été retiré : toute l'opération passe par l'interface Orwellienne."
    s "Analyse les datachunks, tagge les preuves, développe le graphe de relations et surveille ton Heat."

    call screen ghostnet_v2_ui

    s "Session terminée."
    return
