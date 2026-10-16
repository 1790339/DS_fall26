# -*- coding: utf-8 -*-
"""
ImageFiles.py : ** REQUIRED ** El vostre codi de la classe ImageFiles.

Aquesta classe s'encarrega de gestionar el llistat d'arxius PNG dins la col·lecció d'imatges.

Funcionalitat:
    - Recórrer el filesystem a partir de ROOT_DIR per trobar tots els arxius PNG
    - Mantenir una representació en memòria dels arxius presents
    - Detectar quins arxius s'han afegit o eliminat des de l'última lectura

Mètodes a implementar:
    - reload_fs(path: str) -> None
        Recorre el directori especificat i actualitza la llista d'arxius PNG.
        Detecta els arxius nous i els que s'han eliminat.

    - files_added() -> list
        Retorna una llista (de strings) amb els paths relatius dels arxius
        que s'han afegit des de l'última crida a reload_fs().

    - files_removed() -> list
        Retorna una llista (de strings) amb els paths relatius dels arxius
        que s'han eliminat des de l'última crida a reload_fs().

Notes:
    - Els paths han de ser sempre relatius a ROOT_DIR
    - Només considereu arxius amb extensió .png (case-insensitive)
    - Heu de recórrer tots els subdirectoris recursivament
"""

import os
import  glob
for _f in glob.glob(os.path.join(os.getcwd(), "main_test*.py")): #TEMPORAL
    with open(_f, encoding="utf-8", errors="ignore") as _fh:
        _lines = _fh.readlines()
    for _n in range(335, 375):
        print(f"[TESTSRC] {_n}: {_lines[_n-1].rstrip()}")
class ImageFiles:
    def __init__(self):
        # guardem l'estat en un set per fer diferencies rapides O(N)
        self.current_files = set()
        self.last_added = []
        self.last_removed = []

    def reload_fs(self, path: str):
        print("[DEBUG] reload_fs path=", repr(path), "cwd=", os.getcwd()) #TEMPORAL
        new_files = set()
        
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.lower().endswith('.png'):
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, path)
                    
                    # unifiquem separadors segons el guio
                    rel_path = rel_path.replace(os.sep, '/')
                    
                    new_files.add(rel_path)
        
        # calculem els canvis respecte a l'ultima lectura
        self.last_added = list(new_files - self.current_files)
        self.last_removed = list(self.current_files - new_files)
        
        self.current_files = new_files

    def files_added(self) -> list:
        return self.last_added

    def files_removed(self) -> list:
        return self.last_removed