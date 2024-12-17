from patricia import PatriciaTrie

def fusion_trie(pat_1,pat_2):
    trie1=PatriciaTrie()
    trie2= PatriciaTrie()

    trie1.load_from_json(pat_1)
    trie2.load_from_json(pat_2)

    trie1.fusion(trie2)
    
    # Sauvegarder l'arbre mis à jour
    trie1.save_to_json("pat.json")
    print("Arbre sauvegardé dans 'pat.json'.")

