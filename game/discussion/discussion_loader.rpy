init -2 python:
    GHOSTNET_CHARACTER_DIRECTORY = {
        "josef": {"speaker": "Josef Langley", "default_side": "right"},
        "cassandra": {"speaker": "Cassandra Watergate", "default_side": "left"},
        "system": {"speaker": "Système", "default_side": "center"},
    }

    ghostnet_discussions = {}

    def ghostnet_register_discussion(discussion_id, name, summary, day, participants, entries):
        ghostnet_discussions[discussion_id] = {
            "name": name,
            "id": discussion_id,
            "summary": summary,
            "day": day,
            "participants": participants,
            "dialogues": entries,
        }

    def ghostnet_dialogue_builder(day):
        def line(speaker_id, text, side=None):
            profile = GHOSTNET_CHARACTER_DIRECTORY[speaker_id]
            resolved_side = side if side is not None else profile["default_side"]
            return {
                "speaker_id": speaker_id,
                "speaker": profile["speaker"],
                "side": resolved_side,
                "date": day,
                "text": text,
            }

        return line

    def ghostnet_build_victims():
        victims = {}

        for discussion_id, discussion_data in ghostnet_discussions.items():
            dialogues = list(discussion_data["dialogues"])
            initial_count = 1 if dialogues else 0
            last_activity = dialogues[0]["date"] if dialogues else discussion_data["day"]

            victims[discussion_id] = {
                "name": discussion_data["name"],
                "id": discussion_id,
                "summary": discussion_data["summary"],
                "participants": discussion_data["participants"],
                "last_activity": last_activity,
                "visible_count": initial_count,
                "dialogues": dialogues,
            }

        return victims
