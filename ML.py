from PIL import Image
import os
import pandas as pd
import cv2
import tensorflow as tf
from imblearn.over_sampling import RandomOverSampler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten, Conv2D, MaxPooling2D
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.metrics import ConfusionMatrixDisplay
import matplotlib.pyplot as plt
import numpy as np
from imblearn.over_sampling import SMOTE

# Fonction pour charger les images
def charger_images(chemin_dossier_images, liste_ids):
    images = []
    for img_id in liste_ids:
        img_path = os.path.join(chemin_dossier_images, str(img_id) + '.png')
        img = Image.open(img_path)
        img = img.resize((224, 224))
        img_array = np.array(img) / 255.0
        images.append(img_array)
    return np.array(images)

# Fonction pour l'entraînement du modèle
def entrainement_modele(chemin_train_excel, chemin_eval_excel, chemin_test_excel,
                        chemin_images_train, chemin_images_eval, chemin_images_test):
    labels_train = pd.read_csv(chemin_train_excel)
    labels_eval = pd.read_csv(chemin_eval_excel)
    labels_test = pd.read_csv(chemin_test_excel)
    print(1)
    images_train = charger_images(chemin_images_train, labels_train['ID'])
    images_eval = charger_images(chemin_images_eval, labels_eval['ID'])
    images_test = charger_images(chemin_images_test, labels_test['ID'])
    print(2)
    X_train = images_train
    X_eval = images_eval
    X_test = images_test
    print(3)
    y_train = labels_train['Disease_Risk']
    y_eval = labels_eval['Disease_Risk']
    y_test = labels_test['Disease_Risk']


    # Oversampling pour équilibrer les classes avec SMOTE
    # Oversampling pour équilibrer les classes
    oversampler = SMOTE(sampling_strategy='minority', random_state=42)
    X_train_resampled, y_train_resampled = oversampler.fit_resample(X_train.reshape(X_train.shape[0], -1), y_train)
    print(4)
    X_train_resampled = X_train_resampled.reshape(X_train_resampled.shape[0], 224, 224, 3)
    print(5)
    
    print(4)
    print(5)
    model = Sequential([
        Conv2D(64, (3, 3), activation='relu', input_shape=(224, 224, 3)),
        MaxPooling2D((2, 2)),
        Conv2D(128, (3, 3), activation='relu'),
        MaxPooling2D((2, 2)),
        Conv2D(256, (3, 3), activation='relu'),  # Ajout d'une autre couche Conv2D
        MaxPooling2D((2, 2)),
        Conv2D(128, (3, 3), activation='relu'),
        MaxPooling2D((2, 2)),
        Flatten(),
        Dense(128, activation='relu'),
        Dense(1, activation='sigmoid')
    ])
    optimizer = tf.keras.optimizers.Adam(learning_rate=0.0001)  # Réduction du taux d'apprentissage
    model.compile(optimizer=optimizer, loss='binary_crossentropy', metrics=['accuracy'])

    model.fit(X_train_resampled, y_train_resampled, validation_data=(X_eval, y_eval), epochs=7, batch_size=64)

    test_loss, test_acc = model.evaluate(X_test, y_test)
    print("Précision sur l'ensemble de test :", test_acc)

    # Matrice de confusion
    y_pred = model.predict(X_test)
    y_pred_classes = (y_pred > 0.5).astype(int)
    cm = confusion_matrix(y_test, y_pred_classes)
    labels = ["Pas de cancer", "Cancer détecté"]
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=labels)
    disp.plot(cmap='Blues')
    plt.show()

    # Sauvegarder le modèle pour une utilisation future
    model.save('modele_cancer_des_yeux.h5')


chemin_vers_excel_train = 'eyes-dataset/Training_Set/Training_Set/RFMiD_Training_Labels.csv'
chemin_vers_excel_evaluation = 'eyes-dataset/Evaluation_Set/Evaluation_Set/RFMiD_Validation_Labels.csv'
chemin_vers_excel_test = 'eyes-dataset/Test_Set/Test_Set/RFMiD_Testing_Labels.csv'
chemin_vers_dossier_images_train = 'eyes-dataset/Training_Set/Training_Set/Training/'
chemin_vers_dossier_images_evaluation = 'eyes-dataset/Evaluation_Set/Evaluation_Set/Validation/'
chemin_vers_dossier_images_test = 'eyes-dataset/Test_Set/Test_Set/Test/'

# Exemple d'utilisation 
entrainement_modele(chemin_vers_excel_train, chemin_vers_excel_evaluation, chemin_vers_excel_test,
                    chemin_vers_dossier_images_train, chemin_vers_dossier_images_evaluation, chemin_vers_dossier_images_test)