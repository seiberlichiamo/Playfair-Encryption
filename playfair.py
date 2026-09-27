
# Reference of all letters while combining "I/J" into "I"
alphabet = ['A', 'B', 'C', 'D', 'E',
            'F', 'G', 'H', 'I', 'K',
            'L', 'M', 'N', 'O', 'P',
            'Q', 'R', 'S', 'T', 'U',
            'V', 'W', 'X', 'Y', 'Z']


# Method designed to insert the user's key into a 5x5 grid and fill in remaining space with ordered alphabetical characters.
# Removes duplicate characters from the key when inserting.
# @param - keyword is the key the user previously provided.
# @return - the list of strings comprises the 5x5 matrix needed for Playfair.
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

# ENCRYPT FUNCTION

# DECRYPT FUNCTION


# --- USER INPUT ---
mode = input("Encrypt(e) or Decrypt(d)? ")

while(mode):
    if mode.strip().lower() == 'e':
        print("Encrypt Activated")
        # ENCRYPT FUNCTION
        break
    elif mode.strip().lower() == 'd':
        print("Decrypt Activated")
        # DECRYPT FUNCTION
        break
    else:
        print("Invalid mode inputted.")
        mode = input("Encrypt(e) or Decrypt(d)? ")


key = input("Enter playfair keyword: ")

while(key):
    if key:
        key = key.strip().lower().replace("j", "i")
        print(f"Valid key received: {key}")
        build_playfair_matrix(key)
        break
    else:
        print("Invalid keyword.")
        key = input("Enter playfair keyword: ")
