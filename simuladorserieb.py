from random import randint, randrange, random, choice
class Time:
    def __init__(self, nome):
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
    
    def fora(self, placar):
        gols_tomados = int(placar[0])
        gols_feitos = int(placar[2])
        self.gols_contra += gols_tomados
        self.gols_pro += gols_feitos
        self.saldo_gols = self.gols_pro - self.gols_contra
        self.hist_gol.append(gols_feitos)
        self.hist_gol_fora.append(gols_feitos)
        self.jogos += 1
        if gols_feitos > gols_tomados:
            self.vitorias += 1
            self.pontos += 3
            self.vitorias_fora += 1
        elif gols_feitos == gols_tomados:
            self.empates += 1
            self.empates_fora += 1
            self.pontos += 1
        else:
            self.derrotas += 1
            self.derrotas_fora += 1

    def casa(self, placar):
        gols_tomados = int(placar[2])
        gols_feitos = int(placar[0])
        self.gols_contra += gols_tomados
        self.gols_pro += gols_feitos
        self.saldo_gols = self.gols_pro - self.gols_contra
        self.hist_gol.append(gols_feitos)
        self.hist_gol_casa.append(gols_feitos)
        self.jogos += 1
        if gols_feitos > gols_tomados:
            self.vitorias += 1
            self.pontos += 3
            self.vitorias_casa += 1
        elif gols_feitos == gols_tomados:
            self.empates += 1
            self.empates_casa += 1
            self.pontos += 1
        else:
            self.derrotas += 1
            self.derrotas_casa += 1

times = [ "AVA", "BOT", "BRA", "BRU", "CON", "COR", "CRB", "CRU", "CSA", "GOI", "GUA", "LON", "NAU", "OPE", "PON", "REM", "SAM", "VAS", "VIL", "VIT"]

def simula_random(casa, fora):
    placar = f'{randint(0,3)}-{randint(0,3)}'
    dictimes[casa].casa(placar)
    dictimes[fora].fora(placar)

def simula_histo(casa, fora):
    placar = f'{choice(dictimes[casa].hist_gol)}-{choice(dictimes[fora].hist_gol)}'
    dictimes[casa].casa(placar)
    dictimes[fora].fora(placar)

def simula_histo_local(casa, fora):
    placar = f'{choice(dictimes[casa].hist_gol_casa)}-{choice(dictimes[fora].hist_gol_fora)}'
    dictimes[casa].casa(placar)
    dictimes[fora].fora(placar)

def simula_ved_local(casa, fora):
    res = [ '1-0' ] * 10 *(dictimes[casa].vitorias_casa + dictimes[fora].derrotas_fora) 
    res = res + [ '0-0' ] * 10 *  (dictimes[casa].empates_casa + dictimes[fora].empates_fora)
    res = res + [ '0-1'] * 10 * (dictimes[casa].derrotas_casa + dictimes[fora].vitorias_fora)
    placar = choice(res)
    dictimes[casa].casa(placar)
    dictimes[fora].fora(placar)

def simula_ved_corvas(casa, fora):
    casaa = casa
    foraa = fora
    if fora == 'VAS':
        foraa = 'COR'
    elif casa == 'VAS':
        casaa = 'COR'
    
    res = [ '1-0' ] * 10 *(dictimes[casaa].vitorias_casa + dictimes[foraa].derrotas_fora) 
    res = res + [ '0-0' ] * 10 *  (dictimes[casaa].empates_casa + dictimes[foraa].empates_fora)
    res = res + [ '0-1'] * 10 * (dictimes[casaa].derrotas_casa + dictimes[foraa].vitorias_fora)
    placar = choice(res)
    dictimes[casa].casa(placar)
    dictimes[fora].fora(placar)


