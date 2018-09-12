### Cache_project

Direct and Set Associative Cache Implementation without Cache straddling.
Each time the instruction address is read, the address accesses the cache for hit/miss:
Hit:  the clock cycle is increment by 1
Miss: the clock cycle is increment by 15. 

Replacement Policy : For Direct Cache - replace cache line.
                     For Set-Associative - If all ways are valid, then select the way base on (clock_cycle % way_associative).

## Configurations
Cache size: 1K, 2K, 4K, 8K, 16K, 32K-Byte
Way associative: 1, 2, 4, 8-way
Cache line size (block size): 2, 4, 8, 16, 32, 64-byte

## Output
-	Total number of cache accesses
-	Total number of hits
-	Calculate hit ratio
-	Total number of clock cycles
-	Calculate instruction-per-cycle (IPC) = total instruction fetched/total cycles

Graph of y=hit ratio, x=cache sizes
-	Fixed cache line size = 8, 4 graphs for way associative
-	Fixed way associative = 1, 6 graphs for cache line size
-	Fixed way associative = 4, 6 graphs for cache line size
Repeat the graph with y=IPC

