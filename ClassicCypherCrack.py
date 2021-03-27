
alpha = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

SingleLetterFreq = ['E','T','A','O','I','N','S','H','R','D','L','U']
DoubleFreq = ["ss", "ee", "tt", "ff", "ll", "mm", "oo"]
InitLetterFreq = ["T","O","A","W","B","C","D","S","F","M","R","H","I","Y","E","G","L","N","P","U","J","K"]
FinalLetterFreq = ["E", "S", "T", "D", "N", "R", "Y", "F", "L", "O", "G", "H", "A", "K", "M", "P", "U", "W"]
commonWords = ["the", "be", "of", "and", "a", "to", "in", "he", "have", "it", "that", "for", "they", "I", "with", "as", "not", "on", "she", "at", "by", "this", "we", "you", "do", "but", "from", "or", "which", "one", "would", "all", "will", "there", "say", "who", "make", "when", "can", "more", "if", "no", "man", "out", "other", "so", "what", "time", "up", "go", "about", "than", "into", "could", "state", "only", "new", "year", "some", "take", "come", "these", "know", "see", "use", "get", "like", "then", "first", "any", "work", "now", "may", "such", "give", "over", "think", "most", "even", "find", "day", "also", "after", "way", "many", "must", "look", "before", "great", "back", "through", "long", "where", "much", "should", "well", "people", "down", "own", "just", "because", "good", "each", "those", "feel", "seem", "how", "high", "too", "place", "little", "world", "very", "still", "nation", "hand", "old", "life", "tell", "write", "become", "here", "show", "house", "both", "between", "need", "mean", "call", "develop", "under", "last", "right", "move", "thing", "general", "school", "never", "same", "another", "begin", "while", "number", "part", "turn", "real", "leave", "might", "want", "point", "form", "off", "child", "few", "small", "since", "against", "ask", "late", "home", "interest", "large", "person", "end", "open", "public", "follow", "during", "present", "without", "again", "hold", "govern", "around", "possible", "head", "consider", "word", "program", "problem", "however", "lead", "system", "set", "order", "eye", "plan", "run", "keep", "face", "fact", "group", "play", "stand", "increase", "early", "course", "change", "help", "line"]


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

  return [allLetters, initialLetter, finalLetter, twoLetters, threeLetters], [allWords, oneLetterWords, twoLetterWords, threeLetterWords, fourLetterWords]

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

def twoLetterGuess(guesses):
  for word in twoLetterWords:
    if 'O' in guesses and word[0] == guesses['O']:
      #O*  
      if 'N' in guesses and word[1] == guesses['N'] and 'R' in guesses and word[1] == guesses['R']:
        # not ON, OR, probably OF
        guesses['F'] = word[1]
    elif 'T' in guesses:
      if word[0] == guesses['T']:
        guesses['O'] = word[1]
      elif word[1] == guesses['T']:
        # *T, IT or AT
        if 'I' in guesses and word[0] != guesses['I']:
          guesses['A'] = word[0]
        elif 'A' in guesses and word[0] != guesses['A']:
          guesses['I'] = word[0]
    elif 'I' in guesses and word[0] == guesses['I']:
      # I'M may be mistaken as IS, IN, IT if there is no '  
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


def threeLetterGuess(guesses):
  for word in threeLetterWords:

    # Check if the first letter of the word is also a single letter word itself
    for wordB in oneLetterWords:
      if word[0] == wordB:
        # If the first letter of a word is also a single letter word, it's probably an A
        guesses['A'] = word[0]
        
        # If first letter is probably A and is followed by two of the same letters they are probably L
        if word[1:2] == word[2:3]:
          guesses['L'] = word[-1]

      elif 'A' in guesses and guesses['A'] != wordB:
        # If the first letter of a word is also a single letter word, but it's not also A, it's probably I
        guesses['I'] = wordB

    # Candidate is probably a T 
    if ('T' not in guesses or ('T' in guesses and word[0] == guesses['T'])) and word[-1] == singleLetterCandidates['E']:
      guesses['T'] = word[0]
      guesses['H'] = word[1:2]
      guesses['E'] = word[-1]
    elif 'T' in guesses and word[0] == 'T' and word[1:2] == word[2:3]:
      guesses['O'] = word[-1]

    if 'H' in guesses and word[0] == guesses['H']:
      if 'E' in guesses  and word[1] == guesses['E']:
        guesses['Y'] = word[-1]
      elif 'O' in guesses  and word[1] == guesses['O']:
        guesses['W'] = word[-1]
      elif 'A' in guesses  and word[1] == guesses['A']:
        guesses['S'] = word[-1]
      

  return guesses    

def fourLetterGuess(guesses):
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
        if word[-1] != guesses['E']: 
          guesses['Y'] = word[-1]
        else: 
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

def compareCommonWords(guesses):
  missing = {}
  for word in allWordsSorted:
    # Compare words in the cyper to common words
    for commonWord in commonWords:
      if len(word) == len(commonWord):
        compareWords(word, commonWord.upper(), guesses, missing)
  return missing

def test(guesses, missing, accuraccy):
  for match in missing:
    li = missing[match]
    if len(li) == 0 or len(li) == 1: 
      continue 
    
    # Find the most common matches for the letter
    mostFrequent = ""
    count = 1
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

