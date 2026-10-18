# -*- coding: utf-8 -*-
"""
ImageData.py : ** REQUIRED ** El vostre codi de la classe ImageData.

Aquesta classe s'encarrega d'emmagatzemar i gestionar les metadades de les
imatges generades per IA.

Funcionalitat:
    - Afegir i eliminar imatges de la col·lecció
    - Llegir les metadades embegudes dins els arxius PNG
    - Proporcionar accés a totes les metadades d'una imatge

Mètodes a implementar:
    - add_image(uuid: str, file: str) -> None
        Crea una entrada per a la imatge amb l'UUID i el path especificats.
        Inicialment les metadades estan buides (no llegides del disc).

    - remove_image(uuid: str) -> None
        Elimina la imatge i totes les seves metadades de la col·lecció.

    - load_metadata(uuid: str) -> None
        Llegeix les metadades embegudes en l'arxiu PNG i les emmagatzema.
        Aquest mètode es pot cridar múltiples vegades (p.ex. si l'arxiu canvia).

    - get_prompt(uuid: str) -> str
        Retorna el prompt utilitzat per generar la imatge.

    - get_model(uuid: str) -> str
        Retorna el model d'IA utilitzat (p.ex. "SD2", "DALL-E", "Midjourney").

    - get_seed(uuid: str) -> str
        Retorna la llavor aleatòria utilitzada en la generació.

    - get_cfg_scale(uuid: str) -> str
        Retorna el CFG Scale (guidance scale) utilitzat.

    - get_steps(uuid: str) -> str
        Retorna el nombre de passos d'iteració del model.

    - get_sampler(uuid: str) -> str
        Retorna l'algorisme de mostreig utilitzat.

    - get_generated(uuid: str) -> str
        Retorna "true" si la imatge està marcada com a generada.

    - get_created_date(uuid: str) -> str
        Retorna la data de creació en format YYYY-MM-DD.

    - get_dimensions(uuid: str) -> tuple
        Retorna una tupla (width, height) amb les dimensions de la imatge.

Notes:
    - Utilitzeu la llibreria PIL/Pillow per llegir metadades:
      img = Image.open(file)
      metadata = img.text
    - Si un camp no existeix, retorneu "None" (string)
    - Les dimensions es llegeixen amb img.width i img.height
    - Tots els camps de metadades es guarden com a strings
"""
import os
import cfg as cfg
from PIL import Image

class ImageData:
    def __init__(self):
        # Diccionari principal per emmagatzemar totes les dades.
        # Format: { 'uuid': {'file': 'path', 'prompt': '...', 'model': '...'} }
        # Això garanteix accessos i modificacions en temps O(1).
        self.db = {}

    def __len__(self) -> int:
        return len(self.db)

    def add_image(self, uuid: str, file: str):
        if not uuid or not file:
            return
        
        # Creem l'entrada amb tots els camps per defecte a "None"
        # Com que no llegim el disc encara, aquesta funció s'executa a l'instant
        self.db[uuid] = {
            'file': file,
            'prompt': None,
            'seed': None,
            'cfg_scale': None,
            'steps': None,
            'sampler': None,
            'model': None,
            'generated': None,
            'created_date': None,
            'dimensions': None
        }

    def remove_image(self, uuid: str):
        # Esborrem l'entrada del diccionari.
        # Fem servir pop amb un segon argument (None) perquè no doni error si l'UUID no existeix.
        self.db.pop(uuid, None)

    def load_metadata(self, uuid: str):
        if uuid not in self.db:
            return

        rel_file = self.db[uuid]['file']

        candidates = [rel_file, os.path.abspath(rel_file),]
        path = next((p for p in candidates if os.path.isfile(p)), None)

        if path is None: #Llançem un error si no existeix un path
            raise FileNotFoundError(f"AVÍS: L'arxiu {rel_file} no existeix al disc.") 

        try:
            with Image.open(path) as img:
                metadata = img.text
                print("[CLAUS]", dict(text))   # TEMPORAL: borrar al confirmar las claves
                self.db[uuid]['dimensions'] = (img.width, img.height)
                self.db[uuid]['prompt'] = metadata.get('prompt', 'None')
                self.db[uuid]['seed'] = metadata.get('seed', 'None')
                self.db[uuid]['cfg_scale'] = metadata.get('cfg_scale', 'None')
                self.db[uuid]['steps'] = metadata.get('steps', 'None')
                self.db[uuid]['sampler'] = metadata.get('sampler', 'None')
                self.db[uuid]['model'] = metadata.get('model', 'None')
                self.db[uuid]['generated'] = metadata.get('generated', 'None')
                self.db[uuid]['created_date'] = metadata.get('created_date', 'None')
        except OSError:
            raise
        except Exception as e:
            print(f"Error llegint metadades de {rel_file}: {e}")

    # Getters amb temps de resposta O(1) ja que, a partir d'una clau uuid, accedim als seus camps

    def _get(self, uuid, camp):
        entrada = self.db.get(uuid) #Busca l'entrada d'un uuid en el diccionari db
        if entrada == None:
            return None #Retorna None els atributs si l'uuid no existeix
        return entrada[camp] 

    def get_prompt(self, uuid: str) -> str: #Retorna camp prompt
        return self._get(uuid, 'prompt')

    def get_model(self, uuid: str) -> str: #Retorna camp model
        return self._get(uuid, 'model')

    def get_seed(self, uuid: str) -> str: #Retorna camp seed
        return self._get(uuid, 'seed')

    def get_cfg_scale(self, uuid: str) -> str: #Retorna camp cfg_scale
        return self._get(uuid, 'cfg_scale')

    def get_steps(self, uuid: str) -> str: #Retorna camp steps
        return self._get(uuid, 'steps')

    def get_sampler(self, uuid: str) -> str: #Retorna camp sampler
        return self._get(uuid, 'sampler')

    def get_generated(self, uuid: str) -> str: #Retorna camp generated
        return self._get(uuid, 'generated')

    def get_created_date(self, uuid: str) -> str: #Retorna camp created_date
        return self._get(uuid, 'created_date')

    def get_dimensions(self, uuid: str) -> tuple: #retorna dimensions
        return self._get(uuid, 'dimensions')

    def get_filename(self, uuid: str) -> str: #Retorna el nom 
        return self._get(uuid, 'file') 