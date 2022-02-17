# main.py
# By Nick Bukovec
# Wordle solving program
from __future__ import print_function, unicode_literals
from typing import Dict, Set, List
import string
from PyInquirer import prompt

def readFile(path: str) -> Set[str]:
  f = open(path)
  return set(line.strip() for line in f)

def toFiveLetters(words: Set[str]) -> Set[str]:
  newWords: Set[str] = set()
  for word in words:
    if len(word) == 5:
      newWords.add(word)
  return newWords

def getWeightedLetters(words: Set[str]) -> Dict[str, float]:
  weightings: Dict[str, float] = {}
  for word in words:
    for char in word:
      if char not in weightings:
        weightings[char] = 0
      weightings[char] += 1
  for char in weightings:
    weightings[char] /= len(words)
  return weightings
  
def getNWeighted(words: Set[str], n: int, weightings: Dict[str, float]) -> List[str]:
  weightDict: Dict[str, int] = {}
  for word in words:
    weight = 0
    for c in ''.join(set(word)):
      weight += weightings[c]
    weightDict[word] = weight
  return sorted(list(words), key = lambda w: weightDict[w], reverse=True)[:n]
    
# Deprecated for custom word weightings.
def getStarterWords(words: Set[str]) -> Set[str]:
  newWords: Set[str] = set()
  for word in words:
    vowelScore = bool(word.count("a")) + bool(word.count("e")) + bool(word.count("i")) + bool(word.count("o")) + bool(word.count("u")) + bool(word.count("y"))
    if vowelScore > 3:
      newWords.add(word)
  return newWords

def promptWithCharLimit(question, tag) -> str:
  answer = prompt(question)[tag]
  if len(answer) == 5:
    return answer
  print("Please enter a five-letter word.")
  return promptWithCharLimit(question, tag)


def main():
  print("Initializing dictionary...")
  dictionary = toFiveLetters(readFile("words_alpha.txt"))
  weightings = getWeightedLetters(dictionary)
  print("Wordless Started.")
  print("Here are some words to get you started:")
  for word in getNWeighted(dictionary, 20, weightings):
    print(word, end="\t")
  print() # Flush stdout
  wordFound = False
  turnNumber = 1
  letterMap = {}
  # 0 = not known
  # 1 = grey
  # 2 = yellow
  # 3 = green
  for c in string.ascii_lowercase:
    letterMap[c] = 0
  while not wordFound and turnNumber < 7:
    message = 'Enter word #' + str(turnNumber)
    question = [{
        'type': 'input',
        'name': 'word',
        'message': message,
    }]
    currentWord = promptWithCharLimit(question, 'word')
    for c, i in zip(currentWord, range(len(currentWord))):
      message = 'Enter the color of ' + c
      question = [{
        'type': 'list',
        'name': 'status',
        'message': message,
        'choices': [
          'Grey', 'Yellow', 'Green'
        ]
      }]
      color = prompt(question)['status']
      toRemove = set()
      if color == 'Grey' and letterMap[c] == 0:
        letterMap[c] = 1
        for word in dictionary:
          if word.count(c):
            toRemove.add(word)
        dictionary.difference_update(toRemove)
        weightings[c] = 0
      elif color == 'Yellow':
        letterMap[c] = 2
        for word in dictionary:
          if word[i] == c or not word.count(c):
            toRemove.add(word)
        dictionary.difference_update(toRemove)
        weightings[c] = 0
      elif color == 'Green' and letterMap[c] != 3:
        letterMap[c] = 3
        for word in dictionary:
          if word[i] != c:
            toRemove.add(word)
        dictionary.difference_update(toRemove)
        weightings[c] = 0
    question = [{
      'type': 'confirm',
      'name': 'correct',
      'message': "Was this the correct word?",
      'default': False,
    }]
    wordFound = prompt(question)['correct']
    if not wordFound:
      weighted_output = getNWeighted(dictionary, 20, weightings)
      for word in weighted_output:
        print(word, end="\t")
      print()
    turnNumber += 1

  
if __name__ == "__main__":
  main()