promotions = 0
posicoes = 0
n_simulacoes = 10000
for nth_sim in range(n_simulacoes):
    dictimes = {}
    for time in times:
        dictimes[time] = Time(time)

    


    confrontos = [ 
        #       AVA BOT BRA BRU CON COR CRB CRU CSA GOI GUA LON NAU OPE PON REM SAM VAS VIL VIT  
        "AVA	—	1–1	1–1	1–2	2–1	1–2	1–0	R31	R35	1–0	0–1	R27	2–0	1–0	R29	1–0	R38	3–1	1–1	R34",
        "BOT	R28	—	1–0	R31	R33	2–0	R29	3–3	2–0	0–2	R38	4–0	3–1	R36	2–0	3–0	R26	2–0	3–2	1–0",
        "BRA	R33	R37	—	R27	1–1	0–2	0–1	0–0	0–1	2–1	R35	0–0	R32	R29	1–1	1–1	1–2	1–2	R30	1–0",
        "BRU	0–0	2–1	1–0	—	3–0	0–0	R36	1–2	2–3	0–1	R28	0–0	R33	R37	2–1	R30	0–0	0-1	R32	0–0",
        "CON	R30	0–1	1–1	R34	—	0–1	1–2	3–1	0–2	1–2	1–4	R32	R35	R26	R37	1–2	2–0	R28	1–0	1–1",
        "COR	2–0	0–1	R36	4–0	R27	—	1–1	R29	R37	1–1	R26	1–1	3–1	R33	2–0	2–1	R31	1–1	1–0	1–0",
        "CRB	R26	2–1	2–1	3–0	3–2	R32	—	0–0	R28	0–1	R30	R35	1–1	0–0	1–1	2–2	R33	1–1	2–1	R37",
        "CRU	0–3	R30	R28	R35	1–0	0–0	3–4	—	R26	1–1	3–3	2–2	R38	1–1	1–0	R32	1–1	2–1	R33	2–2",
        "CSA	0–0	2-0	R38	R29	R36	3–0	0–1	2–1	—	0–1	1–1	1–0	0–1	R31	R27	R34	0–0	2–2	1–1	2–1",
        "GOI	3–0	R32	2–1	R38	2–0	R35	1–0	1–1	R30	—	2–1	0–0	0–1	1–0	R33	1–1	2–2	1–0	1-2	R28",
        "GUA	R36	1–1	2–0	4–1	R31	0–2	1–0	R27	1–0	R37	—	R29	1–3	3–0	1–0	2–0	0–0	R33	1–4	1–1",
        "LON	1–3	2–2	0–0	0–1	0–0	2–3	0–2	R34	0–2	R31	0–1	—	0–0	1–2	R36	1–0	R28	R38	1–0	R26",
        "NAU	R37	3–1	2–1	1–1	0–4	R34	R27	0–1	1–0	R29	1–1	1–2	—	5–0	1–1	1–1	R36	R31	2–0	1–1",
        "OPE	R32	1–0	2–1	1–1	0–0	1–0	R38	2–1	0–2	R34	2–5	R30	R28	—	1–2	R35	1–0	2–0	1–2	0–1",
        "PON	0–0	R35	R26	3–0	4–2	R38	R34	0–1	2–1	2–1	0–0	2–1	R30	0–0	—	1–2	3–2	1–1	R28	R32",
        "REM	2–1	0–1	1–0	2–1	R38	R28	1–2	1–0	1–0	R36	0–0	R33	1-0	0–1	R31	—	0–2	2–1	0–1	0–0",
        "SAM	0–2	2–0	R34	2–2	3–1	2–3	2–3	R37	2–0	0–0	R32	1–0	2–0	0–0	1–0	R27	—	R29	R35	R30",
        "VAS	0–2	R34	1–1	2–1	1–0	R30	3–0	1–1	R32	R27	4–1	1–2	1–1	0–2	2–0	R37	1–0	—	1–0	R35",
        "VIL	1–0	1–1	0–0	0–1	0–0	0–1	R31	0–0	1–0	0–0	R34	R37	1–0	R27	0–0	R29	0–2	R36	—	0–0",
        "VIT	0–0	R27	R31	3–1	R29	0–0	1–1	R36	R33	1–1	1–0	1–2	0–1	0–0	1–0	1–2	2–2	0–1	R38	—"
    ]
    jogos_restantes = []

    for linha in confrontos:
        time_da_casa = ""
        for i, trecho in enumerate(linha.split("\t")):
            if i == 0:
                time_da_casa = trecho
            else:
                time_visitante = times[i-1]
                if trecho.startswith("R"):
                    jogos_restantes.append((time_da_casa, time_visitante, trecho))
                elif not trecho.startswith("—"):
                    dictimes[time_da_casa].casa(trecho)
                    dictimes[time_visitante].fora(trecho)
                    #print(f'{time_da_casa} {trecho} {time_visitante}')


    jogos_restantes.sort(key=lambda x: x[2])
    
    for jogo in jogos_restantes:
        #simula_random(jogo[0], jogo[1])
        simula_histo_local(jogo[0], jogo[1])
        #simula_ved_local(jogo[0], jogo[1])
        #simula_ved_corvas(jogo[0], jogo[1])
    


    times.sort(key=lambda x: dictimes[x].saldo_gols,reverse=True)
    times.sort(key=lambda x: dictimes[x].vitorias, reverse=True)
    times.sort(key=lambda x: dictimes[x].pontos,reverse=True)
    posicoes += times.index('VAS')

    if 'VAS' in times[0:4]:
        promotions += 1
        #print(f'-nth:{nth_sim}-----------------------')
        #for team in times:
        #    print(f'{team}\t{dictimes[team].pontos}\t{dictimes[team].jogos}')
        #break
    
  
    

print(f'Posição média do Vasco: {posicoes/n_simulacoes}, chances de promoção: {promotions/n_simulacoes}' )
