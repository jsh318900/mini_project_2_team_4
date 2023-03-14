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
