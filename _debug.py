import sys

search = sys.argv[1]
replace = sys.argv[2]

for line in sys.stdin:
    if search in line:
        print(line.replace(search, replace))
    else:
        print(line)