# -*- coding: utf-8 -*-
"""
Gallery.py : ** REQUIRED ** El vostre codi de la classe Gallery.

Aquesta classe s'encarrega de gestionar galeries d'imatges en format JSON.

Funcionalitat:
    - Llegir galeries des d'arxius JSON
    - Visualitzar totes les imatges d'una galeria
    - Afegir i eliminar imatges de la galeria

Format JSON d'una galeria:
{
  "gallery_name": "Cyberpunk Cities",
  "description": "Collection of futuristic urban landscapes",
  "created_date": "2025-09-30",
  "images": [
    "generated_images/city_001.png",
    "generated_images/city_neon_12.png",
    "generated_images/urban_street_45.png"
  ]
}

Mètodes a implementar:
    - load_file(file: str) -> None
        Llegeix un arxiu JSON amb la definició de la galeria.
        Ha de validar que cada imatge referenciada existeix a la col·lecció.
        Si una imatge no existeix, l'ignora i continua processant.
        Emmagatzema internament els UUID de les imatges vàlides.

    - show() -> None
        Visualitza totes les imatges de la galeria en ordre utilitzant
        ImageViewer.show_image().

    - add_image_at_end(uuid: str) -> None
        Afegeix una imatge al final de la galeria.

    - remove_first_image() -> None
        Elimina la primera imatge de la galeria.

    - remove_last_image() -> None
        Elimina l'última imatge de la galeria.

Notes:
    - Utilitzeu la llibreria json per llegir els arxius
    - Els paths dins el JSON són relatius a ROOT_DIR
    - Cada galeria és un objecte independent (instància de Gallery)
    - Podeu tenir múltiples galeries actives simultàniament
    - Les operacions d'afegir/eliminar són ràpides (no busquen a la llista)
"""

import json
import os
import cfg as cfg
from collections import deque

class Gallery:
    def __init__(self, gestor_ids, visualitzador):
        self.gestor_ids = gestor_ids
        self.visualitzador = visualitzador
        
        self.gallery_name = ""
        self.description = ""
        self.created_date = ""
        
        # Substituïm la llista estàndard per una cua de doble final (Doubly Linked List)
        self.image_uuids = deque()

    
def load_file(self, file: str):
    if not os.path.isfile(file):
        print(f"Error: No s'ha trobat l'arxiu '{file}'.")
        return

    try:
        with open(file, "r", encoding="utf-8") as f:
            dades = json.load(f)

        self.gallery_name = dades.get("gallery_name", "Desconeguda")
        self.description = dades.get("description", "Sense descripció")
        self.created_date = dades.get("created_date", "Desconeguda")

        self.image_uuids.clear()

        for path_imatge in dades.get("images", []):
            path_imatge = os.path.normpath(path_imatge)
            path_imatge = path_imatge.replace(os.sep, "/")

            uuid = self.gestor_ids.get_uuid(path_imatge)

            if uuid is not None:
                self.image_uuids.append(uuid)
            else:
                print(
                    f"AVÍS: La imatge '{path_imatge}' "
                    "no existeix a la col·lecció."
                )

    except (json.JSONDecodeError, OSError) as e:
        print(f"Error llegint el fitxer JSON: {e}")


    def show(self):
        if not self.image_uuids:
            print("La galeria està buida o no s'ha carregat correctament.")
            return

        print(f"\n{'=' * 50}")
        print(f" GALERIA: {self.gallery_name}")
        print(f" Total imatges: {len(self.image_uuids)}")
        print(f"{'=' * 50}")
        
        mode_actual = cfg.DISPLAY_MODE
        
        # Iterar seqüencialment per un deque continua sent eficient
        for index, uuid in enumerate(self.image_uuids):
            print(f"\n---> [Diapositiva {index + 1} de {len(self.image_uuids)}] <---")
            self.visualitzador.show_image(uuid, mode_actual)

    # --- FUNC 7: Modificació dinàmica optimitzada amb O(1) absolut ---

    def add_image_at_end(self, uuid: str):
        if uuid:
            self.image_uuids.append(uuid) # Inserció per la cua: O(1)

    def remove_first_image(self):
        if len(self.image_uuids) > 0:
            # popleft() extreu pel cap destruint l'enllaç sense moure memòria: O(1)
            return self.image_uuids.popleft()
        else:
            print("AVÍS: La galeria ja està buida.")
            return None

    def remove_last_image(self):
        if len(self.image_uuids) > 0:
            # pop() extreu per la cua: O(1)
            return self.image_uuids.pop()
        else:
            print("AVÍS: La galeria ja està buida.")
            return None