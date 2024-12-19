
import random
import math
from sympy import randprime, mod_inverse

message = int(input('entrez le message en clair : '))

# choisir des nombres aleatoires

p = randprime(1, 100)
q = randprime(1, 100)

def generate_keypair(p, q):
    n = p * q
    phi = (p-1) * (q-1)

    #Choisir une valeur aleatoire de e inferieur a phi
    e = random.randrange(1, phi)

#  verifier que le pgcd de e et phi egale a  1
    g = math.gcd(e, phi)
    while g != 1:
        e = random.randrange(1, phi)
        g = math.gcd(e, phi) 


    # gener le nombre d en utilisant the extended euclidean algorithm  
        
    d = mod_inverse(e, phi)


    # verifier que d est entre 1 et phi 
    assert 1 < d < phi
    # verifier que le produit de (e , d ) mod phi egale a 1 

    assert (d * e) % phi == 1

    return ((e, n), (d, n))

# affichage des valeurs

print(" p = " ,p)


print(" q =  " , q)

public_key, private_key = generate_keypair(p, q)

print(" The public key is :  " , public_key , "The private key is : " , private_key)




def encrypt(message, public_key):
    n, e = public_key
    # Ensure message is within the interval [0, n-1]
    if message < 0 or message >= n:
        raise ValueError("Message is not within the interval [0, n-1]")
    # Compute ciphertext
    ciphertext = pow(message, e) % n
    return ciphertext



ciphertext = encrypt(message, public_key)
print("Ciphertext:", ciphertext)

def decrypt(ciphertext, private_key):
    d, n = private_key
    plaintext = pow(ciphertext, d) % n
    return plaintext

private_key = private_key
recovered_message = decrypt(ciphertext, private_key)
print("Recovered message: " ,recovered_message)