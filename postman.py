import requests
import pandas as pd
# url = "https://core-api.nba.com/cp/api/v1.3/feeds/gamecardfeed?gamedate=01/31/2024&platform=web"

payload = {}
headers = {
  'sec-ch-ua': '"Not A(Brand";v="99", "Microsoft Edge";v="121", "Chromium";v="121"',
  'Accept': 'application/json',
  'DNT': '1',
  'sec-ch-ua-mobile': '?0',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0',
  'Ocp-Apim-Subscription-Key': '747fa6900c6c4e89a58b81b72f36eb96',
  'sec-ch-ua-platform': '"Windows"',
  'Sec-Fetch-Site': 'same-site',
  'Sec-Fetch-Mode': 'cors',
  'Sec-Fetch-Dest': 'empty',
  'host': 'core-api.nba.com'
}


def map_period(homeTeamPeriod, awayTeamPeriod):
    output = []
    for i in range(len(homeTeamPeriod)):
        quarter = f"Q{i+1}" if i<3 else f"E{i-3}"
        output.append({
            'period': f"Q{i+1}",
            'team1': homeTeamPeriod[i]['score'],
            'team2': awayTeamPeriod[i]['score'],
            
        })
        
    return output

def get_verdict(score1, score2):
    if score1==score2:
        return 2
    elif score1>score2:
        return 0
    return 1


def generate_dictionary(url):

    r = requests.request("GET", url, headers=headers, data=payload).json()

    matches = []

    for i in r['modules'][0]['cards']:
        a = {
            'team1': i['cardData']['homeTeam']['teamName'],
            'team2': i['cardData']['awayTeam']['teamName'],
            'team1_score': i['cardData']['homeTeam']['score'],
            'team1_leader': {
                'name': i['cardData']['homeTeam']['teamLeader']['name'],
                'points': i['cardData']['homeTeam']['teamLeader']['points'],
                'rebounds': i['cardData']['homeTeam']['teamLeader']['rebounds'],
                'assists': i['cardData']['homeTeam']['teamLeader']['assists'],
                'blocks': i['cardData']['homeTeam']['teamLeader']['blocks'],
                'steals': i['cardData']['homeTeam']['teamLeader']['steals'],
            },
            'team2_score': i['cardData']['awayTeam']['score'],
            'team2_leader': {
                'name': i['cardData']['awayTeam']['teamLeader']['name'],
                'points': i['cardData']['awayTeam']['teamLeader']['points'],
                'rebounds': i['cardData']['awayTeam']['teamLeader']['rebounds'],
                'assists': i['cardData']['awayTeam']['teamLeader']['assists'],
                'blocks': i['cardData']['awayTeam']['teamLeader']['blocks'],
                'steals': i['cardData']['awayTeam']['teamLeader']['steals'],
            },
            'periods': map_period(i['cardData']['homeTeam']['periods'], i['cardData']['awayTeam']['periods']),
            'verdict': get_verdict(i['cardData']['homeTeam']['score'], i['cardData']['awayTeam']['score'])
        }
        matches.append(a)
    return matches
    # print(matches)
    # exit()


def generate_csv(matches):
    df = pd.DataFrame(matches)
    
    # Create separate columns for team1, team1_leader, team2_leader, and periods
    df['team1_leader_name'] = df['team1_leader'].apply(lambda x: x['name'])
    df['team1_leader_points'] = df['team1_leader'].apply(lambda x: x['points'])
    df['team1_leader_rebounds'] = df['team1_leader'].apply(lambda x: x['rebounds'])
    df['team1_leader_assists'] = df['team1_leader'].apply(lambda x: x['assists'])
    df['team1_leader_blocks'] = df['team1_leader'].apply(lambda x: x['blocks'])
    df['team1_leader_steals'] = df['team1_leader'].apply(lambda x: x['steals'])

    df['team2_leader_name'] = df['team2_leader'].apply(lambda x: x['name'])
    df['team2_leader_points'] = df['team2_leader'].apply(lambda x: x['points'])
    df['team2_leader_rebounds'] = df['team2_leader'].apply(lambda x: x['rebounds'])
    df['team2_leader_assists'] = df['team2_leader'].apply(lambda x: x['assists'])
    df['team2_leader_blocks'] = df['team2_leader'].apply(lambda x: x['blocks'])
    df['team2_leader_steals'] = df['team2_leader'].apply(lambda x: x['steals'])

    # print(len(df.columns))
    max_rounds, ind = 4, 0
    for i in range(len(df['periods'])):
        if len(df['periods'][i])>max_rounds:
            max_rounds, ind = len(df['periods'][i]), i

    for i in range(0, len(df['periods'][ind])):
        df[f"period_{df['periods'][ind][i]['period']}_team1"] = df['periods'].apply(lambda x: 0 if i>=len(x) else x[i]['team1'])
        df[f"period_{df['periods'][ind][i]['period']}_team2"] = df['periods'].apply(lambda x: 0 if i>=len(x) else x[i]['team2'])
        
    verdict = df['verdict']
    df.drop(['periods', 'verdict', 'team1_leader', 'team2_leader'], axis=1, inplace=True)
    df['verdict']=verdict
    df.to_csv('output.csv', index=False)

# a = generate_dictionary("https://core-api.nba.com/cp/api/v1.3/feeds/gamecardfeed?gamedate=11/01/1949&platform=web")
# print(a)