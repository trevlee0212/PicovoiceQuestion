from typing import Sequence
# create stucture of the PhonemeMap
class PhonemeMap:
    def __init__(self):
        self.isWord = False
        self.children = {}
        self.word = []

# Assum the pronunciation dictionary will be a list structure in python
# the examples of "pico" and "voice" is made up to test edge case
Dict = ["THEIR DH EH R", "THERE DH EH R", "BOOK B UH K", "PICO P I CO", "VOICE V OY S",  "PICOVOICE P I CO V OY S"] 

def createPhonemeMap(key, list, MapDict, idx):
    # if thaat phoneme has not been created before
    if list[idx] not in MapDict:
        MapDict[list[idx]] = PhonemeMap()
    if idx != len(list)-1:
        createPhonemeMap(key, list, MapDict[list[idx]].children, idx+1)
        return
    # in the last phoneme, we mark there is a word to it and store it in the word list
    else:
        MapDict[list[idx]].isWord = True
        MapDict[list[idx]].word.append(key)
        return

# process each word to put them in the phoneme map
def preprocessDict(dictInput):
    MapDict = {}
    for word in dictInput:
        key, value = word.split(maxsplit=1)
        phoneme_list = value.split()
        idx = 0
        createPhonemeMap(key, phoneme_list, MapDict, idx)
    return MapDict

processedDict = preprocessDict(Dict)

# from the user input of phoneme, we find if such word exit in the phoneme map
def outputWord(dictInput, phonemes, idx, tempList, finalList, endWithWord):
    # if we reach the end of the user input and we end with a word, 
    # we add the word into the final output
    if idx == len(phonemes) and endWithWord:
        finalList.append(tempList[:])
        return
    # if we reach the end of the user input and not end with a word, we simply return
    elif idx == len(phonemes):
        return
    
    if phonemes[idx] in dictInput:
        # if we find there is a word wtih the phoneme we encountered before,
        # we can put it into a temporary list
        if dictInput[phonemes[idx]].isWord:
            for word in dictInput[phonemes[idx]].word:
                tempList.append(word)
                outputWord(processedDict, phonemes, idx+1, tempList, finalList, True)
                tempList.pop()
        # check if there are other words that can be formed by adding more phonemes in
        outputWord(dictInput[phonemes[idx]].children, phonemes, idx+1, tempList, finalList, False)
    
def find_word_combos_with_pronunciation(phonemes: Sequence[str]) -> Sequence[Sequence[str]]:
    idx = 0
    tempList = []
    finalList = []
    outputWord(processedDict, phonemes, idx, tempList, finalList, False)
    return finalList

def main():
    find_word_combos_with_pronunciation(["DH", "EH", "R", "DH", "EH", "R"])

    #edge case: should return [['PICO', 'VOICE'], ['PICOVOICE']]
    find_word_combos_with_pronunciation(["P", "I", "CO", "V", "OY", "S"])

if __name__ == "__main__":
    main()