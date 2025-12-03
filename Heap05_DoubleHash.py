# Audrey Hall
# COS 266, HW 5: Hash Something Out
# DUE: NOV 25 @ 11:59

# PUBLIC github repo for this assignment: COS226-Hash-Something-Out

# Create two hash tables:
# Need table size of at least 1500, load in from MOCK_DATA.csv (fake movie data)
#   Table 1: Movie Title as key 
#   Table 2: Movie Quote as key

# Statistics tracking:
# Display these statistics after constructing each hash table so you can compare the performance of different hash function implementations.
#   - how many things collide 
#   - how much empty space is left
#   - Amount of time it takes to construct table

# Optimization Goals: 
#   Minimize wasted space: Design your hash table size and hash function to use space efficiently
#   Minimize collisions: Design your hash function to distribute keys evenly across the hash table buckets

# This HashTable uses Double Hasing. Similar to linear probing, but instead of probing for the next availably slot linearly,
# the new index is created (hashed) from the original hash value using a specific formula 

# use library csv to load in data file
import csv
import time

class DataItem:
    def __init__(self, line):
        self.movieName = line[0]
        self.genre = line[1]
        self.releaseDate = line[2]
        self.director = line[3]
        self.revenue = self.parseRevenue(line[4])    # need to handle '$' at beginning
        self.rating = float(line[5]) if line[5] else 0.0
        self.minDuration = int(line[6]) if line[6] else 0
        self.productionComp = line[7]
        self.quote = line[8]

    # Helper to clean revenue data
    def parseRevenue(self, rev_str):
        if rev_str.startswith('$'):
            rev_str = rev_str.replace('$', '')
        try:
            return float(rev_str)
        except ValueError:
            return 0.0

class HashTable:
    def __init__(self):
        self.Max = 15007
        # self.arr will store the key/value pairs or just the keys
        self.arr = [None for i in range(self.Max)]

# Hash function: get a unicode value of the given key
def unicodeHash(key, tableSize):
    sumChars = 0
    for char in key:
        sumChars += ord(char)
        
    # Using a large prime multiplier helps reduce common factors.
    large_multiplier = 997
    expanded_key = sumChars * large_multiplier

    # mod by the size of the table
    return expanded_key % tableSize

# Hash Function 2: Used for the STEP SIZE in Double Hashing
# R = largest prime less than M=15007 (R=15001)
def secondaryHash(key, R=15001):
    # 1. Convert key to a large integer k (using the unicode sum)
    k = 0
    for char in key:
        k += ord(char)
        
    # Apply the formula h2(k) = R - (k mod R)
    return R - (k % R)


# Function to add a key using DOUBLE HASHING
def addDoubleHash(key, item, hashTableArr, tableSize, hashFunction1, hashFunction2):
    
    startIndex = unicodeHash(key, tableSize)
    stepSize = secondaryHash(key)
    collisions = 0
    
    for i in range(tableSize):
        # Double Hashing formula: curIndex = (h1(k) + i * h2(k)) % M
        curIndex = (startIndex + i * stepSize) % tableSize

        # if slot is Empty (Successful Insertion)
        if hashTableArr[curIndex] is None:
            hashTableArr[curIndex] = item # Insert the DataItem
            return (True, collisions) 

        # if slot is occupied (by a different item) - collision occurs
        elif hashTableArr[curIndex] != item:
            collisions += 1

        # if slot is cccupied (by the SAME key)

        # NOTE: need a way to check equality without comparing the whole DataItem object
        # need to compare item.movieName or item.quote with the existing item's key attribute
        # For simplicity here, assume if the objects are identical (unlikely with DataItem), we stop.
        elif hashTableArr[curIndex] == item:
            return (True, collisions) 
    
    # If the loop completes, insertion failed 
    print(f"ERROR: Hash table is full (Double Hashing Limit Hit). Could not insert key: '{key}'.")
    return (False, tableSize)

def main():
    # how many 'buckets' aka, size of the hash table
    # using the next largest prime number after 15000 to reduce clustering
    size = 15007

    hashTable_movieTitle = [None] * size
    hashTable_quote = [None] * size

    # Statistics Dictionaries
    statsTitles = {
        'titleInsertions': 0,
        'titleCollisions': 0,
        'titleEmptySpace': size
    }

    statsQuotes = {
        'quotesInsertions': 0,
        'quotesCollisions': 0,
        'quotesEmptySpace': size
    }

    file = "MOCK_DATA.csv"
    data_rows = []

    with open(file, 'r', newline = '', encoding = "utf8") as csvfile:

        reader = csv.reader(csvfile)
        # Skip the header row (recommended practice)
        next(reader, None)

        for row in reader:
             # Create DataItem instance now; we'll use it for both tables
             try:
                data_rows.append(DataItem(row))
             except IndexError:
                # Handle incomplete rows if necessary
                pass
        
        included_cols = [0, 8]

    # Start timer 
    title_startTime = time.time()
    for item in data_rows:
        content = list(row[i] for i in included_cols)
        movieTitle_key = content[0]

        key = item.movieName
        insertedTitle, collisionsTitle = addDoubleHash(
            key, item, hashTable_movieTitle, size, unicodeHash, secondaryHash)
        
        if insertedTitle:
            statsTitles['titleInsertions'] += 1
            statsTitles['titleCollisions'] += collisionsTitle
    title_endTime = time.time()


    quote_startTime = time.time()
    for item in data_rows:
        content = list(row[i] for i in included_cols)
        movieQuote_key = content[1]

        key = item.quote
        insertedQuote, collisionsQuote = addDoubleHash(
            key, item, hashTable_quote, size, unicodeHash, secondaryHash)
        
        if insertedQuote:
            statsQuotes['quotesInsertions'] += 1
            statsQuotes['quotesCollisions'] += collisionsQuote
    quote_endTime = time.time()

    #print(hashTable_movieTitle)    # for testing

    # FINAL STATISTICS CALCULATION
    statsTitles['titleEmptySpace'] = size - statsTitles['titleInsertions']
    statsQuotes['quotesEmptySpace'] = size - statsQuotes['quotesInsertions']

    print(f"\nStatistics tracking attempt 5: double hashing")
    
    print("\n--- Hash Table 1 (Movie Titles) Statistics ---")
    print(f"Total Successful Insertions: {statsTitles['titleInsertions']}")   # Not a required statistic, but want to see how many keys are being processed
    print(f"Empty Space Left: {statsTitles['titleEmptySpace']}")
    print(f"Approximate Collisions: {statsTitles['titleCollisions']}")
    print(f"Construction Time: {title_endTime - title_startTime:.4f} seconds") 

    #print(hashTable_quote)     # for testing

    print("\n--- Hash Table 2 (Movie Quotes) Statistics ---")
    print(f"Total Successful Insertions: {statsQuotes['quotesInsertions']}")   # Not a required statistic, but want to see how many keys are being processed
    print(f"Empty Space Left: {statsQuotes['quotesEmptySpace']}")
    print(f"Approximate Collisions: {statsQuotes['quotesCollisions']}")
    print(f"Construction Time: {quote_endTime - quote_startTime:.4f} seconds") 
    
    
if __name__ == "__main__":
    main()
