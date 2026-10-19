from __future__ import annotations

import sys
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path

from strategy import extract_pdf_text
from strategy_analyzer import review_strategy, build_ai_prompt
from agent_router import ask_agent
from updater import check_for_update, install_update, UpdateError
from version import __version__


class ForexAIDesk(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title(f"Forex AI Desk v{__version__}")
        self.geometry("1000x680")
        self.minsize(780, 520)
        self.configure(bg="#101820")
        self.pdf_text = ""
        self._update_check_running = False

        header = tk.Frame(self, bg="#172631", padx=20, pady=16)
        header.pack(fill="x")
        tk.Label(header, text="FOREX AI DESK", font=("Segoe UI", 20, "bold"),
                 fg="#f4f7fa", bg="#172631").pack(anchor="w")
        tk.Label(header, text=f"Version {__version__} • Analyse PDF • Agents IA • MetaTrader 5",
                 font=("Segoe UI", 10), fg="#9db0bd", bg="#172631").pack(anchor="w", pady=(4, 0))

        toolbar = ttk.Frame(self, padding=12)
        toolbar.pack(fill="x")
        ttk.Button(toolbar, text="Importer un PDF", command=self.import_pdf).pack(side="left")
        ttk.Button(toolbar, text="Analyser les règles", command=self.analyze_strategy).pack(side="left", padx=6)
        ttk.Button(toolbar, text="Demander à l'IA", command=self.ask_ai).pack(side="left")
        ttk.Button(toolbar, text="État MT5", command=self.check_mt5).pack(side="left", padx=6)
        ttk.Button(toolbar, text="Rechercher une mise à jour", command=lambda: self.check_updates(manual=True)).pack(side="left")

        self.status = tk.StringVar(value="MODE SIMULATION — aucun ordre réel n'est envoyé.")
        ttk.Label(self, textvariable=self.status, padding=(14, 4)).pack(fill="x")
        self.output = tk.Text(self, wrap="word", font=("Consolas", 10), bg="#0c1218",
                              fg="#dce6ec", insertbackground="white", padx=14, pady=12, relief="flat")
        self.output.pack(fill="both", expand=True, padx=12, pady=(4, 12))
        self.write("Bienvenue dans Forex AI Desk.\n\n")
        self.write("• Importez un PDF pour en extraire le texte.\n")
        self.write("• Analysez la présence de règles de risque et de sortie.\n")
        self.write("• Demandez une synthèse à Jev (si configuré), puis Hermes/OpenCode en secours.\n")
        self.write("• Les mises à jour sont recherchées sur les releases officielles de ce dépôt GitHub.\n")
        self.write("• Les fonctions de trading réel ne sont pas implémentées.\n")
        self.after(1800, lambda: self.check_updates(manual=False))

    def write(self, text: str) -> None:
        self.output.insert("end", text)
        self.output.see("end")

    def check_updates(self, manual: bool = False) -> None:
        if self._update_check_running:
            if manual:
                messagebox.showinfo("Mise à jour", "Une vérification est déjà en cours.")
            return
        self._update_check_running = True
        self.status.set("Vérification des mises à jour…")

        def worker() -> None:
            update = None
            error = None
            try:
                update = check_for_update(__version__)
            except Exception as exc:
                error = str(exc)
            self.after(0, lambda: self._finish_update_check(update, error, manual))

        threading.Thread(target=worker, daemon=True).start()

    def _finish_update_check(self, update, error, manual: bool) -> None:
        self._update_check_running = False
        if error:
            self.status.set("Vérification des mises à jour impossible.")
            if manual:
                messagebox.showwarning("Mise à jour", error)
            return
        if not update:
            self.status.set(f"Forex AI Desk v{__version__} — application à jour.")
            if manual:
                messagebox.showinfo("Mise à jour", f"Tu utilises déjà la version {__version__}.")
            return
        self.status.set(f"Nouvelle version disponible : {update['version']}")
        notes = update.get("notes", "").strip()
        prompt = f"Forex AI Desk v{update['version']} est disponible.\n\n"
        if notes:
            prompt += notes[:1200] + "\n\n"
        prompt += "Télécharger et installer cette mise à jour maintenant ?"
        if not messagebox.askyesno("Mise à jour disponible", prompt):
            self.write(f"\nMise à jour v{update['version']} disponible, installation reportée.\n")
            return
        if not getattr(sys, "frozen", False):
            messagebox.showinfo("Version développeur",
                                "La mise à jour automatique fonctionne uniquement dans l'application EXE compilée.")
            return
        try:
            self.status.set("Téléchargement et vérification SHA-256…")
            self.update_idletasks()
            install_update(update)
            messagebox.showinfo("Mise à jour prête",
                                "Le fichier a été vérifié. Forex AI Desk va se fermer pour appliquer la mise à jour, puis se relancer.")
            self.destroy()
        except (UpdateError, OSError) as exc:
            messagebox.showerror("Mise à jour impossible", str(exc))
            self.status.set("Échec de la mise à jour. L'application actuelle est conservée.")

    def import_pdf(self) -> None:
        filename = filedialog.askopenfilename(title="Choisir un PDF de stratégie",
                                              filetypes=[("Documents PDF", "*.pdf")])
        if not filename:
            return
        try:
            text = extract_pdf_text(Path(filename))
            self.pdf_text = text
            self.write(f"\n--- PDF importé : {Path(filename).name} ---\n")
            self.write(text[:30000] if text else "[Aucun texte extrait. Le PDF est peut-être scanné.]")
            self.write("\n\n--- Fin de l'extrait ---\n")
            self.status.set(f"PDF chargé : {Path(filename).name}")
        except Exception as exc:
            messagebox.showerror("Import PDF impossible", str(exc))

    def analyze_strategy(self) -> None:
        if not self.pdf_text.strip():
            messagebox.showinfo("Aucun document", "Importez d'abord un PDF de stratégie.")
            return
        result = review_strategy(self.pdf_text)
        self.write("\n--- CONTRÔLE INITIAL DE LA STRATÉGIE ---\n")
        self.write(f"Nombre de mots : {result['word_count']}\n")
        for label, found in result["checks"].items():
            self.write(f"{'✓' if found else '✗'} {label} : {'mentionné' if found else 'non repéré'}\n")
        if result["missing"]:
            self.write("Points à clarifier : " + ", ".join(result["missing"]) + "\n")
        for warning in result["warnings"]:
            self.write("Attention : " + warning + "\n")
        self.write("Cette vérification recherche des termes; elle ne valide pas la stratégie.\n")

    def ask_ai(self) -> None:
        if not self.pdf_text.strip():
            messagebox.showinfo("Aucun document", "Importez d'abord un PDF de stratégie.")
            return
        self.status.set("Consultation des agents IA…")
        self.update_idletasks()
        reply = ask_agent(build_ai_prompt(self.pdf_text))
        self.write("\n--- ANALYSE IA ---\n")
        if reply.ok:
            self.write(f"Agent utilisé : {reply.provider}\n\n{reply.text}\n")
            self.status.set(f"Analyse terminée avec {reply.provider}. Mode simulation actif.")
        else:
            self.write(reply.detail + "\n")
            self.status.set("Aucun agent IA disponible; vérifiez sa configuration.")

    def check_mt5(self) -> None:
        try:
            import MetaTrader5 as mt5
        except ImportError:
            messagebox.showinfo("MetaTrader 5", "Le module MetaTrader5 n'est pas installé. "
                                "Installez le terminal MT5 et le package Python sous Windows.")
            return
        try:
            if not mt5.initialize():
                messagebox.showwarning("MetaTrader 5", f"Connexion impossible : {mt5.last_error()}\n"
                                        "Vérifiez que le terminal MT5 est installé et ouvert.")
                return
            info = mt5.terminal_info()
            account = mt5.account_info()
            self.write("\n--- ÉTAT METATRADER 5 ---\n")
            self.write(f"Terminal : {info}\n")
            self.write(f"Compte connecté : {'oui' if account else 'non'}\n")
            self.write("Lecture seule : aucune commande de trading n'est disponible.\n")
        finally:
            mt5.shutdown()


if __name__ == "__main__":
    ForexAIDesk().mainloop()
