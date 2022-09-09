'''simulador serie b'''

from random import randint, uniform, choice
import copy
import timeit

DIVISOR_ELO = 400.0
IMPORTANCIA = 40
BASE_ELO = 10.0


class Time:
    '''representa um time com rating e pontuação em um campeonato'''
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
    '''atualiza os times no campeonato conforme resultado do jogo'''
    casa.gols_pro += gcasa
    casa.gols_contra += gfora
    casa.saldo_gols = casa.gols_pro - casa.gols_contra
    fora.gols_pro += gfora
    fora.gols_contra += gcasa
    fora.saldo_gols = fora.gols_pro - fora.gols_contra
    win = 0
    if gcasa > gfora:
        win = 1
        casa.vitorias += 1
        casa.pontos += 3
        fora.derrotas += 1
    elif gcasa == gfora:
        win = 0.5
        casa.empates += 1
        casa.pontos +=1
        fora.empates += 1
        fora.pontos += 1
    else:
        win = 0
        casa.derrotas += 1
        fora.vitorias += 1
        fora.pontos += 3

    delta_rating = casa.rating - fora.rating
    bonus_saldo = 1
    saldo = abs(gcasa - gfora)
    if saldo == 2:
        bonus_saldo = 1.5
    if saldo == 3:
        bonus_saldo = 1.75
    if saldo > 3:
        bonus_saldo = 1.75 + (saldo-3/8)

    win_expectancy = 1./(1.+BASE_ELO**(-delta_rating/DIVISOR_ELO))
    delta = IMPORTANCIA * bonus_saldo *(win-win_expectancy)
    casa.rating += delta
    fora.rating -= delta

def simula_random(casa: Time, fora: Time):
    '''simulação totalmente aleatória'''
    match(casa, fora, randint(0,3), randint(0,3))


def simula_elo(casa: Time, fora: Time):
    '''simuma pelo metodo ELO sem vantagem para o time da casa'''
    delta_rating = casa.rating - fora.rating
    win_expectancy = 1/(1+BASE_ELO**(-delta_rating/DIVISOR_ELO))
    if win_expectancy > 0.5:
        draw_expectancy = 1-win_expectancy
    else:
        draw_expectancy = win_expectancy
    loss_expectancy = 1-win_expectancy
    results = [] + [(1,0)] *int(100*win_expectancy)
    results += [(0,0)] * int(100*draw_expectancy)
    results += [(0,1)] * int(100*loss_expectancy)
    (gcasa, gfora) = choice(results)
    match(casa, fora, gcasa, gfora)


def simula_elo_hfa(casa: Time, fora: Time):
    '''simula partida pelo metodo elo com vantagem para o time da casa. Pempate = min(V,D)'''
    delta_rating = casa.rating+100 - fora.rating
    win_expectancy = 1/(1+BASE_ELO**(-delta_rating/DIVISOR_ELO))
    if win_expectancy > 0.5:
        draw_expectancy = 1-win_expectancy
    else:
        draw_expectancy = win_expectancy
    loss_expectancy = 1-win_expectancy

    alea = uniform(0, win_expectancy+draw_expectancy+loss_expectancy)
    if alea < win_expectancy:
        (gcasa, gfora) = (1,0)
    elif alea < win_expectancy+draw_expectancy:
        (gcasa, gfora) = (0,0)
    else:
        (gcasa, gfora) = (0,1)

    match(casa, fora, gcasa, gfora)


def simula_elo_hfa_new(casa: Time, fora: Time):
    '''Simula partidas utilizando algoritmo ELO corrigido'''
    delta_rating = casa.rating+100 - fora.rating
    divisor = 1+10**(-1*delta_rating/DIVISOR_ELO)+10**(delta_rating/DIVISOR_ELO)
    win_expectancy = 10**(delta_rating/DIVISOR_ELO)/(divisor)
    #Wl = 10**(-1*dr/DIVISOR_ELO)/(divisor)
    draw_expectancy = 1/(divisor)
    alea = uniform(0, 1)
    if alea < win_expectancy:
        (gcasa, gfora) = (1,0)
    elif alea-win_expectancy < draw_expectancy:
        (gcasa, gfora) = (0,0)
    else:
        (gcasa, gfora) = (0,1)
    match(casa, fora, gcasa, gfora)


