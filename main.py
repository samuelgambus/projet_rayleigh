from passwd import Password
import string

#niveau 0 
"""
p = Password(0)
for c in string.ascii_lowercase:
    print(c)
    print(p.check(c))
"""
#niveau 1
"""
p = Password(1)
for c1 in string.ascii_lowercase:
    for c2 in string.ascii_lowercase:
        for c3 in string.ascii_lowercase:
            check=p.check([c1,c2,c3])
            #print (check )
            if check!=-1:
                print (check )
"""
#niveau 2
"""
p=Password(2)
for i in range(1000000):
    c=str(i)
    c=list(c)
    n=len(c)
    c=['0']*(6-n) + c
    check=p.check(c)
    if check!=-1:
        print (check )
"""
#niveau 3 
p = Password(3)
for i in range(32, 127):
    for j in range(32, 127):
        for k in range(32, 127):
            check=p.check([chr(i),chr(j),chr(k)])
            #print (check )
            if check!=-1:
                print (check )



