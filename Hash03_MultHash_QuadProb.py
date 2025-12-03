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

# this method uses multiplier hash function with quadratic probing to minimize clustering that linear probing causes. Multiplication hashing 
# also 

# use library csv to load in data file
import csv
import time

''' Different Hashing Methods: 
Division Method 
Multiplication Method <--- Used in this version
Mid-Square Method
Folding Method
Cryptographic Hash Functions
Universal Hashing
Perfect Hashing
'''

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
    def __init__(self, size):
        self.size = size
        # self.arr will store the key/value pairs or just the keys
        self.table = [None for i in range(self.Max)]

# Hash function: get a unicode value of the given key using the Multiplication method
def multiplicationHash(key, tableSize):
    A = 0.6180339887    # constant based on the golden ratio 
    sumChars = 0
    for char in key:
        sumChars += ord(char)
       
    # 1. Multiply the key by the constant A
    product = sumChars * A

    # 2. Take the fractional part of the product
    fractional_part = product - int(product) # or product % 1 if using floats

    # 3. Scale the fractional part by the table size and take the floor
    hash_index = int(tableSize * fractional_part)

    return hash_index


# Function to add a key to a hash table array - Using Quadratic (aka Double) probing
def add_quadraticProbing(key, hashTableArr, tableSize):
    # Use the (optimized) unicodeFunction to get the initial hash index
    startIndex = multiplicationHash(key, tableSize)
    collisions = 0 

    for i in range(tableSize):
        # Calculate the index using the QUADRATIC PROBING formula: 
        # index = (start_index + i^2) % tableSize
        curIndex = (startIndex + i*i) % tableSize

        # if slot is emoty
        if hashTableArr[curIndex] is None:
            hashTableArr[curIndex] = key 
            
            # Return True and the total collisions encountered during this search
            return (True, collisions) 

        # if slot has different key - A COLLISION OCCURS
        # check if it's not the same key to count it as a collision *with another item*
        elif hashTableArr[curIndex] != key:
            # We found a different key, meaning the current key collided here.
            collisions += 1
            # Continue probing to find an empty slot

        # if slot is occupied by same key - Key Already Exists
        elif hashTableArr[curIndex] == key:
            # we stop, but still report the collisions 
            # encountered *to find it* (if any).
            return (True, collisions)
    
    # Still fails if table is truly full or secondary clustering becomes bad
    print(f"ERROR: Hash table is full (Quadratic Probing Limit Hit). Could not insert key: '{key}'.")
    return (False, tableSize)

def main():
    # how many 'buckets' aka, size of the hash table
    # using the next largest prime number after 15000 to reduce clustering
    size = 15129

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
            inserted, collision = add_quadraticProbing(movieTitle_key, hashTable_movieTitle, size)
            inserted02, collision02 = add_quadraticProbing(movieQuote_key, hashTable_quote, size)
        
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

    print(f"\nStatistics tracking attempt 3: multiplication hash and quadratic probing")

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
