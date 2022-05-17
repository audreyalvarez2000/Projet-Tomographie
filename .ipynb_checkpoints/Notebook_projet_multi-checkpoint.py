#!/usr/bin/env python
# coding: utf-8

# # Notebook pédagogique pour le TP Tomographie
# 
# ## Introduction
# 
# La tomographie est une technique d’imagerie permettant la reconstruction
# d'images en coupe d’un objet. La tomographie à rayon X repose sur l'interaction des dits rayons avec la matière.
# 
# Dans notre cas, c’est l’objet qui tourne et non la source. 
# La reconstruction sert à reproduire un objet 3D en un ensemble de coupes 2D. L’intérêt de cette méthode est de pouvoir détecter une anomalie à l’intérieur de l’objet sans avoir à l'ouvrir ainsi que de connaître sa structure.
# 
# Deux méthodes de reconstruction sont possibles, une méthode dite analytique et une méthode itérative.
# 
# Dans ce notebook vous allez, étape par étape, découvrir le traitement d'images et les différents algorithmes en question.

# ## Étape 0 : Lancer Anaconda et activer l'environnement
# 
# Tout d'abord il faut lancer Anaconda. Ensuite quand celui-ci est ouvert, ouvrez le terminal Anaconda prompt si celui-ci ne c'est pas ouvert. Tapez-y la commande *'conda activate tomo2122'* pour activer l'environnement. 
# 
# Ensuite en haut à gauche dans *'Applications on'* sélectionnez *'tomo2122'.*

# ## Étape 1 : Importer les bibliothèques, choisir le fichier et le lire
# 
# ### 1. Importation des bibliothèques

# In[ ]:


import tomopy
import dxchange
import matplotlib.pyplot as plt
import datetime
import time
import cv2
import numpy as np
import glob
from imagestacks import create_animation
from IPython.core.display import HTML
from PIL import Image, ImageFilter
get_ipython().run_line_magic('matplotlib', 'inline')
import skimage
from skimage.transform import iradon
from skimage.transform import radon
from skimage.exposure import rescale_intensity


# ### 2. Choix du fichier
# 
# Pour pouvoir traiter les images issues de la machine à rayon X il faut choisir le fichier. Il faut sélectionner le chemin de la première image du dossier les contenant.
# Attention, si le numéro de votre image est 1 (ou 0001 par exemple), il faut mettre dans indice i+1, et i si la première image est numérotée 0.
# Dans fname, remplacer Mettre le chemin par celui de votre image entre apostrophes.

# In[ ]:


fname = 'Mettre le chemin'
ind = [i+1 for i in range(181)]
print(ind)
print(fname)


# ### 3. Lecture du dossier
# Comme c'est un dossier d'images au format tif que l'on souhaite lire, on doit utiliser la bibliothèque dxchange et la fonction reader.

# In[ ]:


start = datetime.datetime.now()
proj = dxchange.reader.read_tiff_stack(fname, ind)
end = datetime.datetime.now() 
duree = end - start #Pour mesurer le temps mis pour effectuer la ligne proj
print(duree)


# ## Étape 2: Traitement de la taille des images et affichage
# 
# Pour cette étape, les images vont être réduite pour diminuer le temps d'exécution grâce à la fonction misc.morph.downsample de la bibliothèque tomopy.

# In[ ]:


#diminuer la taille des images
print('avant',proj.shape)
down = tomopy.misc.morph.downsample(proj, level=1, axis=1)#axe 1 lignes: faire la moyenne des pixels 2 à 2
down = tomopy.misc.morph.downsample(down, level=1, axis=2)# axe 2 colonnes: faire la moyenne des pixels 2 à 2
#Avec axe 0 on aurait pris l'image complète qu'on aurait moyener avec tous les tilts ce qui aurait eu un rendu flou
print('apres',down.shape)


#afficher la  1ere image avant downsampling
image0 = proj[0, :, :]#image zéro, on prend tous les pixels horizontaux et verticaux: toute la matrice des pixels
plt.imshow(image0, cmap='Greys_r')
plt.show()


