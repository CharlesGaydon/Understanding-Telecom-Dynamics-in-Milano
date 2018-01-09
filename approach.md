# Approach to the problem

### Faire une représentation des communication sms+appel et internet au cours du temps



- lire ce qu'est une surcharge de réseau ; 
- trouver l'échelle d'une "antenne réseau" et rassembler nos cases en fonction -> nouvelle grille.
- déterminer par une combinaison linéaire un score par nouvelle case
- prendre les 5 % les plus haut, ca donne un 19e vingtile haut, c'est notre seuil.
- on labellise par "surcharge" tous les timestamp+grosse cases au dessu.
- on prévoit avec les données non scorées. 


- tester la corrélation entre appels, sms, etc. 



ICI : MES NOTES PAS NETTOYEES POUR INSPI :

En vrac pour DM

Comprendre comment se font les appels internes à la ville (moyenne puis répartition des distances pondérée par l'intensité ?) - essayer d'obtenir une représentation simplifiée des flux d'information/d'appel 

Tester corrélation appel/sms et internet versus appel/sms pour justifier futures simplifications.

Construire le voisinage (forme circulaire) moyen d'une cas de grille en pondérant les voisinage avec la somme de leurs voisins.

Transformer l'information des appels/sms d'une journée type en un vecteur par grille, et clustering pour rassembler des cellules de la grille ayant le même profil journalier. 
Par exemple :  
Pour chaque cellule C :
  Sommer dans un vecteur de 24*k (k<=6) cases les intensités de communication pour sms/appel/internet (potentiellement 3 vecteurs donc trois clusterings différents) ; 
  - transformer en un attribut catégoriel chaque case suivant que la valeur est au dessus/en dessous de la médiane 'au bien au desus en dessous de troisième quartile, ou deuxième tercie, à voir), et faire du fréquent mining -> on risque pas de trouver grand-chose si trop de cases de cette façon car dimensionnality curse -> réduire à 24/12 la taille d'un vecteur (justification : le système est humain donc le binning sur des valeurs entières a un sens). 
  - Transformer en valeur numérique distinctes par binning et faire un clustering sur le vecteur total
  - Faire directement du clustering sur vecteur total.


Caractériser une cellule par la moyenne de ses 4 corrélation max parmi ses 8 voisins, garder les cellules ayant valeur au dessus d'un seuil et ensuite faire clustering density-based basée sur la position -> zones de co-activité mises en avant.

De l'itemset mining basé sur une approche graphe : 

  - construire le graphe d'interaction moyen sur une journée ;
  - Ne garder que les interaction au dessus d'un seuil pour tous ;
  - Pour chaque cellule, obtenir la fréquence des voisins de tous ses voisins ;
  - Représenter une cellule par le set des voisins de voisin les plus fréquents, c’est-à-dire par le set des cellules ayant le comportement le plus similaire à elle.
  - Ajouter la cellule dans son propre set ;
  - Clusterer les sets par edit distance sur un vecteur de taille 1000 où un 1 représente a présence dans le set. 
  - On a nos clusters de comportement similaire. 

Partie ML : 
  - Essayer de classifier un profil de quelques zones (style : résidentiel versus travail versus rue si cellule assez petite) et ensuite faire du nearest neighboor progressif.
  - Investiguer le lien entre la pluie et les communications (pas de prédiction possible à priori…)
  - Voir si l'intensité de la pluie peut être donnée par l'intensité des communications… Les données correspondent surement à des nombres d'appel et pas à des forces de signal, donc on ne peut pas forcément tirer quelque chose d'intéressant… Mais pourrait être pertinent pour cartographier des régions sinon…! 
  - Vu que le problème est simple à formaliser (x est un vector à trois valeur pour chaque région et pour chaque dix minutes, y est un chiffre entre 0 et 4, ça vaut le coût de tester ! 

Penser à de la promotion intelligente : dire au client que ses appels/sms/internet lui coûtent moins cher si il est dans un évènement -> détecter les foules de manière macro - proof of concept que c'est possible micro avec surement le même modèle. Donc : faire de la détection d'activité importante et très localisée dans le temps et l'espace! 

Outier/novelty detection par modeles génératifs (c’est-à-dire connaissant p(x|classe) ?
Ou bien simplement on mappe la distribution pour détecter des journées particulières ?

Self organizing networkd : pas vraiment de la ML… Mais prédire la congestion d'une zone pourrait etre utile si la réorganisation n'est pas instantanée.
