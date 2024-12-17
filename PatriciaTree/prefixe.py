import json
from patricia import PatriciaTrie
import time 


def prefixe_mot(filename,prefixe):
    
    trie = PatriciaTrie()
    trie.load_from_json(filename)
    start_time = time.time()
    # Liste des mots dans l'ordre alphabétique
    nb = trie.Prefixe(trie.root,prefixe)

   
    end_time = time.time()
    duration = end_time - start_time

    with open("prefixe.txt", "w", encoding="utf-8") as f:
            f.write(f"{nb}")  

    #print(f"Les résultats ont été sauvegardés dans prefixe.txt.")
    #print(f"Temps total pour lister les mots : {duration:.6f} secondes.")
    print(end_time - start_time)