#afficher la  1ere image apres downsampling
image0 = down[0, :, :]
plt.imshow(image0, cmap='Greys_r')
plt.show()

#Pour faire afficher les images les unes après l'autre
yxratio=down.shape[2]/down.shape[1]
anim2 = create_animation(down, size=4,4/yxratio)
display(HTML(anim2.to_jshtml()))


# ## Étape 3: Traitement des images pour améliorer la qualité
# 
# Afin d'avoir une meilleure reconstruction il faut préalablement améliorer la qualité de nos images pour enlever le bruit.
# 
# 1. Le premier filtre que vous allez tester est le filtre flou (blur).
# 
# Vous allez ouvrir une image de votre dossier. et appliquer le filtre puis afficher votre image.
# 

# In[ ]:


#Ouverture de l'image à traiter
image = cv2.imread('nom de votre image') # lire l'image 
image2 = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY ) # convertir BGR en RGB permet d'avoir sur 1 pixel une seule couleur et pas 3 
plt.imshow(image2,cmap='gray') #converti en GRAY 

#Filtre
figure_size = 9 # les dimension de l'axe x and y du noyau.
new_image = cv2.blur(image2,(figure_size, figure_size)) #Filtre blur (flou)
plt.figure(figsize=(11,6))

#Affiche l'image d'origine et l'image après filtrage
plt.subplot(121),plt.imshow(image2,cmap='gray'),plt.title('Original')
plt.xticks([]), plt.yticks([])

plt.subplot(122), plt.imshow(new_image, cmap='gray'),plt.title('filtre_blur')
plt.xticks([]), plt.yticks([])
plt.show()


# Ce filtre permet donc d’obtenir une image floue de l’originale. Ce filtre n’est pas le résultat attendu car nous aimerions obtenir uniquement le fond uniforme et ne pas toucher à l’image de l'objet observé.
# 
# 2. Le deuxième filtre que vous allez tester est le flou gaussien (GaussianBlur).
# 
# Pour pouvoir exécuter le code ci-dessous vous devez créer un dossier vide sur l'ordinateur dans lequel les images traitées seront enregistrées. Ensuite vous devrez remplacer "Chemin du dossier créé pour y mettre les images traitées+nom de l'image%i.tif" par le chemin de votre dossier et le nom que vous souhaitez donner à vos images.
# 
# Voici un exemple : "/Users/audreyaudrey/Desktop/Projet multi/Dossier image traitée/imtrait%i.tif"

# In[ ]:


#Initialisation
i=0
dossier = 'Mettre le chemin de la première image du dossier'
num_image = [] #on definit des listes qui serviront à tracer les courbes

#Bloucle pour traiter tout les images avec le filtre
for image in glob.glob(dossier+"/*.tif"):
    print('-----------------')
    print('image n°: ',i)
    num_image.append(i)#ajouter à la liste num_image
    img = cv2.imread(image)# lire l'image
    gaussian= cv2.GaussianBlur(img,(5,5),5) #Filtre GaussianBlur (flou gaussien suit une loi gaussienne)
    
    #Permet d'enregistrer les images filtrées
    cv2.imwrite("Chemin du dossier créé pour y mettre les images traitées/+nom de l'image%i.tif"%i,gaussian)
    
    i+= 1


# Ce filtre permet  de définir un flou à partir d’un noyau défini dans la fonction gaussienne. 
# Ce filtre permet donc d’avoir un bruit de fond plus lisse sans endommager l’image de l’objet.   
# 

# ## Étape 4 : Centre de rotation et vérification
# 
# 1. Trouver le centre de rotation
# 
# Pour pouvoir appliquer un algorithme de reconstruction, il faut également regarder le centre de rotation des images afin de vérifier que ce centre n’est pas décalé en fonction de l’angle de projection. 
# Dans la bibliothèque Tomopy il y a la fonction find_center qui permet de trouver ce centre de rotation d’une image. 
# 

# In[ ]:


