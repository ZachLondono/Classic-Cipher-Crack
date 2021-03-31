
alpha = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

SingleLetterFreq = ['E','T','A','O','I','N','S','H','R','D','L','U']
DoubleFreq = ["ss", "ee", "tt", "ff", "ll", "mm", "oo"]
InitLetterFreq = ["T","O","A","W","B","C","D","S","F","M","R","H","I","Y","E","G","L","N","P","U","J","K"]
FinalLetterFreq = ["E", "S", "T", "D", "N", "R", "Y", "F", "L", "O", "G", "H", "A", "K", "M", "P", "U", "W"]

# Counts instances of an item in an array, returns a unique set of instances ordered from most common to least common
def sortByOccurrences(array):
  # Count occurrences in array
  occurences = {}
  for instance in array:
    upCase = instance.upper()
    if upCase not in occurences: occurences[upCase] = 0
    occurences[upCase] = occurences[upCase] + 1

  # Sort letters by occurence 
  return sorted(occurences, key=occurences.get, reverse=True)
  
# Takes an orderd array of the most common items in the cypher and the most common in english and matches them up
def getCandidates(sorted, frequencies):
  candidates = {}
  for i in range(len(frequencies)):
    if i < len(sorted):
      letter = sorted[i]
      candidates[frequencies[i]] = letter

  return candidates 

# Splits Cyper text into relevant groups of letters/words
def splitCypherText(cypher):

  allWords = cypher.split()
  allWordsClean = []
  for word in allWords:
    clean = True
    for letter in word:
      if letter.upper() not in alpha:
        clean = False
    if clean: allWordsClean.append(word)

  allWords = allWordsClean
  
  cypher = "".join(word + " " for word in allWords)

  allLetters = letters = [c for c in cypher if c != ' ']

  initialLetter = []
  finalLetter = []
  twoLetters = []
  threeLetters = []

  for i in range(len(cypher) - 1):
    a = cypher[i]
    b = cypher[i + 1]
    if a == ' ' and b == ' ':
      twoLetters.append(a + b)

  for i in range(len(cypher) - 2):
    a = cypher[i]
    b = cypher[i + 1]
    c = cypher[i + 2]
    if a == ' ' and b == ' ' and c == ' ':
      twoLetters.append(a + b + c) 

  oneLetterWords = []
  twoLetterWords = []
  threeLetterWords = []
  fourLetterWords = []
  
  # Seperate words into categories for freqency analysis
  for word in allWords:
    if len(word) == 1:
      oneLetterWords.append(word)
    elif len(word) == 2:
      twoLetterWords.append(word)
    elif len(word) == 3:
      threeLetterWords.append(word)
    elif len(word) == 4:
      fourLetterWords.append(word)
    
    initialLetter.append(word[0:1])
    finalLetter.append(word[-1])

  return [sortByOccurrences(allLetters), sortByOccurrences(initialLetter), sortByOccurrences(finalLetter), sortByOccurrences(twoLetters), sortByOccurrences(threeLetters)], [sortByOccurrences(allWords), sortByOccurrences(oneLetterWords), sortByOccurrences(twoLetterWords), sortByOccurrences(threeLetterWords), sortByOccurrences(fourLetterWords)]

