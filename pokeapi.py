import json
import requests

def get_pokemon_data(pokemon_name: str):
    """
    Get the data of the provided pokemon.

    Will return a large JSON dictionary of specific details
    about the pokemon such as:
      - base experience
      - abiliites
      - moves
      - sprites (back and front images)
      - stats
      - and more...

    If curious, see https://pokeapi.co/docs/v2#pokemon
    """
    url = f"http://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}/"
    response = requests.get(url)

    # If the request to the pokemon data is successful (HTTP code 200),
    # then we can use the response.
    #
    # See https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/200
    # for information about the different HTTP codes.
    if response.status_code == 200:
        data = json.loads(response.text)
        # see sample_get_pokemon_data_response.json for the response
        return data
    else:
        print("An error occurred querying the API")
        return {}
