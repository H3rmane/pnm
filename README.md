Ce paquet met en place un système structuré pour le traitement des fichiers PNM , avec un focus sur la lecture, le formatage et l'écriture d'entrées structurées. Il est composé de trois classes principales :

PNMFormatter :
Responsable du formatage des enregistrements selon une structure de champs prédéfinie.
Assure que chaque entrée respecte un format à largeur fixe, en appliquant des règles de troncature et d’alignement.
PNMWriter :
Utilise PNMFormatter pour formater correctement les enregistrements avant de les écrire dans un flux de sortie.
Prend en charge l’écriture vers plusieurs destinations (fichiers, mémoire via StringIO, etc.).
PNMReader :
Lit un fichier PNM et détermine le bon format en fonction de sa structure.
Sélectionne dynamiquement le bon parseur parmi les formats disponibles.
