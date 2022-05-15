# Projet-Tomographie

## Dans le cadre de notre quatrième année d'étude 2021-2022 à l'INSA Toulouse, il a été demandé de mener à bien un projet multidisciplinaire qui s'intitule Réalisation d'un programme Python pour reconstruction d'images de tmographie X, dont les tuteurs sont Simon Cayez et Pier Francesco Fazzini

Ce dépôt GitHub a pour but de présenter la tomographie et d’expliquer les différents algorithmes de reconstruction réalisés avec Python et les paramètres. Les différents algorithmes étudiés sont _gridrec_, _filtered back projection_ (fbp) , qui sont tous les deux des _algorithmes analytiques_, et _“BP3D_CUBA”_ qui est un _algorithme itératif_. 

Le premier s’effectue grâce à une _transformée de Fourier_ de chaque projection des images suivi d’une _interpolation_ et d’une _transformée de Fourier inverse_. Le second quant à lui, ne fonctionne pas avec une interpolation mais avec un _filtre rampe_. Cet algorithme a l’avantage de donner une reconstruction avec moins d’artéfacts que celle obtenue avec gridrec. 
Enfin l’algorithme “BP3D_CUBA”, permet de faire une _rétroprojection filtrée sur un objet 3D directement_.

Après avoir étudié ces différents algorithmes, nous avons écrit le nôtre qui se compose d’un _filtrage_ de nos images (qui forment un sinogramme) puis d’une transformée de _Radon inverse_.
Les différents paramètres mis en lumière sont le *filtre, le centre de rotation, la segmentation et la sélection des images utiles*, dont les programmes pour les trois premiers sont ajoutés en amont et le dernier en aval de la reconstruction.

Enfin, nous pouvons conclure sur le type de filtre le plus adapté (le gaussaient flou), et conclure quant au fait que l’algorithme fbp, bien que plus long à exécuter que le gridrec, nous permet d’avoir une reconstruction de plus grande qualité.

Tous ces codes sont répartis de la manière suivante sur GitHub:
* Le code complet qui permet de faire la reconstruction grâce à la blibliothèque tomopy est disponible ici
* Le code pour le centre de rotation et sa vérification
* Le filtre gaussien
* La segmentation
* La sélection des images utiles à la reconstruction
* Le code permettant d'enregistrer les images de la reconstruction
* Le code de notre propre algorithme

Enfin le rapport complet sur notre projet est disponible ici.
