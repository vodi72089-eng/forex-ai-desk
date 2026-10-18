# Forex AI Desk

Application de bureau Windows pour lire des stratégies Forex en PDF, vérifier la présence de règles mesurables, demander une synthèse à des agents IA configurés et consulter MetaTrader 5 en lecture seule.

## État actuel

Le dépôt contient un prototype en cours de développement, pas un robot de trading réel prêt pour la production.

### Fonctionnalités présentes
- Interface de bureau Python/Tkinter.
- Extraction du texte des PDF sélectionnables (pas encore d'OCR pour les PDF scannés).
- Vérification heuristique de la présence de conditions d'entrée, stop-loss, take-profit, timeframe et gestion du risque.
- Routage d'analyse vers une API compatible OpenAI, puis Hermes/OpenCode en secours si ces programmes sont installés et configurés.
- Vérification facultative de la connexion MetaTrader 5 en lecture seule.
- Tests unitaires exécutés avant le build Windows.
- Workflow GitHub Actions pour produire un artefact EXE si les tests et la compilation réussissent.

## Installation locale

Python 3.11 recommandé.

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
```

## Configuration de l'agent API

Les paramètres Jev sont volontairement lus depuis les variables d'environnement. L'API doit être compatible avec le format Chat Completions :

- `JEV_BASE_URL` : URL de base du fournisseur, sans suffixe `/chat/completions`.
- `JEV_API_KEY` : clé secrète.
- `JEV_MODEL` : nom exact du modèle.
- `HERMES_ARGS` : facultatif, tableau JSON de paramètres CLI fixes si la version de Hermes en a besoin.

Ne committez jamais de clés dans ce dépôt public. L'adaptateur Jev n'a pas été validé contre une documentation API Jev spécifique; il nécessite confirmation de son format exact. Les interfaces CLI Hermes/OpenCode peuvent varier selon la version installée.

## MetaTrader 5

Installez le terminal MetaTrader 5 sous Windows. La vérification de connexion est facultative. Le prototype ne contient aucune fonction d'envoi d'ordres.

## Sécurité et limites

- Cette application ne fournit pas de conseil financier et ne prédit pas la rentabilité.
- La détection de mots-clés n'est pas une validation de stratégie.
- Aucune transaction réelle n'est envoyée.
- Les fonctions d'exécution d'ordres, le backtest historique complet, l'OCR et le stockage sécurisé des secrets ne sont pas encore implémentés.
- N'utilisez pas de compte réel pour tester un prototype.

## Compilation Windows

Dans GitHub, ouvrez **Actions**, sélectionnez **Test and build Windows executable**, puis lancez **Run workflow**. Après un succès, téléchargez l'artefact `ForexAIDesk-Windows` depuis l'exécution concernée. Un EXE n'est pas généré tant que le workflow n'a pas réussi.
