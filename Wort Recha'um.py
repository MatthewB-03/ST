# Full alphabet
alphabet = "a b c d e f g h i j k l m n o p q r s t u v w x y z".split(" ")

# Letters that aren't covered by the cypher
cypherBanned = ("q","z")

# Single letters that always result in the same sound
unrestricted = (("a","u"),
                ("b","r'"),
                ("c","r"),
                ("d","k"),
                ("e","u"),
                ("f","k"),
                ("g","a'"),
                ("i","e"),
                ("j","r"),
                ("k","r"),
                ("n","m"),
                ("p","ch"),
                ("s","sh"),
                ("t","p"),
                ("v","z"),
                ("w","z"),
                ("x","da"))

# Double letter cyphers
doubles = (("ee","o'"),
           ("ll","s"),
           ("oo","i'"),
           ("ss","'sh"),
           ("th","p'"),
           ("ea","u"))

# Potential decyphers of individual letters
decypherSingles = (("a", ("g", "h", "o"))
                    ,("b", ())
                    ,("c", ())
                    ,("d", ())
                    ,("e", ("i"))
                    ,("f", ())
                    ,("g", ())
                    ,("h", ())
                    ,("i", ("oo", "o"))
                    ,("j", ())
                    ,("k", ("d", "f"))
                    ,("l", ())
                    ,("m", ("n", "r"))
                    ,("n", ())
                    ,("o", ["ee"])  # ["ee"] used, as ("ee") is simplified to "ee"
                    ,("p", ("th", "m", "t"))
                    ,("q", ())
                    ,("r", ("b", "c", "j", "k"))
                    ,("s", ("ll", "l"))
                    ,("t", ())
                    ,("u", ("a", "e", "ea"))
                    ,("v", ())
                    ,("w", ("r", "u"))
                    ,("x", ())
                    ,("y", ())
                    ,("z", ("v", "w")))

# Potential decyphers of letter doubles
decypherDoubles = (("sh", ("ss", "l", "s"))
                   ,("an", ("h"))
                   ,("am", ("m"))
                   ,("ch", ("p"))
                   ,("wa", ("u"))
                   ,("da", ("x", "y"))
                   ,("ee", ("y"))
                   ,("fa", ("y")))
                   
                    
                       
                  

# Get bank of pre-translated words
wordBank = []

wordFile = open("Wordbank.txt","r")
line = wordFile.readline().split(",")
while line != [""] and line != ["\n"]:
    wordBank.append((line[0],line[1].split("\n")[0]))
    line = wordFile.readline().split(",")

wordFile.close()

# Resolves the h character
def resolveH(word, i):

    hew = False
    # Index overflow check
    if (i+2 < len(word)):
        # E.g. hue
        if (word[i+1]+word[i+2] == "ue"):
            hew = True

        # I.e. hu as hew
        elif (word[i+1]+word[i+2] == "ew"):
            hew = True
            
    # Index overflow check
    if (i+3 < len(word)):

        # E.g. human vs hum
        if (word[i+1]+word[i+2]+word[i+3] == "uma"):
            hew = True

    # Return the character associated with the sound
    if (hew):
        return "an"
    else:
        return "a'"

# Resolves the l character
def resolveL(word, i):

    # Not seen any examples of single L becoming 'SH' as of yet
    return "s"
        
# Resolves the m character
def resolveM(word, i):
    # Assuming "mmm" refers to an m that does not start the word
    if (i == 0):
        return "p"
    else:
        return "am"

# Resolves the o character
def resolveO(word, i):

    oh = False

    # E.g. No
    if (i == len(word)-1):
        oh = True

    # Index overflow check
    elif (i+1 < len(word)):

        # E.g. Or is not an "oh" sound
        if (word[i+1] != "r"):

            # E.g. Over
            if (word[i+1] == "v"):

                # Edgecases i.e. Move & cover vs cove
                if (word[i-1] != "m" and not (word[i-1] == "c" and word != "cove")):
                    oh = True

            # E.g. Oh     
            elif (word[i+1] == "h"):
                oh = True

            # E.g. Ok
            elif (word[i+1] == "k"):
                oh = True
                

    # Return the character associated with the sound
    if (oh):
        return "a"
    else:
        return "i"

# Resolves the r character
def resolveR(word, i):

    # Not seen any examples of R becoming 'W' as of yet
    return "m"

# Resolves the u character
def resolveU(word, i):

    # Assuming 'wa for start of word, and w for middle,
    # based on up = 'wa (given sample) and human = anwamum (cleaner than an'waamum)
    if (i == 0):
        return "'wa"
    else:
        return "w"

# Resolves the y character (end of word)
def resolveY(word, i):
    # Input is configured to reject words starting with Y, so out of range check is unnecessary here
    
    # I.e. Day
    if (word[i-1] == "a" or word[i-1] == "e"):
        return "da"

    # I.e. Ahoy
    if (word[i-1] == "o"):
        return "fa"

    # I.e. Tidy, currently also covers other edgecases, e.g. the why 'i' sound
    else:
        return "ee"

# If the current character starts a double, returns the double's cypher text, else returns ""
def tryGetDouble(word, i):

    # Index out of range check
    if (i+1 < len(word)):

        # Check if this character and the next character form a detectable double
        combo = word[i] + word[i+1]
        for double in doubles:

            # If this character and the next form a detected double, return the cypher text
            if combo == double[0]:
                return double[1]
    return ""

