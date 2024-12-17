import json
from patricia import PatriciaTrie
import time 
def compter_Mots(filename):
    
    trie = PatriciaTrie()
    trie.load_from_json(filename)
    start_time = time.time()
    # Liste des mots dans l'ordre alphabétique
    lesMots = trie.comptageMots(trie.root)

   
    end_time = time.time()
    duration = end_time - start_time

    with open("nbMots.txt", "w", encoding="utf-8") as f:
        f.write(f"{lesMots}\n") # Écrire un mot par ligne

    print(f"Les mots ont été sauvegardés dans mots.txt.")
    print(f"Temps total pour lister les mots : {duration:.6f} secondes.")