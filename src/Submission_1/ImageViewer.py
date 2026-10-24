# -*- coding: utf-8 -*-
"""
ImageViewer.py : ** REQUIRED ** El vostre codi de la classe ImageViewer.

Aquesta classe s'encarrega de visualitzar imatges i mostrar les seves metadades.

Funcionalitat:
    - Imprimir per pantalla les metadades d'una imatge
    - Mostrar la imatge en pantalla
    - Combinar ambdues accions segons la configuració

Mètodes a implementar:
    - print_image(uuid: str) -> None
        Imprimeix per pantalla totes les metadades de la imatge identificada
        per l'UUID. Ha de mostrar:
        - Dimensions (width x height)
        - Prompt (truncat si és molt llarg)
        - Model
        - Seed
        - CFG Scale
        - Steps
        - Sampler
        - Generated
        - Created Date
        - UUID
        - Path de l'arxiu

    - show_file(file: str) -> None
        Mostra la imatge especificada utilitzant PIL.
        Aquesta funció NO espera que la imatge es tanqui (asíncrona).

    - show_image(uuid: str, mode: int) -> None
        Combina print_image() i show_file() segons el mode especificat:
        - mode 0: només metadades
        - mode 1: metadades + imatge
        - mode 2: només imatge

        Aquesta funció ha d'esperar que l'usuari tanqui la imatge abans
        de retornar (síncrona). Podeu utilitzar input() per fer una pausa.

Notes:
    - Utilitzeu cfg.DISPLAY_MODE per determinar el comportament per defecte
    - Per mostrar imatges: img.show() de PIL
    - Gestioneu les excepcions si la imatge no es pot mostrar
    - El format de sortida ha de ser llegible i ben organitzat
"""
import cfg as cfg
import os
from PIL import Image

class ImageViewer:
    def __init__(self, dades_imatge):
        # Guardem les referències als gestors per poder consultar les rutes i les metadades directament des de la memòria.
        self.image_data = dades_imatge

    def print_image(self, uuid: str):
        file = self.image_data.get_filename(uuid) #Comprovem que l'uuid esta al diccionari
        if file == None:
            print(f"Error: UUID {uuid} no registrat")
            return

        # Si encara no s'han llegit les metadades, les carreguem
        if self.image_data.get_prompt(uuid) is None:
            try:
                self.image_data.load_metadata(uuid)
            except OSError as e:
                print(f"Error: {e}")
            
        print(f"\n--- Metadades de la imatge ---")
        print(f" UUID:      {uuid}")
        print(f" Prompt:    {self.gestor_dades.get_prompt(uuid)[:90]}...")
        print(f" Model:     {self.gestor_dades.get_model(uuid)}")
        print(f" CFG Scale: {self.gestor_dades.get_cfg_scale(uuid)}")
        print(f" Steps:     {self.gestor_dades.get_steps(uuid)}")
        print(f" Seed:      {self.gestor_dades.get_seed(uuid)}")
        print(f" Sampler:   {self.gestor_dades.get_sampler(uuid)}")
        print(f" Generated: {self.gestor_dades.get_generated(uuid)}")
        print(f" Data:      {self.gestor_dades.get_created_date(uuid)}")
        print("-" * 30)

    def show_file(self, file: str):
        # Obtenim la ruta absoluta necessària per obrir l'arxiu físic
        abs_file = os.path.join(cfg.get_root(), file)
        
        if not os.path.isfile(abs_file):
            print(f"Error: L'arxiu {abs_file} no existeix al disc.")
            return
            
        try:
            img = Image.open(abs_file)
            img.show()
        except Exception as e:
            print(f"Error en visualitzar la imatge: {e}")

    def show_image(self, uuid: str, mode: int):
        # Recuperem la ruta relativa a partir de l'UUID consultant el diccionari O(1)
        file = self.image_data.get_filename(uuid)
        
        if not file:
            print(f"Error: L'identificador {uuid} no està registrat al sistema.")
            return

        # mode 0: només metadades
        # mode 1: metadades + imatge
        # mode 2: només imatge
        
        if mode == 0 or mode == 1:
            self.print_image(uuid)
            
        if mode == 1 or mode == 2:
            self.show_file(file)