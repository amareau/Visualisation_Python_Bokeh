L'objectif de ce travail est de réaliser une application sous Bokeh.

# Les données
Le fichier *donneesEducation.csv* provient du site web eurostat. Il présente des données européennes sur le niveau d'éducation de la population, par pays, par sexe, par année.

Les informations disponibles sont les suivantes :
- **sex** : Population Hommes, Femmes ou Tous,
- **age** : Classes d'âges avec différentes granularités,
- **niveau** : Niveau d'éducation (les correspondances des niveaux sont données dans le fichier *nomenclatures.ods*),
- **pays** : Origine géographique des données (les correspondances des abbréviations sont données dans le fichier *nomenclatures.ods*),
- **années** : Pour chaque année, indique le pourcentage de la population concernée ayant atteint ce niveau d'éducation.

Nous avons choisi de ne garder que les niveaux d'études suivants : *ED1-2, ED3-4* et *ED5-8* ("primaire ou moins", "collège-lycée", "études supérieures" respectivement).  
Au niveau des tranches d'âge, nous  conservons les suivantes *25-64, 25-34, 35-44, 45-54* et *55-64* afin d'éviter les séquences qui se chevauchent.  
Pour le remplissage des cartes géographiques, nous avons eu besoin des coordonnées des frontières de chaque pays européens (données de taille importante). Afin d'éviter un  temps de chargement conséquent de ces coordonnées à chaque lancement d'application, nous avons décidé de le réaliser en amont, de les exporter vers un fichier csv et de les importer quand on lance l'application.

# Les onglets
Cette application contient 4 onglets :
- Dans le premier onglet, **Cartographie**, le graphe intéractif permet de comparer entre chaque pays le pourcentage de la population choisie ayant le niveau d'étude sélectionné. L'utilisateur intervient donc dans la réalisation du graphe par son choix de l'année, de l'âge de la population et du niveau d'éducation. Un code couleur permet de visualiser les pays ayant les parts les plus importantes jusqu'aux pays ayant les pourcentages les plus faibles. L'utilisateur peut également positionner le curseur de sa souris sur le pays qui l’intéresse pour avoir la valeur exacte de cette proportion observée.
- Dans le deuxième onglet, **Rang**, on se retrouve face à une pyramide représentant le top 10 des pays avec les plus hauts pourcentages d'études supérieures (catégorie *ED5-8*) pour une population âgée de 25 à 64 ans dissociée par le sexe. L'utilisateur intervient dans le choix de l'année pour laquelle il souhaite connaître le classement.
- Dans le troisième onglet, **Evolution**, les courbes représentent les évolutions de proportions d'une population donnée différenciée par le sexe. L'utilisateur intervient dans trois choix, à savoir : le pays, la tranche d'âge et le niveau d'étude. Ce graphique permet de se rendre compte de l'évolution de l'éducation au cours du temps et de la comparer entre femmes et hommes.
- Le dernier onglet, **Répartition en France**, est composé de trois graphiques en secteurs différenciés par le sexe (Femmes, Hommes, Tous). Ces grahiques représentent la part des trois niveaux d'étude dans une population définie par l'utilisateur par le choix de l'année et la tranche d'âge.

# Préliminaires à l'ouverture de l'application
Avant de réaliser les étapes pour ouvrir l'application, il faut bien vérifier à ce que les packages suivants soient bien installés sur Python :
- pandas
- json
- ast
- pyproj import Proj, transform 
- bokeh
- math import pi

# Comment ouvrir l'application ?
- Ouvrir une console (type anaconda prompt)
- Se placer dans le dossier contenant le fichier Script.py
- Taper : bokeh serve --show Script.py
- L'application s'ouvre

# Aperçu de l'application
Le fichier *BokehAppDisplay.avi* disponible sur le GitHub est une brève présentation l'application, libre à vous de le télécharger et de le visionner.

# Auteurs
- DABOUDET Claire
- DURAND HARDY François
- MAREAU Alexis
