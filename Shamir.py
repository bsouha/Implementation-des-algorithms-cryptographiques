import random
import hashlib

from sympy import randprime

def generer_cles():
    # Générer deux nombres premiers aléatoires
    p = randprime(100, 200)
    q = randprime(200, 300)

    # Calculer n
    n = p * q

    # Générer une clé privée
    s = random.randint(2, n-1)

    # Calculer v
    v = (s * s) % n

    # Retourner les clés
    return s, v, n

# Fonction pour générer un engagement
def generer_engagement(s, n):
    # Générer un nombre aléatoire
    r = random.randint(2, n-1)

    # Calculer x
    x = (r * r) % n

    # Retourner l'engagement et r
    return x, r

# Fonction pour générer une réponse
def generer_reponse(s, r, e, n): #generer la reponse de alice qui va etre envoye a bob , s sa cle prive, the random r  , le e envoyé par bob et le n calcule au debut
    # Calculer y
    y = (r * pow(s, e)) % n

    # Retourner y qui va etre envoyé à l'autre partie Bob
    return y

def verifier_reponse(y, v, e, x, n):
    # Calculate y^2 mod n and v^e * x mod n
    y_carre_mod_n = (y*y) % n
    v_e_x_mod_n = (pow(v, e, n) * x) % n

    # Verify if they are equal
    return y_carre_mod_n == v_e_x_mod_n

# Générer une paire de clés
s, v, n = generer_cles()

# Générer un engagement
x, r = generer_engagement(s, n)

# Générer un défi aléatoire
e = random.randint(0, 1)

# Générer une réponse
y = generer_reponse(s, r, e, n)

# Vérifier la réponse
resultat = verifier_reponse(y, v, e, x, n)

print("La vérification a réussi ? ", resultat)


	
