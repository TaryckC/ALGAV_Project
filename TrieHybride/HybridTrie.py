import json
import time  # Importer le module time
import os

class HybridTrie :
    """
    Classe représentant un noeud d'un Trie Hybride

    Attributs :
        - Value : Valeur du Noeud
        - position : Indique si le mot est terminé et commbien le sont aussi au moment de la complétion.
        - childIng : L'enfant inférieur
        - childEq : L'enfant égal
        - childSup : L'enfant supérieur
    """

    # Fin méthodes privée.

    def __init__(self, value = None, position = None) :
        """
        Constructeur de la classe HybridTrieNode.

        Crée un noeud pour un Trie hybride.
        Prend en entrée : Un caractère, Un entier (si le mot est terminé).

        Le noeud crée 3 enfants : Un pour les valeurs plus petites, Un pour les valeurs égales, Un pour les valeurs plus grandes,
        ces Noeuds sont par défaut égaux à None.
        """

        self.value = value
        self.position = position

        self.childInf = None
        self.childEq = None
        self.childSup = None
    
    def isEmpty(self) :
        """
        Méthode vérifiant si un noeud est vide.

        Ne prend rien en argument.

        Renvoie un boolean : 
            - True : si le noeud est vide
            - False : si le noeud n'est pas vide
        """
        if (self.value is None) :
            return True
        return False
    
# Fin classe

compteurInsertion = 0
compteurList = 0
compteurPrefixe = 0
compteurProfMoyenne = 0
compteurSuppression = 0


# Primitives sur les clés des tries :
def prem(cle) :
    """ S−> str Renvoie le premier caractere de la cle. """
    if len(cle) < 1:
        return ""
    return cle[0]

def reste(cle):
    """ Renvoie la clé privée de son premier caractère. """
    if len(cle) <= 1:
        return ""
    return cle[1:]

def car(cle, i):
    """ S * entier -> str Renvoie le i-ème caractère de la cle. """
    if len(cle) < 1 or i >= len(cle):
        return ""
    return cle[i]

def lgueur(cle):
    """ S -> entier Renvoie le nombre de caractères de la cle. """
    return len(cle)

# Question 1.4 : Primitives sur les Trie Hybride :

def TH_Vide():
    """ −> Trie hybride Renvoie le trie a 1 noeud vide avec 3 liens vides . """
    return HybridTrie()

def EstVide(A) :
    """ Trie hybride−> booleen Renvoie vrai ssi A est vide . """
    return A.isEmpty()

def Val(A):
    """ Trie hybride−> elt Renvoie la valeur de la racine du trie . """
    return A.position

def ValVide() :
    return None

def Eq(A) :
    """ Trie hybride > Trie hybride Renvoie une copie du sous arbre égale centrale de A """
    if A.childEq is None :
        return TH_Vide()
    return A.childEq

def Sup(A) :
    """ Trie hybride > Trie hybride Renvoie une copie du sous arbre égale supérieur de A """
    if A.childSup is None :
        return TH_Vide()
    return A.childSup

def Inf(A) :
    """ Trie hybride > Trie hybride Renvoie une copie du sous arbre égale inférieur de A """
    if A.childInf is None :
        return TH_Vide()
    return A.childInf

def Racine(A) :
    return A.value

def SousArbre(A, i) :
    match i :
        case 0 :
            return Inf(A)
        case 1 :
            return Eq(A)
        case 2 :
            return Sup(A)
    raise IndexError("Index must be between 0 and 2")

def EnfantsSauf (A, i):
    """ Trie hybride * entier−> liste [Trie hybride ] Renvoie la liste des sous−arbres du trie privee du i−eme sous−arbre . """
    res = []
    for j in range (3) :
        if i != j :
            res.append(SousArbre(A, j))
    return res

def TrieH(value, inf, eq, sup, position) :
    """ entier* liste [TrieH ]* TrieH> TrieH Renvoie le trie construit a partir de L, en inserant A a la i−eme position . """
    trie = HybridTrie(value, position)
    trie.childInf = inf
    trie.childEq = eq
    trie.childSup = sup
    return trie

