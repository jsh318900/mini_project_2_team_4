from collections import Counter
import pandas as pd
import re

def get_all_food_counter(lunch_col, dinner_col):
	if type(lunch_col) != pd.Series or type(dinner_col) != pd.Series:
		raise ValueError('데이터프레임 칼럼을 각각 입력하세요.')
	
	food_counter = dict(Counter(parse_foods(lunch_col, dinner_col)))

	with open('filter_words.txt', 'r') as fd:
	    for word in fd:
	        if word.strip() in food_counter.keys():
	            food_counter.pop(word.strip())
	for food in list(food_counter.keys()):
	    if food.endswith('김치'):
	        food_counter.pop(food)
	    elif food.startswith('D'):
	        cnt = food_counter[food]
	        new_word = food[1:]
	        food_counter[new_word] = food_counter.setdefault(new_word, 0) + cnt
	        food_counter.pop(food)

	food_counter.pop('오징어')
	food_counter.pop('쇠고기')
	food_counter.pop('갈치')
	food_counter.pop('가지')
	food_counter.pop('간장')
	food_counter.pop('난')
	food_counter.pop('고등어')
	food_counter.pop('돈민찌')
	food_counter.pop('고추가루')
	food_counter.pop('고춧가루')
	food_counter.pop('등뼈')
	food_counter.pop('굴비')
	food_counter.pop('낙지')
	food_counter.pop('닭')
	food_counter.pop('장어')
	food_counter.pop('돈육')
	food_counter.pop('돈육국내산')
	food_counter.pop('동태')
	food_counter.pop('돼지고기')
	food_counter.pop('마늘')
	food_counter.pop('마늘만')
	food_counter['마늘바게트'] += food_counter['마늘바게뜨']
	food_counter['마늘바게트'] += food_counter['마늘빵']
	food_counter.pop('마늘바게뜨')
	food_counter.pop('마늘빵')

	food_counter['맑은국']
	pure_soup = ['맑은버섯국', '맑은계란국', '맑은버섯닭개장', '맑은버섯육개장', '맑은순두부국', '맑은연두부탕', '맑은장국']
	for s in pure_soup:
	    food_counter['맑은국'] += food_counter[s]
	    food_counter.pop(s)
	food_counter['콩나물국'] += food_counter['맑은콩나물국']
	food_counter.pop('맑은콩나물국')

	food_counter['망고드레싱'] += 10
	food_counter['샐러드'] += 3
	food_counter.pop('망고D')
	food_counter.pop('망고드레싱샐러드')

	food_counter.pop('열무')

	food_counter['매실주스'] += 1
	food_counter.pop('매실쥬스')

	food_counter.pop('명태')
	food_counter.pop('목살')
	food_counter.pop('무')
	food_counter.pop('무우')

	food_counter['감귤D'] = food_counter['감귤D'] + food_counter['밀감D']
	food_counter.pop('감귤D')
	food_counter.pop('밀감D')

	food_counter.pop('북어')


	food_counter.pop('삼겹')
	food_counter.pop('숙주들어감')

	food_counter.pop('오리')
	food_counter.pop('오리고기')

	food_counter.pop('콩')
	food_counter.pop('포클랜드')
	food_counter.pop('표고')

	return food_counter

def parse_foods(lunches, dinners):
    parsed_list = []
    splitters = ['.', ',', '/', ':', '+', '-', '*', '&', '<', '>', '(', ')']
    combined = list(lunches) + list(dinners)
    for d in combined:
        for sp in splitters:
            d = d.replace(sp, ' ')
        parsed_list.extend([x for x in d.split(' ') if len(x) > 0])
    return parsed_list