ang = tomopy.angles(180) # Genere des angles de 0° à 180°
rot_center = tomopy.find_center(down, ang, init=None, ind=0, tol=0.5)
print(rot_center)


# Le paramètre ind permet d’indiquer vers quelle valeur de x se trouve le centre à vue d'œil. Cela permet d’aider la fonction à trouver cette valeur.
# 
# Afin de pouvoir effectuer la vérification sans modifier les images pour la reconstruction, vous allez créer un deuxième down nommé down2

# In[ ]:


down2 = tomopy.misc.morph.downsample(proj, level=1, axis=1)#axe 1 lignes: faire la moyenne des pixels 2 à 2
down2 = tomopy.misc.morph.downsample(down2, level=1, axis=2)


# Maintenant vous allez vérifier que le centre de rotation trouvé précédemment est correct.

# In[ ]:


#Permet de vérifier le centre de rotation
#Trace deux lignes: 1-vertical représentant le centre de rotation. 
#2-horizontal: repere pour vérifier si un détail tourne bien à la meme distance du centre de rotation lors des differents angles. 

for k in range(180):
    
    down2[k, :, :]= cv2.line(down2[k, :, :], (int(rot_center),0),(int(rot_center),700), (255,255,255),6) #tracé de la ligne pour verifier le centre de rotation
    down2[k, :, :]= cv2.line(down2[k, :, :], (0,400),(500,400), (255,255,255),2) #verif perpendicularité axe rotation

#permet d'afficher l'image avec la verification
plt.imshow(image0, cmap='Greys_r') 
plt.show()

#Animation pour vérifier la symétrie d'un détail par rapport à l'axe de rotation
yxratio=down2.shape[2]/down2.shape[1]
anim2 = create_animation(down2, size=4,4/yxratio)
display(HTML(anim2.to_jshtml()))


# ## Étape 5 : Normalisation des images

# In[ ]:


#normaliser avec loi log pour loi de beer lambert
norm = tomopy.prep.normalize.minus_log(down, ncore=None, out=None)


#afficher la  1ere image normalisee
image0 = norm[0, :, :]
plt.imshow(image0, cmap='Greys_r')
plt.show()


# ## Étape 6 : Les algorithmes en eux-mêmes
# 
# ### L'algorithme gridrec avec tomopy
# 
# Cet algorithme fait partie de la méthode analytique par transformée de Fourier, c'est la méthode analytique la plus simple et basique disponible dans la bibliothèque Tomopy. En effet, à partir du dossier contenant les images de chaque projection à chaque angle, une transformé de Fourier 2D est faite par cet algorithme dans une grille polaire, suivi d´une interpolation dans un plan cartésien et enfin, il faut faire une transformée de Fourier inverse 2D pour passer dans l’espace réel. 
# 
# Le problème étant qu’il faut interpoler entre le polaire et le cartésien dans l’espace de Fourier. Ce qui implique que toute erreur d’interpolation dans l’espace de Fourier entraîne une erreur dans tout l’espace réel après la transformation inverse. Les calculs pour faire cette interpolation sont longs et très lourds. 
# 
# En revanche, cette méthode implique que l’image est pixelisée afin d’appliquer le théorème de la tranche de Fourier. Celui-ci stipule que la transformée de Fourier d’une projection d’une fonction f(x,y) vue sous un angle est égale à la tranche de la transformée de Fourier de f(x,y) sous cet angle. Ainsi, cela permet d’éliminer en théorie le bruit de chaque composante. 
# 

# In[ ]:


rec = tomopy.recon(norm, ang, center=rot_center, algorithm='gridrec') 
# Reconstruction objet avec prise en compte du centre de rotation.

#Afficher l'image 25
plt.imshow(rec[256,:,:])
plt.show()

yxratio=rec.shape[2]/rec.shape[1]
anim2 = create_animation(rec, size=4,4/yxratio)
display(HTML(anim2.to_jshtml()))