# Fin question 1.4

def TH_Ajout(c, A, v) :
    """ cle* TrieH* valeur−> trieH Renvoie le trie hybride resultant de l’insertion de c dans A. """
    global compteurInsertion
    if c == "" :
        compteurInsertion += 1
        return A

    if EstVide (A):
        compteurInsertion += 1
        if lgueur (c) == 1:
            compteurInsertion += 1
            return TrieH ( prem (c), TH_Vide (), TH_Vide (), TH_Vide (), v)
        else :
            return TrieH ( prem (c), TH_Vide (), TH_Ajout ( reste (c), Eq(A), v), TH_Vide (), ValVide())
    else :
        p = prem (c)
        if p < Racine(A):
            compteurInsertion += 1
            return TrieH (Racine(A), TH_Ajout (c, Inf(A), v), Eq(A), Sup(A), Val(A))
        if p > Racine(A):
            compteurInsertion += 1
            return TrieH (Racine(A), Inf(A), Eq(A), TH_Ajout (c, Sup(A), v), Val(A))
        else :
            if lgueur(c) == 1 :
                compteurInsertion += 1
                # On gère le cas ou le mot que l'on essaye d'ajouter est un préfixe d'un mot déjà présent :
                return TrieH (Racine(A), Inf(A), Eq(A), Sup(A), v if Val(A) is None else Val(A))
            else :
                return TrieH (Racine(A), Inf(A), TH_Ajout ( reste (c), Eq(A), v), Sup(A), Val(A))


# Fonctions Utiles

def afficheTrie(node, prefix="", origin="Root", depth=0):
    """
    Affiche le contenu d'un Trie Hybride avec une structure hiérarchisée
    et précise si le nœud appartient à childInf, childEq ou childSup.

    Arguments :
        node (HybridTrie) : Le nœud actuel du Trie.
        prefix (str) : Chaîne représentant le mot construit jusqu'à ce nœud.
        origin (str) : Indique si le nœud provient de childInf, childEq, ou childSup.
        depth (int) : Niveau actuel dans l'arbre pour indenter l'affichage.

    Retourne :
        None : Affiche directement le contenu du Trie dans la console.
    """
    if node is None:
        return

    indent = "    " * depth  # Indentation pour refléter la profondeur de l'arbre

    # Afficher la valeur du nœud avec son origine
    if node.value is not None:
        print(f"{indent}{origin} -> Value: {node.value}, Position: {node.position}")
    else:
        print(f"{indent}{origin} -> (vide)")

    # Explorer les sous-arbres avec un niveau supplémentaire d'indentation
    afficheTrie(node.childInf, prefix, "Inf", depth + 1)
    afficheTrie(node.childEq, prefix + (node.value if node.value else ""), "Eq", depth + 1)
    afficheTrie(node.childSup, prefix, "Sup", depth + 1)

def printAllWords(node, prefix=""):
    """
    Parcourt le Trie Hybride et affiche tous les mots complets stockés dans l'arbre.

    Arguments :
        node (HybridTrie): Le nœud courant du Trie Hybride.
        prefix (str): Le mot en cours de construction (par les caractères des nœuds parcourus).

    Retourne :
        None: Affiche les mots directement dans la console.
    """
    if node is None:
        return

    # Si le nœud actuel représente la fin d'un mot, on l'affiche
    if node.position is not None:
        print(f"Mot: {prefix + node.value}, Position: {node.position}")

    # Parcours des sous-arbres
    printAllWords(node.childInf, prefix)  # Sous-arbre inférieur
    printAllWords(node.childEq, prefix + (node.value if node.value else ""))  # Sous-arbre égal
    printAllWords(node.childSup, prefix)  # Sous-arbre supérieur

