#!/bin/sh
cat sokoban_levels.txt | sed 's/^$/-----/g' | csplit -s -f 'level_' - /-----/ {48}
for i in level_*; do grep -v -e '-----' level_49 > level_49.txt; done
rm level_??
