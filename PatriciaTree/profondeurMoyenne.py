from .patricia import PatriciaTrie

import time 


def profondeurMoyenne(filename):
    trie = PatriciaTrie()
    trie.load_from_json(filename)

 
    start = time.time()
    profondeur = trie.profondeurMoyenne(trie.root)
    end = time.time()
    
    

    # Écrit la profondeur moyenne dans un fichier
    with open("profondeur.txt", "w", encoding="utf-8") as f:
        f.write(f"{profondeur}\n")  # Convertir profondeur en chaîne si nécessaire
    
    print("Temps d'exécution : ", end-start)
    print("Profondeur sauvegardée dans profondeur.txt")

    
