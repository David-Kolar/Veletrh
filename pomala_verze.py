import heapq

# Algoritmus je stejný, ale tady jsem rekonstruoval trasu neefektivně
def make_graph(pocet, hrany):
    graf = [[] for _ in range(pocet)]
    for start, konec, delka in hrany:
        graf[start].append((konec, delka))
    return graf

def najdi_min(pole):
    minimum = float("inf")
    for prvek in pole:
        if (minimum > prvek != 0):
            minimum = prvek
    return prvek

def solve(vrchol):
    cas = 0
    return recursion_phase(vrchol, cas, 0)

def zkontroluj_dostupnost(cas, mistnostA, udalost):
    mistnostB, start, delka = udalost
    konec = start + delka
    delka_cesty = tabulka[mistnostA][mistnostB]
    if (delka_cesty >= konec - cas):
        return False
    else:
        doba = konec - cas - delka_cesty
        if (cas + delka_cesty < start):
            doba -= start - (cas + delka_cesty)
        return doba


def recursion_phase(vrchol, cas, pozice):
    trasa = []
    pomocne_pole_udalosti = [None for _ in tabulka]
    pocitadlo = 0
    for index in range(pozice, len(udalosti)):
        udalost = udalosti[index]
        mistnost, start, delka = udalost
        dostupnost = zkontroluj_dostupnost(cas, vrchol, udalost)
        if not(pomocne_pole_udalosti[mistnost]) and (dostupnost):
            pomocne_pole_udalosti[mistnost] = (index, udalost)
            pocitadlo += 1
        if (pocitadlo == pocet_mistnosti):
            break
    maximum = 0
    vrchol_maxima = None
    for udalost in pomocne_pole_udalosti:
        if not(udalost):
            continue
        index, udalost = udalost
        novy_vrchol, start, delka = udalost

        zbyvajici_cas = zkontroluj_dostupnost(cas, vrchol, udalost)
        if not(pomocne_pole[index]):
            pomocne_pole[index] = recursion_phase(novy_vrchol, start + delka, index)
        doba = pomocne_pole[index][0] + zbyvajici_cas
        if (doba > maximum):
            maximum = doba
            trasa = pomocne_pole[index][1]
            vrchol_maxima = novy_vrchol
    return maximum, [(cas, vrchol_maxima)] + trasa

def vytvor_cestu(cesta, aktualni_vrchol):
    vystup = []
    cekani = 0
    predchozi_cas = 0
    for index in range(len(cesta)):
        cas_presunu, vrchol = cesta[index]
        cekani = cas_presunu - predchozi_cas
        if not((vrchol==aktualni_vrchol) or (vrchol==None)):
            if (cekani > 0):
                vystup.append(f"C {cekani}")
            cela_trasa = rekonstrukce_cesty(aktualni_vrchol, vrchol)
            for n in cela_trasa:
                vystup.append(f"P {n}")
            cekani = 0
            predchozi_cas = cas_presunu + tabulka[aktualni_vrchol][vrchol]
            aktualni_vrchol = vrchol
    if (cekani > 0):
        vystup.append(f"C {cekani}")
    return "\n".join(vystup)

def rekonstrukce_cesty(start, cil):
    vrchol = cil
    cesta = []
    while(vrchol != start):
        cesta.append(vrchol)
        vrchol = tabulka_predchudcu[start][vrchol]
    return cesta[::-1]


def dijkstra(start, graf):
    vzdalenosti = [False for i in range(len(graf))]
    predchudci = [None for _ in graf]
    halda = []
    heapq.heapify(halda)
    heapq.heappush(halda, (0, start, None))
    while(halda):
        vzdalenost, vrchol, predchudce = heapq.heappop(halda)
        if not(isinstance(vzdalenosti[vrchol], bool)):
            continue
        for soused, hrana in graf[vrchol]:
            if (not vzdalenosti[soused]):
                heapq.heappush(halda, (vzdalenost + hrana, soused, vrchol))
        vzdalenosti[vrchol] = vzdalenost
        predchudci[vrchol] = predchudce
    return vzdalenosti, predchudci


def load_input():
    with open("input", "r") as file:
        hrany = []
        udalosti = []
        for i, line in enumerate(file):
            line = line.strip().split()
            line = [int(n) for n in line]
            if (i == 0):
                pocet_mistnosti, pocet_chodeb, pocet_udalosti = line
                continue
            if (i <= pocet_chodeb):
                hrany.append(line)
                continue
            udalosti.append(line)
    return pocet_mistnosti, hrany, udalosti

def output(maximum, cesta):
    with open("output", "w") as file:
        file.write(str(maximum) + "\n" + cesta)
def nejkratsi_cesty(graf):
    tabulka = []
    tabulka_predchudcu = []
    for vrchol in range(len(graf)):
        radek, predchudci = dijkstra(vrchol, graf)
        tabulka.append(radek)
        tabulka_predchudcu.append(predchudci)
    return tabulka, tabulka_predchudcu

pocet_mistnosti, hrany, udalosti = load_input()
pomocne_pole = [None for _ in udalosti]
graf = make_graph(pocet_mistnosti, hrany)
udalosti.sort(key=lambda vstup: vstup[1])
tabulka, tabulka_predchudcu = nejkratsi_cesty(graf)
maximum, trasa = solve(0)
print(trasa)
cesta = vytvor_cestu(trasa, 0)
output(maximum, cesta)