from translation_table import RNA_CODON_TABLE

def translate(mrna_sequence):
    
    amino_acid = []
    stop_found = False

    counter = 0 # a counter index to find the position where AUG starts
    while counter <= len(mrna_sequence) - 3: # a loop to increment counter 
        if mrna_sequence[counter:counter+3] == "AUG":
            break # exits the loop if condition is true
        else:
            counter += 1 # increments counter and checks for the next 3 letters again
        
    if counter > len(mrna_sequence) - 3: # if "aug" not present in the string it returns nothing
        return amino_acid 

    while counter <= len(mrna_sequence) - 3:
        if mrna_sequence[counter] == "U":  # checks for the the group of lists and creates a variable 'a' to index it
            a = 0
        elif mrna_sequence[counter] == "C":
            a = 1
        elif mrna_sequence[counter] == "A":
            a = 2
        elif mrna_sequence[counter] == "G":
            a = 3
        else:
            return amino_acid
        
        if mrna_sequence[counter+1] == "U": # checks for the the sublistlists and creates a variable 'b' to index it
            b = 0
        elif mrna_sequence[counter+1] == "C":
            b = 1
        elif mrna_sequence[counter+1] == "A":
            b = 2
        elif mrna_sequence[counter+1] == "G":
            b = 3
        else:
            return amino_acid
        
        if mrna_sequence[counter+2] == "U": # checks for the the position in sublist and creates a variable 'c' to index it
            c = 0
        elif mrna_sequence[counter+2] == "C":
            c = 1
        elif mrna_sequence[counter+2] == "A":
            c = 2
        elif mrna_sequence[counter+2] == "G":
            c = 3
        else:
            return amino_acid
        
        append = RNA_CODON_TABLE[a][b][c]
        counter += 3

        if append == "Stop": # breaks the loop if append is "Stop"
            stop_found = True # means there is a "Stop" codon after the "AUG"
            break
        
        amino_acid.append(append)
    
    if not stop_found: # if no stop codon is found after "AUG" an emtpy list should be returned
        return [] 

    return amino_acid

def translate_file(filename):
    
    file = open(filename,'r') # open the file as read
    dna = file.read().upper() # put the string of file into a variable dna
    file.close() # close the file

    mrna = "" # starts an empty string that will be updated with the translation from dna to mrna

    for c in dna: # a loop to go through the entire variable
        if c != 'T': # if c is not t then add it to mrna, if c is t then add u to mrna
            mrna += c
        else:
            mrna += 'U'
    
    amino = translate(mrna)

    print (amino)

if __name__ == "__main__":
    translate_file("sample_short.txt")