def main():
    '''Main function.'''
    n_simulacoes = 100_000
    algoritmo = simula_elo_hfa_new
    dic_inicial = {}
    dic_hist_rating = {}
    jogos_restantes = []
    jogos_realizados = []
    nomes_times = []
    with open('TABELA SERIE B.txt', 'r', encoding='UTF-8') as arquivo:
        for line in arquivo.readlines():
            [ tcasa, placar, tfora] = line.split()
            if tcasa not in nomes_times:
                nomes_times.append(tcasa)
                dic_inicial[tcasa] = Time(tcasa)
                dic_hist_rating[tcasa] = [ 1000.0]
            if tfora not in nomes_times:
                nomes_times.append(tfora)
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

        with open('hist_rating.txt', 'w', encoding='UTF-8') as out_rating:
            lines = [ f'{nome}\t{lista}\nt' for (nome, lista) in dic_hist_rating.items()]
            out_rating.writelines(lines)
        print("Rating dos times considerando os jogos já realizados")
        nomes_times.sort(key= lambda t: dic_inicial[t].rating, reverse=True)
        for nome_time in nomes_times:
            time: Time = dic_inicial[nome_time]
            print(time.nome, f'{time.rating:>8.3f}')

        print("\nProbabilidades de Vitória nos Próximos 10 Jogos:")
        print("Casa\tP.Casa\tEmpate\tP.Fora\tFora")
        for (tcasa, tfora) in jogos_restantes[:10]:
            delta_rating = dic_inicial[tcasa].rating-dic_inicial[tfora].rating+100
            divisor = 1+10**(-1*delta_rating/DIVISOR_ELO)+10**(delta_rating/DIVISOR_ELO)
            win_expectancy = f'{100*10**(delta_rating/DIVISOR_ELO)/(divisor):.2f}'
            loss_expectancy = f'{100*10**(-1*delta_rating/DIVISOR_ELO)/(divisor):.2f}'
            draw_expectancy = f'{100*1/(divisor):.2f}'
            print(f'{tcasa}\t{win_expectancy}\t{draw_expectancy}\t{loss_expectancy}\t{tfora}')

    dicprobs = { nome:{"titulos":0, "acessos":0, "rebaixamentos":0} for nome in nomes_times}
    dictimes = {}
    for _ in range(n_simulacoes):
        for nome_time in nomes_times:
            dictimes[nome_time] = copy.copy(dic_inicial[nome_time])

        for (casa, fora) in jogos_restantes:
            algoritmo(dictimes[casa], dictimes[fora])

        nomes_times.sort(key= lambda x: dictimes[x].saldo_gols, reverse=True)
        nomes_times.sort(key= lambda x: dictimes[x].vitorias, reverse=True)
        nomes_times.sort(key= lambda x: dictimes[x].pontos, reverse=True)
        dicprobs[nomes_times[0]]["titulos"] += 1
        for team in nomes_times[0:4]:
            dicprobs[team]["acessos"] += 1
        for team in nomes_times[-4:]:
            dicprobs[team]["rebaixamentos"] +=1

    nomes_times.sort(key= lambda x: dicprobs[x]["rebaixamentos"])
    nomes_times.sort(key= lambda x: dicprobs[x]["acessos"], reverse=True)
    nomes_times.sort(key= lambda x: dicprobs[x]["titulos"], reverse=True)
    print(f'\nFinal da simulação por {algoritmo.__name__}')
    print('Time\tTítulo\tSubir\tcair')
    div = n_simulacoes/100
    for nome_time in nomes_times:
        titulos = dicprobs[nome_time]["titulos"]/div
        acessos = dicprobs[nome_time]["acessos"]/div
        rebaixamentos = dicprobs[nome_time]["rebaixamentos"]/div
        print(f'{nome_time}\t{titulos:.3f}\t{acessos:.3f}\t{rebaixamentos:.3f}')

if __name__ == "__main__":
    print(timeit.timeit(main,number=1))
