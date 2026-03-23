init -2 python:
    import os
    import json
    import datetime
    import random
    import shlex

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
                "nora": {"status": "infected", "data": ["messages"], "location": "Old Town"},
                "jules": {"status": "scanned", "data": [], "location": "North Checkpoint"},
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
            self.victims[handle] = {"status": "scanned", "data": [], "location": "unknown"}
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
            for k, v in sorted(self.victims.items()):
                self.push("{} [{}] data:{}".format(k, v["status"], ",".join(v["data"]) or "none"))

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

    terminal_engine = TerminalEngine()
    terminal_mode = True

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

    key "K_RETURN" action Function(terminal_submit)
    key "K_KP_ENTER" action Function(terminal_submit)
    key "K_UP" action Function(terminal_history_up)
    key "K_DOWN" action Function(terminal_history_down)
    key "K_TAB" action Function(terminal_autocomplete)
    key "ctrl_K_r" action Function(terminal_engine.push, "reverse-i-search unavailable in demo: use history")
    key "K_F11" action Function(terminal_toggle_fullscreen)