# ### L'algorithme filtered backprojection (fbp) avec tomopy
# 
# L’algorithme de rétroprojection filtrée est la méthode la plus utilisée pour la tomographie 2D. Deux étapes sont nécessaires : un filtrage des images de projections sur chaque angle puis une rétroprojection afin d’obtenir la reconstruction de l’objet en un ensemble de coupe 2D. 
# 
# Le filtre appliqué dans cet algorithme est appelé filtre de rampe. Ce filtre met à zéro la composante continue et introduit des valeurs négatives. Il permet également d’amplifier les fréquences élevées ce qui permet de générer dans le signal des transitions rapides. Les valeurs négatives sont utiles pour effacer les artefacts laissés par les autres projections.
# 
# Cependant, ce filtre amplifie les hautes fréquences. C’est pourquoi, il est nécessaire d’ajouter à ce filtre, un filtre dit “Hamming” qui permettra d’atténuer cette amplification.  
# 
# Voici une image qui permet de comparer les différents filtres
# 
# ![imagecomparative](https://media.springernature.com/lw685/springer-static/image/art%3A10.1007%2Fs13246-014-0291-8/MediaObjects/13246_2014_291_Fig1_HTML.gif)
# 
# Source : Investigation of effect of reconstruction filters on cone-beam computed tomography image quality, Kavitha Srinivasan, Mohammad Mohammadi, Justin Shepherd 
# 
# Avec tomopy, la rétroprojection filtrée est effectuée de manière analytique.

# In[ ]:


rec2 = tomopy.recon(norm, ang, center=rot_center, algorithm='fbp',filter_name='hamming') 


#Afficher l'image 25
plt.imshow(rec2[256,:,:])
plt.show()

yxratio=rec2.shape[2]/rec2.shape[1]
anim2 = create_animation(rec2, size=4,4/yxratio)
display(HTML(anim2.to_jshtml()))


# ### Utilisation d'AstraToolBox avec des algorithmes itératifs
# 
# #### Filtered backprojection en itératif
# 

# In[ ]:


options={'proj_type': 'linear', 'method': 'FBP', 'num_iter':180}

#Reconstruction avec Astra Toolbox à partir des options décrites au dessus
recon=tomopy.recon(proj,ang,center=rot_center,algorithm=tomopy.astra, options=options, ncore=1)
recon=tomopy.circ_mask(recon,axis=0, ratio=0.95) #Appliquer un masque circulaire à un tableau 3D.

#Afficher l'image 25
plt.imshow(recon[256,:,:])
plt.show()

yxratio=recon.shape[2]/recon.shape[1]
anim2 = create_animation(recon, size=4,4/yxratio)
display(HTML(anim2.to_jshtml()))


# #### Utilisation de la méthode CUDA utilisant un GPU

# In[ ]:


extra_options ={'MinConstraint':0}

#methode utilisant un GPU, Permet d'avoir une reconstruction moins longue
options = {'proj_type':'cuda', 'method':'SIRT_CUDA', 'num_iter':200, 'extra_options': extra_options}

#Reconstruction avec Astra Toolbox à partir des options décrites au dessus
recon2 = tomopy.recon(proj, ang, center=rot_center, algorithm=tomopy.astra, ncore=16, options=options)
recon2=tomopy.circ_mask(recon2,axis=0, ratio=0.95) #Appliquer un masque circulaire à un tableau 3D.

#Afficher l'image 25
plt.imshow(recon2[256,:,:])
plt.show()

yxratio=recon2.shape[2]/recon2.shape[1]
anim2 = create_animation(recon2, size=4,4/yxratio)
display(HTML(anim2.to_jshtml()))


