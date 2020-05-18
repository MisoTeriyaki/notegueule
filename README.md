# notagueule
Outil pour augmenter la bienveillance lors de l'évaluation d'élèves.

* Nécessite : python3, pyqt5, pandas, numpy, matplotlib (fonctionne directement avec la distribution Anaconda)
* Procédure : 
  * Les notes sont dans un fichier tel **listeNote.csv** avec la dernière colonne correspondant aux notes à ajuster.
  
    Le séparateur de champ est le point-virgule et les décimales sont représentées délimitées par la virgule.
    
    **Toutes les cellules de la colonn à ajuster doivent contenir un nombre.**
  * Exéctuer le code Python.
  * Définir la note maximale.
  * Ajuster d'abord la moyenne et ensuite l'écart+type.
  * Les notes ajustées sont dans la colonne **notagueule**.
  * Le bouton Export enregistre les notes ajustées dans un fichier **NTGExport.csv**.
  
 * Modifications :
   * Correction d'une grosse boulette dans une formule
   * Le fichier de notes peut contenir plusieurs colonnes.
   * Bouton d'export
  
  
* Prochaines améliorations :
  * Importation d'un fichier de notes à partir d'un sélecteur de fichier
  * Equivalence crédit ECTS pour les élèves de classes préparatoires
  * Génération d'un fichier compatible Pronote
  * Prise en compte de bonus suivant les voeux de poursuite d'étude




