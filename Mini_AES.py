
def hex_to_binary(hex_key):
    # Convert hexadecimal string to binary string
    binary_key = bin(int(hex_key, 16))[2:].zfill(16)
    return binary_key

def xor(a, b):
    # Perform bitwise XOR between two binary strings of equal length
    return ''.join(str(int(x) ^ int(y)) for x, y in zip(a, b))

def split_key(k0):
    # Split the 16-bit key into four 4-bit blocks
    w0 = k0[:4]
    w1 = k0[4:8]
    w2 = k0[8:12]
    w3 = k0[12:]
    return w0, w1, w2, w3

def Nibble_Sub(input_block):
    # Define the Nibble_Sub substitution table
    substitution_table = {
        "0000": "1110",
        "0001": "0100",
        "0010": "1101",
        "0011": "0001",
        "0100": "0010",
        "0101": "1111",
        "0110": "1011",
        "0111": "1000",
        "1000": "0011",
        "1001": "1010",
        "1010": "0110",
        "1011": "1100",
        "1100": "0101",
        "1101": "1001",
        "1110": "0000",
        "1111": "0111"
    }
    return substitution_table[input_block]


def generate_round_keys(k0, record_1, record_2):
    # Split the key into four 4-bit blocks
    w0, w1, w2, w3 = split_key(k0)
    
    # Calculate w4
    w4 = xor(xor(w0, Nibble_Sub(w3)), record_1)

    # Calculate w5
    w5 = xor(w1, w4)

    # Calculate w6
    w6 = xor(w2, w5)

    # Calculate w7
    w7 = xor(w3, w6)
    
    # Construct k1 from w4, w5, w6, and w7
    k1 = w4 + w5 + w6 + w7
    
    # Split k1 into four 4-bit blocks
    w4, w5, w6, w7 = split_key(k1)
    
    # Calculate w8
    w8 = xor(xor(w4, Nibble_Sub(w7)), record_2)

    # Calculate w9
    w9 = xor(w5, w8)

    # Calculate w10
    w10 = xor(w6, w9)

    # Calculate w11
    w11 = xor(w7, w10)
    
    # Construct k2 from w8, w9, w10, and w11
    k2 = w8 + w9 + w10 + w11
    
    return k1, k2

def shift_rows(b0, b1, b2, b3):
    c0, c1, c2, c3 = b0, b3, b2, b1
    return c0, c1, c2, c3


def mix_columns(c0, c1, c2, c3):
    # Define the MixColumns matrix
    mix_columns_matrix = [
        ['0011', '0010'],
        ['0010', '0011']
    ]
    # Perform matrix multiplication
    d0 = format(int(c0, 2) ^ int(c1, 2), '04b')
    d1 = format(int(c2, 2) ^ int(c3, 2), '04b')
    d2 = format(int(c0, 2) ^ int(c1, 2), '04b')
    d3 = format(int(c2, 2) ^ int(c3, 2), '04b')
    return d0, d1, d2, d3


def add_round_key(d0, d1, d2, d3, round_key):
    e0 = format(int(d0, 2) ^ int(round_key[0], 2), '04b')
    e1 = format(int(d1, 2) ^ int(round_key[1], 2), '04b')
    e2 = format(int(d2, 2) ^ int(round_key[2], 2), '04b')
    e3 = format(int(d3, 2) ^ int(round_key[3], 2), '04b')
    return e0, e1, e2, e3




def encrypt_message(message_binary, k1, k2):
    # Step 1: Split message into 4-bit blocks
    p0 = message_binary[:4]
    p1 = message_binary[4:8]
    p2 = message_binary[8:12]
    p3 = message_binary[12:]

    # Step 2: SubByte
    b0 = Nibble_Sub(p0)
    b1 = Nibble_Sub(p1)
    b2 = Nibble_Sub(p2)
    b3 = Nibble_Sub(p3)

    # Step 3: ShiftRows
    c0, c1, c2, c3 = shift_rows(b0, b1, b2, b3)

    # Step 4: MixColumns
    d0, d1, d2, d3 = mix_columns(c0, c1, c2, c3)

    # Step 5: AddRoundKey for round 1
    e0, e1, e2, e3 = add_round_key(d0, d1, d2, d3, k1)

    # Display the encrypted message for round 1
    encrypted_message_round_1 = e0 + e1 + e2 + e3
    print("Encrypted message for round 1:", encrypted_message_round_1)

    # Step 6: AddRoundKey for round 2
    f0, f1, f2, f3 = add_round_key(e0, e1, e2, e3, k2)

    # Display the encrypted message for round 2
    encrypted_message_round_2 = f0 + f1 + f2 + f3
    print("Encrypted message for round 2:", encrypted_message_round_2)



# Prompt the user to input k0 and the message
k0_input = input("Enter the value of k0 (in binary or hexadecimal): ")
message_input = input("Enter the 16-bit message (in binary or hexadecimal): ")

# Convert k0 and the message to binary if they are in hexadecimal
if set(k0_input) <= {'0', '1'}:
    k0_binary = k0_input
else:
    # Convert hexadecimal input to binary
    k0_binary = hex_to_binary(k0_input)

if set(message_input) <= {'0', '1'}:
    message_binary = message_input
else:
    # Convert hexadecimal input to binary
    message_binary = hex_to_binary(message_input)

# Example records
record_1 = "0001"
record_2 = "0010"

# Generate k1 and k2 for the given key
k1, k2 = generate_round_keys(k0_binary, record_1, record_2)

print('k1',k1)
print('k2',k2)

# Encrypt the message
encrypt_message(message_binary, k1, k2)