# Returns the cyphered version of a word
def cypherWord(word):

    # If word already exists in the word bank, return it
    for i in range(0, len(wordBank)):
        if (wordBank[i][0] == word):
            return wordBank[i][1]

    # Else, construct a new cyphered word
    newWord = ""

    # For each letter in the word
    i = 0
    while (i < len(word)):

        # If letter starts a double, add the double cypher and skip the next letter
        double = tryGetDouble(word, i)
        if (double != ""):
            newWord = newWord + double
            i+=1

        # Else cypher the individual letter
        else:
            char = word[i]

            # Characters that require additional resolution (i.e. different cypher for different sounds)
            if char == "h":
                newWord = newWord + resolveH(word, i)

            elif char == "l":
                newWord = newWord + resolveL(word, i)
                    
            elif char == "m":
                newWord = newWord + resolveM(word, i)
                    
            elif char == "o":
                newWord = newWord + resolveO(word, i)

            elif char == "r":
                newWord = newWord + resolveR(word, i)
                    
            elif char == "u":
                newWord = newWord + resolveU(word, i)
                    
            elif char == "y":
                newWord = newWord + resolveY(word, i)

            # Characters that always result in the same output cypher
            else:
                for alphChar in unrestricted:
                    if (alphChar[0] == char):
                        newWord = newWord + alphChar[1]

        # Next character   
        i+=1

    # Add this word to the word bank
    wordBank.append((word, newWord))
    
    wordFile = open("Wordbank.txt","a")
    wordFile.write(word+","+newWord+"\n")
    wordFile.close()

    # Return the word
    return newWord


# Prints all possible decypherings of this message
def decypherMessage(remainingMessage, currentDecypher = ""):
    # If out of characters, print the possible decypher
    if (remainingMessage == ""):
        print(currentDecypher)
    else:
        # Get the next character to try decypher
        char = remainingMessage[0]

        # Get all possible single cypher letter sources for this character
        singlesToTry = []
        for single in decypherSingles:
            if single[0] == char:
                for source in single[1]:
                    singlesToTry.append(source)

        # Get all possible double letter cypher sources for this + the next character 
        doublesToTry = []
        if (len(remainingMessage) > 1):
            pair = remainingMessage[0] + remainingMessage[1]

            for double in decypherDoubles:
                if (double[0] == pair):
                    for source in double[1]:
                        doublesToTry.append(source)

        if (singlesToTry == []) and (doublesToTry ==[]):
            print(currentDecypher + " | stopped at " + char)

        # Remove current character from the remaining message, try all single sources for this character
        remainingMessage = remainingMessage[1:]
        for source in singlesToTry:
            decypherMessage(remainingMessage, currentDecypher+source)

        # Remove next character from the remaining message, try all double sources for the pair
        if (len(remainingMessage) > 0):
            remainingMessage = remainingMessage[1:]
            for source in doublesToTry:
                decypherMessage(remainingMessage, currentDecypher+source)
            
            
    
            
# Checks if a word can be cyphered
def canBeCyphered(word):

    # This word exists in the word bank (e.g. yes should not be rejected if "yes,wir" is in the wordbank)
    for banked in wordBank:
        if banked[0] == word.lower():
            return True
    
    # Character index
    index = 0

    # For each character in the word
    for char in word.lower():
        # Character cannot be cyphered
        if (char not in alphabet) or (char in cypherBanned):
            print("Characters must be alphabetical, and not q or z")
            return False

        # Letter is a Y
        elif (char == "y"):
            
            # Y is not the last letter of the word
            if (index != len(word)-1):
                print("Y must be the last letter in a word")
                return False

            # Y ("I") has no cypher output, since I'm not sure how many words this applies to, best to display a warning.
            else:
                print("Warning: Word '" + word.lower() + "' ends in the letter Y.")
                print("""Only "A" "ee" and "oy" Y sounds have cypher outputs (e.g. 'away', 'tidy', and 'ahoy'; but not 'by' (by has an "I" sound)).""")
                print("")
                
                # Allow user to decide if cypher should continue
                cont = input("Type Y to continue with cypher:")
                if (cont.lower() != "y"):
                    return False
                else:
                    print("")

        # Update character index
        index+=1

    # If not problems were detected, word is cypherable
    return True

# Checks if a word is valid for decyphering
def canBeDeCyphered(word):
    
    # For each character in the word
    for char in word.lower():
        # Character is not alphabetical
        if (char not in alphabet):
            print("Characters must be alphabetical, please omit any 's")
            return False

    # If not problems were detected, word may be decypherable
    return True

# Command format prompt
def printPrompt():
    print("Type 'cypher word1 word2...' or 'decypher word' then press enter.")

printPrompt()
# Program mainloop
while True:
    print("")

    # Take player input
    plInput = input("Input:").lower().split(" ")
    print("")

    # Input should be in the form of [command] [text]
    if len(plInput) > 1:
        if (plInput[0] == "cypher") or (plInput[0] == "cipher"):

            # Remove command, keep subsequent words
            del plInput[0]

            # Check if all words can be cyphered
            canCypher = True
            for word in plInput:
                if not canBeCyphered(word):
                    canCypher = False
            
            if canCypher:
                # Define output text
                newMessage = ""

                # For each word
                for i in range(0, len(plInput)):
                    
                    # Add spaces between words
                    if (i > 0):
                        newMessage = newMessage + " "

                    # Cypher the word, and add it to the output text   
                    newMessage = newMessage + cypherWord(plInput[i])

                # Output the cyphered text 
                print(newMessage.capitalize())
                
        elif (plInput[0] == "decypher") or (plInput[0] == "decipher"):

            # Decypher next word after command
            if (canBeDeCyphered(plInput[1])):
                decypherMessage(plInput[1])
        else:
            printPrompt()
    else:
        printPrompt()
    print("") 
