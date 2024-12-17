import json
class PatriciaNode:
    def __init__(self):
        self.labels = {}

class PatriciaTrie:
    def __init__(self):
        self.root = PatriciaNode()  # La racine de l'arbre
    
    def insererMots(self, mot):
        current_node = self.root

        while mot:
            for label, child in current_node.labels.items():
                # Trouver le préfixe commun entre le label et le mot restant
                i = self.common_prefix_length(label, mot)

                if i > 0:  # Un préfixe commun a été trouvé
                    if i == len(label):  # Le label est un préfixe complet du mot
                        mot = mot[i:]  # Réduire le mot restant
                        current_node = child  # Descendre dans l'enfant
                        break

                    # Cas où le label doit être divisé
                    common_prefix = label[:i]
                    remaining_label = label[i:]
                    remaining_word = mot[i:]

                    # Remplacer le label existant par le préfixe commun
                    current_node.labels.pop(label)
                    new_node = PatriciaNode()
                    current_node.labels[common_prefix] = new_node

                    # Ajouter les deux branches (ancienne et nouvelle)
                    new_node.labels[remaining_label] = child
                    if remaining_word:
                        new_node.labels[remaining_word] = PatriciaNode()
                        new_node.labels[remaining_word].labels["#"] = None
                    else:
                        new_node.labels["#"] = None
                    return  # Fin de l'insertion

            else:  # Aucun préfixe commun n'a été trouvé
                current_node.labels[mot] = PatriciaNode()
                current_node.labels[mot].labels["#"] = None
                return

        # Si le mot est déjà fini mais a des enfants, ajouter "#"
        if "#" not in current_node.labels:
            current_node.labels["#"] = None

            



    def Recherche(self, node, mot):
        
        # Cas de base : Si le mot restant est vide
        if not mot:
            if "#" in node.labels:  # Vérifie si c'est la fin d'un mot
                print("Le mot existe")
                return True
            else:
                print("Le mot n'existe pas")
                return False

        # Parcourir les enfants du nœud actuel
        for label, child in node.labels.items():
            i = self.common_prefix_length(label, mot)

            if i > 0:  # Préfixe commun trouvé
                if i == len(label):  # Préfixe complet, descendre dans l'enfant
                    return self.Recherche(child, mot[i:])
                else:  # Préfixe partiel, le mot n'existe pas
                    print("Le mot n'existe pas")
                    return False

        # Aucun label n'a de préfixe commun
        print("Le mot n'existe pas")
        return False

    def common_prefix_length(self,s1, s2):
        length = 0
        while length < len(s1) and length < len(s2) and s1[length] == s2[length]:
            length += 1
        return length
    


    # def prefixe(self,mot, node=None):
        
    #     if node  is None:
    #         node = self.root
    #     words = self.listeMots()
    #     i=0
    #     for word1 in words :
    #         if self.common_prefix_length(mot,word1) == len(mot):
    #             i=i+1

    #     return i

    def Prefixe(self, node, mot):
        """
        Retourne le nombre de mots pour lesquels 'mot' est un préfixe.
        Le mot 'mot' n'a pas besoin d'exister dans l'arbre en tant que mot complet.
        """
        # Si le mot est entièrement consommé, compter tous les mots sous ce nœud
        if not mot:
            return self.comptageMots(node)

        # Parcourir les labels pour trouver un préfixe commun
        for label, child in node.labels.items():
            common_length = self.common_prefix_length(label, mot)

            if common_length > 0:  # Un préfixe commun est trouvé
                if common_length == len(mot):
                    # Le mot 'mot' est complètement consommé
                    return self.comptageMots(child)
                elif common_length == len(label):
                    # Descendre dans l'arbre avec la partie restante du mot
                    return self.Prefixe(child, mot[common_length:])
                else:
                    # Préfixe partiel mais insuffisant
                    return 0

        # Si aucun préfixe commun n'est trouvé, retourner 0
        return 0

    

    def suppression(self, arbre, mot):
        current_node = arbre

        # Cas de base : le mot est vide
        if not mot:
            if "#" in current_node.labels:  # Vérifier si c'est la fin d'un mot
                del current_node.labels["#"]  # Supprimer l'indicateur de fin de mot
                # Si le nœud n'a plus d'enfants, il peut être supprimé
                if not current_node.labels:
                    return True  # Indique que le nœud peut être supprimé
            return False  # Le mot n'existe pas

        # Parcourir les labels pour trouver un préfixe commun
        for label, child in list(current_node.labels.items()):
            prefix_length = self.common_prefix_length(label, mot)

            if prefix_length > 0:  # Trouver un préfixe commun
                if prefix_length == len(label):  # Correspondance complète du label
                    # Appel récursif avec le reste du mot
                    can_delete = self.suppression(child, mot[prefix_length:])
                    if can_delete:
                        del current_node.labels[label]  # Supprimer le nœud si vide
                        return not current_node.labels  # Vérifier si le nœud parent est vide
                return False  # Préfixe trouvé, mais le mot complet n'existe pas

        
        return False
        
    def Hauteur(self, node):
        if node is None:
            return 0
       
        if not node.labels:
            return 1

        # Calculer la hauteur de chaque sous-arbre
        max_height = 0
        for label, child in node.labels.items():
            # Appel récursif pour chaque enfant
            child_height = self.Hauteur(child)
            max_height = max(max_height, child_height)

        # Retourner 1 + la hauteur maximale des enfants
        return 1 + max_height
            
    def averageLeafDepth(self, node, depth=0):
       

        # Si c'est une feuille (contient le label "#" uniquement)
        if not node.labels or "#" in node.labels and len(node.labels) == 1:
            return depth, 1  # Profondeur actuelle et 1 feuille trouvée

        # Initialiser la somme des profondeurs et le nombre de feuilles
        total_depth = 0
        total_leaves = 0

        # Parcourir tous les enfants
        for label, child in node.labels.items():
            if child:  # Vérifier que l'enfant n'est pas None
                child_depth, child_leaves = self.averageLeafDepth(child, depth + 1)
                total_depth += child_depth
                total_leaves += child_leaves
            elif label == "#":  # Marque une feuille
                total_depth += depth
                total_leaves += 1

        return total_depth, total_leaves

    def profondeurMoyenne(self,arbre):
        total_depth, total_leaves = self.averageLeafDepth(arbre)
        if total_leaves == 0:  # Éviter la division par zéro
            return 0
        return round(total_depth / total_leaves)
    

    def comptageMots(self, node):
        
        # Initialiser le compteur de mots
        word_count = 0

        # Vérifier si le nœud contient le caractère "#" (fin d'un mot)
        if "#" in node.labels:
            word_count += 1

        # Parcourir les enfants du nœud
        for label, child in node.labels.items():
            if child:  # Vérifier que l'enfant n'est pas None
                word_count += self.comptageMots(child)

        return word_count

    def listeMots(self, node=None, prefix=""):
        # Si le nœud est None, commencer à partir de la racine
        if node is None:
            node = self.root
        

        # Liste pour stocker les mots
        words = []

        # Si le label "#" est présent, ajouter le mot complet à la liste
        if "#" in node.labels:
            words.append(prefix)

        # Parcourir les enfants dans l'ordre des clés alphabétiques
        for label in sorted(node.labels.keys()):
            child = node.labels[label]
            if label != "#":  # Ignorer le caractère de fin de mot
                words.extend(self.listeMots(child, prefix + label))

        return words

    
        
    def to_dict(self, node=None, prefix=""):
        """
        Convertit le Patricia-trie en un dictionnaire respectant strictement la structure demandée.
        """
        if node is None:
            node = self.root

        children_dict = {}

        # Parcourir les enfants du nœud courant
        for label, child in sorted(node.labels.items()):
            if label == "#":  # Ignorer le marqueur de fin de mot
                continue

            # La première lettre devient la clé dans `children`
            first_letter = label[0]
            remaining_label = label  # Le reste du label

            # Construire le sous-arbre avec le reste du label
            sub_tree = {
                "label": remaining_label,
                "is_end_of_word": "#" in child.labels,
                "children": {
                    sub_label[0]: self.to_dict(sub_child, prefix=sub_label)
                    for sub_label, sub_child in sorted(child.labels.items())
                    if sub_label != "#"
                }
            }

            # Ajouter au dictionnaire des enfants
            children_dict[first_letter] = sub_tree

        # Retourner le nœud courant avec ses enfants
        return {
            "label": prefix,  # Préfixe propagé
            "is_end_of_word": "#" in node.labels,
            "children": children_dict
        }

   

    def save_to_json(self, filename):
        """
        Sauvegarde l'arbre Patricia-trie dans un fichier JSON.
        """
        # Convertir l'arbre en un dictionnaire JSON-compatible
        tree_dict = self.to_dict()

        # Écrire dans un fichier
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(tree_dict, f, indent=4, ensure_ascii=False)
        
        print(f"Arbre Patricia sauvegardé dans le fichier {filename}")

    def from_dict(self, node_dict, parent_node=None):
        """
        Reconstruit un Patricia-trie à partir d'un dictionnaire JSON.
        """
        if parent_node is None:
            parent_node = self.root

        # Lire le label du nœud courant
        label = node_dict.get("label", "")
        is_end_of_word = node_dict.get("is_end_of_word", False)
        children = node_dict.get("children", {})

        # Ajouter le label courant
        if label:
            parent_node.labels[label] = PatriciaNode()
            current_node = parent_node.labels[label]
        else:
            current_node = parent_node

        # Marquer la fin de mot si nécessaire
        if is_end_of_word:
            current_node.labels["#"] = PatriciaNode()

        # Parcourir les enfants
        for child_label, child_dict in children.items():
            self.from_dict(child_dict, current_node)

    def load_from_json(self, filename):
        """
        Charge un Patricia-trie depuis un fichier JSON.
        """
        with open(filename, 'r') as f:
            tree_dict = json.load(f)
        self.from_dict(tree_dict)

    def ComptageNil(self, node=None):
        
        if node is None:
            node = self.root

        count = 0

        # Parcourir les labels et leurs enfants
        for label, child in node.labels.items():
            if child is None:  # Si le pointeur est None
                count += 1
            else:
                # Appel récursif pour les enfants non vides
                count += self.ComptageNil(child)
        return count
    

    def fusion_nodes(self, node1, node2):
        """
        Fusionne deux nœuds Patricia et retourne le nœud fusionné.
        Les labels sont triés pour faciliter les comparaisons.
        """
        # Si l'un des nœuds est vide, retourner l'autre directement
        if not node1:
            return node2
        if not node2:
            return node1

        # Trier les labels des deux nœuds pour simplifier les comparaisons
        labels1 = sorted(node1.labels.keys())
        labels2 = sorted(node2.labels.keys())

        # Index pour parcourir les labels
        i, j = 0, 0

        # Fusion des labels triés
        while i < len(labels1) and j < len(labels2):
            label1 = labels1[i]
            label2 = labels2[j]

            common_length = self.common_prefix_length(label1, label2)
            if common_length > 0:
                # Préfixe commun trouvé
                common_prefix = label1[:common_length]
                remainder1 = label1[common_length:]
                remainder2 = label2[common_length:]

                # Créer un nœud pour le préfixe commun s'il n'existe pas
                if common_prefix not in node1.labels:
                    node1.labels[common_prefix] = PatriciaNode()
                common_node = node1.labels[common_prefix]

                # Ajouter les parties restantes
                if remainder1:
                    common_node.labels[remainder1] = node1.labels.pop(label1)
                if remainder2:
                    common_node.labels[remainder2] = node2.labels.pop(label2)
                else:
                    # Fusionner récursivement les sous-arbres
                    self.fusion_nodes(common_node, node2.labels.pop(label2))

                # Passer aux labels suivants
                i += 1
                j += 1
            elif label1 < label2:
                # Si label1 est plus petit, avancer dans node1
                i += 1
            else:
                # Si label2 est plus petit, ajouter directement à node1
                node1.labels[label2] = node2.labels.pop(label2)
                j += 1

        # Ajouter les labels restants de node2 à node1
        while j < len(labels2):
            label2 = labels2[j]
            node1.labels[label2] = node2.labels[label2]
            j += 1

        return node1

    def fusion(self, other_trie):
        # Liste des mots des deux Patricia-Tries avant fusion
        words_from_self = self.listeMots()
        words_from_other = other_trie.listeMots()

        # Liste attendue après fusion
        expected_words = set(words_from_self + words_from_other)

        self.fusion_nodes(self.root, other_trie.root)
        # Liste des mots après la fusion
        words_after_merge = self.listeMots()

        # Vérification
        if set(words_after_merge) == expected_words:
            print("Fusion réussie : tous les mots sont présents.")
            return True
        else:
            print("Erreur dans la fusion : certains mots manquent ou sont en trop.")
            print("Mots attendus :", expected_words)
            print("Mots trouvés :", set(words_after_merge))
            return False


    def display(self, node=None, prefix=""):

        if node is None:
            node = self.root  # Si aucun nœud n'est fourni, commence à la racine

        for label, child in node.labels.items():
            # Affiche le label courant
            

            # Si l'enfant n'est pas None, continue à afficher récursivement
            if child:
                self.display(child, prefix + label)
            else:
                print(f"{prefix}{label}")
                


