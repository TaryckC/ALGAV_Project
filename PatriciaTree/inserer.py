import os
import time  # Importer le module time
from .patricia import PatriciaTrie

def insert_words(source):
    """
    Insère des mots depuis un fichier texte ou un dossier contenant des fichiers texte
    dans un Patricia-Trie, et mesure le temps pris pour l'opération.
    """
    trie = PatriciaTrie()

    # Mesure du temps de début
    start_time = time.time()

    # Vérifier si la source est un fichier ou un dossier
    if os.path.isfile(source):  # Cas d'un fichier unique
        _insert_from_file(trie, source)
    elif os.path.isdir(source):  # Cas d'un dossier contenant plusieurs fichiers
        fichiers_txt = [f for f in os.listdir(source) if f.endswith('.txt')]
        
        for file_name in fichiers_txt:
            full_path = os.path.join(source, file_name)  # Construire le chemin complet
           
            _insert_from_file(trie, full_path)
    else:
        raise ValueError(f"{source} n'est ni un fichier ni un dossier valide.")

    # Mesure du temps de fin
    end_time = time.time()
    duration = end_time - start_time

    
    # Sauvegarder l'arbre dans un fichier JSON
    trie.save_to_json("pat.json")
    print(f"Mots insérés depuis {source} et sauvegardés dans pat.json.")
    print(f"Temps total pour insérer les mots : {duration:.2f} secondes.")
    print(f"Nombre de comparaison {trie.comparaisons}")


def _insert_from_file(trie, file_name):
    """
    Insère des mots dans un Patricia-Trie depuis un fichier texte.
    """
    with open(file_name, "r", encoding="utf-8") as file:
        for line in file:
            word = line.strip()
            trie.insererMots(word)
