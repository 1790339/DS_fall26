# -*- coding: utf-8 -*-
"""
ImageID.py : ** REQUIRED ** El vostre codi de la classe ImageID.

Aquesta classe s'encarrega de generar i gestionar identificadors únics (UUID)
per a cada imatge de la col·lecció.

Funcionalitat:
    - Generar un UUID únic a partir del path canònic d'un arxiu
    - Mantenir un registre dels UUID generats per evitar col·lisions
    - Permetre consultar i eliminar UUID

Mètodes a implementar:
    - generate_uuid(file: str) -> str
        Genera un UUID únic per a l'arxiu especificat.
        Ha de comprovar que el UUID no estigui ja en ús.
        Si hi ha col·lisió (cas extremadament improbable), retorna None i
        mostra un missatge d'error.

    - get_uuid(file: str) -> str
        Retorna el UUID associat a l'arxiu, si ja ha estat generat.
        Si no existeix, retorna None.

    - remove_uuid(uuid: str) -> None
        Elimina el UUID del registre d'identificadors actius.
        Després d'eliminar-lo, aquest UUID es podrà tornar a utilitzar.

Notes:
    - Els UUID han de seguir el format estàndard (128 bits)
    - Podeu utilitzar la funció cfg.get_uuid() com a base
    - Els UUID s'emmagatzemen com a strings
    - Un UUID només es pot generar una vegada (fins que s'elimini)
"""
import cfg as cfg

class ImageID:
    def __init__(self):
        # Dos diccionaris (taules hash) per garantir cerques O(1) en ambdues direccions.
        # file_to_uuid busca per path. uuid_to_file busca per UUID (claus i valors invertits).
        self.file_to_uuid = {}
        self.uuid_to_file = {}

    def generate_uuid(self, file: str) -> str:

        print("[DEBUG] generate_uuid recibe:", type(file), repr(file))
        file = str(file)
        try:
            new_uuid = str(cfg.get_uuid(str(file)))
        except Exception as e:
            print("[DEBUG] cfg.get_uuid falla:", type(e).__name__, e)
            raise
        
        # Comprovem col·lisions a l'instant gràcies a la taula hash de uuid_to_file
        if new_uuid in self.uuid_to_file:
            print(f"AVÍS: L'ID {new_uuid} del fitxer '{file}' ja existeix. S'ignora.")
            return None
            
        # Guardem la relació en els dos sentits per mantenir-ho sincronitzat
        self.file_to_uuid[file] = new_uuid
        self.uuid_to_file[new_uuid] = file
        
        return new_uuid

    def get_uuid(self, file: str) -> str:
        # Retorna el UUID si la clau (ruta) existeix, o un string buit si no la troba
        return self.file_to_uuid.get(str(file))

    def remove_uuid(self, uuid: str) -> None:
        uuid = str(uuid)                      # evita objectes no-hashables 
        file = self.uuid_to_file.pop(uuid, None)
        if file is not None:
            self.file_to_uuid.pop(file, None)