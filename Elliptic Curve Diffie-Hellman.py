# ECDH algorithm
# Computes the shared secret using elliptic curve Diffie-Hellman
def ECDH(d_A, P_B):

    # Calculate the shared secret by multiplying A's private key with B's public key
    S = d_A * P_B
    
    # Check if the shared secret is the point at infinity (invalid point)
    if S == (0, 0):
        return "ERROR"  # Return error if the shared secret is invalid
    
    return S  # Return the shared secret







# ECDSA Signature

# Implements the Elliptic Curve Digital Signature Algorithm
import random

# Function to compute the modular inverse
def mod_inverse(a, m):
    # Iterate through possible inverses until one is found
    for i in range(1, m):
        if (a * i) % m == 1:
            return i
    return None

# Function to generate ECDSA signature
def ECDSA_Signature(d, m, t, G, P):
    # Generate a random number k between 1 and t-1
    k = random.randint(1, t-1)
    
    # Calculate temporary point Q as k times the generator point G
    Q = k * G
    
    # Calculate r component of the signature
    r = Q[0] % t
    
    # Check if r is zero, if so, regenerate the signature
    if r == 0:
        return ECDSA_Signature(d, m, t, G, P)
    
    # Compute the modular inverse of k
    k_inv = mod_inverse(k, t)
    
    # Calculate s component of the signature
    s = (k_inv * (d*r + m)) % t
    
    # Check if s is zero, if so, regenerate the signature
    if s == 0:
        return ECDSA_Signature(d, m, t, G, P)
    
    return (r, s)  # Return the signature as a tuple (r, s)

# ECDSA Verification
# Verifies the ECDSA signature
def ECDSA_Verification(P, m, r, s, t, G):
    # Compute the modular inverse of s
    s_inv = mod_inverse(s, t)
    
    # Calculate intermediate values U1 and U2
    U1 = (s_inv * m) % t
    U2 = (s_inv * r) % t
    
    # Calculate temporary point Q
    Q = (U1 * G[0] + U2 * P[0], U1 * G[1] + U2 * P[1])
    
    # Calculate V component
    V = Q[0] % t
    
    # Check if V matches r, if so, the signature is valid
    if V == r:
        return True
    else:
        return False

# Example usage
# Define private key and public key for ECDH
d_A = 5
P_B = (10, 15)  # example public key as a tuple (x, y)

# Compute shared secret using ECDH
S = ECDH(d_A, P_B)
print("ECDH Secret Point S:", S)

# Define parameters and keys for ECDSA
d = 7
m = 123
t = 17
G = (2, 22)  # example generator point as a tuple (x, y)
P = (3, 6)   # example public key as a tuple (x, y)

# Generate ECDSA signature
signature = ECDSA_Signature(d, m, t, G, P)
print("ECDSA Signature:", signature)

# Verify ECDSA signature
is_valid = ECDSA_Verification(P, m, signature[0], signature[1], t, G)
print("ECDSA Verification:", is_valid)
