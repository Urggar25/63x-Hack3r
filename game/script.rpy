# please see phone.rpy for more info and license

define s = Character("Spectre", what_prefix="“", what_suffix="”")

init python:
    intrusion_state = {
        "operation_name": "MIROIR NOIR",
        "stolen_credentials": {},
        "infected_devices": set(),
        "propagation_links": [],
    }

    def initialize_hacker_phone():
        reset_phone_data()
        set_phone_theme("dark")
        phone_config["phone_player_name"] = "Spectre"
        phone_config["channels_title"] = "Ghost Relay"
        phone_config["history_timestamp_prefix"] = "Trace"
        phone_config["pause"]["pause_time"] = False
        phone_config["pause"]["pause_length"] = 0.55

        create_phone_channel("ops_feed", "NEXUS // Supervision", ["NEXUS", phone_config["phone_player_name"]], "phone/icon.png")
        create_phone_channel("target_nora", "Nora Vex", ["Nora Vex", phone_config["phone_player_name"]], "phone/icons/vanessa.png")
        create_phone_channel("market_watch", "Caméras // Boutique 13", ["NEXUS", "Drone-Cam"], "phone/icon.png", is_group=True)

    def log_credential_theft(victim_name, location, token):
        intrusion_state["stolen_credentials"][victim_name] = {
            "location": location,
            "token": token,
        }
        intrusion_state["infected_devices"].add(victim_name)
        register_spy_target(victim_name)

    def infect_device(source_name, target_name, channel_id, display_name, participants, icon_path="phone/icon.png"):
        if channel_id not in phone_channel_data:
            create_phone_channel(channel_id, display_name, participants, icon_path, is_group=True)
        intrusion_state["infected_devices"].add(target_name)
        intrusion_state["propagation_links"].append((source_name, target_name))
        register_spy_target(target_name)

    def send_infection_trace(source_name, target_name, channel_id):
        send_phone_message("", "Propagation latérale détectée", channel_id, 1)
        send_phone_message("Daemon", "Nœud source: %s" % source_name, channel_id)
        send_phone_message("Daemon", "Nœud cible: %s" % target_name, channel_id)
        send_phone_message("Daemon", "Statut: accès micro + messages + galerie", channel_id)

label start:
    scene black

    play sound sfx_phone_vibration
    s "Enfin. C'est parti."
    s "Quelqu'un a mordu à l'hameçon."

    window hide
    $ initialize_hacker_phone()
    $ log_credential_theft("Nora Vex", "Boutique 13 // Vieille ville", "QR-8841-GH0ST")
    show screen phone_ui

    $ send_phone_message("", "22:12 // Appartement de Spectre", "ops_feed", 1)
    $ send_phone_message("NEXUS", "Rapport.", "ops_feed")
    $ send_phone_message(phone_config["phone_player_name"], "Le faux QR code dans la boutique miteuse a marché.", "ops_feed")
    $ send_phone_message(phone_config["phone_player_name"], "Identifiants siphonnés: Nora Vex.", "ops_feed")
    $ send_phone_message("NEXUS", "Confirme l'empreinte.", "ops_feed")
    $ send_phone_message(phone_config["phone_player_name"], "Token capturé: QR-8841-GH0ST.", "ops_feed")

    $ send_phone_message("Drone-Cam", "Capture rue validée. La cible a scanné le code sans hésiter.", "market_watch")
    $ send_phone_message("NEXUS", "Injection du spyware maison autorisée.", "market_watch")

    $ send_phone_message("", "Canal compromis // Nora Vex", "target_nora", 1)
    $ send_phone_message("Nora Vex", "J'ai trouvé un vrai coupon miracle dans cette boutique horrible.", "target_nora")
    $ send_phone_message("Nora Vex", "Mon téléphone bug un peu depuis... sûrement rien.", "target_nora")
    $ send_phone_message("Daemon", "Implant actif. Exfiltration des conversations en temps réel.", "target_nora")
    $ send_phone_message("Nora Vex", "phone/media/food.png", "target_nora", 2, summary_alt="Photo reçue")

    $ switch_channel_view("ops_feed")
    $ send_phone_message("NEXUS", "La charge virale peut se propager à ses contacts. Choisis la prochaine cible.", "ops_feed")

    $ present_phone_choices([
        ("Cibler Jules", "Infecte Jules, chauffeur clandestin.", Jump("infect_jules_choice")),
        ("Cibler Imani", "Infecte Docteure Imani, clinique de fortune.", Jump("infect_imani_choice"))
    ], "ops_feed")
    jump post_target_choice

