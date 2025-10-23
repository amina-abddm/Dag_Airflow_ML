# Pour entraîner un modèle de régression logistique sur un jeu de données publicitaire
# Pour exécuter ce script, assurez-vous d'avoir installé les bibliothèques nécessaires puis dans votre terminal, exécutez :
# python train_model.py

import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import pickle
import os

def train_model():
    # Charger les données
    df = pd.read_csv("data/advertising.csv")

    # Afficher les colonnes et un aperçu
    print("\n📊 Colonnes du fichier :")
    print(df.columns.tolist())
    print("\n🔍 Aperçu des données :")
    print(df.head())

    # Définir les features et la target
    features = ['Daily Time Spent on Site', 'Age', 'Area Income', 'Daily Internet Usage', 'Male']
    target = 'Clicked on Ad'

    X = df[features]
    y = df[target]

    # Séparer en train/test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Entraîner le modèle
    model = LogisticRegression()
    model.fit(X_train, y_train)

    # Évaluer le modèle
    y_pred = model.predict(X_test)
    print("\n📈 Rapport de classification :")
    print(classification_report(y_test, y_pred))

    # Sauvegarder le modèle
    os.makedirs("output", exist_ok=True)
    with open("output/model.pkl", "wb") as f:
        pickle.dump(model, f)

    print("\n✅ Modèle entraîné et sauvegardé dans output/model.pkl")

#if __name__ == "__main__":
#   train_model()
