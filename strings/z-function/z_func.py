def z_function(a):
    z = [0 for x in range(len(a))]
    if len(set(a)) == 1:
        z = [x for x in range(len(a), 0, -1)]
    elif len(set(a)) == len(a):
        z[0] = len(a)
    else:
        z[0] = len(a)
        l = r = 1
        for i in range(1, len(a)):
            if a[i] == a[0]:
                if i < r:
                    z[i] = min(r-i+1, z[i-l])
                else:
                    z[i] = 1
                    while (i+z[i] < len(a) and a[z[i]] == a[i+z[i]]):
                        z[i] += 1
                    if (i+z[i]-1 > r):
                        l = i
                        r = i+z[i]-1
    return z

a = input()
print(*z_function(a))
