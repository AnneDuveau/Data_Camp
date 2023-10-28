from flask import Flask, render_template, request, jsonify, redirect, url_for,  flash
from flask_sqlalchemy import SQLAlchemy
import os
from werkzeug.utils import secure_filename
from Analyse_image import traiter_image
import shutil



app = Flask(__name__)



# Define the path where you want to save the downloaded images
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Créez le répertoire si nécessaire
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


# Home Page
@app.route('/')
def index():
    return render_template('page.html')


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

                    # Calling up the image processing function
                    resultat_treatment=traiter_image(filename)

                    return render_template('Resultats.html', uploaded_image=uploaded_image.filename, resultat_treatment=resultat_treatment)
                    
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

                    