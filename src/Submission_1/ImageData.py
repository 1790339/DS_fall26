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
import cfg

class ImageData:
    def __init__(self):
        # Diccionari principal per emmagatzemar totes les dades.
        # Format: { 'uuid': {'file': 'path', 'prompt': '...', 'model': '...'} }
        # Això garanteix accessos i modificacions en temps O(1).
        self.db = {}

    def add_image(self, uuid: str, file: str):
        # Creem l'entrada amb tots els camps per defecte a "None"
        # Com que no llegim el disc encara, aquesta funció s'executa a l'instant
        self.db[uuid] = {
            'file': file,
            'prompt': 'None',
            'seed': 'None',
            'cfg_scale': 'None',
            'steps': 'None',
            'sampler': 'None',
            'model': 'None',
            'generated': 'None',
            'created_date': 'None'
        }

    def remove_image(self, uuid: str):
        # Esborrem l'entrada del diccionari.
        # Fem servir pop amb un segon argument (None) perquè no doni error si l'UUID no existeix.
        self.db.pop(uuid, None)

    def load_metadata(self, uuid: str):
        # Si la imatge no està registrada, no fem res
        if uuid not in self.db:
            return

        rel_file = self.db[uuid]['file']
        
        # Per llegir l'arxiu físicament necessitem la ruta absoluta del disc,
        # ja que internament només guardem la relativa.
        abs_file = os.path.join(cfg.get_root(), rel_file)

        if not os.path.isfile(abs_file):
            print(f"AVÍS: L'arxiu {abs_file} no existeix al disc.")
            return

        try:
            # Utilitzem la funció proporcionada per l'assignatura per llegir els chunks del PNG
            metadata = cfg.read_png_metadata(abs_file)
            
            if metadata:
                # Actualitzem el diccionari intern. 
                # Fem servir .get() per mantenir "None" si la imatge no té algun camp
                self.db[uuid]['prompt'] = metadata.get('Prompt', 'None')
                self.db[uuid]['seed'] = metadata.get('Seed', 'None')
                self.db[uuid]['cfg_scale'] = metadata.get('CFG_Scale', 'None')
                self.db[uuid]['steps'] = metadata.get('Steps', 'None')
                self.db[uuid]['sampler'] = metadata.get('Sampler', 'None')
                self.db[uuid]['model'] = metadata.get('Model', 'None')
                self.db[uuid]['generated'] = metadata.get('Generated', 'None')
                self.db[uuid]['created_date'] = metadata.get('Created_Date', 'None')
                
        except Exception as e:
            # Si una imatge està corrupta, capturem l'error per evitar que el programa sencer peti
            print(f"Error llegint metadades de {rel_file}: {e}")

    # --- Getters amb temps de resposta O(1) ---
    # Fem servir un encadenament de .get() per evitar excepcions KeyError
    # si per algun motiu l'UUID no existís al diccionari.

    def get_prompt(self, uuid: str) -> str:
        return self.db.get(uuid, {}).get('prompt', 'None')

    def get_model(self, uuid: str) -> str:
        return self.db.get(uuid, {}).get('model', 'None')

    def get_seed(self, uuid: str) -> str:
        return self.db.get(uuid, {}).get('seed', 'None')

    def get_cfg_scale(self, uuid: str) -> str:
        return self.db.get(uuid, {}).get('cfg_scale', 'None')

    def get_steps(self, uuid: str) -> str:
        return self.db.get(uuid, {}).get('steps', 'None')

    def get_sampler(self, uuid: str) -> str:
        return self.db.get(uuid, {}).get('sampler', 'None')

    def get_generated(self, uuid: str) -> str:
        return self.db.get(uuid, {}).get('generated', 'None')

    def get_created_date(self, uuid: str) -> str:
        return self.db.get(uuid, {}).get('created_date', 'None')