import sys, os

def run_training():
    import sys, os
    try:
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
        from ml_logistical_regression.train_model import train_model
        train_model()
    except Exception as e:
        raise RuntimeError(f"Erreur dans l'entraînement du modèle : {e}")


def fail_task():
    raise ValueError("Échec d'alerte email")