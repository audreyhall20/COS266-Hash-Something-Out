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


Method 3: Multiplication Hashing w/ Quadratic Probing 
	I chose this combination of methods as my next attempt because quadratic probing resulted in less collisions than linear probing did. The multiplication method also seems to be less sensitive to the overall size of the table than the other hashing method. This method seems to work better when the table size is a power of two. So I changed the table size and this decreased the initial run time from 0.2837 to 0.0927 seconds (Hard to say if some of this was cut down because of running the code twice and things being stored in local memory, but it felt like enough of a difference to justify the extra empty space). Unfortunately this did result in even more 'None' values being found (3822 to be exact) in the final table, even though there should only be approximately 129 (which is successfully tracked in the statistics) because of the additional table size. I did not double check the amount of 'None' values in the quotes table, but I assume there are more than in the previous methods.

	Title Approximate Collisions: 40,184
	Quote Approximate Collisions: 100,673

	Construction Time: 0.0855 seconds


Method 4: Chaining
	Chaining is known as a fairly easy implementation, but I wanted to wait to do it in a later attempt because I wanted to see how other methods ran and I saw it as a little more complex than it really is. I was not expecting the times to be as low. I had a feeling before this that I wasn't properly individually tracking the times for the construction on each table, and after further research, discovered I was correct. So I now believe the construction times for past methods isn't the time for the tables individually (as in they both took the same amount of time to create), but a combined time for both tables. I'm going to have to go back and change this. I was not expecting the collisions to be as low as they were either. There are vastly more 'None' values in this table than in the others (11,244), which I believe is because the table size does not need to be so large here since each index would have a linked list attached to it and not all indexes would be used if items with the same has value are actually going into the same indexed list as opposed to the next index slot. I would likely need to figure out either a better hash size to stick with to reduce empty spots. In my haste to fix the time tracking, I realized I changed how the items within the table are printed (as their address rather than the contents) which doesn't matter unless you choose to uncomment either lines which print the whole tables. It is something I want to edit, but for the sake of submission, will likely get to that later. Instead of completely writing over my files I opted to create new ones, and didn't realize when I created my 4th attempt that I copied from attempt 2 with division hashing instead of attempt 3 with multiplication hashing. I would have rather combined multiplication with chaining. 

	Title Approximate Collisions: 28,458
	Quote Approximate Collisions: 56,049

	Title Construction Time: 0.0451 seconds
	Quote Construction Time: 0.0582 seconds

	Title 'None' values: 11,244


Method 5: Double Hashing
	Double hashing is supposed to take the Unicode value from a string, create a hash value from it, then if a collision occurs the original hash value is hashed a second time with another equation to find the next available slot. This second hash equation is used over and over again until an empty index is found within the table. This is supposed to create more unique hash indexes and cut down on the amount of clustering within a table. Unfortunately, the table hits a max insertion around 14885 and will not insert anymore values because it thinks the table is full, despite the table sizes being set to 15007. As of now, this method results in the 2nd fastest method, but I believe this is more because the table 'fills' and the time stops, not because the table is filled to completion. I will need to figure out why this filling is happening early.
