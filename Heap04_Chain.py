# Audrey Hall
# COS 266, HW 5: Hash Something Out
# DUE: NOV 25 @ 11:59

# PUBLIC github repo for this assignment: COS226-Hash-Something-Out

# Create two Hash tables:
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

# this method uses chain probing after a hash value is created in order to organize collisions.
# items that have the same hash value get placed at the same index in the hashtable, but new values get added to a linked list attached to the table index
# this currently needs some adjustment in table size to minimize empty space used

# **CANNOT use the random library for this assignment**
import csv      # load in data file
import time     # keep track of build time

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
        self.Max = 1500
        # self.arr will store the key/value pairs or just the keys
        self.arr = [None for i in range(self.Max)]

# Hash function: get a unicode value of the given key TODO: CHANGE? From Div to multiplication? 
def unicodeFunction(key, tableSize):
    sumChars = 0
    for char in key:
        sumChars += ord(char)
        
    # Using a large prime multiplier helps reduce common factors.
    large_multiplier = 997
    expanded_key = sumChars * large_multiplier

    # mod by the size of the table
    return expanded_key % tableSize


# Function to add a key (dataItem) to a specific hash table array - using double hasing for collisions
def addChaining(key, item, hashTableArr, tableSize, hashFunction):
    
    # 1. Get the initial hash index
    index = unicodeFunction(key, tableSize)

    # 2. Check the bucket (the list at that index)
    bucket = hashTableArr[index]
    
    # Collision count for THIS specific key insertion
    collisions = 0
    
    # If the index is empty, initialize it with a list
    if bucket is None:
        hashTableArr[index] = [item]
        # Note: In Chaining, the first item added to a bucket is NOT a collision.
        return (True, 0)
    
    # If the index is occupied (a list exists), iterate through the chain
    # Every item we check in the chain is a COLLISION
    for itemExsit in bucket:
        # Check if the key already exists (Movie Title or Quote)
        # We assume 'key' matches the item's primary attribute for this table
        itemKey = getattr(itemExsit, 'movieName') if key == itemExsit.movieName else getattr(itemExsit, 'quote')
        
        if key == itemKey:
            # Key found. This is typically an update in real-world use.
            # We don't update here, just return the collisions encountered to find it.
            return (True, collisions) 
        
        # If the item is different, it is a collision event (a link in the chain)
        collisions += 1

    # 3. If the loop completes, the key is new. Append the DataItem to the chain/bucket
    bucket.append(item)
    
    return (True, collisions) # Successful insertion

def main():
    # how many 'buckets' aka, size of the hash table
    # using the next largest prime number after 15000 to reduce clustering
    size = 15000

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

        # # get number of columns
        # for line in csvfile.readlines():
        #     array = line.split(',')
        #     first_item = array[0]

        # num_columns = len(array)
        # csvfile.seek(0)
        
        included_cols = [0, 8]

    # Start timer 
    title_startTime = time.time()
    for item in data_rows:
        content = list(row[i] for i in included_cols)

        movieTitle_key = content[0]

        key = item.movieName
        inserted, collisions = addChaining(key, item, hashTable_movieTitle, size, unicodeFunction)
        
        if inserted:
            statsTitles['titleInsertions'] += 1
            statsTitles['titleCollisions'] += collisions
    title_endTime = time.time()


    quote_startTime = time.time()
    for item in data_rows:
        content = list(row[i] for i in included_cols)

        movieQuote_key = content[1]

        key = item.quote
        inserted, collisions = addChaining(key, item, hashTable_quote, size, unicodeFunction)
        
        if inserted:
            statsQuotes['quotesInsertions'] += 1
            statsQuotes['quotesCollisions'] += collisions
    quote_endTime = time.time()

    #print(hashTable_movieTitle)    # for testing

    # FINAL STATISTICS CALCULATION
    statsTitles['titleEmptySpace'] = size - statsTitles['titleInsertions']
    statsQuotes['quotesEmptySpace'] = size - statsQuotes['quotesInsertions']

    print(f"\nStatistics tracking attempt 4: division hashing and chaining")
    
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
