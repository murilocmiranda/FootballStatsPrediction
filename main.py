# API:https://github.com/wgenial/cartrolandofc/blob/master/nova-api.md
from urllib.request import urlopen
from datetime import datetime
import json


def get_schedule():
    # Consome a lista de rodadas
    global results_no

    url = "https://api.cartolafc.globo.com/rodadas"
    response = urlopen(url)
    data = json.loads(response.read())
    results_no = len(data)
    print("Foram carregadas %s rodadas." % (results_no))

def get_general_info():
    # Consome estado do jogo
    global rodada_atual

    url = "https://api.cartolafc.globo.com/mercado/status"
    response = urlopen(url)
    data = json.loads(response.read())
    rodada_atual = data['rodada_atual']
    status_mercado = data['status_mercado']
    fechamento = datetime.fromtimestamp(data['fechamento']['timestamp'])

    print("#########################################")
    print("# Rodada atual: %s" % rodada_atual)
    print("# Estado do mercado: Aberto" if  status_mercado else "Estado do mercado: Fechado")
    print("# Fechamento: %s" % fechamento)
    print("#########################################")

def get_matches_and_teams(matchday):
    # Consome a lista de jogos por rodada
    global matches
    global teams

    url = "https://api.cartolafc.globo.com/partidas/%s" % matchday
    response = urlopen(url)
    data = json.loads(response.read())
    matches = data['partidas']
    teams = data['clubes']

def get_team(team_id):
    # Carrega dados de um time por ID
    data = json.dumps(teams, indent = 4)
    loaded_teams = json.loads(data)
    return loaded_teams[str(team_id)]

def list_matches():
    for game in matches:
        team_home = get_team(game['clube_casa_id'])
        team_away = get_team(game['clube_visitante_id'])
        team_home_results_str = str(', '.join(game['aproveitamento_mandante'])).upper()
        team_away_results_str = str(', '.join(game['aproveitamento_visitante'])).upper()

        print("\n=========================================")
        print("# {home} ({home_rank}) x {away} ({away_rank})".format(home=team_home['nome'], home_rank=game['clube_casa_posicao'], away=team_away['nome'], away_rank=game['clube_visitante_posicao']))
        print("=========================================")
        print("# Casa: {home} ({results})".format(home=team_home['nome'], results=team_home_results_str))
        print("# Fora: {away} ({results})".format(away=team_away['nome'], results=team_away_results_str))
        print("=========================================")

if __name__ == '__main__':
    # Carrega informação geral
    get_general_info()

    # Carrega informação dos jogos por rodada
    get_matches_and_teams(rodada_atual)
    list_matches()