def twoLetterGuess(guesses, twoLetterWords):
  for word in twoLetterWords:
    if 'O' in guesses and word[0] == guesses['O']:
      #O*  
      if 'N' in guesses and word[1] == guesses['N'] and 'R' in guesses and word[1] == guesses['R']:
        # not ON, OR, probably OF
        guesses['F'] = word[1]
    elif 'T' in guesses:
      if word[0] == guesses['T'] and 'V' in guesses and word[1] != guesses['V']:
        guesses['O'] = word[1]
      elif word[1] == guesses['T']:
        # *T, IT or AT
        if 'I' in guesses and word[0] != guesses['I']:
          guesses['A'] = word[0]
        elif 'A' in guesses and word[0] != guesses['A']:
          guesses['I'] = word[0]
    elif 'I' in guesses and word[0] == guesses['I']:
      # I'M or I'D may be mistaken as IS, IN, IT if there is no '
      # I*
      if 'S' in guesses and word[1] != guesses['S'] and 'N' in guesses and word[1] != guesses['N']:
        guesses['T'] = word[1]
      elif 'S' in guesses and word[1] != guesses['S'] and 'T' in guesses and word[1] != guesses['T']:
        guesses['N'] = word[1]
      elif 'T' in guesses and word[1] != guesses['T'] and 'N' in guesses and word[1] != guesses['N']:
        guesses['S'] = word[1]
    elif 'E' in guesses and word[1] == guesses['E']:
      if 'M' in guesses and word[0] != guesses['H'] and 'M' in guesses and word[0] != guesses['M'] and 'W' in guesses and word[0] != guesses['W']:
        guesses['B'] = word[0]
      elif 'B' in guesses and word[0] != guesses['B'] and 'M' in guesses and word[0] != guesses['M'] and 'W' in guesses and word[0] != guesses['W']:
        guesses['H'] = word[0]
      elif 'B' in guesses and word[0] != guesses['B'] and 'H' in guesses and word[0] != guesses['H'] and 'W' in guesses and word[0] != guesses['W']:
        guesses['M'] = word[0]
      elif 'B' in guesses and word[0] != guesses['B'] and 'H' in guesses and word[0] != guesses['H'] and 'M' in guesses and word[0] != guesses['M']:
        guesses['W'] = word[0]
      
  return guesses


def threeLetterGuess(guesses, oneLetterWords, threeLetterWords):
  for word in threeLetterWords:

    # Check if the first letter of the word is also a single letter word itself
    for wordB in oneLetterWords:
      if word[0] == wordB:
        # If the first letter of a word is also a single letter word, it's probably an A
        if 'I' in guesses and guesses['I'] != word[0]:
          guesses['A'] = word[0]
        
        # If first letter is probably A and is followed by two of the same letters they are probably L, or P
        # if word[1:2] == word[2:3]:
        #   guesses['L'] = word[-1]

      elif 'A' in guesses and guesses['A'] != wordB:
        # If the first letter of a word is also a single letter word, but it's not also A, it's probably I
        guesses['I'] = wordB

    # Candidate is probably a T 
    if ('T' not in guesses or ('T' in guesses and word[0] == guesses['T'])) and word[-1] == guesses['E']:
      guesses['T'] = word[0]
      guesses['H'] = word[1:2]
      guesses['E'] = word[-1]
    elif 'T' in guesses and word[0] == 'T' and word[1:2] == word[2:3]:
      guesses['O'] = word[-1]

    if 'H' in guesses and word[0] == guesses['H']:
      if 'E' in guesses  and word[1] == guesses['E']:
        if 'R' in guesses and word[-1] != guesses['R']:
          guesses['Y'] = word[-1]
        if 'Y' in guesses and word[-1] != guesses['Y']:
          guesses['R'] = word[-1]
      elif 'O' in guesses  and word[1] == guesses['O']:
        guesses['W'] = word[-1]
      elif 'A' in guesses  and word[1] == guesses['A']:
        if 'S' in guesses and word[-1] != guesses['S']:
          guesses['D'] = word[-1]
        elif 'D' in guesses and word[-1] != guesses['D']:
          guesses['S'] = word[-1]

      

  return guesses    

