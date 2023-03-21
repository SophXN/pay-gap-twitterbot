import os
import json

dir_path = os.path.dirname(os.path.realpath("__file__"))
data_path = dir_path + '/../raw_data/gender_pay_gap_app'

agg_dict = {'data': {'id_set': set(), 'data': []},
            'includes': {'users': {'id_set': set(), 'data': []},
                         'tweets': {'id_set': set(), 'data': []}},
            'errors': [],
            'meta': []}

total_tweets = 0
for filename in os.listdir(data_path):
    if filename.endswith('.json'):
        with open(f'{data_path}/{filename}', 'r') as fh:
            file_data = json.load(fh)
            real_data = file_data["_realData"]
            for key in real_data:
                if key == 'data':
                # check if tweet is already in data set
                    for tweet in real_data[key]:
                        total_tweets += 1
                        if tweet['id'] in agg_dict['data']['id_set']:
                            pass
                        else:
                           agg_dict['data']['id_set'].add(tweet['id'])
                           agg_dict['data']['data'].append(tweet)
                elif key == 'includes':
                    for inner_object, value in real_data[key].items():

                        for item in value:
                            if item['id'] in agg_dict['includes'][inner_object]['id_set']:
                                pass
                            else:
                                agg_dict['includes'][inner_object]['id_set'].add(item['id'])
                                agg_dict['includes'][inner_object]['data'].append(item)
                else:
                    agg_dict[key].extend(real_data[key])

out_dict = {'data': agg_dict['data']['data'],
            'includes': {
                'users': agg_dict['includes']['users']['data'],
                'tweets': agg_dict['includes']['tweets']['data'],
            },
            'errors': agg_dict['errors'],
            'meta': agg_dict['meta']}

with open('../data/gender_pay_gap_tweets.json', 'w') as fh:
    json.dump(out_dict, fh)
