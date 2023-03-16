import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin

class MorningDropper(BaseEstimator, TransformerMixin):
    '''
    입력받은 DataFrame에서 '조식메뉴' columns을 drop하여 반환한다.
    '''
    def fit(self, X, y=None):
        return self
    
    def transform(self, X, y=None):
        return X.drop(['조식메뉴'], axis=1)

    def set_output(self, transform):
        return

    
class DayMonthMaker(BaseEstimator, TransformerMixin):
    '''
    입력받은 DateFrame에서 '일자' column의 type을
    object에서 datetime으로 변환한다.
    type이 변환된 '일자' column을 활용해 새로운 칼럼 '연도'과'월'을 생성한다.
    '''
    def fit(self, X, y=None):
        return self
    
    def transform(self, X, y=None):
        X = X.copy()
        X['일자'] = pd.to_datetime(X['일자'])
        X['연도'] = X['일자'].apply(lambda X : X.year)
        X['월'] = X['일자'].apply(lambda X : X.month)
        return X

    def set_output(self, transform):
        return


class OfficeCount(BaseEstimator, TransformerMixin):
    '''
    입력받은 DateFrame에서 '사무실출근자수' column을 생성한다.
    '사무실출근자수'는 '본사정원수'에서 '본사휴가자수', '본사출장자수', '현본사소속재택근무자수'를 뺀 값이다.
    '''
    def fit(self, X, y=None):
        return self
    
    def transform(self, X, y=None):
        X = X.copy()
        X['사무실출근자수'] = X['본사정원수'] - (X['본사휴가자수'] + X['본사출장자수'] + X['현본사소속재택근무자수'])
        return X

    def set_output(self, transform):
        return


class DayofWeekOHE(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self
    
    def transform(self, X, y=None):
        X = X.copy()
        X = pd.concat([pd.get_dummies(X['요일'], prefix='요일'), X], axis=1)
        return X

    def set_output(self, transform):
        return

