# COS266-Hash-Something-Out
5 Variations of Hash Functions in python. Using two hash tables from fake movie records data. Table 1 uses the Movie Title as the key and table 2 uses the Movie Quote as the key. Keeping track of wasted space, collisions, and time taken to create each table for each different hash function.


Method 1: Optimized Division Method w/ Linear Probing Collisions

  I tried to stay as simple as possible for this first hash functions. The hashing function is a combination of the division and multiplication methods which is better known as an optimized division method. Collisions are handled with linear probing - if a slot is filled, the next available slot is searched for. The statistics for both tables show that there are 7 empty spaces left in each table. However, if the tables are printed out there are many more shown 'None' values for each. My searching shows that this could be because the next available slot for a key-value is too far away so the loop quits before it can actually find an empty slot to put it into. Which is weird because the statistics also claim that all of the data is successfully entered into the tables, but the 'successful insertion' counter might get called too soon.

  Title Approximate Collisions: 49,992
  Quote Approximate Collisions: 438,023

  Construction Time: 0.0977 seconds (for both tables)


Method 2: Optimized Division Hashing w/ Quadratic Probing
	Same hashing method as before, but quadratic probing results in much less collisions than with linear probing. Faster than linear probing as well. This is better than linear probing, because instead of moving forward individually (or linearly) until an empty slot is found, the quadratic formula is used to find a new possible index. This formula is used until an empty slot is found. Resulting in (hopefully) less probing ultimately occurring, and reducing the amount of clustering that happens in a table. Clustering was a big problem in the first method, resulting in large chunks of the table being filled, and large chunks of empty data. Same amount of None values appear in the title table as Method 1, however the table IS at least organized just slightly differently, showing different indexes are being produced from the different probing method.

  Title Approximate Collisions: 46,336
  Quote Approximate Collisions: 179,751
	
  Title & Quote: 'None' values same amount as method 1. The last run I tried resulted in 3700 'None' values appearing in the Title table for method 1, I think other checks produced slightly less, but not by enough to prove that a solution was found or that those versions simply ran better before changes were made.
	
  Construction Time: 0.0874 seconds
