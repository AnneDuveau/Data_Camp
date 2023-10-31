from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
import os
from werkzeug.utils import secure_filename
from Analyse_image import traiter_image
import shutil
import cv2
import psutil



app = Flask(__name__)

# Define the path where you want to save the downloaded images
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Créez le répertoire si nécessaire
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Carbon footprint function (adapt as needed)
def calculate_carbon_footprint(time_execution):
    consommation_energy = estimate_consommation_energy(time_execution)
    carbon_footprint = estimate_carbon_footprint(consommation_energy)

    return carbon_footprint

# Function for estimate energy consommation 
def estimate_consommation_energy(time_execution):
    puissance = 15  # In watts
    consommation_energy = puissance * time_execution
    print(f"Estimation of consommation energy: {consommation_energy} Wh")
    return consommation_energy


# Fonction to estimate carbon foot print 
def estimate_carbon_footprint(consommation_energy):
    carbon_footprint_per_wh = 0.074  # In CO2 per Wh
    carbon_footprint = carbon_footprint_per_wh * (consommation_energy / 3600)  
    return carbon_footprint


# Home Page
@app.route('/')
def index():
    return render_template('page.html')

@app.route('/about')
def about():
    return render_template('About.html')

@app.route('/FirstReport')
def FirstReport():
    return render_template('FirstReport.html')

@app.route('/SecondReport')
def SecondReport():
    return render_template('SecondReport.html')

# Image download management
@app.route('/uploads', methods=['POST'])
def upload():
    if 'image' in request.files:
        uploaded_image = request.files['image']
        if uploaded_image.filename != '':
            # Assurez-vous que l'extension est .png
            if uploaded_image.filename.endswith('.png'):
                try:
                    if not os.path.exists(app.config['UPLOAD_FOLDER']):
                        os.makedirs(app.config['UPLOAD_FOLDER'])
                    # Rename the file
                    filename = secure_filename(uploaded_image.filename) # Renommer le fichier en utilisant secure_filename
                    filename = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    uploaded_image.save(filename)
                    print(filename)

                    # Generate the copied filename
                    rep, nom_fichier = os.path.split(filename)
                    nom_fichier_copie = os.path.splitext(nom_fichier)[0] + "_copie" + os.path.splitext(nom_fichier)[1]
                    chemin_image_copie = os.path.join(app.config['UPLOAD_FOLDER'], nom_fichier_copie)
                    print("chemin_image_copie:" + chemin_image_copie)

                    # Affichez l'image téléchargée
                    # Construisez le chemin de l'image téléchargée
                    image_path = url_for('static', filename='uploads/' + uploaded_image.filename)
                    print(image_path)

                    # Record the start time of the execution
                    start_execution = psutil.cpu_times()


                    # Calling up the image processing function
                    resultat_treatment=traiter_image(filename)

                   # Record the end time of the execution
                    end_execution = psutil.cpu_times()

                    # Calculate the execution time in seconds
                    times_execution = (end_execution.user - start_execution.user) + (end_execution.system - start_execution.system)
                    print(f"Time execution: {times_execution} seconds")
                   
                   # Call the carbon footprint calculation function
                    empreinte_carbone = calculate_carbon_footprint(times_execution)
                    print(f"Estimation of the carbon foot print : {empreinte_carbone} kg of CO2")
                    # Récupérez le nom du fichier copié depuis la session
                    

                    return render_template('Resultats.html', uploaded_image=nom_fichier_copie, analyzed_image=uploaded_image.filename,   resultat_treatment=resultat_treatment)
                    
                except Exception as e:
                    return f'Erreur lors de l\'enregistrement de l\'image : {str(e)}'
            else:
                return 'Seules les images PNG sont autorisées.'
    return redirect(url_for('index'))

 
@app.route('/delete_uploads', methods=['POST'])
def delete_uploads():
    uploads_directory = 'static/uploads'

    # Supprime le dossier "uploads" et tout son contenu
    shutil.rmtree(uploads_directory)

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)

                    