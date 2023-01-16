import json

scores = []

scores.append({'name': 'John', 'time': '01:14:14', 'deaths':3})
scores.append({'name': 'Doe', 'time': '01:13:14', 'deaths':1})
scores.append({'name': 'Jane', 'time': '01:17:14', 'deaths':6})

with open('scoreboard_1.json', 'w') as f:
    json.dump(scores, f)