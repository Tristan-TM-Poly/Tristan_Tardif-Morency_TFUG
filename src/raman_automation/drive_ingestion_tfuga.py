import os
import io
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
# Importation de ton moteur Raman existant
from spectrometre_tfuga import SpectrometreAllInOne

# --- GOLIATH : CONFIGURATION DES CLÉS INTERDIMENSIONNELLES ---
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
SERVICE_ACCOUNT_FILE = 'credentials.json' # La clé secrète injectée par GitHub Secrets

def initialiser_pont_mycelien():
    """Établit la connexion Zéro-Touch avec l'écosystème Google."""
    print("[AI-7] Authentification HGFM auprès de Google Drive...")
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    return build('drive', 'v3', credentials=creds)

def extraire_donnees_drive(service, folder_id, telechargement_path="data/"):
    """Moissonne les spectres Raman depuis le dossier TTM-TFUGA-AI7-TRISTAN2."""
    print(f"[TRISTAN2] Scan du répertoire ID : {folder_id}")
    
    # Recherche spécifique de fichiers CSV/TXT dans le dossier cible
    query = f"'{folder_id}' in parents and (mimeType='text/csv' or mimeType='text/plain')"
    results = service.files().list(q=query, fields="files(id, name)").execute()
    items = results.get('files', [])

    if not items:
        print("[AXIOME] Le vide quantique est stable. Aucun nouveau fichier.")
        return []

    fichiers_locaux = []
    if not os.path.exists(telechargement_path):
        os.makedirs(telechargement_path)

    for item in items:
        print(f"[AI-7] Ingestion de la matière : {item['name']}")
        request = service.files().get_media(fileId=item['id'])
        fh = io.FileIO(os.path.join(telechargement_path, item['name']), 'wb')
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
        fichiers_locaux.append(os.path.join(telechargement_path, item['name']))
    
    return fichiers_locaux

if __name__ == '__main__':
    # ID du dossier Raman dans ton Drive (à extraire depuis l'URL de ton dossier Drive)
    DOSSIER_RAMAN_ID = 'INSERER_L_ID_DU_DOSSIER_ICI' 
    
    # 1. Connexion au Drive
    drive_service = initialiser_pont_mycelien()
    
    # 2. Téléchargement des CSV bruts (Acétaminophène, Urée, etc.)
    fichiers = extraire_donnees_drive(drive_service, DOSSIER_RAMAN_ID)
    
    # 3. Traitement TFUGA en chaîne
    for fichier in fichiers:
        nom_echantillon = os.path.basename(fichier).split('.')[0]
        spectre = SpectrometreAllInOne(nom_echantillon)
        spectre.ingest_reality(fichier)
        
        # Le calcul de l'aire sous la courbe est garanti absolu
        spectre.extract_absolute_truth()
        spectre.forge_goliath_latex(f"rapport_{nom_echantillon}.tex")
        
    print("\n[AXIOME] Transfert et analyse terminés. La vérité est scellée.")