def fourLetterGuess(guesses, fourLetterWords):
  for word in fourLetterWords:
    if 'T' in guesses and word[0] == guesses['T']:
      # Word starts with T

      if word[0] == word[-1]:
        # T**T
        # Word is probably THAT, another check for A and H if not found in previous tests
        if 'H' in guesses and word[1] == guesses['H']:
            guesses['A'] = word[2]
        elif 'A' in guesses and word[2] == guesses['A']:
            guesses['H'] = word[1]
      else:
        if 'H' in guesses and word[1] == guesses['H']:
          # TH**
          if 'A' in guesses and word[2] == guesses['A']:
            # word is probably THAN
            guesses['N'] = word[-1]
          elif 'E' in guesses and word[2] == guesses['E']:
            # word is probably THEY, THEN, THEM
            if 'Y' in guesses and word[-1] != guesses['Y'] and 'N' in guesses and word[-1] != guesses['N']:
              guesses['M'] = word[-1]
            elif 'Y' in guesses and word[-1] != guesses['Y'] and 'M' in guesses and word[-1] != guesses['M']:
              guesses['N'] = word[-1]
            elif 'M' in guesses and word[-1] != guesses['M'] and 'N' in guesses and word[-1] != guesses['N']:
              guesses['Y'] = word[-1]

    elif 'H' in guesses and word[0] == guesses['H']:
      # Word starts with H
      if 'E' in guesses and word[1] == guesses['E']:
        # HE**
        if word[-1] == guesses['E']:
          # HE*E
          guesses['R'] = word[2]
      elif 'E' in guesses and word[-1] == guesses['E']:
        #H**E
        if word[1] == guesses['A']:
            # HA*E
            guesses['V'] = word[2]
        elif 'O' in guesses  and word[1] == guesses['O']:
          # HO*E
          # Probably HOME, HOSE
          if 'S' in guesses and word[2] != guesses['S']:
            guesses['M'] = word[2]
          elif 'M' in guesses and word[2] != guesses['M']:
            guesses['S'] = word[2]

  return guesses


# Use previously made guesses to make further guesses of words
def guessCommonWords(guesses, wordsSplit):
  guesses = threeLetterGuess(guesses, wordsSplit[1], wordsSplit[3])
  guesses = fourLetterGuess(guesses, wordsSplit[4])
  guesses = twoLetterGuess(guesses, wordsSplit[2])

  for word in wordsSplit[1]:
    if 'A' in guesses and word != guesses['A']:
      guesses['I'] = word
    if 'I' in guesses and word != guesses['I']:
      guesses['A'] = word

  return guesses


def get_key(dictionary, val):
    for key, value in dictionary.items():
        if val == value:
            return key
    return

def compareWords(cypherWord, commonWord, guesses, missing):
  # If most letters match, then add the missing letter to a list of potential replacments
  tempMissing = {} # letters which do not have a guess yet, {CyperLetter, [CommonLetter, ...] }

  matches = 0 # number of letters decoded with guesses that match the common word
  for cypherLetter, commonLetter in zip(cypherWord, commonWord):

    decryptLetter = get_key(guesses, cypherLetter)
    if not not decryptLetter: #key in guesses:
      # There exists a guess for this letter
      if decryptLetter == commonLetter:
        matches += 1 # keeping count of matching letters so we can set a minimum number of letters in the word that must be guessed right
      else:
        # The guess for this letter does not match the common word
        return
    else:
      # There does not yet exist a guess for this letter, it might be the letter in the common word
      if cypherLetter not in tempMissing: tempMissing[cypherLetter] = []
      tempMissing[cypherLetter].append(commonLetter)
  # Every letter in the cypher word had a letter in the guesses that matched up with a common word
  if len(cypherWord) - matches < len(cypherWord) / 2:
    for temp in tempMissing:
      if temp not in missing: missing[temp] = []
      missing[temp] += tempMissing[temp]

def compareCommonWords(guesses, allWordsSorted, commonWords):
  missing = {}
  for word in allWordsSorted:
    # Compare words in the cyper to common words
    for commonWord in commonWords:
      if len(word) == len(commonWord):
        compareWords(word, commonWord.upper(), guesses, missing)

  return missing

def decodeFromWords(guesses, missing, accuraccy):
  for match in missing:
    li = missing[match]
    if len(li) == 0:
      continue

    # Find the most common matches for the letter
    mostFrequent = ""
    count = 0
    for i in range(len(li)):
      currCount = 1
      for j in range(len(li)):
        if i == j: continue
        if li[i] == li[j]:
          currCount += 1
      if currCount > count:
        count = currCount
        mostFrequent = li[i]

    if count/len(missing[match]) < accuraccy:
      mostFrequent = ""
    else:
      if mostFrequent != '' and mostFrequent not in guesses:
        guesses[mostFrequent] = match

