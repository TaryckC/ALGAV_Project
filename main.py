import sys
from PatriciaTree.inserer import insert_words
from PatriciaTree.suppression import delete_words
from PatriciaTree.fusion import fusion_trie
from PatriciaTree.listMots import list_Mots
from PatriciaTree.prefixe import prefixe_mot
from PatriciaTree.profondeurMoyenne import profondeurMoyenne

from TrieHybride.HybridTrie import *

def main():
    # Vérifie que 3 ou 4 arguments sont fournis
    if len(sys.argv) < 4:
        print("Usage: python main.py <action> <x> <filename> [optional_param]")
        sys.exit(1)

    # Lecture des arguments obligatoires
    action = sys.argv[1]
    try:
        x = int(sys.argv[2])  # Convertit x en entier
    except ValueError:
        print("Erreur : <x> doit être un entier (0 ou 1).")
        sys.exit(1)

    filename = sys.argv[3]  # Récupère le nom du fichier

    # Vérifie s'il y a un quatrième argument
    optional_param = None
    if len(sys.argv) == 5:
        optional_param = sys.argv[4]  # Récupère le quatrième argument

    # Traitement en fonction de x, de l'action et de l'optional_param
    if x == 0:
        if action == "inserer":
            insert_words(filename)
        elif action == "suppression":
            delete_words(filename)
        elif action == "listeMots":
            list_Mots(filename)
        elif action == "profondeurMoyenne":
            profondeurMoyenne(filename)
        elif action == "fusion":
            if optional_param:
                fusion_trie(filename, optional_param)  # Exemple d'utilisation de l'optional_param
            else:
                print("Erreur : L'action 'fusion' nécessite un paramètre supplémentaire (trie à fusionner).")
        elif action =="prefixe":
            if optional_param:
                prefixe_mot(filename, optional_param)  # Exemple d'utilisation de l'optional_param
            else:
                print("Erreur : L'action 'prefixe' nécessite un paramètre supplémentaire (prefixe recherché).")
        else:
            print(f"Action non reconnue : {action}")
    elif x == 1:
        if action == "inserer":
            insert_words_TH(filename)
        elif action == "suppression":
            delete_words_TH(filename)
        elif action == "listeMots":
            list_Mots_TH(filename)
        elif action == "profondeurMoyenne":
            profondeurMoyenne_TH(filename)
        elif action == "fusion":
            print("Erreur : Il n'a pas été demandé d'implémenter une fonction de fusion pour les trie hybride.")
        elif action == "prefixe":
            prefixe_TH(filename, optional_param)
        else:
            print(f"Action non reconnue : {action}")
    else:
        print("Valeur de x non reconnue : x doit être 0 ou 1")

if __name__ == "__main__":
    main()
