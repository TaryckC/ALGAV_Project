from .patricia import PatriciaTrie
import time  # Importer le module time

def delete_words(file_name):
    """
        Supprime un mot du Patricia-Trie chargé depuis un fichier JSON
        et sauvegarde le résultat dans un nouveau fichier.
    """
    try:
        # Charger l'arbre depuis le fichier JSON
        trie = PatriciaTrie()
        trie.load_from_json("pat.json")
        

        # Mesure du temps de début
        start_time = time.time()

        # Supprimer le mot
        with open(file_name, "r") as file:
            for line in file:
                word = line.strip()
                
                trie.suppression(trie.root,word)

        # Mesure du temps de fin
        end_time = time.time()
        duration = end_time - start_time
        
        
        # Sauvegarder l'arbre mis à jour
        trie.save_to_json("pat.json")
        print("Arbre sauvegardé dans 'pat.json'.")
        print(f"Temps total pour supprimer les mots : {duration:.2f} secondes.")
    except FileNotFoundError:
        print("Erreur : Le fichier 'pat.json' est introuvable.")
    except Exception as e:
        print(f"Une erreur s'est produite : {e}")
