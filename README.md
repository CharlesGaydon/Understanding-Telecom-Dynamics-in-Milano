___
Auteurs du projet : Romain CANDY, Charles GAYDON, Tangui de CREVOISIER, Enzo LEBRUN

Année universitaire 2017-2018

[*Lien vers ce répertoire GitHub*](https://github.com/CharlesGaydon/Understanding-Telecom-Dynamics-in-Milano/).
___

# Comprendre le réseau de télécommunications à Milan 
Clustering, règles d'association, ML prédictif et classification

Les italiens sont connus pour etre bavards. Que peut nous apprendre sur eux les enregistrement de leurs télécommunications ?

**Se référer aux rapports HTML joints pour comprendre les enjeux et les résultats de ce projet !**

### Structure du répertoire:

- trois premiers *jupyter notebook* = travail de machine learning (exploration descriptive, régression (LSTM), classification)
- dossiers DataMining : contient un *jupyter notebook* ainsi que de nombreuses sources (scripts python pour génération de clustering + site web pour leur visualisation)
- dossier Milano-pregel : contient un projet spark, écrit en scala et impliquant la librairie GraphX, pour une utilisation de l'algorithme Google-Pregel sur les données de telcom à Milan

### Setup :

Pour créer l'environnement virtuel Anaconda3, utiliser : 
	
	conda env create --file conda_Milano_env.yml

puis l'activer (avec *source activate* si sous windows):
	
	(source) activate Milano

Cet environnement nous permettra d'employer tensorflow avec une devanture Keras pour la tâche de régression sur la prédiction d'usage. On peut également y adjoindre manuellement *pytorch* en suivant les instructions officielles.

### Processing pour modèle de régression

Le modèle de Machine Learning utilisé dans le notebook *2_Predictive_LSTM_1_steps* est entraînable *square* par *square* (une aggrégation est cependant envisageable).

Pour extraire les données d'un *square* dans un format approprié, s'assurer que l'arborescence des fichiers soit de la forme :

- ./data/MI_data (ici tous les fichiers jour par jour des communications à Milan, non directionnelles)
- ./data/MI_squares (ici dossier vide où seront crés les dossiers contenant les données isolées par square)

et faire : 

	python preprocess_tools.py square_to_extract
