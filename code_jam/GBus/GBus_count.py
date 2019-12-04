from StringIO import StringIO
import sys
import codecs
# Simulate the redirect stdin.
if len(sys.argv) > 1:
    filename = sys.argv[1]
    inp = ''.join(open(filename, "r").readlines())
    sys.stdin = StringIO(inp)

output = []
t = int(raw_input())  # read a line with a single integer
for t_id in xrange(1, t + 1):
    nums_bus = int(raw_input())
    # record bus
    bus_rangs = []
    bus_rangs_str = raw_input().split()
    for i in range(0, len(bus_rangs_str), 2):
        a, b = int(bus_rangs_str[i]),  int(bus_rangs_str[i + 1])
        bus_rangs.append((a, b))
    # sort bus rangs
    bus_rangs = sorted(bus_rangs, key=lambda x: x[0])
    # P
    P = int(raw_input())
    total_c = []
    for _ in range(P):
        city = int(raw_input())
        # check in it is inside range
        c = 0
        for r in bus_rangs:
            # out of range
            if city < r[0]:
                break
            if city <= r[1]:
                c += 1
        total_c.append(str(c))
    print "Case #%d: %s" % (t_id, " ".join(total_c))
    output.append("Case #%d: %s" % (t_id, " ".join(total_c)))
    # empty line
    if t_id != t:
        raw_input()

# output
f = codecs.open("output_big", "w")

for line in output:
    f.write(line + "\n")