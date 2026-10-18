# Forex AI Desk

Application Windows pour analyser des stratégies Forex avec l'IA, consulter MetaTrader 5 et tester des idées en **paper trading**.

## État actuel

Ce dépôt contient le socle initial. Ce n'est pas encore un robot de trading réel prêt pour la production.

### Objectifs
- Interface desktop Windows.
- Import et extraction de texte depuis des PDF de stratégies.
- Connexion MetaTrader 5 facultative pour lire le compte et les prix.
- Mode simulation par défaut.
- Adaptateurs séparés pour Hermes, OpenCode CLI et une API Jev, à configurer lorsque leurs interfaces exactes sont confirmées.
- Création d'un exécutable Windows via GitHub Actions.

## Installation locale

Python 3.11 recommandé.

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
```

## MetaTrader 5

Installez le terminal MetaTrader 5 et connectez-vous à un compte de démonstration. Le package Python `MetaTrader5` est pris en charge principalement sous Windows. La connexion est facultative; l'application démarre en mode simulation si MT5 n'est pas disponible.

## Sécurité financière

- Le mode simulation est le comportement par défaut.
- Aucune transaction réelle n'est envoyée par cette version initiale.
- Ne mettez jamais de clé API, mot de passe ou fichier de compte dans GitHub.
- Toute fonction de trading réel devra exiger une activation explicite, une validation du risque, des limites de taille/perte et des tests avant son implémentation.

## Compilation Windows

Le workflow GitHub Actions `.github/workflows/build-windows.yml` produit un artefact `.exe` après une exécution réussie. Ce build n'est pas encore signé numériquement.
