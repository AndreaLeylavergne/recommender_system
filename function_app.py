import azure.functions as func
import logging
import pandas as pd
import json
from azure.storage.blob import BlobServiceClient
import requests

# Charger les recommandations depuis le fichier CSV
RECOMMENDATIONS_DF = pd.read_csv("https://functiondef2.blob.core.windows.net/stockblobrecommender/user_recommendations_last.csv?sv=2022-11-02&ss=b&srt=co&se=2024-09-21T09%3A51%3A26Z&sp=rwl&sig=HsaeDs7oLsVBt80DUNodtdcgOZ9U%2BVhgYrRUBdlBmL8%3D")

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="get_recommendations")
def get_recommendations(req: func.HttpRequest) -> func.HttpResponse:
    logging.info(f"Colonnes disponibles : {RECOMMENDATIONS_DF.columns.tolist()}")
    logging.info('Processing recommendation request.')

    # Récupérer l'user_id depuis les paramètres de la requête
    user_id = req.params.get('user_id')
    
    if not user_id:
        return func.HttpResponse(
            "Veuillez fournir un user_id dans la requête.",
            status_code=400
        )
    
    # Convertir user_id en int pour correspondre au type dans le CSV
    user_id = int(user_id)
    
    # Filtrer les recommandations pour l'utilisateur
    user_recommendations_last = RECOMMENDATIONS_DF[RECOMMENDATIONS_DF['user_id'] == user_id]
    
    if user_recommendations_last.empty:
        return func.HttpResponse(
            f"Aucune recommandation trouvée pour l'utilisateur {user_id}.",
            status_code=404
        )
    
    # Récupérer les recommandations sous forme de liste
    recommendations = user_recommendations_last['recommended_articles'].tolist()
    
    # Retourner les recommandations sous forme de JSON
    return func.HttpResponse(
        json.dumps(recommendations),
        mimetype="application/json",
        status_code=200
    )
