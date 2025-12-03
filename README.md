# COS266-Hash-Something-Out
5 Variations of Hash Functions in python. Using two hash tables from fake movie records data. Table 1 uses the Movie Title as the key and table 2 uses the Movie Quote as the key. Keeping track of wasted space, collisions, and time taken to create each table for each different hash function.


Method 1: Optimized Division Method w/ Linear Probing Collisions

  I tried to stay as simple as possible for this first hash functions. The hashing function is a combination of the division and multiplication methods which is better known as an optimized division method. Collisions are handled with linear probing - if a slot is filled, the next available slot is searched for. The statistics for both tables show that there are 7 empty spaces left in each table. However, if the tables are printed out there are many more shown 'None' values for each. My searching shows that this could be because the next available slot for a key-value is too far away so the loop quits before it can actually find an empty slot to put it into. Which is weird because the statistics also claim that all of the data is successfully entered into the tables, but the 'successful insertion' counter might get called too soon.

  Title Approximate Collisions: 49,992
  Quote Approximate Collisions: 438,023

  Construction Time: 0.0977 seconds (for both tables)
