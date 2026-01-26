# Suite et services d’automatisation et de testing

L'application SSAT permet à ses utilisateurs de créer et exécuter des
scénarios tests pour des applications web. SSAT utilise des fichier 
de configuration JSON pour définir les scénarios de test et chaque 
fichier représente un groupe de scénarios.

## Pour commencer

SSAT dépend sur un environnement compatible avec conda et un gestionnaire 
dépendance similairement compatible. L'application est testé sur Windows 
et macOS. Nous essayons aussi d'assurer que l'application fonctionne sur 
Linux. SSAT peut être installée à partir de la section [publication]
(https://github.com/StatCan/tass-ssat/releases) du projet.

### Développement

Pour contribuer au projet, lisez notre document à propos de nos 
[pratiques standards](best_practices_FR.md). Vous pouvez créer 
votre environnement via la commande 

`conda env create -f environment.yaml`.

L'environnement conda contient toutes les dépendances de SSAT 
sauf pour Appium. Appium peut être installé via la commande 
 `npm -g install appium`. Pour exécuter les tests, installé 
 SSAT de façon éditable avec la commande `pip install -e <module>` 
 à partir du dossier de base. Remplacez `<module>` par la 
 composante appropriée:
 
- tass-core
- tass-converter
- tass-report
- tass-orchestrator

Vous pouvez aussi télécharger le script "install_tass" pour votre 
environnement du dossier "scripting" et l'exécuter pour automatiquement 
copier le projet git, créer l'environnement conda et installer les 
versions éditables des composantes tass.

#### Bâtir le projet pour Pypi

#### Bâtir le projet pour Conda

### Installation

#### pip

#### conda

### Utilisation

#### Demo

## Licence / Droits d'auteurs
