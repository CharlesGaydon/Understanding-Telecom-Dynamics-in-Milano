# Understanding Telecom Dynamics in Milano

Italians are known to be quite talkative. What can their telecommunications teach us about the dynamic of Milano ?

Here is the link of the hackmd : https://hackmd.io/GwMwxsCMBGkKwFoCcITQQFgMwY8kwwCAHAIYECm0ADNCBgCbRA==
A enlever quand on passera public evidemment.

usage :

Pour créer l'environnement anaconda, utiliser : 
	
	conda env create --file conda_Milano_env.yml
puis l'activer (source si sous windows):
	
	(source) activate Milano

Cet environnement nous permettra d'employer tensorflow avec une devanture Keras pour la tâche de régression sur la prédiction d'usage. On peut également y adjoindre manuellement *pytorch* en suivant les instructions officielles.

### Traitement de données

Les modèles de Machine Learnng sont pour l'instant entraînable *square* par *square*.
Pour extraire les données d'un *square* dans un format approprié, s'assurer que l'arborescence des fichiers soit de la forme :

- ./data/MI_data (ici tous les fichiers jour par jour des communications à Milan, non directionnelles)
- ./data/MI_squares (ici dossier vide où seront crés les dossiers contenant les données isolées par square)

et faire : 

	python preprocess_tools.py square_to_extract

Dans le jupyter notebook peuvent être trouvées quelques explorations de données ainsi que les script d'entraînement et de test d'un modèle LSTM pour la prédiction de l'intensité des communications.