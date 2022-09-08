from collections import defaultdict
from random import randint, randrange, uniform, choice
import copy
import timeit

DIVISOR_ELO = 400.0
IMPORTANCIA = 40
BASE_ELO = 10.0

hist_vitorias = []
hist_empates = []
hist_derrotas = []

class Time:
    def __init__(self, nome):
        self.rating = 1000.0
        self.nome = nome
        self.jogos = 0
        self.vitorias = 0
        self.empates = 0
        self.derrotas = 0
        self.gols_pro = 0
        self.gols_contra = 0
        self.saldo_gols = 0
        self.pontos = 0
  

def match( casa: Time, fora: Time, gcasa: int, gfora: int ):
    casa.gols_pro += gcasa
    casa.gols_contra += gfora
    casa.saldo_gols = casa.gols_pro - casa.gols_contra
    fora.gols_pro += gfora
    fora.gols_contra += gcasa
    fora.saldo_gols = fora.gols_pro - fora.gols_contra
    W = 0
    if gcasa > gfora:
        W = 1
        casa.vitorias += 1
        casa.pontos += 3
        fora.derrotas += 1
    elif gcasa == gfora:
        W = 0.5
        casa.empates += 1
        casa.pontos +=1
        fora.empates += 1
        fora.pontos += 1
    else:
        W = 0
        casa.derrotas += 1
        fora.vitorias += 1
        fora.pontos += 3
    dr = casa.rating - fora.rating
    
    k = 1
    gd = abs(gcasa - gfora)
    if gd == 2: 
        k = 1.5
    if gd == 3:
        k = 1.75
    if gd > 3:
        k = 1.75 + (gd-3/8)

    We = 1./(1.+BASE_ELO**(-dr/DIVISOR_ELO))
    delta = IMPORTANCIA * k *(W-We)
    casa.rating += delta
    fora.rating -= delta


times = []#["BRU","GUA","VAS","VNO","BAH","CRU","CHA","ITU","PON","GRE","SPT","SCO","TOM","OPE","LEC","NAU","NOV","CRB","CSA","CRI"]

   

def simula_random(casa: Time, fora: Time):
    match(casa, fora, randint(0,3), randint(0,3))


def simula_ELO(casa: Time, fora: Time):
    dr = casa.rating - fora.rating
    We = 1/(1+BASE_ELO**(-dr/DIVISOR_ELO))
    if We > 0.5:
        Wdraw = 1-We    
    else:
        Wdraw = We
    Wb = 1-We
    results = [] + [(1,0)] *int(100*We)
    results += [(0,0)] * int(100*Wdraw)
    results += [(0,1)] * int(100*Wb)
    (gcasa, gfora) = choice(results)
    match(casa, fora, gcasa, gfora)


def simula_ELOHFA(casa: Time, fora: Time):
    dr = casa.rating+100 - fora.rating
    We = 1/(1+BASE_ELO**(-dr/DIVISOR_ELO))
    if We > 0.5:
        Wdraw = 1-We    
    else:
        Wdraw = We
    Wb = 1-We

    alea = uniform(0, We+Wdraw+Wb)
    if alea < We:
        (gcasa, gfora) = (1,0)
    elif alea < We+Wdraw:
        (gcasa, gfora) = (0,0)
    else:
        (gcasa, gfora) = (0,1)

    match(casa, fora, gcasa, gfora)


def simula_ELOHFA_NEW(casa: Time, fora: Time):
    dr = casa.rating+100 - fora.rating
    divisor = 1+10**(-1*dr/DIVISOR_ELO)+10**(dr/DIVISOR_ELO)
    We = 10**(dr/DIVISOR_ELO)/(divisor)
    Wl = 10**(-1*dr/DIVISOR_ELO)/(divisor)
    Wdraw = 1/(divisor)

    alea = uniform(0, 1)
    
    if alea < We:
        (gcasa, gfora) = (1,0)
    elif alea-We < Wdraw:
        (gcasa, gfora) = (0,0)
    else:
        (gcasa, gfora) = (0,1)
    
    match(casa, fora, gcasa, gfora)


