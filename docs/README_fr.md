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

Pour créer le fichier d'installation pour pypi, il faut taper la commande 
`python -m build <module>` et remplacer `<module>` par le module TASS que 
l'on veut bâtir. Le fichier d'installation peut être trouvé dans le dossier 
`dist`.

#### Bâtir le projet pour Conda

Pour créer le fichier d'installation pour conda, il faut taper la commande 
`conda build <module>/conda-recipe` et remplacer `<module>` par le module TASS que 
l'on veut bâtir. Le fichier d'installation peut être installé avec la commande 
`conda install --use-local <module>`.

### Installation

TASS peut être installé en téléchargeant le fichier d'installation approprié 
et utilisé la commande d'installation appropriée.

#### pip

Téléchargez le fichier .whl pour la version désirée. Dans le programme CLI, 
installé le fichier avec `pip install <chemin/au/fichier/wheel>`.

#### conda

Téléchargez le fichier .tar.bz2 pour la version désirée. Dans votre 
environnement conda, utiliser la commande `conda install <chemin/au/fichier/tar.bz2>`.
Ensuite, utiliser la commande `conda install --use-local <nom du module>` pour 
installer les dépédences.

### Utilisation

TASS peut être utilisé dans la CLI avec les commandes documentées dans les pages 
des modules appropriées:

- [tass-core](https://github.com/StatCan/tass-ssat/tree/main/tass-core)
- [tass-converter](https://github.com/StatCan/tass-ssat/tree/main/tass-converter)
- [tass-orchestrator](https://github.com/StatCan/tass-ssat/tree/main/tass-orchestrator)
- [tass-report](https://github.com/StatCan/tass-ssat/tree/main/tass-report)

#### Démo

Le projet contient plusieurs examples et fichiers de démonstrations. Pour les 
utiliser, faîtes une copie du projet et créer votre environnement conda. Tous 
les fichiers nécessaires sont dans le dossier d'examples.

[EXAMPLES](https://github.com/StatCan/tass-ssat/tree/main/examples)

## Licence / Droits d'auteurs

Le code et tous les fichiers dans ce projet sont sous la licence Apache 
license version 2, sauf si une licence différente est spécifiée dans le 
fichier. Si c'est le cas, la licence du fichier est applicable.

Copyright © Sa Majesté le Roi du chef du Canada, représentée par le ministre responsable de Statistique Canada, 2023.

Le texte ci-bas est tiré de la notification officielle d'Apache:

Licensed under the Apache License, Version 2.0 (the "License"); you may
not use this file except in compliance with the License. You may obtain
a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
License for the specific language governing permissions and limitations
under the License.
