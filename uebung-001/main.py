# Uebung 001 — Schleifen & Funktionen
# Schreibe deinen Code hier.

# Definitions

x = 0
n1 = 437
n2 = 32482

# Aufgabe 1 Summieren von Ganzzahlen zwischen 437 und 32482
for i in range (n1, n2) :
    x += i 
print (x)  
   
    
# Aufgabe 2
y1 = float (45.1)
y2 = float (5.511)

if ( y1 > y2) :
   z = y1 / y2
   print (z)
elif (y2 > y1) :
   z = y2 / y1
   print (z)
else :
    print ("1")