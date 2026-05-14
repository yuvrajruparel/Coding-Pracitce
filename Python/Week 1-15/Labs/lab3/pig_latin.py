def translate_pig_latin(phrase):
    vowels = "aeiou"
    first_letter = None
    answer = ""
    word_starts_with_vowel = False  # to track if current word starts with a vowel
    
    for c in phrase:
        if first_letter is None:
            first_letter = c
            word_starts_with_vowel = c in vowels
            if word_starts_with_vowel:
                answer = answer + c  # start word normally
        elif c == " ":
            if word_starts_with_vowel:
                answer = answer + "-yay "
            else:
                answer = answer + "-" + first_letter + "ay "
            first_letter = None
        else:
            answer = answer + c

    # Finish last word
    if first_letter is not None:
        if word_starts_with_vowel:
            answer = answer + "-yay"
        else:
            answer = answer + "-" + first_letter + "ay"

    return answer