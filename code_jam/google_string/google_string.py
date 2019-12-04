from StringIO import StringIO
import sys
import codecs
# Simulate the redirect stdin.
if len(sys.argv) > 1:
    filename = sys.argv[1]
    inp = ''.join(open(filename, "r").readlines())
    sys.stdin = StringIO(inp)


def reverse(text):
    l = ""
    for i in range(len(text) - 1, -1, -1):
        l += text[i]
    return l


def switch(text):
    l = ""
    for i in text:
        if i == '0':
            l += '1'
        else:
            l += '0'
    return l


output = []
t = int(raw_input())  # read a line with a single integer
S = ""
for i in range(15):
    S = S + "0" + switch(reverse(S))

# found 128, 288, 448 repeated
repeat = 432
S = S[:repeat]
# find the digit
for t_id in range(1, t + 1):
    i_th = int(raw_input())
    i_th = (i_th - 1) % repeat
    # i_th -= 1
    print "Case #%d: %s" % (t_id, S[i_th])
# # print "TEST:", S[9]
#
# search repeat
save = ""
BIG_SAVE = []
c = 0
long = 3
for t in range(0, len(S), long):
    # c += 1
    # if t + 3 < len(S) and (c == 4 or c == 8):
    #     print S[t + 3],
    # if c == 8:
    #     print '\n',
    #     c = 0
    #
    four_string = S[t:t+long]
    save += four_string
    c += 1
    if c == 16:
        # one repeat epoach
        c = 0
        if save in BIG_SAVE:
            print "FOUND repeat"
            print save
            print t + long
            # BIG_SAVE = []
        else:
            BIG_SAVE.append(save)
        save = ""

# print '\n',
# print S
# for t_id in xrange(1, t + 1):
#