def printCompletedWords(node, prefix=""):
    """
    Parcourt le Trie Hybride et affiche uniquement les mots terminés (ceux avec une position définie).

    Arguments :
        node (HybridTrie): Le nœud courant du Trie Hybride.
        prefix (str): Le mot en cours de construction (par les caractères des nœuds parcourus).

    Retourne :
        None: Affiche les mots terminés directement dans la console.
    """
    if node is None:
        return

    # Si le nœud actuel représente la fin d'un mot, on l'affiche
    if node.position is not None and node.value is not None:
        print(f"Mot: {prefix + node.value}, Position: {node.position}")

    # Parcours des sous-arbres
    printCompletedWords(node.childInf, prefix)  # Sous-arbre inférieur
    printCompletedWords(node.childEq, prefix + (node.value if node.value else ""))  # Sous-arbre égal
    printCompletedWords(node.childSup, prefix)  # Sous-arbre supérieur

#  Fin utiles

# Question 1.5 :

def getWord(string):
    """
    Extrait un mot de la chaîne et retourne le mot en minuscules,
    en ignorant tout ce qui n'est pas une lettre.

    Arguments :
        string (str): La chaîne à analyser.

    Retourne :
        tuple (str, int): Le mot extrait (en minuscules) et l'offset total.
    """
    res = ""
    offset = 0
    length = len(string)

    # Ignorer les caractères non alphabétiques au début
    while offset < length and not string[offset].isalpha():
        offset += 1

    # Lire les caractères valides (lettres uniquement)
    while offset < length and (string[offset].isalpha()):
        res += string[offset].lower()
        offset += 1

    return res, offset

def lookup(A, c) :
    """
    Cherche le mot dans le trie.

    Arguments :
        arbre (HybridTrie) : Trie ou sera chercher le mot
        mot (str) : mot recherché dans le trie

    Retourne :
        Un boolean : True si le mot a été trouvé et False sinon
    """
    if c == "" :
        return False
    elif not EstVide(A) :
        if lgueur(c) == 1 and c == Racine(A) and not (Val(A) is None) :
            return True
        else :
            p = (prem(c))
            if p < Racine(A):
                return lookup(Inf(A), c)
            if p > Racine(A):
                return lookup(Sup(A), c)
            return lookup(Eq(A), reste(c))
    # Sinon : L'arbre est vide et donc ne contient aucun mot.
    return False

def textToTH(s):
    trie = TH_Vide()
    v = 0
    i = 0
    length = len(s)

    while i < length:
        word, offset = getWord(s[i:])
        if word:
            if not lookup(trie, word):
                trie = TH_Ajout(word, trie, v)
                v += 1
        else:
            # Si aucun mot n'est trouvé, avancer d'un caractère
            offset = 1
        i += offset

    return trie

exempleDeBase = "A quel genial professeur de dactylographie sommes nous redevables de la superbe phrase ci dessous, un modele du genre, que toute dactylo connait par coeur puisque elle fait appel a chacune des touches du clavier de la machine a ecrire ?"
newTrie = textToTH(exempleDeBase)
# Fin question 1.5

# Qestion 2.6 : On entend quoi par "dictionnaire" ?

# Recherche :

def Recherche(A, c) :
    """
    Cherche le mot dans le trie en ignorant la casse.

    Arguments :
        arbre (HybridTrie) : Trie ou sera chercher le mot
        mot (str) : mot recherché dans le trie (la asse est ignorée)

    Retourne :
        Un boolean : True si le mot a été trouvé et False sinon
    """
    c = c.lower()
    return lookup(A, c)

# ComptageMots :
def ComptageMots(A) :
    """
    Compte le nombre de mots présent dans le trie

    Arguments :
        Une Trie Hybride

    Retourne :
        Un entier correspondant au nombre de mot présent dans le trie
    """
    res = 0
    if EstVide(A) :
        return 0
    elif not (Val(A) is None) :
        res += 1
    res += ComptageMots(Inf(A)) + ComptageMots(Eq(A)) + ComptageMots(Sup(A))
    return res

# ListeMots :

