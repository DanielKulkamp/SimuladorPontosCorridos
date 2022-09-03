from random import randint, randrange, uniform, choice
import copy

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
        self.vitorias_casa = 0
        self.vitorias_fora = 0
        self.empates_casa = 0
        self.empates_fora = 0
        self.derrotas_casa = 0
        self.derrotas_fora = 0
        self.hist_gol = []
        self.hist_gol_casa = []
        self.hist_gol_fora = []
  



def match( casa: Time, fora: Time, gcasa: int, gfora: int ):
    casa.gols_pro += gcasa
    #casa.hist_gol_casa.append(gcasa)
    #casa.hist_gol.append(gcasa)
    casa.gols_contra += gfora
    casa.saldo_gols = casa.gols_pro - casa.gols_contra
    fora.gols_pro += gfora
    #fora.hist_gol_fora.append(gfora)
    #fora.hist_gol.append(gfora)
    fora.gols_contra += gcasa
    fora.saldo_gols = fora.gols_pro - fora.gols_contra
    W = 0
    if gcasa > gfora:
        W = 1
        casa.vitorias += 1
        casa.vitorias_casa += 1
        casa.pontos += 3
        fora.derrotas += 1
        fora.derrotas_fora += 1
    elif gcasa == gfora:
        W = 0.5
        casa.empates += 1
        casa.empates_casa += 1
        casa.pontos +=1
        fora.empates += 1
        fora.empates_fora += 1
        fora.pontos += 1
    else:
        W = 0
        casa.derrotas += 1
        casa.derrotas_casa += 1
        fora.vitorias += 1
        fora.vitorias_fora += 1
        fora.pontos += 3
    dr = casa.rating - fora.rating
    I = 60
    We = 1./(1.+10.0**(-dr/400.0))
    delta = I * (W-We)
    casa.rating += delta
    fora.rating -= delta


times = ["BRU",  "GUA","VAS",  "VNO","BAH",  "CRU","CHA",  "ITU","PON",  "GRE","SPT",  "SCO","TOM",  "OPE","LEC",  "NAU","NOV",  "CRB","CSA",  "CRI"]


dicprobs = { time:{"titulos":0, "acessos":0, "rebaixamentos":0} for time in times}

   


def simula_random(casa: Time, fora: Time):
    match(casa, fora, randint(0,3), randint(0,3))

def simula_hist_local(casa: Time, fora: Time):
    match(casa, fora, choice(casa.hist_gol_casa), choice(fora.hist_gol_fora))

def simula_ELO(casa: Time, fora: Time):
    dr = casa.rating - fora.rating
    We = 1/(1+10**(-dr/400))
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
    We = 1/(1+10**(-dr/400))
    if We > 0.5:
        Wdraw = 1-We    
    else:
        Wdraw = We
    Wb = 1-We
    #results = [] + [(1,0)] *int(100*We)
    #results += [(0,0)] * int(100*Wdraw)
    #results += [(0,1)] * int(100*Wb)
    #(gcasa, gfora) = choice(results)
    alea = uniform(0, We+Wdraw+Wb)
    if alea < We:
        (gcasa, gfora) = (1,0)
    elif alea < We+Wdraw:
        (gcasa, gfora) = (0, 0)
    else:
        (gcasa, gfora) = (0, 1)
    
    match(casa, fora, gcasa, gfora)

def main():
    n_simulacoes = 100000
    algoritmo = simula_ELOHFA

    for nth_sim in range(n_simulacoes):
        if nth_sim % 1000 == 0:
            print(f'-',end="")

        dictimes = {}
        for time in times:
            dictimes[time] = Time(time)
        jogos_restantes = []
        with open('TABELA SERIE B.txt', 'r') as arquivo:
            for line in arquivo.readlines():
                [ tcasa, placar, tfora] = line.split()
                if not placar == '-':
                    casa = dictimes[tcasa]
                    fora = dictimes[tfora]
                    [gcasa, gfora] = placar.split('-')
                    match(casa, fora, int(gcasa), int(gfora))
                else:
                    jogos_restantes.append( (tcasa, tfora) )

        #dictimes = copy.deepcopy(dic_start)

        for (casa, fora) in jogos_restantes:
            algoritmo(dictimes[casa], dictimes[fora])

        dictimes['BRU'].pontos -= 3

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
        print(f'{time}\t{dicprobs[time]["titulos"]/div:.2f}\t{dicprobs[time]["acessos"]/div:.2f}\t{dicprobs[time]["rebaixamentos"]/div:.2f}')

if __name__ == "__main__":
    main()