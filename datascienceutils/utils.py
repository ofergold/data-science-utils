import os
# Type checkers taken from here. http://stackoverflow.com/questions/25039626/find-numeric-columns-in-pandas-python
def is_type(df, baseType):
    import numpy as np
    import pandas as pd
    test = [issubclass(np.dtype(d).type, baseType) for d in df.dtypes]
    return pd.DataFrame(data = test, index = df.columns, columns = ["test"])

def calculate_anova(df, targetCol, sourceCol):
    from statsmodels.formula.api import ols
    lm = ols('conformity ~ C(%s, Sum)*C(%s, Sum)'% (targetCol, sourceCol),
            data=df).fit()
    table = sm.stats.anova_lm(lm, typ=2)
    return table

def is_float(df):
    import numpy as np
    return is_type(df, np.float)

def is_number(df):
    import numpy as np
    return is_type(df, np.number)

def is_integer(df):
    import numpy as np
    return is_type(df, np.integer)

def chunks(combos, size=9):
    for i in range(0, len(combos), size):
        yield combos[i:i + size]

# Sigh lightgbm insist this is the only wa
os.environ['LIGHTGBM_EXEC'] = os.path.join(os.getenv("HOME"), 'bin', 'lightgbm')
def get_model_obj(modelType, **kwargs):
    if modelType == 'knn':
        from sklearn.neighbors import KNeighborsClassifier
        # 6 seems to give the best trade-off between accuracy and precision
        knn = KNeighborsClassifier(n_neighbors=6, **kwargs)
        return knn
    elif modelType == 'gaussianNB':
        from sklearn.naive_bayes import GaussianNB
        gnb = GaussianNB(**kwargs)
        return gnb

    elif modelType == 'multinomialNB':
        from sklearn.naive_bayes import MultinomialNB
        # TODO: figure out how to configure binomial distribution
        mnb = MultinomialNB(**kwargs)
        return mnb

    elif modelType == 'bernoulliNB':
        from sklearn.naive_bayes import BernoulliNB
        bnb = BernoulliNB(**kwargs)
        return bnb

    elif modelType == 'randomForest':
        from sklearn.ensemble import RandomForestClassifier
        rfc = RandomForestClassifier(random_state=234, **kwargs)
        return rfc

    elif modelType == 'svm':
        from sklearn.svm import SVC
        svc = SVC(random_state=0, probability=True, **kwargs)
        return svc

    elif modelType == 'linearRegression':
        #assert column, "Column name required for building a linear model"
        #assert dataframe[column].shape == target.shape
        from sklearn import linear_model
        l_reg = linear_model.LinearRegression(**kwargs)
        return l_reg

    elif modelType == 'logisticRegression':
        from sklearn.linear_model import LogisticRegression
        log_reg = LogisticRegression(random_state=123, **kwargs)
        return log_reg

    elif modelType == 'kde':
         from sklearn.neighbors.kde import KernelDensity
         kde = KernelDensity(kernel='gaussian', bandwidth=0.2, **kwargs)
         return kde

    elif modelType == 'AR':
        import statsmodels.api as sm
        # fit an AR model and forecast
        ar_fitted = sm.tsa.AR(dataframe).fit(maxlag=9, method='mle', disp=-1, **kwargs)
        #ts_forecast = ar_fitted.predict(start='2008', end='2050')
        return ar_fitted

    elif modelType == 'SARIMAX':
        mod = sm.tsa.statespace.SARIMAX(df.riders, trend='n', order=(0,1,0),
                seasonal_order=(1,1,1,12), **kwargs)
        return mod

    elif modelType == 'sgd':
        # Online classifiers http://scikit-learn.org/stable/auto_examples/linear_model/plot_sgd_comparison.html
        from sklearn.linear_model import SGDClassifier
        sgd = SGDClassifier(**kwargs)
        return sgd

    elif modelType == 'perceptron':
        from sklearn.linear_model import Perceptron
        perceptron = Perceptron(**kwargs)
        return perceptron

    elif modelType == 'xgboost':
        import xgboost as xgb
        xgbm = xgb.XGBClassifier(**kwargs)
        return xgbm

    elif modelType == 'baseNN':
        from keras.models import Sequential
        from keras.layers import Dense
        # create model
        model = Sequential()
        assert args.get('inputParams', None)
        assert args.get('outputParams', None)
        model.add(Dense(inputParams))
        model.add(Dense(outputParams))
        if args.get('compileParams'):
            # Compile model
            model.compile(compileParams)# loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
        return model

    elif modelType == 'lightGBMRegression':
        from pylightgbm.models import GBMRegressor
        lgbm_lreg = GBMRegressor(   num_iterations=100, early_stopping_round=10,
                                    num_leaves=10, min_data_in_leaf=10)
        return lgbm_lreg

    elif modelType == 'lightGBMBinaryClass':
        from pylightgbm.models import GBMClassifier
        lgbm_bc = GBMClassifier(metric='binary_error', min_data_in_leaf=1)
        return lgbm_bc

    else:
        raise ''

