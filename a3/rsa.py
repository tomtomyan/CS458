n = 2877108316427887325303441168918606337867297158465631133791972250355158115988231577608742390819005983
e = 87697089310260388311745882286169271754292422215687
c = 287392805283491791254311949486085072916872625575628570842522186582705423038355275986357982637743200

# START PRODUCTION
m1 = "19200118200016181504210320091514"
# HALT PRODUCTION
m2 = "080112200016181504210320091514"
# SELL INVENTORY
m3 = "1905121200091422051420151825"

for i in range(10):
    for j in range(10):
        for k in range(10):
            m = m3 + str(i) + str(j) + str(k)
            cc = pow(int(m), e, n)
            print(m)
            if cc == c:
                print("found")
                print(m)
                sys.exit()