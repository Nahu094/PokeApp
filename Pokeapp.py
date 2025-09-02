import requests
import sys
from dataclasses import dataclass

pokeapi = "https://pokeapi.co/api/v2/pokemon/"# Link a 
typefects = "https://pokeapi.co/api/v2/type/"
translateApi = "https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl=es&dt=t&q="

@dataclass
class Pokemon:
	'''
	La clase pokemon 
	'''
	name: str
	pokedexId: int
	weight: int
	height: int
	typpe: str
	typeurl:str
	hp: int
	attack: int
	defense: int
	sp_attack: int
	sp_defense: int
	speed: int
	damage_effective: list = None
	damage_not_efective: list = None
	damage_normal: list = None


	def to_kg(self):
		"""
		Convierte el peso dado por la api de hectogramo a kilogramo
		"""
		self.weight = round(self.weight/10)
		return True
	

	def effects(self, url):
		"""
		Traduce los efectos obtenidos de la api del ingles al español

		Args:
			Enlace (url): Enlace a la api para obtener los efectos.

		"""
		response = requests.get(url)
		if response.status_code == 200:
			data = response.json()
			self.damage_effective= [translate(effect['name']) for effect in data['damage_relations']['double_damage_to']]
			self.damage_not_efective= [translate(effect['name']) for effect in data['damage_relations']['no_damage_to']]
			self.damage_normal= [translate(effect['name']) for effect in data['damage_relations']['half_damage_to']]
			return False
        #
		self.damage_effective = None
		self.damage_not_efective = None
		self.damage_normal = None
		return True

	def __post_init__(self):
		'''
		Inicializa y regula los valores obtenidos por la API
		'''
		#if self.height < 100:
		#	self.to_meter()
		
		self.to_kg()
		self.effects(self.typeurl)

def translate(text):
	'''
	Traduce una frase

	Args:
		Texto (text): Texto a traducir
	'''
	query = {
		"q": text,
		"source": "es",
		"target": "en",
		"format": "text",
		"alternatives": 1,
		"api_key": ""
	}
	response = requests.get(translateApi+text)
	if response.status_code == 200:
		data = response.json()
		return data[0][0][0]


def search_pokemon(pokemon):
	'''
	Obtiene los datos de un Pokemon desde la API de PokeAPI.co

	Args:
		Pokemon (pokemon): Pokemon a encontrar
	'''
	response = requests.get(pokeapi+pokemon)
	if response.status_code == 200:
		data = response.json()
		return Pokemon(
			data['name'],
			data['id'],
			data['weight'],
			data['height'],
			data['types'][0]['type']['name'],
			data['types'][0]['type']['url'],
			data['stats'][0]['base_stat'],
			data['stats'][1]['base_stat'],
			data['stats'][2]['base_stat'],
			data['stats'][3]['base_stat'],
			data['stats'][4]['base_stat'],
			data['stats'][5]['base_stat']
			)
	return response

if __name__ == "__main__":
	# Si no hay argumentos muestra el uso correcto del programa
	if len(sys.argv) > 1 and len(sys.argv) < 3:
		arg = sys.argv[1]
		poke = search_pokemon(arg)
		# Si el resultado no es de tipo Pokemon hubo un fallo al buscar
		if not isinstance(poke, Pokemon):
			if poke.status_code == 404:
				print("Pokemon no encontrado")
		# Muestra el resultado por pantalla
		else:
			print(f"Nombre: {poke.name}")
			print(f"PokedexID: {poke.pokedexId}")
			print(f"Peso: {poke.weight} kg")
			print(f"Altura: {poke.height} cm")
			print(f"Tipo: {poke.typpe}")
			print(f"Vida base: {poke.hp} hp")
			print(f"Ataque base: {poke.attack}")
			print(f"Defensa base: {poke.defense}")
			print(f"Ataque especial base: {poke.sp_attack}")
			print(f"Defensa especial base: {poke.sp_defense}")
			print(f"Velocidad: {poke.speed}")
			print(f"Efectivo contra: {poke.damage_effective}")
			print(f"No efectivo contra: {poke.damage_not_efective}")
			print(f"Normal contra: {poke.damage_normal}")
    
	else:
		print("Uso: Pokeapp nombre_pokemon")