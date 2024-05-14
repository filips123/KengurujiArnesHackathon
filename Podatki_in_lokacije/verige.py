from geopy.distance import geodesic 

#verige smo na podlagi zemljevida zaradi mnogih faktorjev, kot so kanali, stranski potoki ter manjkajoči podatek o smeri rek napisali na roke
radovna = [3180, 3080, 3420, 3465, 3530 ,3660, 3725, 3850, 3900]
bohinjka = [3200, 3320, 3250, 3420, 3465, 3530 ,3660, 3725, 3850, 3900]
mostnica = [3300, 3320, 3250, 3420, 3465, 3530 ,3660, 3725, 3850, 3900]
lipnica = [4025, 3465, 3530 ,3660, 3725, 3850, 3900]
trziska = [4050, 3465, 3530 ,3660, 3725, 3850, 3900]
kokra = [4120, 4155, 3530 ,3660, 3725, 3850, 3900]

seljska = [4298, 4200, 4209, 3530 ,3660, 3725, 3850, 3900]
poljanska = [4222, 4230, 4200, 4209, 3530 ,3660, 3725, 3850, 3900]

gradascica = [5500, 5479, 5078 ,3660, 3725, 3850, 3900]
horjulscica = [5540, 5479, 5078 ,3660, 3725, 3850, 3900]

ljubljanica = [5030, 5078 ,3660, 3725, 3850, 3900]
ljublja = [5030, 5078 ,3660, 3725, 3850, 3900]
bistra  = [5270, 5078 ,3660, 3725, 3850, 3900]
borovnisnica = [5330, 5078 ,3660, 3725, 3850, 3900]
iska = [5425, 5078 ,3660, 3725, 3850, 3900]
izica = [5440, 5078 ,3660, 3725, 3850, 3900]

kamniska = [4480, 4400, 4430, 4445 ,3660, 3725, 3850, 3900]
raca  = [4515, 4520, 4445 ,3660, 3725, 3850, 3900]
pisata = [4570, 4575, 3660, 3725, 3850, 3900]

sava_naprej = [3660, 3725, 3850, 3900]

savinja = [6020, 6060, 6068, 6120, 6140, 6200, 6210, 3850, 3900]
lucnica = [6220, 6060, 6068, 6120, 6140, 6200, 6210, 3850, 3900]
dreta = [6240, 6060, 6068, 6120, 6140, 6200, 6210, 3850, 3900]
paka = [6280, 6300, 6340, 6120, 6140, 6200, 6210, 3850, 3900]
bolska = [6550, 6120, 6140, 6200, 6210, 3850, 3900]
loznica = [6630, 6140, 6200, 6210, 3850, 3900]
sevnicna = [4706, 3850, 3900]
sopota = [4650, 3850, 3900]
medlja = [4626, 3725, 3850, 3900]

hudinja = [6770, 6790, 6200, 6210, 3850, 3900]
voganja = [6691, 6720, 6200, 6210, 3850, 3900]
gracnica= [6835, 6210, 3850, 3900]

radescica = [7272, 7110, 7160,3850, 3900]
krka = [7029, 7060, 7110, 7160, 3850, 3900]
precna = [7340, 7110, 7160, 3850, 3900]
radulja = [7380, 7160, 3850, 3900]
mirna = [4671, 4695, 3850, 3900]

mislinja = [2372, 2250, 2150, 2160]
suhodolnica = [2420, 2250, 2150, 2160]
meza = [2220, 2150, 2160]
radonja = [2530, 2150, 2160]
pesnica = [2830, 2880, 2900]
polskava = [2754, 2652, 2880, 2900]
dravinja = [2600, 2620, 2640, 2652, 2880, 2900]
oplotnica = [2667, 2620, 2640, 2652, 2880, 2900]
loznica = [2693, 2652, 2880, 2900]
dodatna = [2719, 2754, 2652, 2880, 2900]
vse_sz =[loznica, oplotnica, dravinja, polskava, pesnica, radonja, meza, suhodolnica, mislinja, mirna, radulja,
           precna, krka, radescica, gracnica, voganja, hudinja, medlja, sopota, sevnicna, loznica, bolska, paka, dreta,
           lucnica, savinja, pisata, raca, kamniska, izica, iska, borovnisnica, bistra, ljublja, ljubljanica,
           horjulscica, gradascica, poljanska, seljska, kokra, trziska, lipnica, mostnica, bohinjka, radovna]

vsi_stevci = []
ze = []
for veriga in vse_sz:
    for stevec in veriga:
        vmesni = []
        if not stevec in ze:
            ze.append(stevec)
            for x in vse_sz:
                if stevec in x:
                    for j in x:
                        if not j == stevec:
                            vmesni.append(j)
                        else:
                            break
            vsi_stevci.append((stevec, list(set(vmesni))))
#za vsak števec poiščemo vse prejšnje števce višje po reki
slovar_pretokov = {}
with open("meta_stations.txt", "r", encoding="utf-8")as dat:
    for vrstica in dat:
        seznam = vrstica.rstrip().split(";")
        if not seznam[0] == 'CODE':
            slovar_pretokov[int(seznam[0])] = (seznam[1], seznam[2], float(seznam[3]), float(seznam[4]), float(seznam[5]), float(seznam[6]))
import math
def razdalja(prvi, drugi):
        
        kor1 = (slovar_pretokov[prvi][3], slovar_pretokov[prvi][4])
        kor2 = (slovar_pretokov[drugi][3], slovar_pretokov[drugi][4])
        return (geodesic(kor1, kor2).km)
#spravimo vse v željeno obliko, ki jo bomo kasneje znali obdelati
stevci_in_razdalje = []
for j in vsi_stevci:
    middle = []
    slo = []
    if j[1]:
        for x in j[1]:
            try:
                middle.append((x, razdalja(j[0], x)))
            except:
                a = 0
   
    stevci_in_razdalje.append((j[0], middle))
slovar_razdalj = {}
for neki in stevci_in_razdalje:
    slovar_razdalj[neki[0]] = neki[1]
print(slovar_razdalj)