# Use previously made guesses to make further guesses of words
def makeGuess(guesses):
  guesses = threeLetterGuess(guesses)  
  guesses = fourLetterGuess(guesses)
  guesses = twoLetterGuess(guesses)
  for word in oneLetterWords:
    if 'A' in guesses and word != guesses['A']:
      guesses['I'] = word
    if 'I' in guesses and word != guesses['I']:
      guesses['A'] = word

  return guesses



if __name__ == '__main__':
  plaintext = "The presidency of Donald Trump began at noon EST (17:00 UTC) on January 20, 2017, when Donald Trump was inaugurated as the 45th president of the United States, and ended on January 20, 2021. Trump, a Republican originally from New York City, took office following his surprise Electoral College victory over Democratic nominee Hillary Clinton in the 2016 presidential election, in which he did not win a plurality of the popular vote. Trump made many false or misleading statements during his campaign and presidency. His presidency ended following his defeat in the 2020 presidential election by Democrat Joe Biden.  Trump was unsuccessful in his efforts to repeal the Affordable Care Act (ACA), but rescinded the individual mandate and took measures to hinder the ACA’s functioning. Trump sought substantial spending cuts to major welfare programs, including Medicare and Medicaid. He signed the Great American Outdoors Act, pursued energy independence, reversed numerous environmental regulations, and withdrew from the Paris Accord. He signed criminal justice reform through the First Step Act and appointed three Justices to the U.S. Supreme Court. In economic policy, he partially repealed the Dodd–Frank Act and signed the Tax Cuts and Jobs Act of 2017. He enacted tariffs, triggering retaliatory tariffs from China, Canada, Mexico, and the EU. He withdrew from the Trans-Pacific Partnership negotiations and signed the USMCA, a successor agreement to NAFTA. The federal deficit increased under Trump due to spending increases and tax cuts.  He implemented a controversial family separation policy for migrants apprehended at the U.S.–Mexico border. Trump's demand for the federal funding of a border wall resulted in the longest US government shutdown in history. He deployed federal law enforcement forces in response to protests in 2020. Trump faced the COVID-19 pandemic in his final year. He signed the CARES Act and a second stimulus package in response to the economic impact of the pandemic. Trump's \"America First\" foreign policy was characterized by unilateral actions, disregarding traditional allies. The administration implemented a major arms sale to Saudi Arabia, recognized Jerusalem as the capital of Israel, and denied citizens from several Muslim-majority countries entry into the U.S. His administration withdrew U.S. troops from northern Syria, allowing Turkey to occupy the area. Trump met North Korea's leader, Kim Jong-un, three times. Trump withdrew the U.S. from the Iran nuclear agreement, and later escalated tensions in the Persian Gulf by ordering the assassination of General Qasem Soleimani.  Robert Mueller's Special Counsel investigation (2017–2019) concluded that Russia interfered to favor Trump's candidacy, and that while the prevailing evidence \"did not establish that members of the Trump campaign conspired or coordinated with the Russian government\", possible obstructions of justice occurred during the course of that investigation.  Trump attempted to pressure Ukraine to announce investigations into his political rival Joe Biden, triggering his first impeachment by the House of Representatives in December 2019, but he was acquitted by the Senate.  Following his loss in the 2020 presidential election to Biden, Trump refused to concede and initiated an aggressive pursuit to overturn the results, alleging unproven claims of widespread electoral fraud. On January 6, 2021, during a rally at The Ellipse, Trump urged his supporters to \"fight like hell\" and march to the Capitol, where the electoral votes were being counted by Congress in order to formalize Biden's victory. A mob of Trump supporters stormed the Capitol, suspending the count as Vice President Mike Pence and other members of Congress were evacuated. On January 13, the House voted to impeach Trump an unprecedented second time for \"incitement of insurrection\", but he was again acquitted by the Senate."
  cypher = ""
  for letter in plaintext:
    ul = letter.upper()
    if ul not in alpha: cypher += ul
    else:
      i = alpha.index(ul)
      if i == 25:
        i = -1
      cypher += alpha[i + 1]


  lettersSplit, wordsSplit = splitCypherText(plaintext)
  singleLettersSorted = sortByOccurrences(lettersSplit[0])
  initialLettersSorted = sortByOccurrences(lettersSplit[1])
  finalLettersSorted = sortByOccurrences(lettersSplit[2])
  twoLettersSorted = sortByOccurrences(lettersSplit[3])
  threeLettersSorted = sortByOccurrences(lettersSplit[4])

  allWordsSorted = sortByOccurrences(wordsSplit[0])
  oneLetterWords = sortByOccurrences(wordsSplit[1])
  twoLetterWords = sortByOccurrences(wordsSplit[2])
  threeLetterWords = sortByOccurrences(wordsSplit[3])
  fourLetterWords = sortByOccurrences(wordsSplit[4])

  singleLetterCandidates = getCandidates(singleLettersSorted, SingleLetterFreq)

  guesses = makeGuess({})
  guesses = makeGuess(guesses)
  print(len(guesses))
  print(guesses)

  accuraccy = 1.00
  while accuraccy > 0:
    initLen = len(guesses)
    missing = compareCommonWords(guesses)
    test(guesses, missing, accuraccy)
    if len(guesses) - initLen == 0:
      accuraccy -= .05

  print(guesses)
  print(len(guesses))