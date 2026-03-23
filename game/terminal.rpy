init -2 python:
    import os
    import json
    import datetime
    import random
    import shlex
    import renpy.store as store

    class TerminalEngine(object):
        def __init__(self):
            self.max_buffer = 500
            self.max_history = 200
            self.prompt_cfg_path = os.path.join(config.basedir, "game", "saves", "terminal_prompt.cfg")
            self.reset_runtime()
            self.load_prompt_cfg()

        def reset_runtime(self):
            self.cwd = "/"
            self.fs = {
                "/": {
                    "type": "dir",
                    "children": {
                        "logs": {"type": "dir", "children": {"boot.log": {"type": "file", "content": "[BOOT] Ghost kernel loaded.\n[OK] RetroCRT enabled."}}},
                        "tools": {"type": "dir", "children": {"readme.txt": {"type": "file", "content": "use help or man <command>."}}},
                        "victims": {"type": "dir", "children": {}},
                        "scripts": {"type": "dir", "children": {"auto_grab.sh": {"type": "file", "content": "for target in victims/*; do grab $target --data photos; done"}}},
                        "notes.txt": {"type": "file", "content": "Terminal GhostOS v0.1"},
                    },
                }
            }
            self.output = []
            self.history = []
            self.history_cursor = None
            self.input = ""
            self.prompt_text = "ghost@shadow:~# "
            self.prompt_color = "#00ff66"
            self.input_color = "#99ffcc"
            self.text_color = "#66ff99"
            self.glitch = 0.2
            self.font_scale = 1
            self.fullscreen = False
            self.heat = 12
            self.ghostlevel = 1
            self.victims = {
                "nora": {
                    "display_name": "Nora Vex",
                    "status": "infected",
                    "infection": 82,
                    "heat": 48,
                    "value": 9,
                    "data": ["messages", "photos", "location"],
                    "location": "Old Town",
                    "job": "OnlyFanz Creator",
                    "relationship": "Mariée (instable)",
                    "tags": ["Mariée", "Endettée", "Créatrice"],
                    "last_activity": "il y a 12 min",
                    "connections": ["jules", "mika", "daria"],
                    "timeline": [
                        {"ts": "14:32", "type": "message", "text": "« je t'attends ce soir… »"},
                        {"ts": "15:02", "type": "photo", "text": "Nouvelle photo intime"},
                        {"ts": "15:28", "type": "search", "text": "divorce avocat"},
                    ],
                },
                "jules": {
                    "display_name": "Jules Mercer",
                    "status": "scanned",
                    "infection": 27,
                    "heat": 22,
                    "value": 5,
                    "data": [],
                    "location": "North Checkpoint",
                    "job": "Barista chez CheapCoffee",
                    "relationship": "Célibataire",
                    "tags": ["Dépensier", "Insomniaque"],
                    "last_activity": "il y a 43 min",
                    "connections": ["nora"],
                    "timeline": [
                        {"ts": "13:05", "type": "call", "text": "Appel 08:22 avec Nora"},
                        {"ts": "13:57", "type": "location", "text": "Quartier North Checkpoint"},
                    ],
                },
                "mika": {
                    "display_name": "Mika Sol",
                    "status": "infected",
                    "infection": 66,
                    "heat": 73,
                    "value": 7,
                    "data": ["messages", "passwords"],
                    "location": "Dockside",
                    "job": "Analyste cyber (freelance)",
                    "relationship": "En couple toxique",
                    "tags": ["Hacker", "Paranoïaque"],
                    "last_activity": "il y a 3 min",
                    "connections": ["nora", "daria", "eon"],
                    "timeline": [
                        {"ts": "15:40", "type": "alert", "text": "Antivirus scan détecté"},
                        {"ts": "15:44", "type": "message", "text": "Parle de cybersécurité dans ses DM"},
                    ],
                },
            }
            self.running_jobs = []
            self.echo_banner()

        def echo_banner(self):
            self.push("Ghost Terminal // always-on shell")
            self.push("Type 'help' to list commands.")

        def push(self, msg, is_error=False):
            prefix = "[ERR] " if is_error else ""
            self.output.append(prefix + msg)
            self.output = self.output[-self.max_buffer:]

        def save_prompt_cfg(self):
            data = {
                "prompt_text": self.prompt_text,
                "prompt_color": self.prompt_color,
                "input_color": self.input_color,
                "glitch": self.glitch,
                "font_scale": self.font_scale,
            }
            try:
                with open(self.prompt_cfg_path, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
            except Exception:
                pass

        def load_prompt_cfg(self):
            try:
                if os.path.exists(self.prompt_cfg_path):
                    with open(self.prompt_cfg_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    self.prompt_text = data.get("prompt_text", self.prompt_text)
                    self.prompt_color = data.get("prompt_color", self.prompt_color)
                    self.input_color = data.get("input_color", self.input_color)
                    self.glitch = float(data.get("glitch", self.glitch))
                    self.font_scale = int(data.get("font_scale", self.font_scale))
            except Exception:
                pass

        def resolved_prompt(self):
            now = datetime.datetime.utcnow().strftime("%Y-%m-%d")
            return (
                self.prompt_text
                .replace("%heat%", str(self.heat))
                .replace("%victims%", str(len(self.victims)))
                .replace("%date%", now)
                .replace("%ghostlevel%", str(self.ghostlevel))
            )

        def _split_path(self, p):
            bits = [b for b in p.split("/") if b]
            return bits

        def _resolve_abs(self, p):
            if not p:
                return self.cwd
            if p.startswith("/"):
                current = []
                parts = self._split_path(p)
            else:
                current = self._split_path(self.cwd)
                parts = self._split_path(p)
            for bit in parts:
                if bit == ".":
                    continue
                if bit == "..":
                    if current:
                        current.pop()
                else:
                    current.append(bit)
            return "/" + "/".join(current)

        def _node(self, abs_path):
            cur = self.fs["/"]
            if abs_path == "/":
                return cur
            for bit in self._split_path(abs_path):
                if cur["type"] != "dir" or bit not in cur["children"]:
                    return None
                cur = cur["children"][bit]
            return cur

        def _parse_args(self, raw):
            try:
                return shlex.split(raw)
            except Exception:
                return raw.strip().split()

        def run_input(self):
            raw = (self.input or "").strip()
            if not raw:
                return
            prompt = self.resolved_prompt()
            self.push("{}{}".format(prompt, raw))
            self.history.append(raw)
            self.history = self.history[-self.max_history:]
            self.history_cursor = None
            self.input = ""
            self.execute(raw)

        def navigate_history(self, direction):
            if not self.history:
                return
            if self.history_cursor is None:
                self.history_cursor = len(self.history)
            self.history_cursor = max(0, min(len(self.history) - 1, self.history_cursor + direction))
            self.input = self.history[self.history_cursor]

        def composing_line(self):
            return "{}{}".format(self.resolved_prompt(), self.input or "")

        def autocomplete(self):
            chunk = (self.input or "").strip()
            if not chunk:
                return
            tokens = chunk.split()
            commands = sorted(self.command_table().keys())
            if len(tokens) <= 1 and not chunk.endswith(" "):
                matches = [c for c in commands if c.startswith(tokens[0])]
                if len(matches) == 1:
                    self.input = matches[0] + " "
                    self.push("[auto] {}".format(matches[0]))
                elif matches:
                    self.push("matches: " + ", ".join(matches[:8]))
                return
            if len(tokens) >= 2:
                partial = tokens[-1]
                victim_matches = [v for v in self.victims.keys() if v.startswith(partial)]
                flag_matches = [f for f in ["--method", "--data", "--webcam", "--screen", "--mic", "--start", "--stop", "--verbose", "--quiet", "--force"] if f.startswith(partial)]
                matches = victim_matches + flag_matches
                if len(matches) == 1:
                    tokens[-1] = matches[0]
                    self.input = " ".join(tokens) + " "
                    self.push("[auto] {}".format(matches[0]))
                elif matches:
                    self.push("choices: " + ", ".join(matches[:8]))

        def command_table(self):
            return {
                "help": self.cmd_help,
                "man": self.cmd_man,
                "ls": self.cmd_ls,
                "dir": self.cmd_ls,
                "cd": self.cmd_cd,
                "cat": self.cmd_cat,
                "type": self.cmd_cat,
                "echo": self.cmd_echo,
                "clear": self.cmd_clear,
                "cls": self.cmd_clear,
                "history": self.cmd_history,
                "exit": self.cmd_exit,
                "prompt": self.cmd_prompt,
                "scan": self.cmd_scan,
                "infect": self.cmd_infect,
                "i": self.cmd_infect,
                "grab": self.cmd_grab,
                "spy": self.cmd_spy,
                "watch": self.cmd_watch,
                "keylog": self.cmd_keylog,
                "victims": self.cmd_victims,
                "profile": self.cmd_profile,
                "market": self.cmd_market,
                "heat": self.cmd_heat,
                "propagate": self.cmd_propagate,
                "deepfake": self.cmd_deepfake,
                "erase": self.cmd_erase,
                "script": self.cmd_script,
                "panic": self.cmd_panic,
                "ghostmode": self.cmd_ghostmode,
                "sleep": self.cmd_sleep,
            }

        def execute(self, raw):
            argv = self._parse_args(raw)
            if not argv:
                return
            cmd = argv[0].lower()
            handler = self.command_table().get(cmd)
            if not handler:
                self.heat = min(100, self.heat + 1)
                self.push("Connection refused by endpoint security (unknown command: {}).".format(cmd), is_error=True)
                return
            try:
                handler(argv[1:])
            except Exception:
                self.heat = min(100, self.heat + 2)
                self.push("Kernel trap while running '{}'".format(cmd), is_error=True)

        def cmd_help(self, args):
            self.push("Core: ls/cd/cat/echo/clear/help/man/history/exit")
            self.push("Gameplay: scan infect(i) grab spy watch keylog victims profile market heat")
            self.push("Advanced: propagate deepfake erase script panic ghostmode")

        def cmd_man(self, args):
            if not args:
                self.push("usage: man <command>")
                return
            name = args[0]
            manuals = {
                "infect": "infect <target> --method qr|phish|sms [--verbose|--quiet|--force]",
                "scan": "scan <email|phone|username> -> creates victim card",
                "prompt": "prompt set|color|glitch|reset",
                "script": "script run <name> -> executes /scripts/<name>",
            }
            self.push(manuals.get(name, "No manual entry for {}".format(name)))

        def cmd_ls(self, args):
            target = self._resolve_abs(args[0]) if args else self.cwd
            node = self._node(target)
            if not node or node["type"] != "dir":
                self.push("ls: cannot access {}".format(target), is_error=True)
                return
            self.push("  ".join(sorted(node["children"].keys())) or "<empty>")

        def cmd_cd(self, args):
            target = self._resolve_abs(args[0]) if args else "/"
            node = self._node(target)
            if not node or node["type"] != "dir":
                self.push("cd: no such directory: {}".format(target), is_error=True)
                return
            self.cwd = target

        def cmd_cat(self, args):
            if not args:
                self.push("usage: cat <file>")
                return
            target = self._resolve_abs(args[0])
            node = self._node(target)
            if not node or node["type"] != "file":
                self.push("cat: {}: no such file".format(args[0]), is_error=True)
                return
            self.push(node["content"])

        def cmd_echo(self, args):
            raw = " ".join(args)
            if ">" in raw:
                left, right = raw.split(">", 1)
                content = left.strip().strip('"')
                name = right.strip()
                if not name:
                    self.push("echo: missing file target", is_error=True)
                    return
                path = self._resolve_abs(name)
                parent_path = "/" + "/".join(self._split_path(path)[:-1]) if self._split_path(path)[:-1] else "/"
                base = self._split_path(path)[-1]
                parent = self._node(parent_path)
                if not parent or parent["type"] != "dir":
                    self.push("echo: invalid path", is_error=True)
                    return
                parent["children"][base] = {"type": "file", "content": content}
                self.push("wrote {}".format(path))
                return
            self.push(raw)

        def cmd_clear(self, args):
            self.output = []

        def cmd_history(self, args):
            if args and args[0] == ">" and len(args) > 1:
                filename = args[1]
                path = self._resolve_abs(filename)
                parent_path = "/" + "/".join(self._split_path(path)[:-1]) if self._split_path(path)[:-1] else "/"
                parent = self._node(parent_path)
                if parent and parent["type"] == "dir":
                    parent["children"][self._split_path(path)[-1]] = {"type": "file", "content": "\n".join(self.history[-50:])}
                    self.push("history exported to {}".format(path))
                return
            for i, cmd in enumerate(self.history[-50:], start=max(1, len(self.history) - 49)):
                self.push("{:03d} {}".format(i, cmd))

        def cmd_exit(self, args):
            self.push("connection lost... reconnected")

        def cmd_prompt(self, args):
            if not args:
                self.push("prompt set|color|glitch|reset")
                return
            sub = args[0]
            if sub == "set":
                self.prompt_text = " ".join(args[1:]).strip('"') or self.prompt_text
            elif sub == "color" and len(args) >= 2:
                if args[1] == "text" and len(args) >= 3:
                    self.input_color = args[2]
                else:
                    self.prompt_color = args[1]
            elif sub == "glitch" and len(args) >= 2:
                try:
                    self.glitch = max(0.0, min(1.0, float(args[1])))
                except Exception:
                    self.push("prompt glitch expects 0.0..1.0", is_error=True)
            elif sub == "reset":
                self.prompt_text = "ghost@shadow:~# "
                self.prompt_color = "#00ff66"
                self.input_color = "#99ffcc"
                self.glitch = 0.2
            elif sub == "font" and len(args) >= 2:
                try:
                    self.font_scale = max(0, min(2, int(args[1])))
                except Exception:
                    pass
            else:
                self.push("unknown prompt subcommand", is_error=True)
            self.save_prompt_cfg()

        def cmd_scan(self, args):
            if not args:
                self.push("usage: scan <email|phone|username>")
                return
            handle = args[0].lower().replace("@", "_").replace(".", "_")
            self.victims[handle] = {
                "display_name": handle.title(),
                "status": "scanned",
                "infection": random.randint(5, 25),
                "heat": random.randint(10, 40),
                "value": random.randint(2, 7),
                "data": [],
                "location": "unknown",
                "job": "Inconnu",
                "relationship": "Inconnu",
                "tags": ["Nouveau"],
                "last_activity": "à l'instant",
                "connections": [],
                "timeline": [{"ts": "maintenant", "type": "scan", "text": "Profil découvert par scan OSINT"}],
            }
            self.fs["/"]["children"]["victims"]["children"][handle + ".txt"] = {"type": "file", "content": "Victim {} scanned.".format(handle)}
            self.push("target acquired: {}".format(handle))

        def _parse_flag(self, args, name, default=None):
            if name in args:
                idx = args.index(name)
                if idx + 1 < len(args):
                    return args[idx + 1]
                return True
            return default

        def cmd_infect(self, args):
            if not args:
                self.push("usage: infect <target> --method qr|phish|sms")
                return
            target = args[0].lower()
            method = self._parse_flag(args, "--method", "qr")
            if target not in self.victims:
                self.push("Victim changed password – retry in 24h", is_error=True)
                self.heat = min(100, self.heat + 2)
                return
            self.victims[target]["status"] = "infected"
            self.victims[target]["infection"] = min(100, self.victims[target].get("infection", 20) + random.randint(15, 35))
            self.push("infection success on {} via {}".format(target, method))

        def cmd_grab(self, args):
            if not args:
                self.push("usage: grab <target> --data photos|messages|passwords|location")
                return
            target = args[0].lower()
            if target not in self.victims:
                self.push("No route to victim {}".format(target), is_error=True)
                return
            data = self._parse_flag(args, "--data", "messages")
            if data not in self.victims[target]["data"]:
                self.victims[target]["data"].append(data)
            self.victims[target]["infection"] = min(100, self.victims[target].get("infection", 20) + 6)
            self.heat = min(100, self.heat + 1)
            self.push("grabbed {} from {}".format(data, target))

        def cmd_spy(self, args):
            if not args:
                self.push("usage: spy <target>")
                return
            self.push("Live Shadow stream open for {} [webcam + feed popups]".format(args[0]))

        def cmd_watch(self, args):
            if not args:
                self.push("usage: watch <target> --webcam|--screen|--mic [&]")
                return
            target = args[0]
            modes = [a for a in args[1:] if a.startswith("--")]
            if "&" in args:
                self.running_jobs.append("watch {} {}".format(target, " ".join(modes)))
                self.heat = min(100, self.heat + 2)
                self.push("watch running in background")
            else:
                self.push("watching {} {}".format(target, " ".join(modes) if modes else "--screen"))

        def cmd_keylog(self, args):
            if len(args) < 2:
                self.push("usage: keylog <target> --start|--stop")
                return
            self.push("keylogger {} {}".format("armed" if "--start" in args else "stopped", args[0]))

        def cmd_victims(self, args):
            for k, v in sorted(self.victims.items(), key=lambda item: item[1].get("infection", 0), reverse=True):
                self.push("{} [{}] inf:{}% heat:{} data:{}".format(k, v["status"], v.get("infection", 0), v.get("heat", 0), ",".join(v["data"]) or "none"))
            store.ghost_net_mode = True
            renpy.restart_interaction()

        def cmd_profile(self, args):
            if not args:
                self.push("usage: profile <target>")
                return
            t = args[0].lower()
            v = self.victims.get(t)
            if not v:
                self.push("profile: target not found", is_error=True)
                return
            self.push("target={} status={} location={} data={}".format(t, v["status"], v["location"], ",".join(v["data"]) or "none"))
            store.ghost_net_selected = t

        def cmd_market(self, args):
            self.push("Shadow Market: use market buy rat_v3 | market list")

        def cmd_heat(self, args):
            state = "stable"
            if self.heat > 80:
                state = "critical"
            elif self.heat > 50:
                state = "warning"
            self.push("HEAT {}% ({})".format(self.heat, state))
            if self.heat > 80:
                self.push("Advice: run ghostmode or panic immediately.")

        def cmd_propagate(self, args):
            self.push("propagation pulse sent to {}".format(self._parse_flag(args, "--to", "contacts")))
            self.heat = min(100, self.heat + 3)

        def cmd_deepfake(self, args):
            self.push("deepfake job queued (crypto debited)")
            self.heat = min(100, self.heat + 1)

        def cmd_erase(self, args):
            self.push("trace erasure triggered; detection risk elevated")
            self.heat = min(100, self.heat + 4)

        def cmd_script(self, args):
            if len(args) >= 2 and args[0] == "run":
                name = args[1]
                node = self._node(self._resolve_abs("/scripts/" + name))
                if not node:
                    self.push("script not found", is_error=True)
                    return
                job_name = "script:{}".format(name)
                self.running_jobs.append(job_name)
                self.push("{} running in background (cpu +heat)".format(job_name))
                self.heat = min(100, self.heat + 2)
                return
            self.push("usage: script run <nom_script>")

        def cmd_panic(self, args):
            self.history = []
            self.running_jobs = []
            self.heat = max(0, self.heat - 30)
            self.push("panic mode: logs wiped, links severed")

        def cmd_ghostmode(self, args):
            self.heat = max(0, self.heat - 15)
            self.push("ghostmode enabled: heat reduced, actions slowed")

        def cmd_sleep(self, args):
            self.push("sleep acknowledged (simulation only)")

        def visual_noise(self):
            if self.heat > 80:
                return "▒▒"
            if self.heat > 50:
                return "░"
            if random.random() < self.glitch * 0.05:
                return "~"
            return ""

        def sorted_victim_keys(self):
            return [k for k, _ in sorted(self.victims.items(), key=lambda item: item[1].get("infection", 0), reverse=True)]

        def victim_heat_advice(self, victim):
            heat = victim.get("heat", 0)
            if heat >= 70:
                return "Risque élevé: couper webcam 48h et réduire les actions actives."
            if heat >= 45:
                return "Risque modéré: espacer les grabs et éviter les scans agressifs."
            return "Risque bas: fenêtre d'exploitation stable."

    terminal_engine = TerminalEngine()
    terminal_mode = True
    ghost_net_mode = False
    ghost_net_view = "table"
    ghost_net_selected = "nora"
    ghost_net_query = ""

    def terminal_submit():
        terminal_engine.run_input()

    def terminal_history_up():
        terminal_engine.navigate_history(-1)

    def terminal_history_down():
        terminal_engine.navigate_history(1)

    def terminal_autocomplete():
        terminal_engine.autocomplete()

    def terminal_toggle_fullscreen():
        terminal_engine.fullscreen = not terminal_engine.fullscreen
        prefs.fullscreen = terminal_engine.fullscreen

screen terminal_ui():
    zorder 200
    modal False
    if not ghost_net_mode:

        frame:
            background "#020402"
            xfill True
            yfill True

            has vbox

            frame:
                background None
                xfill True
                padding (16, 8)

                text "[terminal_engine.visual_noise()] GHOST TERMINAL // heat [terminal_engine.heat]% // jobs [len(terminal_engine.running_jobs)]":
                    color terminal_engine.prompt_color
                    size 20 + (terminal_engine.font_scale * 3)

            viewport:
                draggable True
                mousewheel True
                yadjustment ui.adjustment(
                    range=max(0, len(terminal_engine.output) * 24),
                    value=max(0, len(terminal_engine.output) * 24)
                )
                xfill True
                yfill True

                frame:
                    background None
                    xfill True
                    padding (16, 8)

                    vbox:
                        spacing 2

                        for line in terminal_engine.output:
                            text line:
                                color terminal_engine.text_color
                                size 17 + (terminal_engine.font_scale * 2)

                        text terminal_engine.composing_line() + "▌":
                            color terminal_engine.input_color
                            size 17 + (terminal_engine.font_scale * 2)

            frame:
                background "#000000"
                xfill True
                ysize 52
                xpadding 16
                ypadding 8

                hbox:
                    spacing 8
                    text terminal_engine.resolved_prompt():
                        color terminal_engine.prompt_color
                        size 18 + (terminal_engine.font_scale * 2)
                        yalign 0.5

                    input value VariableInputValue("terminal_engine.input") length 240:
                        color terminal_engine.input_color
                        caret "#66ff99"
                        size 18 + (terminal_engine.font_scale * 2)
                        yalign 0.5

    frame:
        xalign 0.98
        yalign 0.02
        background "#081018cc"
        xpadding 12
        ypadding 6
        textbutton ("TERMINAL" if ghost_net_mode else "GHOST NET [V]"):
            text_size 16
            text_color "#86faff"
            action ToggleVariable("ghost_net_mode")

    key "K_RETURN" action Function(terminal_submit)
    key "K_KP_ENTER" action Function(terminal_submit)
    key "K_UP" action Function(terminal_history_up)
    key "K_DOWN" action Function(terminal_history_down)
    key "K_TAB" action Function(terminal_autocomplete)
    key "ctrl_K_r" action Function(terminal_engine.push, "reverse-i-search unavailable in demo: use history")
    key "K_F11" action Function(terminal_toggle_fullscreen)
    key "K_v" action ToggleVariable("ghost_net_mode")


screen ghost_net_ui():
    zorder 205
    modal False
    if ghost_net_mode:
        default graph_positions = {
            "nora": (0.27, 0.32),
            "jules": (0.58, 0.27),
            "mika": (0.72, 0.52),
            "daria": (0.40, 0.68),
            "eon": (0.83, 0.38),
        }

        frame:
            background "#05070d"
            xfill True
            yfill True

            frame:
                background "#0d1420"
                xfill True
                ysize 90
                xpadding 18
                ypadding 10

                hbox:
                    spacing 12
                    xfill True
                    yalign 0.5
                    text "GHOST NET // SHADOW NEXUS":
                        color "#7ff9ff"
                        size 30
                    text "Infected [len(terminal_engine.victims)] cibles // Heat global [terminal_engine.heat]%":
                        color "#c9f6ff"
                        size 17
                    null width 40
                    textbutton ("Mode Tableau" if ghost_net_view != "table" else "Mode Graphe"):
                        action (SetVariable("ghost_net_view", "graph") if ghost_net_view == "table" else SetVariable("ghost_net_view", "table"))
                        text_size 15
                    textbutton "Retour terminal":
                        action SetVariable("ghost_net_mode", False)
                        text_size 15

            if ghost_net_view == "table":
                frame:
                    background "#060a12"
                    xfill True
                    yfill True
                    xpadding 14
                    ypadding 14

                    hbox:
                        spacing 14
                        textbutton "Heat > 50%":
                            action SetVariable("ghost_net_query", "heat")
                        textbutton "Infection < 30%":
                            action SetVariable("ghost_net_query", "low_inf")
                        textbutton "Reset filtres":
                            action SetVariable("ghost_net_query", "")
                        text "Recherche rapide (nom/tag) : [ghost_net_query if ghost_net_query else 'aucune']":
                            color "#88adc4"

                    viewport:
                        draggable True
                        mousewheel True
                        scrollbars "vertical"
                        xfill True
                        yfill True

                        vbox:
                            spacing 8
                            for key in terminal_engine.sorted_victim_keys():
                                $ victim = terminal_engine.victims[key]
                                if not ((ghost_net_query == "heat" and victim.get("heat", 0) <= 50) or (ghost_net_query == "low_inf" and victim.get("infection", 0) >= 30)):
                                    button:
                                        background "#0f1a2a"
                                        hover_background "#12223a"
                                        xfill True
                                        xpadding 10
                                        ypadding 8
                                        action SetVariable("ghost_net_selected", key)

                                        hbox:
                                            spacing 18
                                            text "[victim.get('display_name', key)]":
                                                color "#ebf7ff"
                                                size 20
                                                xminimum 235
                                            text "INF [victim.get('infection', 0)]%":
                                                color "#7dffbb" if victim.get("infection", 0) < 50 else ("#ffc65a" if victim.get("infection", 0) < 80 else "#ff5e6a")
                                                size 18
                                                xminimum 130
                                            text "HEAT [victim.get('heat', 0)]%":
                                                color "#8be0ff" if victim.get("heat", 0) < 50 else "#ff62a8"
                                                size 18
                                                xminimum 130
                                            text "Valeur ★[victim.get('value', 0)]":
                                                color "#f5b7ff"
                                                size 17
                                                xminimum 110
                                            text "[victim.get('last_activity', 'inconnue')]":
                                                color "#91a8be"
                                                size 16
                                                xminimum 160
                                            text ", ".join(victim.get("tags", [])):
                                                color "#b4fbff"
                                                size 16

            else:
                frame:
                    background "#050a16"
                    xfill True
                    yfill True
                    xpadding 20
                    ypadding 20
                    for key in terminal_engine.sorted_victim_keys():
                        $ victim = terminal_engine.victims[key]
                        $ pos = graph_positions.get(key, (random.random(), random.random()))
                        frame:
                            xpos int(config.screen_width * pos[0])
                            ypos int(config.screen_height * pos[1])
                            background "#121d2d"
                            xpadding 14
                            ypadding 8
                            textbutton "[victim.get('display_name', key)]\nINF [victim.get('infection', 0)]%":
                                action SetVariable("ghost_net_selected", key)
                                text_color "#7ff9ff" if victim.get("heat", 0) < 50 else "#ff63ad"
                                text_size 15

        if ghost_net_selected in terminal_engine.victims:
            $ sv = terminal_engine.victims[ghost_net_selected]
            frame:
                xalign 0.985
                yalign 0.53
                xmaximum 500
                ymaximum 860
                background "#0e1320ef"
                xpadding 16
                ypadding 14
                vbox:
                    spacing 9
                    text "[sv.get('display_name', ghost_net_selected)]":
                        color "#e8f8ff"
                        size 28
                    text "[sv.get('job', 'Inconnu')] // [sv.get('location', 'Unknown')]":
                        color "#7bcde4"
                    text "Statut relationnel: [sv.get('relationship', 'Inconnu')]":
                        color "#b5d9ef"
                    text "Infection [sv.get('infection', 0)]% | Heat [sv.get('heat', 0)]% | Valeur [sv.get('value', 0)]":
                        color "#f3b2ff"
                    text "Accès: mail [max(20, sv.get('infection', 0)-5)]% | social [max(10, sv.get('infection', 0)-25)]% | webcam [max(0, sv.get('infection', 0)-45)]%":
                        color "#8effcf"
                        size 15
                    text "Keylogger: [ 'Oui' if sv.get('infection', 0) >= 40 else 'Non' ]":
                        color "#7fe3ff"
                        size 15
                    text "Conseil risque: [terminal_engine.victim_heat_advice(sv)]":
                        color "#ff86b5"
                        size 15
                    text "Timeline":
                        color "#8cf6ff"
                        size 19
                    viewport:
                        draggable True
                        mousewheel True
                        ymaximum 220
                        vbox:
                            spacing 4
                            for event in sv.get("timeline", []):
                                text "[event.get('ts', '--')] · [event.get('type', 'event')] · [event.get('text', '')]":
                                    color "#d5e8ff"
                                    size 14
                    text "Connexions: [', '.join(sv.get('connections', [])) if sv.get('connections') else 'Aucune']":
                        color "#8ab6cf"

                    hbox:
                        spacing 8
                        textbutton "Upgrade infection":
                            action Function(terminal_engine.push, "RAT upgrade lancé pour {}".format(ghost_net_selected))
                        textbutton "Grab data":
                            action Function(terminal_engine.push, "Data burst capturé sur {}".format(ghost_net_selected))
                        textbutton "Spy live":
                            action Function(terminal_engine.push, "Flux live ouvert sur {}".format(ghost_net_selected))
