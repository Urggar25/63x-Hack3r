init -2 python:
    GHOSTNET_CHARACTER_DIRECTORY = {
        "romie": {"speaker": "Romie Guillet", "default_side": "right", "device_name": "Mon X-Phone"},
        "bryonn": {"speaker": "Bryonn Guillet", "default_side": "left", "device_name": "X-Phone de Bryonn"},
        "system": {"speaker": "Système", "default_side": "center"},
    }

    ghostnet_discussions = {}

    def ghostnet_register_discussion(
        discussion_id,
        name,
        summary,
        day,
        participants,
        entries,
        device_owner,
        unlock_tag=None,
        unlock_requires=None,
        unlocks_discussions=None,
        unlocks_content=None,
    ):
        ghostnet_discussions[discussion_id] = {
            "name": name,
            "id": discussion_id,
            "summary": summary,
            "day": day,
            "participants": participants,
            "dialogues": entries,
            "device_owner": device_owner,
            "unlock_tag": unlock_tag,
            "unlock_requires": list(unlock_requires or []),
            "unlocks_discussions": list(unlocks_discussions or []),
            "unlocks_content": list(unlocks_content or []),
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
                "device_owner": discussion_data["device_owner"],
                "unlock_tag": discussion_data["unlock_tag"],
                "unlock_requires": discussion_data["unlock_requires"],
                "unlocks_discussions": discussion_data["unlocks_discussions"],
                "unlocks_content": discussion_data["unlocks_content"],
                "last_activity": last_activity,
                "visible_count": initial_count,
                "dialogues": dialogues,
            }

        return victims
