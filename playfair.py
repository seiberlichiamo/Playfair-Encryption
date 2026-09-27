# Encryption and decryption system using Playfair
# Accepts input from designated files and sends output to designated files
#
# Authors - Ryan Shaw, Christian Torrazo, & Hayden Seiberlich
# Version - September 27, 2026

# Reference of all letters while combining "I/J" into "I"
alphabet = ['A', 'B', 'C', 'D', 'E',
            'F', 'G', 'H', 'I', 'K',
            'L', 'M', 'N', 'O', 'P',
            'Q', 'R', 'S', 'T', 'U',
            'V', 'W', 'X', 'Y', 'Z']


# Insert keyword into a 5x5 matrix
def build_playfair_matrix(keyword: str) -> list[list[str]]:
    # Init empty matrix, alphabet reference, keyword
    matrix = ['' for _ in range(25)]
    alpha_list = alphabet.copy()
    keyword = list(keyword.upper())
    matrix_index = 0

    # Compares first char of keyword to alphabet, if it has not been used it is added to the playfair matrix
    # Duplicates are ignored, runs until keyword list is empty
    while(keyword):
        if keyword[0] not in matrix:
            matrix.insert(matrix_index, keyword[0])
            matrix.pop()
            alpha_list.remove(keyword[0])
            keyword.remove(keyword[0])
            matrix_index += 1
        else:
            keyword.remove(keyword[0])

    # Cleans and appends the remaining letters to the matrix
    del matrix[matrix_index:]
    matrix.extend(alpha_list)
    # Row list formatting for matrix
    row_size = 5
    matrix = [matrix[i: i + row_size] for i in range(0, len(matrix), row_size)]

    # Clean matrix print to console
    print("\nPlayfair Matrix:")
    for row in matrix:
        print(*row)

    # Returns list of lists
    return matrix


# ENCRYPT FUNCTION(S)
# Finds the position of the desired character in the matrix.
def find_position(matrix, char):
    # Tracks which row a character is in and the index in the row
    for r, row in enumerate(matrix):
        if char in row:
            return r, row.index(char)
    return None


# Build out playfair version of plaintext
def prepare_text(text):
    # Set up text from plaintext file
    text = "".join([c.upper() for c in text if c.isalpha()]).replace('J', 'I')

    # Start with a blank prepared statement
    prepared = ""

    i = 0
    while i < len(text):
        # Loops through to find characters 2 at a time
        # Insert placeholder x if odd number of characters
        char1 = text[i]
        char2 = text[i + 1] if i + 1 < len(text) else 'X'

        # Inserts a placeholder x if a pair of letters are duplicates
        # Adds the 2 letters to the prepared text string
        if char1 == char2:
            prepared += char1 + 'X'
            i += 1
        else:
            prepared += char1 + char2
            i += 2

    # Add x to end of prepared plaintext if necessary (extra precaution)
    if len(prepared) % 2 != 0:
        prepared += 'X'
    return prepared


# Encrypt a single pair of characters
def encrypt_pairs(matrix, p1, p2):
    # Locate row and column value for each character in the matrix
    r1, c1 = find_position(matrix, p1)
    r2, c2 = find_position(matrix, p2)

    # Encryption logic
    if r1 == r2:
        # Assuming same row, increment matrix character by 1 for each and mod 5 to find new place in row
        return matrix[r1][(c1 + 1) % 5] + matrix[r2][(c2 + 1) % 5]
    elif c1 == c2:
        # Assuming same column, increment matrix character by 1 for each and mod 5 to find new place in column
        return matrix[(r1 + 1) % 5][c1] + matrix[(r2 + 1) % 5][c2]
    else:
        # Base case: replace pair with row of first, column of second, and replace with row of second, column of first
        return matrix[r1][c2] + matrix[r2][c1]


# Outputs encrypted text to a new text file in pairs
def output_playfair_encryption(key):
    # Initialize matrix
    matrix = build_playfair_matrix(key)

    # Read supplied file. Hardcoded as the requested file.
    with open("plaintext.txt", 'r', encoding='utf-8') as file:
        raw_text = file.read()

    # Set up plaintext and ciphertext
    plaintext = prepare_text(raw_text)
    ciphertext = ''

    # Iterates through plaintext using established functions
    for i in range(0, len(plaintext), 2):
        ciphertext += encrypt_pairs(matrix, plaintext[i], plaintext[i + 1])

    # Split ciphertext into pairs separated by spaces before writing
    formatted_ciphertext = " ".join(ciphertext[i:i + 2] for i in range(0, len(ciphertext), 2))

    # Output to new file.
    with open("out1.txt", 'w', encoding='utf-8') as file:
        file.write(formatted_ciphertext)


# DECRYPT FUNCTION
def decrypt_message(matrix, char1, char2):
    # Tracks the row/column position of each character in the matrix
    r1, c1 = find_position(matrix, char1)
    r2, c2 = find_position(matrix, char2)

    # Assuming same row, decrement matrix character by 1 for each and mod 5 to find new place in row
    if r1 == r2:
        new_char1 = matrix[r1][(c1 - 1) % 5]
        new_char2 = matrix[r2][(c2 - 1) % 5]

    # Assuming same column, decrement matrix character by 1 for each and mod 5 to find new place in column
    elif c1 == c2:
        new_char1 = matrix[(r1 - 1) % 5][c1]
        new_char2 = matrix[(r2 - 1) % 5][c2]

    # Otherwise, swap the column of each character to find new place
    else:
        new_char1 = matrix[r1][c2]
        new_char2 = matrix[r2][c1]

    return new_char1 + new_char2


def decrypt(matrix, ciphertext):
    # Set up text from ciphertext file
    ciphertext = "".join([c.upper() for c in ciphertext if c.isalpha()]).replace('J', 'I')

    # Start with a blank plaintext string
    plaintext = ""

    i = 0
    while i < len(ciphertext) - 1:
        # Loops through to decrypt characters 2 at a time
        char1 = ciphertext[i]
        char2 = ciphertext[i + 1]

        # Decrypts the message and adds it to the plaintext string
        plaintext += decrypt_message(matrix, char1, char2)
        i += 2

    return plaintext


# Outputs decrypted text to a new text file
def output_playfair_decryption(key):
    # Initialize matrix
    matrix = build_playfair_matrix(key)

    # Read supplied file. Hardcoded as the requested file.
    with open("ciphertext.txt", 'r', encoding='utf-8') as file:
        raw_text = file.read()

    # Set up ciphertext
    ciphertext = "".join([c.upper() for c in raw_text if c.isalpha()]).replace('J', 'I')
    plaintext = ''

    # Iterates through ciphertext using established functions
    for i in range(0, len(ciphertext) - 1, 2):
        plaintext += decrypt_message(matrix, ciphertext[i], ciphertext[i + 1])

    # Output to new file.
    with open("out2.txt", 'w', encoding='utf-8') as file:
        file.write(plaintext)


# --- USER INPUT ---
mode = input("Encrypt(e) or Decrypt(d)? ")

key = input("Enter playfair keyword: ")

while(key):
    if key:
        key = key.strip().lower().replace("j", "i")
        print(f"Valid key received: {key}")
        break
    else:
        print("Invalid keyword.")
        key = input("Enter playfair keyword: ")

while(mode):
    if mode.strip().lower() == 'e':
        print("Encrypt Activated")
        output_playfair_encryption(key)
        break
    elif mode.strip().lower() == 'd':
        print("Decrypt Activated")
        output_playfair_decryption(key)
        break
    else:
        print("Invalid mode inputted.")
        mode = input("Encrypt(e) or Decrypt(d)? ")