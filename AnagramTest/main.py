from collections import Counter
#check if two words are anagram
#Exammple 

#find_anagram("hello", "check") False
#find_anagram("below", "elbow") True

def find_anagram(word, anagram):
    # [assignment] Add your code here
    # if sorted(word) == sorted(anagram):
    if Counter(word) == Counter(anagram):  
        return True
    else:
        return False
        
print(find_anagram("hello", "check"))
print(find_anagram("below", "elbow")) 

