from __future__ import annotations

import os
import sys
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path

from strategy import extract_pdf_text
from strategy_analyzer import review_strategy, build_ai_prompt
from agent_router import ask_agent, diagnose_opencode
from updater import check_for_update, install_update, UpdateError
from version import __version__


BG = "#0b1220"
PANEL = "#111c2e"
PANEL_2 = "#17263a"
TEXT = "#eef4fb"
MUTED = "#9aaec4"
ACCENT = "#39c6b0"
BORDER = "#26384f"


class ForexAIDesk(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title(f"Forex AI Desk · v{__version__}")
        self.geometry("1120x760")
        self.minsize(850, 600)
        self.configure(bg=BG)
        self.pdf_text = ""
        self.pdf_name = ""
        self._update_check_running = False
        self._busy = False
        self._build_style()
        self._build_ui()
        self._append("Bienvenue", "Importe un PDF de stratégie, vérifie ses règles, puis demande une analyse à un agent IA.")
        self._append("Sécurité", "Mode lecture seule / simulation. Cette application n'envoie aucun ordre de trading.")
        self.after(1800, lambda: self.check_updates(manual=False))

    def _build_style(self) -> None:
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure(".", font=("Segoe UI", 10))
        style.configure("TFrame", background=BG)
        style.configure("Panel.TFrame", background=PANEL)
        style.configure("TLabel", background=BG, foreground=TEXT)
        style.configure("Muted.TLabel", background=BG, foreground=MUTED)
        style.configure("Panel.TLabel", background=PANEL, foreground=TEXT)
        style.configure("Title.TLabel", background=PANEL, foreground=TEXT, font=("Segoe UI", 21, "bold"))
        style.configure("Subtitle.TLabel", background=PANEL, foreground=MUTED, font=("Segoe UI", 10))
        style.configure("TButton", padding=(12, 9), background=PANEL_2, foreground=TEXT, borderwidth=0)
        style.map("TButton", background=[("active", "#263b55"), ("disabled", "#1a2738")],
                  foreground=[("disabled", "#718196")])
        style.configure("Accent.TButton", padding=(14, 10), background=ACCENT, foreground="#07131d",
                        font=("Segoe UI", 10, "bold"))
        style.map("Accent.TButton", background=[("active", "#69e0ce")])
        style.configure("TNotebook", background=BG, borderwidth=0)
        style.configure("TNotebook.Tab", padding=(14, 9), background=PANEL_2, foreground=MUTED)
        style.map("TNotebook.Tab", background=[("selected", PANEL)], foreground=[("selected", TEXT)])
        style.configure("Horizontal.TProgressbar", troughcolor=PANEL_2, background=ACCENT, borderwidth=0)

    def _build_ui(self) -> None:
        header = ttk.Frame(self, style="Panel.TFrame", padding=(24, 20))
        header.pack(fill="x", padx=16, pady=(16, 10))
        top = ttk.Frame(header, style="Panel.TFrame")
        top.pack(fill="x")
        ttk.Label(top, text="FOREX AI DESK", style="Title.TLabel").pack(side="left")
        ttk.Label(top, text=f"VERSION {__version__}", style="Subtitle.TLabel").pack(side="right", anchor="s")
        ttk.Label(header, text="Analyse de stratégies  /  Agents IA  /  Connexion MetaTrader 5",
                  style="Subtitle.TLabel").pack(anchor="w", pady=(5, 0))

        actions = ttk.Frame(self, padding=(16, 2, 16, 10))
        actions.pack(fill="x")
        self.pdf_button = ttk.Button(actions, text="＋  Importer un PDF", style="Accent.TButton", command=self.import_pdf)
        self.pdf_button.pack(side="left")
        self.analyze_button = ttk.Button(actions, text="Analyser les règles", command=self.analyze_strategy)
        self.analyze_button.pack(side="left", padx=(8, 0))
        self.ai_button = ttk.Button(actions, text="Demander à l'IA", command=self.ask_ai)
        self.ai_button.pack(side="left", padx=(8, 0))
        ttk.Button(actions, text="Tester OpenCode", command=self.test_opencode).pack(side="left", padx=(8, 0))
        ttk.Button(actions, text="État MT5", command=self.check_mt5).pack(side="left", padx=(8, 0))
        ttk.Button(actions, text="Mise à jour", command=lambda: self.check_updates(manual=True)).pack(side="right")

        self.doc_status = tk.StringVar(value="Aucun PDF importé")
        status_panel = ttk.Frame(self, style="Panel.TFrame", padding=(14, 10))
        status_panel.pack(fill="x", padx=16, pady=(0, 10))
        ttk.Label(status_panel, textvariable=self.doc_status, style="Panel.TLabel").pack(side="left")
        self.status = tk.StringVar(value="Prêt · Mode simulation")
        ttk.Label(status_panel, textvariable=self.status, style="Panel.TLabel").pack(side="right")

        body = ttk.Frame(self, padding=(16, 0, 16, 12))
        body.pack(fill="both", expand=True)
        self.tabs = ttk.Notebook(body)
        self.tabs.pack(fill="both", expand=True)
        console_tab = ttk.Frame(self.tabs, style="Panel.TFrame", padding=10)
        self.tabs.add(console_tab, text="  Espace de travail  ")
        self.output = tk.Text(console_tab, wrap="word", font=("Consolas", 10), bg=PANEL, fg=TEXT,
                              insertbackground=TEXT, selectbackground="#284d65", padx=14, pady=12,
                              relief="flat", borderwidth=0, spacing1=2, spacing3=5)
        scrollbar = ttk.Scrollbar(console_tab, orient="vertical", command=self.output.yview)
        self.output.configure(yscrollcommand=scrollbar.set)
        self.output.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self.output.tag_configure("heading", foreground=ACCENT, font=("Segoe UI", 11, "bold"), spacing1=10)
        self.output.tag_configure("body", foreground=TEXT)
        self.output.tag_configure("muted", foreground=MUTED)
        self.output.tag_configure("error", foreground="#ff9d9d")
        self.output.configure(state="disabled")

        footer = ttk.Frame(self, padding=(18, 0, 18, 12))
        footer.pack(fill="x")
        self.progress = ttk.Progressbar(footer, mode="indeterminate", length=140)
        self.progress.pack(side="left", padx=(0, 10))
        ttk.Label(footer, text="Les analyses IA ne garantissent pas la rentabilité.", style="Muted.TLabel").pack(side="left")
        ttk.Label(footer, text="Aucun ordre réel envoyé", style="Muted.TLabel").pack(side="right")

    def _append(self, heading: str, body: str, error: bool = False) -> None:
        self.output.configure(state="normal")
        self.output.insert("end", f"\n{heading}\n", "heading")
        self.output.insert("end", body.rstrip() + "\n", "error" if error else "body")
        self.output.see("end")
        self.output.configure(state="disabled")

    def _set_busy(self, busy: bool, message: str = "") -> None:
        self._busy = busy
        self.status.set(message or ("Traitement en cours…" if busy else "Prêt · Mode simulation"))
        if busy:
            self.progress.start(12)
        else:
            self.progress.stop()
        state = "disabled" if busy else "normal"
        for button in (self.pdf_button, self.analyze_button, self.ai_button):
            button.configure(state=state)

    def _run_background(self, task, on_success, title: str) -> None:
        if self._busy:
            messagebox.showinfo("Traitement en cours", "Attends la fin de l'opération en cours.")
            return
        self._set_busy(True, title)

        def worker():
            try:
                result = task()
                self.after(0, lambda: (self._set_busy(False), on_success(result)))
            except Exception as exc:
                error = str(exc)
                self.after(0, lambda: (self._set_busy(False, "Échec · consulte le message d'erreur"),
                                       self._append("Erreur", error, True),
                                       messagebox.showerror("Opération impossible", error)))
        threading.Thread(target=worker, daemon=True).start()

    def import_pdf(self) -> None:
        filename = filedialog.askopenfilename(title="Choisir un PDF de stratégie",
                                              filetypes=[("Documents PDF", "*.pdf")])
        if not filename:
            return
        path = Path(filename)

        def task():
            return extract_pdf_text(path)

        def done(text):
            if not text.strip():
                self.pdf_text = ""
                self.pdf_name = path.name
                self.doc_status.set(f"{path.name} · aucun texte extrait")
                self._append("PDF sans texte exploitable",
                    "Ce document est peut-être scanné, protégé par mot de passe ou constitué d'images. "
                    "Cette version ne fait pas encore d'OCR. Essaie un PDF avec du texte sélectionnable.")
                return
            self.pdf_text = text
            self.pdf_name = path.name
            self.doc_status.set(f"PDF chargé · {path.name} · {len(text.split())} mots")
            self._append(f"PDF importé · {path.name}",
                         f"{len(text.split())} mots extraits. Voici un aperçu :\n\n{text[:6000]}\n\n"
                         "Le document complet reste chargé pour l'analyse.")
            self.status.set("PDF prêt à être analysé")

        self._run_background(task, done, "Lecture du PDF…")

    def analyze_strategy(self) -> None:
        if not self.pdf_text.strip():
            messagebox.showinfo("Aucun document", "Importe d'abord un PDF contenant du texte sélectionnable.")
            return
        result = review_strategy(self.pdf_text)
        lines = [f"Nombre de mots : {result['word_count']}"]
        for label, found in result["checks"].items():
            lines.append(f"{'✓' if found else '✗'} {label} : {'mentionné' if found else 'non repéré'}")
        if result["missing"]:
            lines.append("À clarifier : " + ", ".join(result["missing"]))
        lines.extend("Attention : " + w for w in result["warnings"])
        lines.append("Cette vérification repère des termes; elle ne valide pas la stratégie.")
        self._append("Contrôle initial de la stratégie", "\n".join(lines))
        self.status.set("Contrôle terminé · résultat indicatif")

    def ask_ai(self) -> None:
        if not self.pdf_text.strip():
            messagebox.showinfo("Aucun document", "Importe d'abord un PDF de stratégie.")
            return
        prompt = build_ai_prompt(self.pdf_text)

        def task():
            return ask_agent(prompt, preferred="opencode")

        def done(reply):
            if reply.ok:
                self._append(f"Analyse IA · {reply.provider}", reply.text)
                self.status.set(f"Analyse terminée · {reply.provider}")
            else:
                self._append("Agent IA indisponible", reply.detail, True)
                self.status.set("Échec de connexion à l'agent IA")

        self._run_background(task, done, "Connexion à OpenCode / agent IA…")

    def test_opencode(self) -> None:
        def task():
            return diagnose_opencode()
        def done(reply):
            if reply.ok:
                self._append("Diagnostic OpenCode", reply.text)
                self.status.set("OpenCode accessible")
            else:
                self._append("Diagnostic OpenCode échoué", reply.detail, True)
                self.status.set("OpenCode indisponible")
                messagebox.showwarning("OpenCode", reply.detail)
        self._run_background(task, done, "Test d'OpenCode…")

    def check_mt5(self) -> None:
        def task():
            try:
                import MetaTrader5 as mt5
            except ImportError as exc:
                raise RuntimeError("Module MetaTrader5 introuvable dans cet EXE. Vérifie que le build Windows inclut "
                                   "le package MetaTrader5; installe aussi le terminal MetaTrader 5 64 bits.") from exc
            initialized = False
            try:
                terminal_path = os.getenv("MT5_TERMINAL_PATH", "").strip()
                ok = mt5.initialize(path=terminal_path) if terminal_path else mt5.initialize()
                if not ok:
                    err = mt5.last_error()
                    return False, f"mt5.initialize() a échoué : {err}.\n\n"
                    "Ouvre MetaTrader 5, connecte-toi au compte dans le terminal, puis réessaie. "
                    "Si plusieurs terminaux sont installés, définis MT5_TERMINAL_PATH avec le chemin exact de terminal64.exe."
                initialized = True
                terminal = mt5.terminal_info()
                account = mt5.account_info()
                if terminal is None:
                    return False, f"Connexion au terminal sans informations terminal. Erreur : {mt5.last_error()}"
                details = [
                    f"Terminal : {getattr(terminal, 'name', 'MetaTrader 5')}",
                    f"Chemin : {getattr(terminal, 'path', 'inconnu')}",
                    f"Connecté au serveur : {'oui' if account else 'non'}",
                ]
                if account:
                    details.extend([f"Numéro de compte : {account.login}",
                                    f"Serveur : {account.server}",
                                    f"Devise : {account.currency}",
                                    f"Mode démo : {'oui' if getattr(account, 'trade_mode', -1) == 0 else 'non confirmé'}"])
                else:
                    details.append(f"Compte indisponible : {mt5.last_error()}")
                details.append("Lecture seule : l'application n'envoie aucun ordre.")
                return True, "\n".join(details)
            finally:
                if initialized:
                    mt5.shutdown()

        def done(result):
            ok, details = result
            self._append("État MetaTrader 5", details, not ok)
            self.status.set("MT5 connecté (lecture seule)" if ok else "MT5 non connecté")
            if not ok:
                messagebox.showwarning("Connexion MT5 impossible", details)
        self._run_background(task, done, "Vérification de MetaTrader 5…")

    def check_updates(self, manual: bool = False) -> None:
        if self._update_check_running:
            return
        self._update_check_running = True

        def worker():
            update, error = None, None
            try:
                update = check_for_update(__version__)
            except Exception as exc:
                error = str(exc)
            self.after(0, lambda: self._finish_update_check(update, error, manual))
        threading.Thread(target=worker, daemon=True).start()

    def _finish_update_check(self, update, error, manual: bool) -> None:
        self._update_check_running = False
        if error:
            if manual:
                messagebox.showwarning("Mise à jour", error)
            return
        if not update:
            if manual:
                messagebox.showinfo("Mise à jour", f"Tu utilises déjà la version {__version__}.")
            return
        prompt = f"Forex AI Desk v{update['version']} est disponible.\n\nInstaller maintenant ?"
        if not messagebox.askyesno("Mise à jour disponible", prompt):
            return
        if not getattr(sys, "frozen", False):
            messagebox.showinfo("Version développeur", "L'auto-mise à jour fonctionne uniquement dans l'EXE compilé.")
            return
        try:
            install_update(update)
            messagebox.showinfo("Mise à jour prête", "L'application va se fermer puis redémarrer après installation.")
            self.destroy()
        except (UpdateError, OSError) as exc:
            messagebox.showerror("Mise à jour impossible", str(exc))


if __name__ == "__main__":
    ForexAIDesk().mainloop()
