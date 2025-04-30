import requests
from dataclasses import dataclass

pokeapi = "https://pokeapi.co/api/v2/pokemon/"
typefects = "https://pokeapi.co/api/v2/type/"
translateApi = "https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl=es&dt=t&q="

@dataclass
class Pokemon:
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
		return self.weight/10

	def effects(self, url):
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
		self.effects(self.typeurl)

def translate(text):
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
	return None

sandshrew = search_pokemon("sandshrew")

print(f"Nombre: {sandshrew.name}")
print(f"PokedexID: {sandshrew.pokedexId}")
print(f"Peso: {sandshrew.weight}")
print(f"Altura: {sandshrew.height}")
print(f"Tipo: {sandshrew.typpe}")
print(f"Vida base: {sandshrew.hp}")
print(f"Ataque base: {sandshrew.attack}")
print(f"Defensa base: {sandshrew.defense}")
print(f"Ataque especial base: {sandshrew.sp_attack}")
print(f"Defensa especial base: {sandshrew.sp_defense}")
print(f"Velocidad: {sandshrew.speed}")
print(f"Efectivo contra: {sandshrew.damage_effective}")
print(f"No efectivo contra: {sandshrew.damage_not_efective}")
print(f"Normal contra: {sandshrew.damage_normal}")