def main():
    n_simulacoes = 100000
    algoritmo = simula_ELOHFA_NEW

    dic_inicial = {}
    dic_hist_rating = {}

    jogos_restantes = []
    jogos_realizados = []
    

    with open('TABELA SERIE B.txt', 'r') as arquivo:
        for line in arquivo.readlines():
            [ tcasa, placar, tfora] = line.split()
            if tcasa not in times:
                times.append(tcasa)
                dic_inicial[tcasa] = Time(tcasa)
                dic_hist_rating[tcasa] = [ 1000.0]
            if tfora not in times:
                times.append(tfora)
                dic_inicial[tfora] = Time(tfora)
                dic_hist_rating[tfora] = [ 1000.0]
            if not placar == '-':
                casa = dic_inicial[tcasa]
                fora = dic_inicial[tfora]
                [gcasa, gfora] = placar.split('-')
                jogos_realizados.append((tcasa, int(gcasa), tfora, int(gfora)))
            else:
                jogos_restantes.append( (tcasa, tfora) )


        for (casa, gcasa, fora, gfora) in jogos_realizados:
            match(dic_inicial[casa], dic_inicial[fora], gcasa, gfora)
            dic_hist_rating[casa].append(dic_inicial[casa].rating)
            dic_hist_rating[fora].append(dic_inicial[fora].rating)
        with open('hist_rating.txt', 'w') as out_rating:
            lines = [ f'{nome}\t{lista}\nt' for (nome, lista) in dic_hist_rating.items()]
            out_rating.writelines(lines)
        

        print("Rating dos times considerando os jogos já realizados")
        times.sort(key= lambda t: dic_inicial[t].rating, reverse=True)
        for time in times:
            t: Time = dic_inicial[time]
            print(t.nome, f'{t.rating:>8.3f}')

        print("\nProbabilidades de Vitória nos Próximos 10 Jogos:")
        print("Casa\tP.Casa\tEmpate\tP.Fora\tFora")
        for (tcasa, tfora) in jogos_restantes[:10]:
            dr = dic_inicial[tcasa].rating-dic_inicial[tfora].rating+100
            divisor = 1+10**(-1*dr/DIVISOR_ELO)+10**(dr/DIVISOR_ELO)
            We = 10**(dr/DIVISOR_ELO)/(divisor)
            Wl = 10**(-1*dr/DIVISOR_ELO)/(divisor)
            Wdraw = 1/(divisor)
            print(f'{tcasa}\t{100*We:.2f}\t{100*Wdraw:.2f}\t{100*Wl:.2f}\t{tfora:10}')

    
    dicprobs = { time:{"titulos":0, "acessos":0, "rebaixamentos":0} for time in times}
    for nth_sim in range(n_simulacoes):
        
        dictimes = {}
        for time in times:
            dictimes[time] = copy.copy(dic_inicial[time])

        for (casa, fora) in jogos_restantes:
            algoritmo(dictimes[casa], dictimes[fora])

 
        times.sort(key= lambda x: dictimes[x].saldo_gols, reverse=True)
        times.sort(key= lambda x: dictimes[x].vitorias, reverse=True)
        times.sort(key= lambda x: dictimes[x].pontos, reverse=True)

        dicprobs[times[0]]["titulos"] += 1
        for team in times[0:4]:
            dicprobs[team]["acessos"] += 1
        for team in times[-4:]:
            dicprobs[team]["rebaixamentos"] +=1
        

        
    times.sort(key= lambda x: dicprobs[x]["rebaixamentos"])
    times.sort(key= lambda x: dicprobs[x]["acessos"], reverse=True)
    times.sort(key= lambda x: dicprobs[x]["titulos"], reverse=True)
    print(f'\nFinal da simulação por {algoritmo.__name__}')
    print('Time\tTítulo\tSubir\tcair')
    div = n_simulacoes/100
    for time in times:
        print(f'{time}\t{dicprobs[time]["titulos"]/div:.3f}\t{dicprobs[time]["acessos"]/div:.3f}\t{dicprobs[time]["rebaixamentos"]/div:.3f}')

if __name__ == "__main__":
    print(timeit.timeit(lambda: main(),number=1))
    