def guessRareLetters(guesses, allWords):
  # Find possible Qs
  potentialQ = []
  potentialJ = []
  potentialZ = []
  potentialX = []

  for word in allWords:
    word = word.upper()

    if 'U' in guesses and 'Q' not in guesses:
      for i in range(len(word) - 1):
        letterA = word[i].upper()
        letterB = word[i + 1].upper()
        if letterB == guesses['U']:
          potentialQ.append(letterA)

    if 'Z' not in guesses:
      if 'I' in guesses:
        for i in range(len(word) - 2):
            if 'E' in guesses:
              if word[i] == guesses['I'] and word[i + 2] == guesses['E']:
                potentialZ.append(word[i + 1])
            if 'G' in guesses:
              if word[i + 1] == guesses['I'] and word[i + 2] == guesses['G']:
                potentialZ.append(word[i])

        for i in range(len(word) - 3):
          if 'B' in guesses and 'U' in guesses:
            if word[i] == guesses['B'] and word[i + 1] == guesses['U'] and word[i + 2] == word[i + 3]:
              potentialZ.append(word[i+2])

      if 'C' in guesses and 'R' in guesses and 'A' in guesses:
        for i in range(len(word) - 4):
          if word[i] == guesses['C'] and word[i + 1] == guesses['R'] and word[i + 2] == guesses['A']:
            if 'E' in guesses and word[i + 4] == guesses['E'] or 'Y' in guesses and word[i + 4] == guesses['Y']:
              potentialZ.append(word[i + 3])

    if 'U' in guesses and 'S' in guesses and 'T' in guesses and 'J' not in guesses:
      for i in range(len(word) - 3):
        if word[i + 1] == guesses['U'] and word[i + 2] == guesses['S'] and word[i + 3] == guesses['T']:
          potentialJ.append(word[i])

    if 'X' not in guesses:
      for i in range(len(word) - 2):
        if 'T' in guesses and 'A' in guesses:
          if word[i] == guesses['T'] and word[i + 1] == guesses['A']:
            potentialX.append(word[i + 2])
        if 'M' in guesses and 'A' in guesses:
          if word[i] == guesses['M'] and word[i + 1] == guesses['A']:
            potentialX.append(word[i + 2])
        if 'B' in guesses and 'O' in guesses:
            if word[i] == guesses['B'] and word[i + 1] == 'O':
              potentialX.append(word[i + 2])
      for i in range(len(word) - 3):
        if 'T' in guesses and 'E' in guesses:
          if word[i] == guesses['T'] and word[i + 1] == guesses['E'] and word[-1] == guesses['T']:
            potentialX.append(word[i + 2])

  def removeDup(potentials):
    temp = []
    for candidate in potentials:
      if not get_key(guesses, candidate):
        temp.append(candidate)
    return sortByOccurrences(temp)

  potentialQ = removeDup(potentialQ)
  potentialJ = removeDup(potentialJ)
  potentialZ = removeDup(potentialZ)
  potentialX = removeDup(potentialX)

  potentialQ = [x for x in potentialQ if x not in potentialJ and x not in potentialZ and x not in potentialX]
  potentialJ = [x for x in potentialJ if x not in potentialQ and x not in potentialZ and x not in potentialX]
  potentialZ = [x for x in potentialZ if x not in potentialQ and x not in potentialJ and x not in potentialX]
  potentialX = [x for x in potentialX if x not in potentialQ and x not in potentialJ and x not in potentialZ]

  if len(potentialQ) != 0: guesses['Q'] = potentialQ[0]
  if len(potentialJ) != 0: guesses['J'] = potentialJ[0]
  if len(potentialZ) != 0: guesses['Z'] = potentialZ[0]
  if len(potentialX) != 0: guesses['X'] = potentialX[0]

