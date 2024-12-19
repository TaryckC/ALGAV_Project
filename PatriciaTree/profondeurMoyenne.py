from .patricia import PatriciaTrie

def profondeurMoyenne(filename):
    trie = PatriciaTrie()
    trie.load_from_json(filename)

 

    profondeur = trie.profondeurMoyenne(trie.root)

    
    

    # Écrit la profondeur moyenne dans un fichier
    with open("profondeur.txt", "w", encoding="utf-8") as f:
        f.write(f"{profondeur}\n")  # Convertir profondeur en chaîne si nécessaire
    
    print(f"Profondeur sauvegardée dans profondeur.txt ")
    print(f"Nombre de visite de noeuds {trie.comparaisons}")

    
