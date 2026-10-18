from __future__ import annotations

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path

from strategy import extract_pdf_text


class ForexAIDesk(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Forex AI Desk")
        self.geometry("1000x680")
        self.minsize(780, 520)
        self.configure(bg="#101820")
        self.pdf_text = ""

        header = tk.Frame(self, bg="#172631", padx=20, pady=16)
        header.pack(fill="x")
        tk.Label(
            header, text="FOREX AI DESK", font=("Segoe UI", 20, "bold"),
            fg="#f4f7fa", bg="#172631"
        ).pack(anchor="w")
        tk.Label(
            header, text="Analyse de stratégies • MetaTrader 5 • Simulation",
            font=("Segoe UI", 10), fg="#9db0bd", bg="#172631"
        ).pack(anchor="w", pady=(4, 0))

        toolbar = ttk.Frame(self, padding=12)
        toolbar.pack(fill="x")
        ttk.Button(toolbar, text="Importer une stratégie PDF", command=self.import_pdf).pack(side="left")
        ttk.Button(toolbar, text="État de MetaTrader 5", command=self.check_mt5).pack(side="left", padx=8)

        self.status = tk.StringVar(value="Mode simulation actif — aucune transaction réelle n'est envoyée.")
        ttk.Label(self, textvariable=self.status, padding=(14, 4)).pack(fill="x")

        self.output = tk.Text(
            self, wrap="word", font=("Consolas", 10), bg="#0c1218",
            fg="#dce6ec", insertbackground="white", padx=14, pady=12,
            relief="flat"
        )
        self.output.pack(fill="both", expand=True, padx=12, pady=(4, 12))
        self.write("Bienvenue dans Forex AI Desk.\n\n")
        self.write("1. Importez un PDF de stratégie pour extraire son texte.\n")
        self.write("2. Vérifiez si MetaTrader 5 est installé et ouvert.\n")
        self.write("3. Les opérations sont limitées à l'analyse et à la simulation dans cette version.\n")

    def write(self, text: str) -> None:
        self.output.insert("end", text)
        self.output.see("end")

    def import_pdf(self) -> None:
        filename = filedialog.askopenfilename(
            title="Choisir un PDF de stratégie",
            filetypes=[("Documents PDF", "*.pdf")]
        )
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

    def check_mt5(self) -> None:
        try:
            import MetaTrader5 as mt5
        except ImportError:
            messagebox.showinfo(
                "MetaTrader 5",
                "Le module MetaTrader5 n'est pas installé. Installez le terminal MT5 et le package Python sous Windows."
            )
            return
        try:
            if not mt5.initialize():
                messagebox.showwarning(
                    "MetaTrader 5",
                    f"Connexion impossible : {mt5.last_error()}\nVérifiez que le terminal MT5 est installé et ouvert."
                )
                return
            info = mt5.terminal_info()
            account = mt5.account_info()
            self.write("\n--- État MetaTrader 5 ---\n")
            self.write(f"Terminal : {info}\n")
            self.write(f"Compte connecté : {'oui' if account else 'non'}\n")
            self.write("Lecture uniquement : aucune commande de trading n'est disponible.\n")
        finally:
            mt5.shutdown()


if __name__ == "__main__":
    ForexAIDesk().mainloop()