def CreateWord(node, prefix="") :
    """
    Renvoie la liste des mots contenus dans le trie dans l'ordre alphabétique

    Arguments :
        - Un trie Hybride
        - Un préfix (facultatif) déstiné à être modifier par les différents appelles récursifs de la fonction pour se souvenir du mot lu

    Retourne :
        - La liste des mots du trie dans l'ordre alphabétique
    """
    global compteurList, compteurPrefixe
    compteurList += 1
    compteurPrefixe += 1
    res = []
    if EstVide(node) :
        return res
    else :
        word = prefix + Racine(node)
        res += CreateWord(Inf(node), prefix)
        if (isinstance(Val(node), int)) :
            print(word)
            res.append(word)
        res += CreateWord(Eq(node), word)
        res += CreateWord(Sup(node), prefix)
        return res

def ListeMots(A) :
    """
    Renvoie la liste des mots contenus dans le trie dans l'ordre alphabétique

    Arguments :
        - Un trie Hybride

    Retourne :
        - La liste des mots du trie dans l'ordre alphabétique
    """
    return CreateWord(A)

# ComptageNil(arbre)

def ComptageNil(A) :
    """
    Compte le nombre de pointeur vers un Noeud vide (Nil)

    Arguments :
        - Un trie Hybride

    Retourne :
        - Le nombre de pointeur vers un Noeud vide
    """
    res = 0
    if EstVide(A) :
        return 1
    else :
        res += ComptageNil(Inf(A)) + ComptageNil(Eq(A)) + ComptageNil(Sup(A))
        return res

# Hauteur :

def Hauteur(A):
    """
    Calcule la hauteur d'un Trie Hybride.

    Arguments :
        - A (HybridTrie) : Le Trie Hybride dont on souhaite calculer la hauteur.

    Retourne :
        - Un entier correspondant à la hauteur du Trie :
            - 0 si le Trie est vide.
            - Le maximum entre les hauteurs des sous-arbres inférieur, égal et supérieur, plus 1 (pour le nœud courant).
    """
    if EstVide(A) :
        return 0
    else :
        return 1+max(Hauteur(Inf(A)), Hauteur(Eq(A)), Hauteur(Sup(A)))

# Profondeur moyenne :

def ToutesProfondeurs(A, current=0) :
    """
    Calcule la profondeur de tous les nœuds d'un Trie Hybride.

    Cette fonction parcourt récursivement tous les nœuds du Trie pour collecter leurs profondeurs
    (le niveau dans l'arbre où se trouve chaque nœud).

    Arguments :
        - A (HybridTrie) : Le Trie Hybride à analyser.
        - current (int) : La profondeur actuelle, utilisée pour la récursion (par défaut 0, représentant la racine).

    Retourne :
        - list[int] : Une liste contenant la profondeur de chaque nœud du Trie.
                      Chaque élément représente la profondeur d'un nœud visité.

    Cas particuliers :
        - Si le Trie est vide, retourne une liste vide.
    """
    global compteurProfMoyenne
    compteurProfMoyenne += 1
    res = []
    if EstVide(A) :
        return res
    else :
        current += 1
        res.append(current)
        return res + ToutesProfondeurs(Inf(A), current) + ToutesProfondeurs(Eq(A), current) + ToutesProfondeurs(Sup(A), current)
    
def ProfondeurMoyenne(A) :
    """
    Calcule la profondeur moyenne des nœuds d'un Trie Hybride.

    La profondeur moyenne est définie comme la somme des profondeurs de tous les nœuds
    divisée par le nombre total de nœuds visités.

    Arguments :
        - A (HybridTrie) : Le Trie Hybride à analyser.

    Retourne :
        - float : La profondeur moyenne des nœuds.
                  Retourne 0 si le Trie est vide.

    Cas particuliers :
        - Si le Trie est vide, retourne 0 pour éviter une division par zéro.
    """
    profondeurs = ToutesProfondeurs(A)
    res = 0
    compteur = 0
    for i in profondeurs :
        res += i
        compteur += 1
    # On prend en compte le cas où le trie est vide
    return res/compteur if compteur != 0 else 0

# Prefixe :

