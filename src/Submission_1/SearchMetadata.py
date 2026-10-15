# -*- coding: utf-8 -*-
"""
SearchMetadata.py : ** REQUIRED ** El vostre codi de la classe SearchMetadata.

Aquesta classe s'encarrega de cercar imatges segons criteris basats en metadades.

Funcionalitat:
    - Cercar imatges que continguin una subcadena en les seves metadades
    - Combinar resultats de cerques amb operadors lògics (AND, OR)

Mètodes a implementar:
    - prompt(sub: str) -> list
        Retorna una llista d'UUID de les imatges que contenen 'sub'
        en el camp Prompt.

    - model(sub: str) -> list
        Retorna una llista d'UUID de les imatges que contenen 'sub'
        en el camp Model.

    - seed(sub: str) -> list
        Retorna una llista d'UUID de les imatges que contenen 'sub'
        en el camp Seed.

    - cfg_scale(sub: str) -> list
        Retorna una llista d'UUID de les imatges que contenen 'sub'
        en el camp CFG_Scale.

    - steps(sub: str) -> list
        Retorna una llista d'UUID de les imatges que contenen 'sub'
        en el camp Steps.

    - sampler(sub: str) -> list
        Retorna una llista d'UUID de les imatges que contenen 'sub'
        en el camp Sampler.

    - date(sub: str) -> list
        Retorna una llista d'UUID de les imatges que contenen 'sub'
        en el camp Created_Date.

    - and_operator(list1: list, list2: list) -> list
        Retorna una llista amb els UUID que apareixen en AMBDUES llistes.
        (Intersecció de conjunts)

    - or_operator(list1: list, list2: list) -> list
        Retorna una llista amb els UUID que apareixen en QUALSEVOL de
        les dues llistes, sense duplicats.
        (Unió de conjunts)

Notes:
    - Les cerques són case-sensitive (distingeixen majúscules/minúscules)
    - Utilitzeu str.find() per cercar subcadenes
    - Les llistes retornades poden estar buides
    - Els operadors lògics NO modifiquen les llistes originals
    - Aquests mètodes NO retornen objectes Gallery, sinó llistes simples
"""

class SearchMetadata:
    def __init__(self, gestor_dades):
        # Necessitem accés a la base de dades per consultar els valors
        self.gestor_dades = gestor_dades

    def _cerca_generica(self, getter_func, sub: str) -> list:
        # Mètode privat que encapsula la lògica de cerca per no repetir codi.
        # getter_func és la funció que extreu la dada (ex: get_prompt)
        resultats = []
        sub_net = sub.lower() # Passem a minúscules per fer la cerca insensible a majúscules
        
        # Iterem sobre tots els UUIDs registrats a la memòria O(N)
        for uuid in self.gestor_dades.db.keys():
            # Forcem la càrrega de metadades des del disc si encara no s'ha fet
            if self.gestor_dades.get_prompt(uuid) == 'None':
                self.gestor_dades.load_metadata(uuid)
                
            valor = getter_func(uuid)
            
            # Comprovem si la subcadena existeix dins del valor
            if valor != 'None' and sub_net in str(valor).lower():
                resultats.append(uuid)
                
        return resultats

    def prompt(self, sub: str) -> list:
        return self._cerca_generica(self.gestor_dades.get_prompt, sub)

    def model(self, sub: str) -> list:
        return self._cerca_generica(self.gestor_dades.get_model, sub)

    def seed(self, sub: str) -> list:
        return self._cerca_generica(self.gestor_dades.get_seed, sub)

    def cfg_scale(self, sub: str) -> list:
        return self._cerca_generica(self.gestor_dades.get_cfg_scale, sub)

    def steps(self, sub: str) -> list:
        return self._cerca_generica(self.gestor_dades.get_steps, sub)

    def sampler(self, sub: str) -> list:
        return self._cerca_generica(self.gestor_dades.get_sampler, sub)

    def date(self, sub: str) -> list:
        return self._cerca_generica(self.gestor_dades.get_created_date, sub)

    # --- Operadors Lògics O(N) utilitzant Taules Hash ---

    def and_operator(self, list1: list, list2: list) -> list:
        # Intersecció: retorna només els UUIDs que estan a les dues llistes
        return list(set(list1) & set(list2))

    def or_operator(self, list1: list, list2: list) -> list:
        # Unió: retorna els UUIDs que estan en almenys una de les llistes, eliminant duplicats
        return list(set(list1) | set(list2))