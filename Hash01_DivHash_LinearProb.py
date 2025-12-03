# Audrey Hall
# COS 266, HW 5: Hash Something Out
# DUE: NOV 25 @ 11:59

# PUBLIC github repo for this assignment: COS226-Hash-Something-Out

# Create two tables:
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

# this method uses a division method for hasing, a little bit combined with a multiplication method for an 'optimized division method'
# but different from a later used multiplication method. Collisions are handled using linear probing where the table is searched through 
# for the next available empty slot for insertion. This causes a lot of clustering.

# use library csv to load in data file
import csv
import time

''' Different Hashing Methods: 
Division Method <--- Used in this version ("optimized" division method)
Multiplication Method
Mid-Square Method
Folding Method
Cryptographic Hash Functions
Universal Hashing
Perfect Hashing
'''

# TODO: readme file with reflection on each method



class DataItem:
    def __init__(self, line):
        self.movieName = str
        self.genre = str
        # self.releaseDate
        self.director = str
        self.revenue = float    # need to handle '$' at beginning
        self.rating = float
        self.minDuration = int
        self.productionComp = str
        self.quote = str
        pass

class HashTable:
    def __init__(self):
        self.Max = 1500
        # self.arr will store the key/value pairs or just the keys
        self.arr = [None for i in range(self.Max)]

# Hash function: get a unicode value of the given key using Optimized Division method
def unicodeFunction(key, tableSize):
    sumChars = 0
    for char in key:
        sumChars += ord(char)
        
    # Using a large prime multiplier helps reduce common factors.
    large_multiplier = 997
    expanded_key = sumChars * large_multiplier

    # mod by the size of the table
    return expanded_key % tableSize


# Function to add a key to a specific hash table array - using linear probing
def add(key, hashTableArr, tableSize):
    startIndex = unicodeFunction(key, tableSize)

    # Statistics tracking
    collisions = 0
    
    # 2. Start probing from the initial index
    # We use a loop to check the current index and subsequent indices
    for i in range(tableSize):
        # Calculate the index using the Linear Probing formula: 
        curIndex = (startIndex + i) % tableSize
        
        # if the slot is empty (None)
        if hashTableArr[curIndex] is None:
            hashTableArr[curIndex] = key   # found empty slot, insert key
            return (True, collisions) # Successful insertion

        # if the slot is occupied by a different key
        elif hashTableArr[curIndex] != key:
            collisions += 1

        # slot is occupied (by the SAME key)
        elif hashTableArr[curIndex] == key:
            # Key already exists, but we still count collisions encountered to find it.
            return (True, collisions)
    
    # 3. If the loop completes, the table is full
    # This shouldn't happen unless the table is 100% full (load factor = 1.0)
    print(f"ERROR: Hash table is full. Could not insert key: '{key}'.")
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
    counter = 0

    with open(file, 'r', newline = '', encoding = "utf8") as csvfile:

        # get number of columns
        for line in csvfile.readlines():
            array = line.split(',')
            first_item = array[0]

        num_columns = len(array)
        csvfile.seek(0)
        
        reader = csv.reader(csvfile)
        included_cols = [0, 8]

        # Skip the header row if your CSV has one (recommended practice)
        next(reader, None)

        # Start timer 
        title_start_time = time.time()
        quote_start_time = time.time()

        for row in reader:
            #print(row)     # prints all of the data in the sheet - just for early testing

            content = list(row[i] for i in included_cols)

            # create a DataItem field into the hash function to get a key
            movieTitle_key = content[0]
            movieQuote_key = content[1]

            # Call the insertion function
                # mod the key value by the hash table length (unicodeFunction - called by add)
                # try to insert DatItem into hash table (add)
                # handle any collisions
            inserted, collision = add(movieTitle_key, hashTable_movieTitle, size)
            inserted02, collision02 = add(movieQuote_key, hashTable_quote, size)
        
            # Update statistics based on the insertion result
            if inserted:
                statsTitles['titleInsertions'] += 1
                statsTitles['titleCollisions'] += collision # Accumulate the extra probes
                title_end_time = time.time()

            if inserted02:
                statsQuotes['quotesInsertions'] += 1
                statsQuotes['quotesCollisions'] += collision02
                quote_end_time = time.time()

    #print(hashTable_movieTitle)    # for testing

    # FINAL STATISTICS CALCULATION
    statsTitles['titleEmptySpace'] = size - statsTitles['titleInsertions']
    statsQuotes['quotesEmptySpace'] = size - statsQuotes['quotesInsertions']

    print(f"\nStatistics tracking attempt 1: Division hash and linear probing")
    
    print("\n--- Hash Table 1 (Movie Titles) Statistics ---")
    print(f"Total Successful Insertions: {statsTitles['titleInsertions']}")   # Not a required statistic, but want to see how many keys are being processed
    print(f"Empty Space Left: {statsTitles['titleEmptySpace']}")
    print(f"Approximate Collisions: {statsTitles['titleCollisions']}")
    print(f"Construction Time: {title_end_time - title_start_time:.4f} seconds") 

    #print(hashTable_quote)     # for testing

    print("\n--- Hash Table 2 (Movie Quotes) Statistics ---")
    print(f"Total Successful Insertions: {statsQuotes['quotesInsertions']}")   # Not a required statistic, but want to see how many keys are being processed
    print(f"Empty Space Left: {statsQuotes['quotesEmptySpace']}")
    print(f"Approximate Collisions: {statsQuotes['quotesCollisions']}")
    print(f"Construction Time: {quote_end_time - quote_start_time:.4f} seconds") 
    
    
if __name__ == "__main__":
    main()
