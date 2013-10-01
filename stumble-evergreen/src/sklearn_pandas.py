import numpy as np
import scipy as sp
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.feature_extraction import DictVectorizer
from sklearn import cross_validation

#
#def cross_val_score(estimator, X, *args, **kwargs):
#    class DataFrameWrapper(object):
#        def __init__(self, df):
#            self.df = df
#
#        def __eq__(self, other):
#            return self.df is other.df
#
#    class DataFrameMapper(BaseEstimator):
#        def __init__(self, estimator, X):
#            self.estimator = estimator
#            self.X = X
#
#        def fit(self, x, y):
#            self.estimator.fit(self._get_row_subset(x), y)
#            return self
#
#        def transform(self, x):
#            return self.estimator.transform(self._get_row_subset(x))
#
#        def predict(self, x):
#            return self.estimator.predict(self._get_row_subset(x))
#
#        def _get_row_subset(self, rows):
#            return self.X.df.iloc[rows].reset_index(drop=True)
#
#    X_indices = range(len(X))
#    X_wrapped = DataFrameWrapper(X)
#    df = DataFrameMapper(estimator, X_wrapped)
#    return cross_validation.cross_val_score(df, X_indices, *args, **kwargs)
#
class DataFrameMapper(BaseEstimator, TransformerMixin):
    def __init__(self, features, sparse=True):
        self.features = features
        self.sparse = sparse

    def dict_data(self, X, column):
        rows = []
        # vectorize those dicts
        for index in X[column].index:
            rows.append({column : X[column][index]})
        return rows

    
    def fit(self, X, y=None):
        for columns, transformer in self.features:
            try:
                print 'fitting :' + str(columns)
                if isinstance(transformer, DictVectorizer):
                    print 'is a Dict:' + str(columns)
                    transformer.fit(self.dict_data(X, columns))
                else:
                    transformer.fit(X[columns], y)
            except TypeError:
                transformer.fit((X[columns]))
        return self

    def transform(self, X):
        extracted = []
        for columns, transformer in self.features:
            if isinstance(transformer, DictVectorizer):
                fea = transformer.transform(self.dict_data(X, columns))
            else:
                fea = transformer.transform(X[columns])
            if hasattr(fea, "toarray"):
                if self.sparse:
                    extracted.append(fea)
                else:
                    extracted.append(fea.toarray())
            else:
                if len(fea.shape) == 1:
                    fea = np.array([fea]).T
                extracted.append(fea)
        if len(extracted) > 1:
            if self.sparse:
                return sp.sparse.hstack(extracted)
            else:
                return sp.hstack(extracted)
        else:
            return extracted[0]
