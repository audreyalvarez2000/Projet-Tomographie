![Logo INSA](https://bibliotheques.univ-toulouse.fr/sites/default/files/etablissements/logo/insa.png)

# Projet-Tomographie

### Dans le cadre de notre quatrième année d'étude 2021-2022 à l'INSA Toulouse, il a été demandé de mener à bien un projet multidisciplinaire qui s'intitule Réalisation d'un programme Python pour reconstruction d'images de tmographie X, dont les tuteurs sont Simon Cayez et Pier Francesco Fazzini

Ce dépôt GitHub a pour but de présenter la tomographie et d’expliquer les différents algorithmes de reconstruction réalisés avec Python et les paramètres. Les différents algorithmes étudiés sont **gridrec**, **filtered back projection** (fbp) , qui sont tous les deux des **algorithmes analytiques**, et **“BP3D_CUBA”** qui est un **algorithme itératif**. 

### Explication brève des algorithmes

Le premier s’effectue grâce à une **transformée de Fourier** de chaque projection des images suivi d’une **interpolation** et d’une **transformée de Fourier inverse**. Le second quant à lui, ne fonctionne pas avec une interpolation mais avec un **filtre rampe**. Cet algorithme a l’avantage de donner une reconstruction avec moins d’artéfacts que celle obtenue avec gridrec. 
Enfin l’algorithme “BP3D_CUBA”, permet de faire une **rétroprojection filtrée sur un objet 3D directement**.

Après avoir étudié ces différents algorithmes, nous avons écrit le nôtre qui se compose d’un **filtrage** de nos images (qui forment un sinogramme) puis d’une transformée de **Radon inverse**.
Les différents paramètres mis en lumière sont le *filtre, le centre de rotation, la segmentation et la sélection des images utiles*, dont les programmes pour les trois premiers sont ajoutés en amont et le dernier en aval de la reconstruction.

### Conclusion

Enfin, nous pouvons conclure sur le type de filtre le plus adapté (le flou gaussien), et conclure quant au fait que l’algorithme fbp, bien que plus long à exécuter que le gridrec, nous permet d’avoir une reconstruction de plus grande qualité.

### Les Codes

Tous ces codes sont répartis de la manière suivante sur GitHub:

* Le code complet qui permet de faire la reconstruction grâce à la blibliothèque tomopy avec l'algorithme gridrec est disponible [ici](https://github.com/audreyalvarez2000/Projet-Tomographie/blob/Codes-s%C3%A9par%C3%A9s/Reconstruction_Gridrec.ipynb)
* Le code complet qui permet de faire la reconstruction grâce à la blibliothèque tomopy avec l'algorithme fbp est disponible ici
* Le code complet qui permet de faire la reconstruction grâce à la blibliothèque tomopy  et AstraToolBox est disponible ici
* Le code pour le [centre de rotation](https://github.com/audreyalvarez2000/Projet-Tomographie/blob/Codes-s%C3%A9par%C3%A9s/Centre_de_rotation.ipynb) et sa [vérification](https://github.com/audreyalvarez2000/Projet-Tomographie/blob/Codes-s%C3%A9par%C3%A9s/Verification_centre_rotation.ipynb)
* Les [filtres pour le traitement d'images](https://github.com/audreyalvarez2000/Projet-Tomographie/blob/Codes-s%C3%A9par%C3%A9s/Filtres_traitement_signal.ipynb)
* La [segmentation](https://github.com/audreyalvarez2000/Projet-Tomographie/blob/Codes-s%C3%A9par%C3%A9s/segmentation_image.ipynb)
* La [sélection des images utiles](https://github.com/audreyalvarez2000/Projet-Tomographie/blob/Codes-s%C3%A9par%C3%A9s/Selection_image_utile.ipynb) à la reconstruction
* Le code permettant d'[enregistrer les images de la reconstruction](https://github.com/audreyalvarez2000/Projet-Tomographie/blob/Codes-s%C3%A9par%C3%A9s/Sauvegarde_reconstruction.ipynb)
* Le code de notre propre algorithme
* Les autres codes sont disponibles sur ce [lien](https://github.com/audreyalvarez2000/Projet-Tomographie/tree/Codes-s%C3%A9par%C3%A9s)

Enfin le rapport complet sur notre projet est disponible ici.
