#keys generation
# Permutation box P10
P10 = [3, 5, 2, 7, 4, 10, 1, 9, 8, 6]

# Permutation box P8
P8 = [6, 3, 7, 4, 8, 5, 10, 9]

def permute(key, permutation_box):
    permuted_key = [key[i - 1] for i in permutation_box]
    return ''.join(permuted_key)

def left_circular_shift(bits):
    return bits[1:] + bits[0]

def generate_keys(K0):
    # Apply P10 permutation
    K0_permuted = permute(K0, P10)
    
    # Split K0 into two parts
    L0 = K0_permuted[:5]
    R0 = K0_permuted[5:]
    
    # Left circular shift on L0 and R0 for K1
    L1 = left_circular_shift(L0)
    R1 = left_circular_shift(R0)
    
    # Concatenate L1 and R1 for K1
    result1 = L1 + R1
    
    # Apply P8 permutation to get K1
    K1 = permute(result1, P8)
    
    # Left circular shift on L1 and R1 by 2 bits for K2
    L2 = left_circular_shift(left_circular_shift(L1))
    R2 = left_circular_shift(left_circular_shift(R1))
    
    # Concatenate L2 and R2 for K2
    result2 = L2 + R2
    
    # Apply P8 permutation to get K2
    K2 = permute(result2, P8)
    
    return K1, K2   


# encryption

PI = [2, 6, 3, 1, 4, 8, 5, 7]

def initial_permutation(text):
    return permute(text, PI)


EP = [4, 1, 2, 3]

S0 = [
    ['01', '00', '11', '10'],
    ['11', '10', '01', '00'],
    ['00', '10', '01', '11'],
    ['11', '01', '00', '10']
]

S1 = [
    ['00', '10', '10', '11'],
    ['10', '00', '01', '11'],
    ['11', '00', '01', '00'],
    ['10', '01', '00', '11']
]

P4 = [2, 4, 3, 1]

def xor(a, b):
    # Perform bitwise XOR between two binary strings of equal length
    return ''.join(str(int(x) ^ int(y)) for x, y in zip(a, b))


def s_box(bits, sbox):
    row = int(bits[0] + bits[3],2)
    col = int(bits[1]+ bits[2], 2)
    return sbox[row][col]

def f(R0, K1):
    # Expand R0 using EP
    expanded_R0 = permute(R0, EP)
    # XOR with K1
    xor_result = xor(expanded_R0, K1)
    # Split the result into two 4-bit halves
    left_half = xor_result[:4]
    right_half = xor_result[4:]
    print("Left half:", left_half)
    print("Right half:", right_half)  # Add this line for debugging
    # Apply S-boxes
    s0_result = s_box(left_half, S0)
    s1_result = s_box(right_half, S1)
    # Concatenate the results
    concatenated_result = s0_result + s1_result
    # Apply permutation P4
    permuted_result = permute(concatenated_result, P4)
    return permuted_result

def swap_and_permute(R0, R1):
    return R1 + R0

K1 = input("Enter the 8-bit key K1: ")
K2 = input("Enter the 8-bit key K2: ")

def f_with_k2(R0, K2):
    return f(R0, K2)


def swap_and_permute_final(R2, R1):
    return R2 + R1


IP_1 = [4, 1, 3, 5, 7, 2, 8, 6]

def final_permutation(text):
    return permute(text, IP_1)


def encrypt(plaintext, K1, K2):
    # Initial permutation
    permuted_text = initial_permutation(plaintext)
    # Split into L0 and R0
    L0 = permuted_text[:4]
    R0 = permuted_text[4:]
    # Round 1
    R1 = f(R0, K1)
    # Swap and permute
    swapped_text = swap_and_permute(R0, R1)
    # Round 2
    R2 = f_with_k2(swapped_text[:4], K2)
    # Swap and permute final
    final_text = swap_and_permute_final(R2, swapped_text[4:])
    # Final permutation
    encrypted_text = final_permutation(final_text)
    return encrypted_text

# Take input for K0
K0 = input("Enter the 10-bit key K0: ")

# Generate K1 and K2
K1, K2 = generate_keys(K0)

plaintext = input("Enter the plaintext (8 bits): ")


# Encrypt and print the result
print("K1:", K1)
print("K2:", K2)
encrypted_text = encrypt(plaintext, K1, K2)
print("Encrypted text:", encrypted_text)