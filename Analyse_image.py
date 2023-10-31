
from keras.preprocessing import image
import numpy as np
import cv2
import os
from keras.models import load_model
from flask import session

# Importez le modèle ici
modele = load_model('modele_cancer_des_yeux.h5')

def traiter_image(filename):
    if filename.endswith('.png'):
        try:
            img = image.load_img(filename, target_size=(224, 224))
            img_array = image.img_to_array(img)
            img_array = img_array / 255.0
            img_array = np.expand_dims(img_array, axis=0)
            predictions = modele.predict(img_array)
            img_cv2 = cv2.imread(filename)
            # Create a copy of the image
            image_copie = img_cv2.copy()
            # Renommez la copie avec "_copie" ajouté au nom du fichier
            rep, nom_fichier = os.path.split(filename)
            nom_fichier_copie = os.path.splitext(nom_fichier)[0] + "_copie" + os.path.splitext(nom_fichier)[1]
            chemin_image_copie = os.path.join(rep, nom_fichier_copie)
            # Enregistrez l'image copie sous le nouveau nom de fichier
            cv2.imwrite(chemin_image_copie, image_copie)
            probability_cancer_detected = predictions[0][0]
            seuil = 0.5
            if probability_cancer_detected > seuil:
                cv2.putText(img_cv2, "Cancer detecte", (10, 75), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 255), 3)
                cv2.imwrite(filename, img_cv2)
                return "Cancer detecté"
            else:
                cv2.putText(img_cv2, "Pas de cancer detecte", (10, 75), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 0), 3)
                cv2.imwrite(filename, img_cv2)
                return "Pas de cancer detecté"
    
            
        except Exception as e:
            return f'Erreur lors du traitement de l\'image : {str(e)}'
    else:
        return 'Seules les images PNG sont autorisées.'
