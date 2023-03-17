import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sklearn

import re
from collections import Counter
import operator

def usefulmenu(lunchmenu, dinnermenu):
    '''
    중/석식 메뉴 칼럼에 대한 전처리 함수. 
    구내식당 방문 결정에 있어서 미약한 영향력을 지닌 메뉴들을 drop 처리하는 것이 목적이다.
    1) 입력받은 DataFrame에서 중/석식에 있는 모든 메뉴리스트에 대하여 등장 빈도수 순으로 튜플 리스트로 변환한다.
    2) 위에서 메뉴가 아닌 것[원산지 표기, 원재료 표기, 메뉴 설명('자기계발의날')] + 영향력이 떨어지는 메뉴[쌀밥 /쌈장 / 간장 / 포기김치 / 라면사리] 들을 제외시킨 결과물 튜플 리스트를 반환한다.
    '''
    
    lunchmenu = list(lunchmenu)
    dinnermenu = list(dinnermenu)
    daymenu = lunchmenu + dinnermenu


    #marks = ['(', ')', ':', ' ', '*', '/']

    menu1_list = []

    for menus in daymenu:   
        menu1 = menus.replace('(', ' ')
        menu1 = menu1.replace(')', ' ')
        menu1 = menu1.replace(':', ' ')
        menu1 = menu1.replace('*', ' ')
        menu1 = menu1.replace('/', ' ')
        menu1 = menu1.replace(',', ' ')
        menu1 = menu1.replace('.', ' ')
        menu1 = menu1.replace('&', ' ')
        menu1 = re.split(r' ', menu1)
        menu1_list.extend(menu1)
        

    menu_list= [menu for menu in menu1_list if menu != '' ]

    drop_menu = pd.read_csv('drop_menu.csv')
    drop = drop_menu['Menu']


    menu_cnt = dict(Counter(menu_list))

    for d in drop:
        menu_cnt.pop(d)
        
    menu_cnt = sorted(menu_cnt.items(), key = operator.itemgetter(1), 
                          reverse = True)

    return menu_cnt


from sklearn.base import BaseEstimator, TransformerMixin


class SpicyViewer(BaseEstimator, TransformerMixin):
    '''
    중/석식 메뉴 칼럼의 각 행에 대해 매운 음식이 포함되어있는지를 확인하는 특성 추출 변환기.
    중식/석식 칼럼을 각각, 한번에 처리하여 -> '매운중식' /'매운석식' 칼럼을 반환한다.
    메뉴의 이름 중 ['매운'/'매콤'/'고추'/'짬뽕'] 이 들어가 있으면 True, 없으면 False를 값으로써 반환한다.
    meal_type1은 필수값, meal_type2는 옵션이며 '중식' 또는 '석식'을 입력한다.
    '''
    
    def __init__(self, meal_type1, meal_type2 = None):
        '''
        meal_type1은 필수값, meal_type2는 옵션으로, '중식' 또는 '석식'을 입력한다.
        '''
        
        if meal_type1 != '중식' and meal_type1 != '석식':
            raise ValueError('Invalid meal type:', meal_type1, "'중식' 또는 '석식' 중 한가지로 입력해주세요")
        elif meal_type2 != '중식' and meal_type2 != '석식' and meal_type2 != None:
              raise ValueError('Invalid meal type:', meal_type2, "'중식' 또는 '석식' 중 한가지로 입력해주세요")
        self.meal_type1 = meal_type1
        self.meal_type2 = meal_type2
    
    def fit(self, X, y = None):
        return self
    
    def transform(self, X):
        
        #X는 전체 DataFrame
        X = X.copy()
        mae_oom_idx1 = X[self.meal_type1 + '메뉴'].str.contains('매운|매콤|고추|짬뽕')
        X['매운' + self.meal_type1] =  mae_oom_idx1
        
        if self.meal_type2 != None: 
            mae_oom_idx2 = X[self.meal_type2 + '메뉴'].str.contains('매운|매콤|고추|짬뽕') 
            X['매운' + self.meal_type2] =  mae_oom_idx2
            
        return X