def ChercherNoeudPrefixe(A, prefixe="") :
    """
    Cherche et renvoie le noeud marquant la fin du préfixe passé en argument

    Arguments :
        - A (HybridTrie) : Le Trie Hybride à analyser.
        - préfixe (str) : Le mot à vérifier en tant que préfixe.

    Retourne :
        - Noeud (HybridTrie) : le noeud marquant la fin du préfixe.
    """
    global compteurPrefixe
    compteurPrefixe += 1
    if EstVide(A) :
        return None
    elif prefixe == "" :
        return A
    else :
        p = prem(prefixe)
        if p < Racine(A) :
            return ChercherNoeudPrefixe(Inf(A), prefixe)
        elif p > Racine(A) :
            return ChercherNoeudPrefixe(Sup(A), prefixe)
        else :
            nouveauPrefixe = reste(prefixe)
            return ChercherNoeudPrefixe(Eq(A), nouveauPrefixe) if nouveauPrefixe != "" else Eq(A)



def Prefixe(A, mot):
    """
    Calcule le nombre de mots dans le Trie Hybride pour lesquels le mot donné est un préfixe.

    Arguments :
        - A (HybridTrie) : Le Trie Hybride à analyser.
        - mot (str) : Le mot à vérifier en tant que préfixe.

    Retourne :
        - int : Le nombre de mots pour lesquels le mot donné est un préfixe.
                Retourne 0 si aucun mot correspondant n'est trouvé.
    """
    node = ChercherNoeudPrefixe(A, mot)
    if node is not None :
        return len(CreateWord(node, mot))
    else :
        return 0
    
# Suppression :
        
def Suppression(A, mot):
    """
    Supprime le mot du trie hybride si présent, en reconstruisant l'arbre à chaque étape avec TrieH.

    Arguments :
        - A (HybridTrie): Le trie hybride.
        - mot (str): Le mot à supprimer.

    Retourne :
        - HybridTrie: Le nouveau trie après suppression du mot.
    """
    global compteurSuppression
    if EstVide(A) or mot == "" or not lookup(A, mot):
        compteurSuppression += 1
        return A  # Rien à supprimer ou mot vide

    p = prem(mot)
    racine = Racine(A)
    val = Val(A)
    inf = Inf(A)
    eq = Eq(A)
    sup = Sup(A)

    if p < racine:
        compteurSuppression += 5
        new_inf = Suppression(inf, mot)
        if val is None and EstVide(new_inf) and EstVide(eq) and EstVide(sup):
            return TH_Vide()
        else:
            return TrieH(racine, new_inf, eq, sup, val)
    elif p > racine:
        compteurSuppression += 5
        new_sup = Suppression(sup, mot)
        if val is None and EstVide(inf) and EstVide(eq) and EstVide(new_sup):
            return TH_Vide()
        else:
            return TrieH(racine, inf, eq, new_sup, val)
    else:
        # p == racine
        if lgueur(mot) == 1:
            compteurSuppression += 1
            new_val = None
            new_eq = eq
        else:
            new_eq = Suppression(eq, reste(mot))
            new_val = val
        compteurSuppression += 4
        if new_val is None and EstVide(inf) and EstVide(new_eq) and EstVide(sup):
            return TH_Vide()
        else:
            return TrieH(racine, inf, new_eq, sup, new_val)

# Lancer les tests

# Équilibrage 

def LargeurToutNiveau(A) :
    if (EstVide(A)) :
        return 1
    else :
        return 1+max(LargeurToutNiveau(Inf(A)), LargeurToutNiveau(Sup(A)), 1 - LargeurToutNiveau(Eq(A)))

def EstEquilibre(A) :
    """ Trie Hybride -> booléen indiquant si oui (vrai) ou non (faux) le trie hybride est équilibré """
    if EstVide(A) or (EstVide(Inf(A)) and EstVide(Sup(A))):
        return True
    else :
        hauteurInf = Hauteur(Inf(A))
        hauteurSup = Hauteur(Sup(A))

        #print("Racine de l'arbre : ", Racine(A))
        if (abs(hauteurInf - hauteurSup) > 1 ) :
            #print("Passage false : ", Racine(A))
            #afficheTrie(A)
            return False
        else :
            return (EstEquilibre(Inf(A)) and EstEquilibre(Sup(A)) and EstEquilibre(Eq(A)))
        