def decodeKey(cypher):
  lettersSplit, wordsSplit = splitCypherText(cypher)
  dictionary = ""
  try:
    dictionary = open("dictionary_medium.txt", 'r')
    dictionaryWords = dictionary.read()
    commonWords = dictionaryWords.split('\n')
  except Exception as e:
    print("Failed to read dictionary, using smaller word set. Will likely have lower accuracy")
    commonWords = ["the", "be", "of", "and", "a", "to", "in", "he", "have", "it", "that", "for", "they", "I", "with",
                   "as", "not", "on", "she", "at", "by", "this", "we", "you", "do", "but", "from", "or", "which", "one",
                   "would", "all", "will", "there", "say", "who", "make", "when", "can", "more", "if", "no", "man",
                   "out", "other", "so", "what", "time", "up", "go", "about", "than", "into", "could", "state", "only",
                   "new", "year", "some", "take", "come", "these", "know", "see", "use", "get", "like", "then", "first",
                   "any", "work", "now", "may", "such", "give", "over", "think", "most", "even", "find", "day", "also",
                   "after", "way", "many", "must", "look", "before", "great", "back", "through", "long", "where",
                   "much", "should", "well", "people", "down", "own", "just", "because", "good", "each", "those",
                   "feel", "seem", "how", "high", "too", "place", "little", "world", "very", "still", "nation", "hand",
                   "old", "life", "tell", "write", "become", "here", "show", "house", "both", "between", "need", "mean",
                   "call", "develop", "under", "last", "right", "move", "thing", "general", "school", "never", "same",
                   "another", "begin", "while", "number", "part", "turn", "real", "leave", "might", "want", "point",
                   "form", "off", "child", "few", "small", "since", "against", "ask", "late", "home", "interest",
                   "large", "person", "end", "open", "public", "follow", "during", "present", "without", "again",
                   "hold", "govern", "around", "possible", "head", "consider", "word", "program", "problem", "however",
                   "lead", "system", "set", "order", "eye", "plan", "run", "keep", "face", "fact", "group", "play",
                   "stand", "increase", "early", "course", "change", "help", "line"]

  singleLetterCandidates = getCandidates(lettersSplit[0], SingleLetterFreq)
  initalLetterCandidates = getCandidates(lettersSplit[1], InitLetterFreq)
  finalLetterCandidates = getCandidates(lettersSplit[2], FinalLetterFreq)

  # Try to find words in the encrypted text assuming the most common letter is E
  commonWordGuesses = guessCommonWords({'E':singleLetterCandidates['E']}, wordsSplit)

  guesses = commonWordGuesses

  # Using those guesses, try to guess more letters using more common words
  accuraccy = 1.00
  while accuraccy > 0:
    initLen = len(guesses)
    missing = compareCommonWords(guesses, wordsSplit[0], commonWords)
    decodeFromWords(guesses, missing, accuraccy)
    if len(guesses) - initLen == 0:
      accuraccy -= .15

  guessRareLetters(guesses, wordsSplit[0])

  for letter in alpha:
    if letter not in guesses:
      for letterB in alpha:
        if not get_key(guesses,letterB):
          guesses[letter] = letterB

  key = ""
  for letter in alpha:
    key += guesses[letter]

  return key


import sys
import ClassicCypherCrack as crack

if __name__ == '__main__':
	if len(sys.argv) != 2:
		print(f"Invlid arguments\npython3 Usage: {sys.argv[0]} [filepath]")
		exit()

	# Open file which contains encrypted data
	try:
		encryptedFile = open(sys.argv[1], 'r')
	except Exception as e:
		print("Error: failed to open file")
		exit()

	# Read encrypted data
	try:
		encryptedText = encryptedFile.read()
		encryptedFile.close()
	except Exception as e:
		print("Error: failed to read from file")
		print(e)
		exit()

	# Find key from data
	key = crack.decodeKey(encryptedText)

	if not key:
		print("Failed to find valid key")
		exit()

	# Write key to file
	try:
		keyFile = open("key.txt", 'w')
		keyFile.write(str(key))
	except Exception as e:
		print("Failed to write key to file")
		exit()


