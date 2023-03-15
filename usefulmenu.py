import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sklearn

#from sklearn.model_selection import train_test_split
#from sklearn.impute import SimpleImputer
#from sklearn.preprocessing import OrdinalEncoder
#from sklearn.preprocessing import OneHotEncoder
#from sklearn.preprocessing import StandardScaler
#from sklearn.preprocessing import MinMaxScaler
#from sklearn.preprocessing import FunctionTransformer
#from sklearn.pipeline import Pipeline
#from sklearn.base import BaseEstimator, TransformerMixin
#from sklearn.cluster import KMeans

import re
from collections import Counter
import operator

def usefulmenu(lunchmenu, dinnermenu):
    
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
    def __init__(self, meal_type1, meal_type2 = None):
        if meal_type1 != '중식' and meal_type1 != '석식':
            raise ValueError('Invalid meal type:', meal_type1, "'중식' 또는 '석식' 중 한가지로 입력해주세요")
        elif meal_type2 != '중식' and meal_type2 != '석식':
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
        
        mae_oom_idx2 = X[self.meal_type2 + '메뉴'].str.contains('매운|매콤|고추|짬뽕')
        
        X['매운' + self.meal_type2] =  mae_oom_idx2
        return X