label infect_jules_choice:
    $ infect_device("Nora Vex", "Jules Rane", "jules_thread", "Relais // Jules Rane", ["Jules Rane", "Nora Vex"], "phone/icons/avery.png")
    $ send_infection_trace("Nora Vex", "Jules Rane", "jules_thread")
    $ send_phone_message("Jules Rane", "J'ai livré le colis près du checkpoint militaire. Personne ne m'a suivi.", "jules_thread")
    $ send_phone_message("Nora Vex", "Garde ton calme. Les drones tournent toute la nuit.", "jules_thread")
    $ send_phone_message("Daemon", "Nouveau carnet d'adresses exfiltré depuis Jules Rane.", "jules_thread")
    $ send_phone_message("NEXUS", "Bon choix. Les itinéraires de contrebande valent cher.", "ops_feed")
    jump post_target_choice

label infect_imani_choice:
    $ infect_device("Nora Vex", "Docteure Imani", "imani_thread", "Relais // Docteure Imani", ["Docteure Imani", "Nora Vex"], "phone/icons/study_buddies.png")
    $ send_infection_trace("Nora Vex", "Docteure Imani", "imani_thread")
    $ send_phone_message("Docteure Imani", "La réserve d'antiviraux est vide. Les enfants de la zone rouge rechutent.", "imani_thread")
    $ send_phone_message("Nora Vex", "Je peux tenter le marché noir, mais les prix ont triplé.", "imani_thread")
    $ send_phone_message("Daemon", "Dossiers médicaux chiffrés copiés. Déchiffrement en tâche de fond.", "imani_thread")
    $ send_phone_message("NEXUS", "Bon choix. Les données biométriques ouvrent toutes les portes.", "ops_feed")
    jump post_target_choice

label post_target_choice:

    $ create_phone_channel("spread_map", "Propagation // Carte virale", ["Daemon", phone_config["phone_player_name"]], "phone/icon.png", is_group=True)
    $ send_phone_message("", "Synthèse automatique", "spread_map", 1)
    $ send_phone_message("Daemon", "Appareils infectés: %d" % len(intrusion_state["infected_devices"]), "spread_map")

    python:
        for source, target in intrusion_state["propagation_links"]:
            send_phone_message("Daemon", "%s  ->  %s" % (source, target), "spread_map")

    $ send_phone_message("Daemon", "Le virus se réplique à chaque pièce jointe ouverte.", "spread_map")
    $ send_phone_message("Daemon", "Probabilité de compromission globale du district en 72h: 78%.", "spread_map")

    # Démo explicite de la règle Joseph-Marie visible depuis les deux cibles.
    $ infect_device("Nora Vex", "Joseph", "joseph_marie", "Joseph ↔ Marie", ["Joseph", "Marie"], "phone/icons/avery.png")
    $ infect_device("Joseph", "Marie", "joseph_marie", "Joseph ↔ Marie", ["Joseph", "Marie"], "phone/icons/study_buddies.png")
    $ send_phone_message("", "Canal miroir actif // Joseph-Marie", "joseph_marie", 1)
    $ send_phone_message("Joseph", "Je passe au checkpoint nord dans 20 minutes.", "joseph_marie")
    $ send_phone_message("Marie", "Reçu. J'efface le trajet après lecture.", "joseph_marie")
    $ send_phone_message("Joseph", "phone/media/run.png", "joseph_marie", 2, summary_alt="Photo interceptée")

    $ switch_channel_view("ops_feed")
    $ send_phone_message("NEXUS", "Tu vois ? Une seule arnaque QR, et toute la ville devient transparente.", "ops_feed")
    $ send_phone_message(phone_config["phone_player_name"], "Je n'espionne plus des téléphones. J'écoute un monde en train de mourir.", "ops_feed")
    $ send_phone_message("NEXUS", "Continue, Spectre. Le silence est notre seule morale.", "ops_feed")

    pause
    hide screen phone_ui
    $ phone_end()
    window show

    "La pluie acide frappe les vitres comme du code qui s'effondre."
    "Ton application tourne encore, tapie dans les poches de centaines d'inconnus."
    "Dans cette dystopie, chaque notification est une confession forcée."

    return
