import csv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

class SpotifyAPI:

    def __init__(self):
        self.client_id = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
        self.client_secret = "XXXXXXXXXXXXXXXXXXXXXXXXXXXX"
        self.auth_manager = SpotifyClientCredentials(client_id=self.client_id, client_secret=self.client_secret)
        self.sp = spotipy.Spotify(auth_manager=self.auth_manager)

    def get_playlist_tracks(self, playlist_id):
        tracks = []
        offset = 0
        limit = 100

        try:
            playlist_info = self.sp.playlist(playlist_id, fields='tracks(total)')
            total = playlist_info['tracks']['total']

            while offset < total:
                results = self.sp.playlist_items(playlist_id, offset=offset, limit=limit)

                for item in results['items']:
                    track = item['track']
                    artist_name = track['artists'][0]['name']
                    track_name = track['name']
                    tracks.append((artist_name, track_name))

                offset += limit

        except spotipy.SpotifyException as e:
            print("Erreur de l'API Spotify :", e)

        return tracks

    def export_playlist_to_csv(self, tracks, filename):
        if tracks:
            try:
                with open(filename, 'w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow(['Artiste', 'Titre'])

                    for artist_name, track_name in tracks:
                        writer.writerow([artist_name, track_name])

                print(f"La playlist a été exportée avec succès dans le fichier : {filename}")
            except IOError:
                print("Erreur lors de l'exportation de la playlist vers le fichier CSV.")
        else:
            print("La playlist est vide ou une erreur s'est produite.")


playlist_id = input("Entrez l'ID de la playlist Spotify : ")
csv_filename = input("Entrez le nom du fichier CSV de sortie : ")

spotify_api = SpotifyAPI()
playlist_tracks = spotify_api.get_playlist_tracks(playlist_id)

if playlist_id.isalnum():
    playlist_tracks = spotify_api.get_playlist_tracks(playlist_id)

    if playlist_tracks and csv_filename.isalnum():
        spotify_api.export_playlist_to_csv(playlist_tracks, csv_filename + ".csv")
    else:
        print("La playlist est vide ou une erreur s'est produite car le format du nom saisi est invalide.")
else:
    print("L'ID de la playlist doit être un nombre entier.")