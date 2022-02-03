# Projet-Tomographie

Les différents algorithmes.

gridrec: Fourier grid reconstruction algorithm
Le théorème de la tranche de Fourier stipule que la transformée de Fourier d'une projection d'une fonction f(x,y), vue sous un angle θ, est égale à la tranche de la transformée de Fourier de f(x,y), F(f(x,y )) = F(ωx, ωy), sous cet angle θ.

Si des projections de tous les angles 0 <= θ < π sont données, leurs transformées de Fourier couvriront complètement la transformée de Fourier de la fonction f(x,y). Ainsi, la fonction f(x,y) peut être déterminée par ses projections lors de l'assemblage correct des transformées de Fourier des projections, puis rétro-transformée dans le domaine spatial.

(image dans le notebook)

fbp: Filtered back-projection algorithm.



art: Algebraic reconstruction technique
