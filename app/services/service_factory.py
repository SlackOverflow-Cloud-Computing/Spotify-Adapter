from framework.services.service_factory import BaseServiceFactory
from app.services.spotify_api import SpotifyAPIService
import dotenv, os

dotenv.load_dotenv()
client_id = os.getenv('SPOTIFY_CLIENT_ID') 
client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')


class ServiceFactory(BaseServiceFactory):

    def __init__(self):
        super().__init__()

    @classmethod
    def get_service(cls, service_name):

        # match service_name:
        #     case "SpotifyAPIService":
        #         result = SpotifyAPIService(client_id, client_secret)
        #
        #     case _:
        #         result = None

        if service_name == "SpotifyAPIService":
            result = SpotifyAPIService(client_id, client_secret)

        else:
            result = None

        return result