def RotationDroite(A) :
    """ Trie Hybride -> Trie hybride ayant subis ue rotation droite """
    if EstVide(A) or EstVide(Inf(A)):
        raise ValueError("Impossible de faire une rotation droite : sous-arbre gauche vide.")
    else :
        NouvelRacine = Inf(A)
        nouveauFilsDroit = TrieH(Racine(A), Sup(NouvelRacine), Eq(A), Sup(A), Val(A))
        return TrieH(Racine(NouvelRacine), Inf(NouvelRacine), Eq(NouvelRacine), nouveauFilsDroit, Val(NouvelRacine))
    
def RotationGauche(A) :
    """ Trie Hybride -> Trie hybride ayant subis ue rotation gauche """
    if EstVide(A) or EstVide(Sup(A)):
        raise ValueError("Impossible de faire une rotation gauche : sous-arbre droit vide.")
    else :
        NouvelRacine = Sup(A)
        nouveauFilsGauche = TrieH(Racine(A), Inf(A), Eq(A), Inf(NouvelRacine), Val(A))
        return TrieH(Racine(NouvelRacine), nouveauFilsGauche, Eq(NouvelRacine), Sup(NouvelRacine), Val(NouvelRacine))

def Equilibrage(A):
    if EstVide(A):
        return A

    # Équilibrage récursif des sous-arbres
    A.childInf = Equilibrage(A.childInf)
    A.childEq = Equilibrage(A.childEq)
    A.childSup = Equilibrage(A.childSup)

    # Calcul du facteur d'équilibre
    balance = Hauteur(A.childInf) - Hauteur(A.childSup)

    # Déséquilibre à gauche
    if balance > 1:
        # Sous-arbre gauche plus bas ?
        if Hauteur(A.childInf.childSup) > Hauteur(A.childInf.childInf):
            # Double rotation gauche-droite
            A.childInf = RotationGauche(A.childInf)
            A = RotationDroite(A)
        else:
            # Rotation droite simple
            A = RotationDroite(A)

    # Déséquilibre à droite
    elif balance < -1:
        # Sous-arbre droit penché à gauche ?
        if Hauteur(A.childSup.childInf) > Hauteur(A.childSup.childSup):
            # Double rotation droite-gauche
            A.childSup = RotationDroite(A.childSup)
            A = RotationGauche(A)
        else:
            # Rotation gauche simple
            A = RotationGauche(A)

    return A
    
def Ajout_Equilibrage(mot, A, v) :
    A = TH_Ajout(mot, A, v)
    return Equilibrage(A)

def Ajout_Equilibrage_Mots(s) :
    trie = TH_Vide()
    v = 0
    i = 0
    length = len(s)

    while i < length:
        word, offset = getWord(s[i:])
        if word:
            if not lookup(trie, word):
                trie = Ajout_Equilibrage(word, trie, v)
                #print(word)
                #afficheTrie(trie)
                #assert EstEquilibre(trie), word + " : Pose un problème"
                v += 1
        else:
            # Si aucun mot n'est trouvé, avancer d'un caractère
            offset = 1
        i += offset

    return trie

def motsDansOrdreTrie(node, prefix=""):
    """
    Parcourt le Trie Hybride dans l'ordre correct (Eq -> Inf -> Sup) 
    pour obtenir les mots dans l'ordre d'insertion permettant de recréer 
    la même structure de trie.

    Arguments :
        node (HybridTrie): Le nœud actuel du trie.
        prefix (str): Le mot en cours de construction.

    Retourne :
        list[str]: La liste des mots dans l'ordre d'insertion.
    """
    if node is None or node.value is None:
        return []

    mots = []

    # Ajout du mot courant si le nœud représente une fin de mot
    if node.position is not None:
        mots.append(prefix + node.value)

    # Parcours du sous-arbre égal (milieu) en priorité
    mots += motsDansOrdreTrie(node.childEq, prefix + (node.value if node.value else ""))

    # Parcours du sous-arbre inférieur
    mots += motsDansOrdreTrie(node.childInf, prefix)

    # Parcours du sous-arbre supérieur
    mots += motsDansOrdreTrie(node.childSup, prefix)

    return mots
    

