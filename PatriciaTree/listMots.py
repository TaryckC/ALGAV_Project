from .patricia import PatriciaTrie
import time 
def list_Mots(filename):
    
    trie = PatriciaTrie()
    trie.load_from_json(filename)
    start_time = time.time()
    # Liste des mots dans l'ordre alphabétique
    lesMots = trie.listeMots()

   
    end_time = time.time()
    duration = end_time - start_time

    with open("mots.txt", "w", encoding="utf-8") as f:
        for word in lesMots:
            f.write(word + "\n")  # Écrire un mot par ligne

    print(f"Les mots ont été sauvegardés dans mots.txt.")
    print(f"Temps total pour lister les mots : {duration:.6f} secondes.")
    print(f"Nombre de visite de noeuds {trie.comparaisons}")