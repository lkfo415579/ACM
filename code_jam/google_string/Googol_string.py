from StringIO import StringIO
import sys
import codecs
# Simulate the redirect stdin.
if len(sys.argv) > 1:
    filename = sys.argv[1]
    inp = ''.join(open(filename, "r").readlines())
    sys.stdin = StringIO(inp)


def isone(l, k):
    # in the middle
    if k == l / 2:
        return False
    # left side
    if k < l / 2:
        return isone(l / 2, k)
    else:
        # right side
        return not isone(l / 2, l - k - 1)


# t = int(raw_input())
ith = 9
k = ith - 1
# s(i+1) = l * 2 + 1
l = 0
while l <= k: l = l * 2 + 1
res = isone(l, k)
if res:
    print "1"
else:
    print "0"

