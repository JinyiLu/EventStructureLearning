import sys
import keyang

for line in sys.stdin:
    print parseOneTweet(line.strip())