from Crypto.Util.number import getPrime
import random
import hashlib
def gcd(a, b):
    if a < b:
        return gcd(b, a)
    elif a % b == 0:
        return b
    else:
        return gcd(b, a % b)

# Exponentiation Modulaire 
def power(a, b, c):
    x = 1
    y = a
 
    while b > 0:
        if b % 2 != 0:
            x = (x * y) % c
        y = (y * y) % c
        b = int(b / 2)
 
    return x % c

def generate_keys():
    # Choisir un grand nombre premier p et deux nombres a et g
    p = getPrime(128)  # Choisir un nombre premier de 128 bits
    g = 13  # Choisir un générateur arbitraire, par exemple, 2

    # Choisir un nombre aléatoire a tel que 1 < a < p
    a = random.randint(5, p - 1)

    # Calculer A = g^a mod p
    A = power(g, a, p)
    
    # Clé publique : (A, g, p), Clé privée : a
    public_key = (A, g, p)
    private_key = a
    print('La clé publique est', public_key)
    print('La clé privée est', private_key)

    return private_key, public_key,g,p

# Chiffrement 
def encrypt(msg):
    en_msg = []
 
    a, (A, _, _),g,p = generate_keys()  # Clé privée pour le chiffrement

    # Choisir un nombre aléatoire b tel que b < a et gcd(b, p - 1) = 1
    b = random.randint(2, a - 1)
    while gcd(b, p - 1) != 1:
        b = random.randint(2, a - 1)

    # Calcul de B = g^b mod p
    B = power(g, b, p)
    
    # Calcul de C = M * A^b mod p
    C = (msg * pow(A,b) )% p
     
    # Message chiffré
    return (B, C)


msg = input('entrez le message en claire')

encrypted_msg = encrypt(msg)
print("Message chiffré:", encrypted_msg)

def decrypt(encrypted_msg):
    B, C = encrypted_msg
    a,_,_,p = generate_keys()   
    # Calcul de M = C * B^(p-a-1) mod p
    M = (C * pow(B, p - a - 1, p)) % p
    
    return M

# Test de la fonction de déchiffrement
decrypted_msg = decrypt(encrypted_msg)
print("Message déchiffré:", decrypted_msg)

 # la signature numerique 
def sign(msg):

    _, _, g, p = generate_keys()  # Clé publique pour la signature
    a, _, _, _ = generate_keys()  # Clé privée pour la signature

    # Choisir un nombre aléatoire k tel que 1 < k < p-1 et gcd(k, p-1) = 1
    k = random.randint(2, p - 2)
    while gcd(k, p - 1) != 1:
        k = random.randint(2, p - 2)

    # Calcul de r = g^k mod p
    r = power(g, k, p)

    # Calcul de s = (msg - a * r) * k^(-1) mod (p-1)
    s = (msg - a * r) * pow(k, -1, p - 1) % (p - 1)

    # Signature : (r, s)
    return (r, s)


def hash_function(msg):
    # Convert the message to bytes (if it's not already)
    msg_bytes = msg.encode('utf-8') if isinstance(msg, str) else msg
    # Calculate the SHA-256 hash of the message
    hash_value = hashlib.sha256(msg_bytes).hexdigest()
    return int(hash_value, 16)  # Convert hexadecimal hash to integer

# Vérification de la signature
def verify(msg, signature):
    A, _, g, p = generate_keys()  # Clé publique pour la vérification
    r, s = sign()

    # Calculate the hash of the message
    h = hash_function(msg)

    # Calcul de v1 = A^r * r^s mod p
    v1 = (power(A, r, p) * pow(r, s, p)) % p

    # Calcul de v2 = g^h mod p
    v2 = pow(g, h, p)

    # La signature est valide si v1 == v2
    return v1 == v2

# Test de la signature numérique
msg_signature = sign(msg)
print("Signature numérique:", msg_signature)

# Vérification de la signature
valid = verify(msg, msg_signature)
print("La signature est valide:", valid)
