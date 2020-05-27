# notagueule v0.3
Outil pour augmenter la bienveillance lors de l'évaluation d'élèves.

* Nécessite : python3, pyqt5, pandas, numpy, matplotlib (fonctionne directement avec la distribution Anaconda)
* Procédure : 
  * Vous disposez d'un fichier de notes avec la colonne à ajuster est la dernière colonne à droite et le tableau de notes commence à la première ligne. Il n'y a pas de texte dans les cellules à "ajuster"
  * Depuis un tabteur, exportez les notes dans un fichier au format csv avec **;** comme délimiteur et **,** comme signe des décimales
  * Exéctuer le code Python.
  * Ouvrir votre fichier
  * Définir la note maximale.
  * Ajuster **d'abord la moyenne**.
  * Les notes ajustées sont dans la colonne **notagueule**.
  * Exporter les notes au format csv.
  
  
* Prochaines améliorations :
  * Equivalence crédit ECTS pour les élèves de classes préparatoires
  * Génération d'un fichier compatible Pronote
  * Prise en compte de bonus suivant les voeux de poursuite d'étude




