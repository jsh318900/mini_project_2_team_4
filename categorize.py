import pandas as pd

from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import MinMaxScaler

"""
데이터 탐색단계에서 미리 도출한 재료들의 카테고리

식단에 있는 메뉴들 중에서, 각 카테고리에 포함되어있는 단어를 하나라도 포함하면 그 카테고리에 속한다고 가정한다.

예시) '삼겹살부추볶음'은 육류 단어인 삼겹도 포함하고 채소2 단어인 부추도 포함하기때문에 분류 육류와 채소2에 모두 해당하는 음식이다.
"""
CATEGORIES = {
'해산물' : '가자미 갈치 고등어 꽁치 동태 황태 북어 코다리 낙지 오정어 쭈꾸미 새우 다시마 파래 미역'.split(' '),
'조미료': '가쯔오 간장 겨자 양념 고추장 된장 로제 케찹 초장 마늘'.split(' '),
'알': '계란 메추리알'.split(' '),
'채소1': '감자 고구마 호박 무'.split(' '),
'채소2': '나물 치커리 상추 깻잎 청경채 봄동 배추 부추 새싹 시금치 시래기 얼갈이 근대'.split(' '),
'채소3': '토마토 브로컬리 브로콜리 도라지 오이 버섯'.split(' '),
'육류': '삼겹 고기 닭 돼지 돈육 오리 차돌박이'.split(' '),
'과일': '과일 딸기 레몬 사과 오렌지 바나나 귤'.split(' '),
'가공식품1': '피클 단무지 맛살 어묵 비엔나 미트볼 순대'.split(' '),
'가공식품2': '두부 곤약 묵 떡 김치'.split(' '),
'곡물': '들깨 땅콩 수수 현미 흑미'.split(' '),
'면류': '파스타 우동 국수 냉면 비빔면 소면'.split(' ')
}

class MenuCategorizer(BaseEstimator, TransformerMixin):
	"""
	MenuCategorizer 변환기 옵션들

	include_lunch:  기본값 True.  True일 때 중식식단을 분류화한다. False이면 중식식단칼럼은 무시한다.
	include_dinner: 기본값 True.  True일 때 석식식단을 분류화한다. False이면 석식식단칼럼은 무사한다.
	lunch_cat:      기본값 None.  중식식단 분류화할 칼럼 리스트 ex) ['채소1', '채소2']이면 각 채소1과 채소2에 해당하는 음식들만 확인한다.
                                 None이면 가능한 모든 분류를 확인한다.
	dinner_cat:     기본값 None.  석식식단 분류화할 칼럼 리스트 ex) ['채소1', '채소2']이면 각 채소1과 채소2에 해당하는 음식들만 확인한다.
	                             None이면 가능한 모든 분류를 확인한다.
	"""
	def __init__(self, include_lunch=True, include_dinner=True, lunch_cat=None, dinner_cat=None):
		self.include_lunch = include_lunch
		self.include_dinner = include_dinner
		self.lunch_cat = lunch_cat
		self.dinner_cat = dinner_cat

	def fit(self, X, y=None):
		return self

	def transform(self, X, y=None):
		X = X.copy()
		if self.include_lunch:
			if self.lunch_cat is None:
				categories = CATEGORIES.keys()
			else:
				categories = self.lunch_cat

			for cat in categories:
				X['중식_' + cat] = X['중식메뉴'].apply(lambda x : count_hit(cat, x))

		if self.include_dinner:
			if self.dinner_cat is None:
				categories = CATEGORIES.keys()
			else:
				categories = self.dinner_cat

			for cat in categories:
				X['석식_' + cat] = X['석식메뉴'].apply(lambda x : count_hit(cat, x))
		return X

class RatingCalculator(BaseEstimator, TransformerMixin):

	def __init__(self, meal_type):
		if meal_type != '중식' and meal_type != '석식':
			raise ValueError('Invalid meal type:', meal_type, '"중식" 또는 "석식"중 한가지로 입력해주세요.')
		self.meal_type = meal_type

	def fit(self, X, y):
		menus = X[self.meal_type + '메뉴']
		ratings = y / X['사무실출근자수'].values.reshape(-1, 1)

		ratings = pd.DataFrame(MinMaxScaler().fit_transform(ratings), index=ratings.index, columns=ratings.columns)
		ratings = ratings[self.meal_type + '계']

		appearance_counts_per_cat = {}
		rating_sum_per_cat = {}

		for row in X.index:
			for cat in CATEGORIES:
				cnt = 0
				keywords = CATEGORIES[cat]
				for key in keywords:
					if key in menus[row]:
						cnt = 1
				if cnt > 0:
					appearance_counts_per_cat[cat] = appearance_counts_per_cat.setdefault(cat, 0) + 1
					rating_sum_per_cat[cat] = rating_sum_per_cat.setdefault(cat, 0) + ratings[row]

		for k in rating_sum_per_cat:
			rating_sum_per_cat[k] /= appearance_counts_per_cat[cat]

		self.cat_ratings = rating_sum_per_cat
		return self

	def transform(self, X, y=None):
		X = X.copy()
		X[self.meal_type + '_선호도점수'] = X[self.meal_type + '메뉴'].apply(self._calculate_menu_rating)
		return X

	def _calculate_menu_rating(self, menu_string):
		menu_string = remove_origin(menu_string)
		total_hit_cnt = 0
		rating_sum = 0
		for cat in CATEGORIES:
			hit_cnt = count_hit(cat, menu_string)
			total_hit_cnt += hit_cnt
			rating_sum += hit_cnt * self.cat_ratings[cat]
		if total_hit_cnt == 0:
			return 0.0
		else:
			return rating_sum / total_hit_cnt

def count_hit(category, menu_string):
	if category not in CATEGORIES:
		raise ValueError('unknown category:', category)

	cnt = 0
	menus = ' '.join([x for x in remove_origin(menu_string).split(' ') if len(x) > 0 and not (x.endswith('김치') or x.startswith('쌀'))])
	for food_cat in CATEGORIES[category]:
		if food_cat in menus:
				cnt += 1
	return cnt

def remove_origin(menu_string):
	i = 0
	while i < len(menu_string) and menu_string[i] != '(':
		i += 1

	j = i + 1
	while j < len(menu_string) and menu_string[j] != ')':
		j += 1

	if i < j and i < len(menu_string) and j < len(menu_string):
		return remove_origin(menu_string[:i] + menu_string[j + 1:])
	else:
		return menu_string
