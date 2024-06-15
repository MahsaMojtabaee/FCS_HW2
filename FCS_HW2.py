def reshape_list(input_list, rows, columns):

    reshaped_list = [input_list[i * columns:(i + 1) * columns] for i in range(rows)]

    return reshaped_list




def cyclic_left_shift(binary_str, shift):
    bit_length = len(binary_str)
    shift %= bit_length
    shifted_str = binary_str[shift:] + binary_str[:shift]
    return shifted_str

def key_gen(key):

    sub_keys_list = []
    key = convert_hex_to_binary(key)
    while len(sub_keys_list) < 32:
        subkeys = [key[i:i + 32] for i in range(0, len(key), 32)]
        for each in subkeys:
            sub_keys_list.append(each)
            if len(sub_keys_list) == 32:
                break
            key = cyclic_left_shift(key, 25)
    return sub_keys_list



# output is int
def algorithm (plaintext, iteration, key, salt):
    keys = key_gen(key)
    out = plaintext
    int_salt = convert_hex_to_int('0x' + salt[2:].zfill(64))
    for each in range(iteration):
        box_output = box(out, keys)
        out = bin(box_output ^ int_salt)[2:].zfill(64)
    return out


# the output is int
def box(box_input, keys):
    out = box_input
    for i in range(32):
        out = feistel_round(out, keys[i])
    last = int(last_round(out, subkey1=keys[30], subkey2=keys[31]), 2)
    return last


def last_round(my_input, subkey1, subkey2):
    left = my_input[:32]
    right = my_input[32:]
    new_right = bin((int(left, 2) ^ int(subkey1, 2) + int(subkey2, 2)) % 2 ** 32)[2:]
    new_left = bin((int(right, 2) ^ int(subkey2, 2) + int(subkey1, 2)) % 2 ** 32)[2:]
    return new_left.zfill(32) + new_right.zfill(32)


def binary_str_to_bytes(binary_str):
    byte_str = bytes(int(binary_str[i:i + 8], 2) for i in range(0, len(binary_str), 8))
    return byte_str


def binary_str_to_int(binary_str):
    return int(binary_str, 2)


def int_to_binary_str(value, bit_length):
    return bin(value)[2:].zfill(bit_length)


def modular_addition(a, b, mod, bit_length):
    a_int = binary_str_to_int(a)
    b_int = binary_str_to_int(b)
    result = (a_int + b_int) % mod
    return int_to_binary_str(result, bit_length)


def modular_multiplication(a, b, mod, bit_length):
    a_int = binary_str_to_int(a)
    b_int = binary_str_to_int(b)
    result = (a_int * b_int) % mod
    return int_to_binary_str(result, bit_length)


def modular_xor(a, b, mod, bit_length):
    a_int = binary_str_to_int(a)
    b_int = binary_str_to_int(b)
    result = (a_int ^ b_int) % mod
    return int_to_binary_str(result, bit_length)

def convert_hex_to_binary(hex_string):
    integer_value = int(hex_string, 16)
    binary_string = bin(integer_value)[2:]
    return binary_string


def convert_hex_to_int(hex_string):
    integer_value = int(hex_string, 16)
    return integer_value


# inputs are both binary
def feistel_round(plaintext, subkey):
    right = plaintext[32:]
    left = plaintext[:32]
    new_right = left
    my_input = bin((int(left, 2) ^ int(subkey, 2)) % 2**32)[2:].zfill(32)
    new_left = bin(int(my_input, 2) ^ int(right, 2))[2:]

    out = new_left.zfill(32)+new_right
    return out


def call(plaintext, iteration, key, salt):
    original_plaintext = convert_hex_to_binary(plaintext)
    # print(f'length of original plaintext is {len(original_plaintext)}')
    plaintext = '0' * (64 - len(original_plaintext)) + original_plaintext
    # print(f'length of plaintext after padding is {len(plaintext)}')
    print(f'output:\n{hex(int(algorithm(plaintext, iteration, key, salt), 2))}')



plaintext = '0x000000000'
key = '0x701309b2b76e6e2d'
salt = '0x39c6c1e33ec00e2b'
iteration = 1
call(plaintext, iteration=iteration, key=key, salt=salt)
