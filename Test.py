
for a in range(0, 9):
    for b in range(0, 9):
        for c in range(0, 9):
            for d in range(0, 9):
                r1 = a * 1000 + b * 100 + c * 10 + d
                r2 = d * 1000 + c * 100 + b * 10 + a
                if r1 *4 == r2:
                    print(a, b, c, d)