def hybrid_trie_to_dict(A):
    # Si le nœud est vide ou None, on renvoie None.
    if EstVide(A):
        return None

    return {
        "char": Racine(A),
        "is_end_of_word": isinstance(Val(A), int),
        "left": hybrid_trie_to_dict(Inf(A)),
        "middle": hybrid_trie_to_dict(Eq(A)),
        "right": hybrid_trie_to_dict(Sup(A))
    }

def save_to_json_TH(A, filename):
        """
        Sauvegarde l'arbre Patricia-trie dans un fichier JSON.
        """
        # Convertir l'arbre en un dictionnaire JSON-compatible
        tree_dict = hybrid_trie_to_dict(A)

        # Écrire dans un fichier
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(tree_dict, f, indent=4, ensure_ascii=False)
        
        print(f"Trie Hybride sauvegardé dans le fichier {filename}")

# Insérer dans un TH :

def _insert_in_TH_from_file(trie, file_name, compteur = 0):
    """
    Insère des mots dans un trie hybride depuis un fichier texte.
    """
    with open(file_name, "r", encoding="utf-8") as file:
        # Est-ce qu'il faut que je continue de mettre à jour mon compteur à partir de sa dernière valeur ?
        for line in file:
            word = line.strip()
            trie = TH_Ajout(word, trie, compteur) # Est-ce qu'il faut équilibré ici ? On doit juste faire des ajouts sans équilibrage ?
            compteur += 1
    return (trie,compteur)

def insert_words_TH(source):
    """
    Insère des mots depuis un fichier texte ou un dossier contenant des fichiers texte
    dans un Trie hybride, et mesure le temps pris pour l'opération.
    """
    trie = TH_Vide()

    # Mesure du temps de début
    start_time = time.time()

    # Vérifier si la source est un fichier ou un dossier
    if os.path.isfile(source):  # Cas d'un fichier unique
        _insert_in_TH_from_file(trie, source)
    elif os.path.isdir(source):  # Cas d'un dossier contenant plusieurs fichiers
        fichiers_txt = [f for f in os.listdir(source) if f.endswith('.txt')]
        compteur = 0
        for file_name in fichiers_txt:
            full_path = os.path.join(source, file_name)  # Construire le chemin complet
            trie,compteur = _insert_in_TH_from_file(trie, full_path, compteur)
    else:
        raise ValueError(f"{source} n'est ni un fichier ni un dossier valide.")

    # Mesure du temps de fin
    end_time = time.time()
    duration = end_time - start_time

    # Sauvegarder l'arbre dans un fichier JSON
    save_to_json_TH(trie,"trie.json")
    print("Nb de mot dans le trie : ", ComptageMots(trie))
    print(f"Mots insérés depuis {source} et sauvegardés dans trie.json.")
    print(f"Temps total pour insérer les mots : {duration:.2f} secondes.")
    global compteurInsertion
    print("\n \n Nombre totate de comparaisons : ", compteurInsertion)

def dict_to_hybrid_trie(node_dict):
    """
    Reconstruit un Trie Hybride à partir d'un dictionnaire JSON.

    Arguments :
        - node_dict (dict) : Dictionnaire représentant un nœud du Trie Hybride.

    Retourne :
        - HybridTrie : Racine de l'arbre reconstruit.
    """
    if node_dict is None:
        return TH_Vide()

    # Créer le nœud courant
    value=node_dict.get("char", None),
    position=None if not node_dict.get("is_end_of_word", False) else True

    # Construire récursivement les sous-arbres
    Inf = dict_to_hybrid_trie(node_dict.get("left"))
    Eq = dict_to_hybrid_trie(node_dict.get("middle"))
    Sup = dict_to_hybrid_trie(node_dict.get("right"))

    return TrieH(value, Inf, Eq, Sup, position)

