# -*- coding: utf-8 -*-
"""
p1_main.py : ** OPTIONAL ** Si heu fet un main vostre, poseu aquí el codi.
                            Aquest arxiu no s'avalua automàticament.

Aquí podeu posar el vostre codi de proves per testejar les funcionalitats
implementades.

Exemples d'ús:
    - Carregar la col·lecció d'imatges
    - Generar UUID per a totes les imatges
    - Llegir metadades d'algunes imatges
    - Visualitzar imatges
    - Carregar i mostrar galeries
    - Fer cerques i crear galeries a partir dels resultats
"""
import cfg
import json
import os

from ImageFiles import ImageFiles
from ImageID import ImageID
from ImageData import ImageData
from ImageViewer import ImageViewer
from Gallery import Gallery
from SearchMetadata import SearchMetadata

if __name__ == "__main__":
    print("=" * 60)
    print("       INICI DE LES PROVES: FASES 1 A 6")
    print("=" * 60)

    # ---------------------------------------------------------
    # FASE 1: GESTIÓ DE FITXERS I CONJUNTS (ImageFiles)
    # ---------------------------------------------------------
    print("\n[--- FASE 1: LECTURA DE DISC I DETECCIO DE CANVIS ---]")
    gestor_fitxers = ImageFiles()
    ruta_base = cfg.get_root()
    
    print(f"Escanejant directori: {ruta_base}")
    gestor_fitxers.reload_fs(ruta_base)
    afegits = gestor_fitxers.files_added()
    print(f"Total fitxers inicials detectats: {len(afegits)}")
    
    # Comprovació de que els sets no detecten canvis si no es toca la carpeta
    gestor_fitxers.reload_fs(ruta_base)
    print("Recarrega sense modificacions:")
    print(f" -> Nous: {len(gestor_fitxers.files_added())}")
    print(f" -> Esborrats: {len(gestor_fitxers.files_removed())}")

    if not afegits:
        print("\nERROR: No s'han trobat imatges per continuar les proves.")
        exit()

    # ---------------------------------------------------------
    # FASE 2: GESTIÓ D'IDENTIFICADORS ÚNICS (ImageID)
    # FASE 3: EMMAGATZEMATGE I LAZY LOADING (ImageData)
    # ---------------------------------------------------------
    print("\n[--- FASES 2 I 3: GENERACIO D'UUIDs I REGISTRE EN MEMORIA ---]")
    gestor_ids = ImageID()
    gestor_dades = ImageData()
    
    uuids_registrats = 0
    for fitxer in afegits:
        nou_uuid = gestor_ids.generate_uuid(fitxer)
        if nou_uuid != "":
            # Fase 3: registre superficial O(1) amb valors per defecte "None"
            gestor_dades.add_image(nou_uuid, fitxer)
            uuids_registrats += 1
            
    print(f"UUIDs generats i entrades creades a ImageData: {uuids_registrats}")

    # Comprovació del funcionament del Lazy Loading amb la primera imatge
    exemple_fitxer = afegits[0]
    exemple_uuid = gestor_ids.get_uuid(exemple_fitxer)
    print(f"\nVerificacio de Lazy Loading per a: {exemple_fitxer}")
    print(f" -> UUID associat (O(1)): {exemple_uuid}")
    print(f" -> Prompt abans de carregar (ha de ser 'None'): {gestor_dades.get_prompt(exemple_uuid)}")
    
    # Forcem la càrrega manual de disc d'aquesta imatge concreta
    gestor_dades.load_metadata(exemple_uuid)
    print(f" -> Prompt despres de carregar: {gestor_dades.get_prompt(exemple_uuid)[:60]}...")

    # ---------------------------------------------------------
    # FASE 4: VISUALITZACIÓ D'IMATGES (ImageViewer)
    # ---------------------------------------------------------
    print("\n[--- FASE 4: VISUALITZACIO D'UNA IMATGE ---]")
    visualitzador = ImageViewer(gestor_ids, gestor_dades)
    mode_actual = cfg.DISPLAY_MODE
    print(f"Executant show_image() en mode {mode_actual}...")
    visualitzador.show_image(exemple_uuid, mode_actual)

    # ---------------------------------------------------------
    # FASE 5: GESTIÓ DE GALERIES JSON (Gallery)
    # ---------------------------------------------------------
    print("\n[--- FASE 5: CARREGA I VISUALITZACIO DE GALERIA ---]")
    galeria = Gallery(gestor_ids, visualitzador)
    
    # Generem un JSON temporal amb un maxim de 3 imatges reals per validar el funcionament
    num_mostres = min(3, len(afegits))
    fitxer_json_prova = "galeria_test_execucio.json"
    dades_galeria = {
        "gallery_name": "Galeria de Test Automatitzat",
        "description": "Validacio de la Fase 5 amb una llista ordenada d'imatges",
        "created_date": "2026-10-04",
        "images": afegits[:num_mostres]
    }
    
    with open(fitxer_json_prova, "w", encoding="utf-8") as f:
        json.dump(dades_galeria, f, indent=4)
        
    print(f"Arxiu JSON creat: '{fitxer_json_prova}' amb {num_mostres} imatges.")
    galeria.load_file(fitxer_json_prova)
    galeria.show()

    # ---------------------------------------------------------
    # FASE 6: CERCA I OPERADORS LÒGICS (SearchMetadata)
    # ---------------------------------------------------------
    print("\n[--- FASE 6: MOTOR DE CERCA I OPERACIONS DE CONJUNTS ---]")
    cercador = SearchMetadata(gestor_dades)
    
    # 1. Cerca per subcadena de text al prompt
    criteri_prompt = "a"
    res_prompt = cercador.prompt(criteri_prompt)
    print(f"1. Imatges amb '{criteri_prompt}' al prompt: {len(res_prompt)}")
    
    # 2. Cerca per model (utilitzem el model detectat de la primera imatge per garantir resultats)
    criteri_model = gestor_dades.get_model(exemple_uuid)
    res_model = cercador.model(criteri_model)
    print(f"2. Imatges amb el model '{criteri_model}': {len(res_model)}")
    
    # 3. Operador AND (Intersecció de conjunts)
    res_and = cercador.and_operator(res_prompt, res_model)
    print(f"3. Coincidencies AND (Prompt '{criteri_prompt}' I Model '{criteri_model}'): {len(res_and)}")
    
    # 4. Operador OR (Unio de conjunts)
    res_or = cercador.or_operator(res_prompt, res_model)
    print(f"4. Coincidencies OR (Prompt '{criteri_prompt}' O Model '{criteri_model}'): {len(res_or)}")

    print("\n" + "=" * 60)
    print("       PROVES COMPLETADES AMB EXIT")
    print("=" * 60)