# ### Autre algorithme utilisant la transformée de Radon
# 
# La transformée de Radon permet de faire l'intégration de la fonction représentant l'objet, soit f(x,y), selon des droites de différentes orientations.
# 
# ![principe_radon_transform](https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSC4AZcJUDKqGfdL0CRJaw-XHwNP3BArQBlBnqa_ID8D3RlBGDRKl_oxT-RXwXM60e6T_E&usqp=CAU)
# 
# Source : APPLICATION OF RADON TRANSFORM IN CT IMAGE MATCHING, Yufang Cai, Kuan Shen, Jue Wang 
# 
# La transformée de Radon permet d'obtenir le sinogramme. Or, les images que vous possédez forment déjà un sinogramme.
# 
# Afin de faire la reconstruction, vous allez l'effectuer trois fois en faisant la transformée inverse de Radon mais une première fois sans filtre, une deuxième fois avec le filtre de Hanning et enfin avec le filtre de Hamming.
# 
# Pour pouvoir exécuter le code ci-dessous vous devez créer un dossier vide sur l'ordinateur dans lequel les images traitées seront enregistrées. Ensuite vous devrez remplacer "Chemin du dossier créé pour y mettre les images traitées+nom de l'image%i.tif" par le chemin de votre dossier et le nom que vous souhaitez donner à vos images.
# 
# Voici un exemple : 'R:\\4eme Annee GP\\TP4\\RadioX\\ProjetTomo_A&L\\test_reconstruc_radon\\test%i.tif'

# In[ ]:


#Permet de faire la transformée inverse de Radon sur toutes les images 
for k in range(180):
    img1 = proj[k,:,:]  
    reconstructed = iradon(gaussian,np.linspace(0, 180, img1.shape[1], endpoint=False))# Inverse de la transformée de Radon 
    reconstructed1 = iradon(img1,np.linspace(0, 180, img1.shape[1], endpoint=False), filter_name='hann') # Inverse de la transformée de Radon avec filtre de Hanning
    reconstructed2 = iradon(gaussian,np.linspace(0, 180, img1.shape[1], endpoint=False), filter_name='hamming')# Inverse de la transformée de Radon avec filtre de Hamming