def json_to_hybrid_trie(json_file):
    """
    Convertit un fichier JSON représentant un Trie Hybride en objet HybridTrie.

    Arguments :
        - json_file : Chemin du fichier JSON.

    Retourne :
        - L'objet racine du Trie Hybride.
    """
    def dict_to_node(data):
        """
        Fonction récursive pour reconstruire un HybridTrie à partir d'un dictionnaire.
        """
        if not data:
            return TH_Vide()

        # Reconstruction du nœud à partir des données
        value = data.get("char")
        isEndWord = data.get("is_end_of_word", None)
        position = 0 if isEndWord else None
        Inf = dict_to_node(data.get("left"))
        Eq = dict_to_node(data.get("middle"))
        Sup = dict_to_node(data.get("right"))

        return TrieH(value, Inf, Eq, Sup, position)

    # Lecture du fichier JSON
    with open(json_file, "r", encoding="utf-8") as file:
        trie_data = json.load(file)

    # Conversion en HybridTrie
    return dict_to_node(trie_data)

def delete_words_TH(file_name):
    """
        Supprime un mot du Patricia-Trie chargé depuis un fichier JSON
        et sauvegarde le résultat dans un nouveau fichier.
    """
    global compteurSuppression
    try:
        # Charger l'arbre depuis le fichier JSON
        trie = json_to_hybrid_trie("trie.json")        
        # Supprimer le mot
        start = time.time()
        with open(file_name, "r") as file:
            for line in file:
                word = line.strip()
                trie = Suppression(trie, word)

        end = time.time()
        
        # Sauvegarder l'arbre mis à jour
        save_to_json_TH(trie, "trie.json")
        print("Arbre sauvegardé dans 'trie.json'.")
        print("Nombre de mots : ", len(ListeMots(trie)))
        print("Temps passé pour la suppression : ", end-start, " secondes.")
        print("\n \n Nombre totate de comparaison : ", compteurSuppression)
    except FileNotFoundError:
        print("Erreur : Le fichier 'trie.json' est introuvable.")
    except Exception as e:
        print(f"Une erreur s'est produite : {e}")

def list_Mots_TH(filename):

    trie = json_to_hybrid_trie(filename)
    start = time.time()
    lesMots = ListeMots(trie)

    with open("mot.txt", "w", encoding="utf-8") as f:
        for word in lesMots:
            f.write(word + "\n")  # Écrire un mot par ligne
    
    end = time.time()

    print(f"Les mots ont été sauvegardés dans mot.txt.")
    print("Temps de l'opération de listage des mots ", end-start, "secondes")
    print("\n \n Nombre totate de visite de noeuds : ", compteurList)


def profondeurMoyenne_TH(filename) :
    global compteurProfMoyenne
    trie = json_to_hybrid_trie(filename)
    start = time.time()
    with open("profondeur.txt", "w", encoding="utf-8") as f:
        f.write(str(ProfondeurMoyenne(trie))+"\n")
    end = time.time()
    print("La profondeur moyenne a été écrite dans le fichier : profondeur.txt.")
    print("Temps de l'opération : ", end-start)
    print("\n \n Nombre totate de visite de noeuds : ", compteurProfMoyenne)


def prefixe_TH(filename, prefixe) :
    global compteurPrefixe
    trie = json_to_hybrid_trie(filename)
    start = time.time()
    with open("prefixe.txt", "w", encoding="utf-8") as f:
        f.write(str(Prefixe(trie, prefixe))+"\n")
    end = time.time()
    print("Le nombre de mot possèdant le préfixe : ", prefixe, " a été écrit dans le fichier : prefixe.txt.")
    print("Temps de l'opération : ", end-start)

    print("\n \n Nombre totate de visite de noeuds : ", compteurPrefixe)