#Permet d'enregistrer la reconstruction
    cv2.imwrite('Chemin du dossier créé pour y mettre les images traitées/+nom de l'image%i.tif'%k,reconstructed)
    
#Permet d'afficher les images de reconstruction avec les differents filtres
plt.subplot(121),plt.imshow(reconstructed,cmap="gray"),plt.title('filtre hanning')
plt.show()

yxratio=reconstructed.shape[2]/reconstructed.shape[1]
anim2 = create_animation(reconstructed, size=4,4/yxratio)
display(HTML(anim2.to_jshtml()))
                
plt.subplot(122),plt.imshow(reconstructed1,cmap="gray"),plt.title('filtre gaussian')
plt.show()
                
yxratio=reconstructed1.shape[2]/reconstructed1.shape[1]
anim2 = create_animation(reconstructed1, size=4,4/yxratio)
display(HTML(anim2.to_jshtml()))

plt.subplot(131),plt.imshow(reconstructed2,cmap="gray"),plt.title('filtre hamming')
plt.show()
                
yxratio=reconstructed2.shape[2]/reconstructed2.shape[1]
anim2 = create_animation(reconstructed2, size=4,4/yxratio)
display(HTML(anim2.to_jshtml()))


# ## Étape 7 : Sauvegarde de la reconstruction
# 
# Pour les reconstructions précédentes qui ne nécessitent pas de boucles comme celle du dernier algorithme, vous allez exécuter le code suivant pour enregistrer les images. Choisissez le nom de vos images comme par exemple 'imagerec'.

# In[ ]:


import matplotlib.image as mpim #Definir la bibliothèque

IMAGE="imagerec%d.tiff" #Nom des images reconstruites
for i in range (0,694):
    fichier=IMAGE %i # permet de donner le nom de l'image avec le numéro de l'image associée
    mpim.imsave(fichier,rec[i,100:350,100:350]) #Permet de sauvegarder toute la reconstruction
    i=i+1


# ## Étape 8 : Sélection des images utiles
# 
# Maintenant, si vous regardez attentivement l'animation des reconstructions vous verrez que sur certaines images, aucune reconstruction est visible.
# 
# Afin d'afficher une animation plus optimale il faut sélectionner les images utiles. Pour cela, vous allez seuiller les images afin d'obtenir des images ne comportant que des pixels noirs et blancs.

# In[ ]:


#Initialisation
i=0
dossier = 'Chemin du dossier contenant les images' 
num_image = [] #on definit des listes qui serviront à tracer les courbes
blanc = []
noir = []


for i in range(0,500):
    num_image.append(i)#ajouter à la liste num_image
    img = cv2.imread('Chemin du dossier/+ nom image%i.tiff'%i, cv2.IMREAD_GRAYSCALE)
    ret, thresh1 = cv2.threshold(img, 120, 255, cv2.THRESH_BINARY) #permet de définir le seuil
    n_white_pix = np.sum(thresh1 == 255)  #compter les pixels blancs dans l'image seuillée  
    blanc.append(n_white_pix)
    #print('Number of white pixels:', n_white_pix)
    n_black_pix = np.sum(thresh1 == 0) #compter les pixels noirs dans l'image seuillée
    noir.append(n_black_pix)
    #print('Number of black pixels:', n_black_pix)

#Affiche les graphiques pour trouver le numéro de l'image à partir de laquelle les reconstructions ne sont plus visibles.
plt.subplot(121),plt.plot(num_image,blanc,"r")
plt.subplot(122),plt.plot(num_image,noir,"g")


# ## Étape intermédiaire entre les étapes 2 et 3 : Segmentation par binarisation
# 
# Un autre point qui peut être utile lorsque le bruit de fond d’une image est trop important est de pouvoir segmenter l’image. C’est à dire pouvoir retirer l’objet de l’image et la mettre sur un fond blanc afin d’annuler toute source de bruit inutile sur l’image.
# 
# Une autre segmentation intéressante est celle par binarisation. Les étapes de cette segmentation sont :
# 1. Ouvrir l’image initial avec Image.open(« nom ») 
# 2. Création d’une image vide avec Image.new (‘RBV’, (dimx,dimy), (255,255,255)
# 3. Parcours de l’image initiale et test de chaque pixel pour savoir si la norme des 8 voisins du pixel est supérieure à une valeur seuil choisie. Si tel est le cas alors le pixel est reformé sur l’image vide.
# 

# In[ ]:


# Importation des librairies 
from PIL import Image
from math import *

#Ouverture de l'image en noir et blanc initiale
image1 = Image.open("nom de l'image.tiff") 

#Affiche l'image d'origine
plt.imshow(image1)
plt.show()

# Récupération des dimensions de l'image
dimx=image1.size[0] 
dimy=image1.size[1]

# Création d'une image vide.
image2 = Image.new ('RGB' , (dimx,dimy),(255,255,255)) 

#Binarisation
for  y in range(1,dimy-1) :
    for x in range ( 1,dimx-2):
        rvbCentre = image1.getpixel((x,y)) # le pixel central 
        rvbVoisin1= image1.getpixel((x+1,y-1)) # Les 8 vois
        rvbVoisin2= image1.getpixel((x-1,y+1))
        rvbVoisin3= image1.getpixel((x-1,y-1))
        rvbVoisin4= image1.getpixel((x+1,y+1))
        rvbVoisin5= image1.getpixel((x,y-1))
        rvbVoisin6= image1.getpixel((x,y+1))
        rvbVoisin7= image1.getpixel((x-1,y))
        rvbVoisin8= image1.getpixel((x+1,y))
        norme=sqrt((rvbVoisin1[1]-rvbVoisin2[2])**2+(rvbVoisin3[1]-rvbVoisin4[1])**2+(rvbVoisin5[1]-rvbVoisin6[1])**2+(rvbVoisin7[1]-rvbVoisin8[1])**2)
        if norme > 10 :
            image2.putpixel((x,y),(0,0,0))

#On sauvegarde la nouvelle image
image2.save("contour.jpg") 
plt.imshow(image2)
plt.show()


# ## Conclusion
# 
# Plusieurs paramètres sont à prendre en compte si vous souhaitez une reconstruction adéquat. De plus, vous remarquerez, que les différents algorithmes ne sont pas tous adaptés pour certains types d'objets. C'est donc à vous de choisir l'algorithme qui permettra d'obtenir la reconstruction que vous souhaitez.
