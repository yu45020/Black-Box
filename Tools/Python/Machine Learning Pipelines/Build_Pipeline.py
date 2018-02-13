"""
TODO: Rewrite models's loss function with negative correlation. It has been used in ensemble neural networks.
https://pdfs.semanticscholar.org/5d90/3630f3c2bf8bd3f6a2c5a36f988ca6bd41ff.pdf

Goal: Provide a simple framework for building pipelines for machine learning.
User needs to explore data distribution and then customize the data cleaning process via sklearn pipeline.
Then the model will fine tune several models and compare their results. The best model will be returned.
Or user can also use ensemble method to average all the model results with fine tuned parameters.

Structure:
    1. Logger for model fitting
    2. Pipe for Process Data ( work with pd.DataFrame )
        Config "data_process_pipe" to change order
        a. MissionValueImputer : define funcs to impute & cache parameters
        b. AttributeAdder : define funcs to add/change columns
        c. DataSelector : subset data by number / category
            |    (numeric) DataFrameToArray: dataframe to array
            ---> |
                (category) Label_BinarizerV2 : encode into dummy columns

    3. Pipe for model fitting (work with numpy array )
        a. divine_buster : (core) grid search one model's parameters for pre-defined values
        b. fit : apply divine_buster on all models
    4. Models for cross validation and grid search
        a. regressor & regressor_metrics
        b. classifier & classifier_metrics

Example:
    dat = pd.read_csv("data_file.csv")
    dat["income_group"] = np.ceil(dat.median_income / 1.5)
    # subsample by key distribution
    dat["income_group"].where(dat.income_group < 5, other=5.0, inplace=True)
    split = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=1)
    for train_index, test_index in split.split(dat, dat.income_cat):
        dat_train = dat.loc[train_index]
        dat_test = dat.loc[test_index]
    dat_train_Y, dat_test_Y = dat_train['target'], dat_test['target']
    dat_train, dat_test = dat_train.drop(['target'], axis=1),   dat_test.drop(['target'], axis=1)

    Data_process_pipe  = DataProcessingPipe()
    dat_train = Data_process_pipe.fit_transform(dat_train)
    dat_test = Data_process_pipe.transform(dat_test)

    Divine_Buster = ModelFittingPipe(model_type='regression') # return the best model and use it to fit the data
    Divine_Buster.fit(dat_train, dat_train_Y, cv_folds=5, scoring_metric = 'neg_mean_squared_error',
    save_models=False)  # if random forest is large on save, reduce max_depth

    Divine_Buster.predict(dat_test)
    # or use Divine_Buster.divine_buster( same parameters ) to grid search a single model

"""
import functools
import logging
import time

import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier, BaggingRegressor
from sklearn.externals import joblib
from sklearn.linear_model import Lasso, Ridge, ElasticNet, BayesianRidge
from sklearn.model_selection import GridSearchCV
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor, NearestCentroid
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.preprocessing import LabelBinarizer
from sklearn.svm import LinearSVR, LinearSVC


# ++++++++++++++++++++++++++++++++++++++++++++++++++
#           Logger
# --------------------------------------------------
# catch exceptions during grid search and write in log
class Logger():
    def __init__(self):
        logging.basicConfig(filename='./model.log', filemode='w',
                            format='%(asctime)s %(levelname)s %(message)s'
                            )
        self.logger = logging.getLogger('logger')

    def __call__(self, *args, **kwargs):
        pass

    def runtime_recorder(self, func):
        """
        catch and log error during model fitting, and print run time
        :param func: divin_buster (gridsearch_cv on models)
        :return: None
        """

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                _t = time.time()
                result = func(*args, **kwargs)
                runtime = time.time() - _t
                print('Model is completed. Runtime:{0:.2f} '.format(runtime))
                return result
            except Exception as e:
                print("++++++++++++++++++++++++++++")
                print("Error. Info has been logged.")
                print("============================")
                self.logger.exception(e)

        return wrapper


# ++++++++++++++++++++++++++++++++++++++++++++++++++
#           Process Data pipe Config
# --------------------------------------------------
# Work with pandas dataframe

class MissingValueImputer(BaseEstimator, TransformerMixin):
    """
    Define method to impute missing value, and run upon fit(X,y),
    then cache the parameters and apply it on new data.
    """

    def __init__(self):
        self.cache = pd.Series()
        super().__init__()

    def imput_func(self, X):
        # suppose use median to impute missing values
        num_cols = X.select_dtypes(include=['float', 'int64'])
        col_median = num_cols.median(axis=0)
        self.cache = dict(zip(list(num_cols), col_median))
        return self

    def fit(self, X, y=None):
        self.imput_func(X)
        return self

    def transform(self, X, y=None):
        return X.fillna(value=self.cache, method=None, axis=0)


class AttributeAdder(BaseEstimator, TransformerMixin):

    def __init__(self):
        super().__init__()

    def attri_func(self, X):
        X['rooms_per_household'] = X['total_rooms'] / X['households']
        X['bedrooms_per_room'] = X['total_bedrooms'] / X['total_rooms']
        X['population_per_household'] = X['population'] / X['households']
        return X

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        return self.attri_func(X)


class DataSelector(BaseEstimator, TransformerMixin):
    # subset data either into numeric or category/object
    # numeric cols go to DataFrameToArray() to be np.array
    # category/object go to Label_BinarizerV2() to get dummy np.array

    def __init__(self, col_type):
        super().__init__()
        self.col_type = col_type

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        return X.select_dtypes(include=self.col_type)


class DataFrameToArray(TransformerMixin):
    def __init__(self):
        super().__init__()

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        return X.values


class Label_BinarizerV2(LabelBinarizer):
    """
    Convert categorical columns into dummy columns.
    Add parameters in fit and transform for building pipeline
    """

    def __init__(self):
        super().__init__()
        self.unique_types = {}

    def fit(self, y, X=None):
        # y is a dataframe with types: object & category
        self.unique_types = self.get_unique_types(y)
        return super().fit(y)

    def transform(self, y, X=None):
        unique_types = self.get_unique_types(y)
        new_types = self.get_unseen_types(y, unique_types)
        if not new_types.empty:
            print("The following unique values are not observed in the training data and are "
                  "ignored during one hot dummy encoding \n {}".format(new_types))
        return super().transform(y)

    def fit_transform(self, y, X=None):
        return self.fit(y).transform(y)

    def get_unique_types(self, y):
        col_names = list(y)
        unique_types = {}
        for col in col_names:
            unique_var = list(y[col].drop_duplicates())
            unique_types[col] = unique_var
        return unique_types

    def get_unseen_types(self, y, types_dict):
        # Find values in test data (types_dict) that are not in training data (self.unique_types)
        # skp (y,x) and read it as 2 loops starting from 'for y in ..."
        new_types = [(col, x, y[col].value_counts()[x])
                     for col in types_dict.keys()
                     for x in types_dict[col]
                     if x not in self.unique_types[col]]

        new_types = pd.DataFrame(new_types, columns=['Col names', 'New Types', 'Counts'])
        new_types.index += 1
        return new_types


# ++++++++++++++++++++++++++++++++++++++++++++++++++
#           Process Data Pipeline
# --------------------------------------------------
class DataProcessingPipe():
    def __init__(self):
        self.data_process_pipe = Pipeline([
            ('imputer', MissingValueImputer()),
            ('add_attri', AttributeAdder()),
            ("clean", FeatureUnion([
                ("numeric_pipe", Pipeline([
                    ('selector_n', DataSelector(col_type=['float', 'int64', 'int'])),
                    ('to_array', DataFrameToArray())
                ])),
                ('category_pipe', Pipeline([
                    ("selector_c", DataSelector(col_type=['object', 'category'])),
                    ("onehot", Label_BinarizerV2())
                ]))
            ]))

        ])

    def fit(self, X):
        return self.data_process_pipe.fit(X)

    def fit_transform(self, X, y=None, **fit_params):
        return self.data_process_pipe.fit_transform(X, y, **fit_params)

    def transform(self, X, y=None):
        return self.data_process_pipe.transform(X)


# ++++++++++++++++++++++++++++++++++++++++++++++++++
#           Fitting Model Pipeline
# --------------------------------------------------
class ModelFittingPipe():
    logger = Logger()

    def __init__(self, model_type='regression'):
        assert model_type in ['regression', 'classification'], "Wrong type, either 'regression' or 'classification'"
        self.model_type = model_type
        self.models_params = self.get_model_config(model_type)
        self.grid_res = {}  # nested { model name: {"best_score":[], "best_estimator":[], "best_params":[]}}
        self.scoring_metric = None

    def fit(self, X, y, cv_folds=5, scoring_metric="r2", save_models=False):
        self.scoring_metric = scoring_metric
        for model_name in self.models_params:
            model_ = self.models_params[model_name]['model']
            params_ = self.models_params[model_name]['params']
            print("Running model: {}".format(model_name))
            self.divine_buster(X=X, y=y, model_name=model_name, model=model_,
                               params=params_, cv=cv_folds, scoring=scoring_metric, save_model=save_models)

        best_model = self.get_best_model_name()
        print("Best model :{}".format(best_model))
        print("Best score :{}".format(self.grid_res[best_model]['best_score']))
        return self

    @logger.runtime_recorder
    def divine_buster(self, X, y, model_name, model, params, cv, scoring, save_model):
        grid_search = GridSearchCV(model, params, cv=cv, scoring=scoring, return_train_score=False, n_jobs=-1)
        grid_search.fit(X, y)
        self.grid_res[model_name]={
            'best_estimator': grid_search.best_estimator_,
            'best_score': grid_search.best_score_,
            'best_params':grid_search.best_params_
        }
        if save_model:
            joblib.dump(grid_search.best_estimator_, model_name + "best_estimator.gz", compress=3)
            print("Best model of {} is saved.".format(model_name))
        return self


    def SLB_avg_fit(self, X, y, save_model=False):
        # random forest on all fine tuned modes' prediction against true values
        model_name = 'ensemble_all'
        ensemble = RandomForestRegressor()
        params = {'max_features':['log2','sqrt','auto'],
                  "n_estimators": [240]}

        find_tuned_m = self.get_fine_tuned_models()
        models_pred = [x.predict(X) for x in find_tuned_m]
        models_pred = np.array(models_pred).T
        self.divine_buster(X=models_pred, y=y,
                           model_name=model_name, model=ensemble,
                           params=params, cv=5, scoring=self.scoring_metric,
                           save_model=save_model)
        print("Ensemble method's score: {}".format(self.grid_res[model_name]['best_score']))
        return self

    def SLB_avg_predict(self, X):
        find_tuned_m = self.get_fine_tuned_models()
        models_pred = [x.predict(X) for x in find_tuned_m]
        models_pred = np.array(models_pred).T
        return self.grid_res['ensemble_all']['best_estimator'].predict(models_pred)


    def predict(self, X):
        best_model = self.get_best_model_name()
        return self.grid_res[best_model]['best_estimator'].predict(X)


    def get_best_model_name(self):
        model_names = [x for x in list(self.grid_res) if x is not 'ensemble_all']
        scores = [self.grid_res[x]['best_score'] for x in model_names]
        best_id = scores.index(max(scores))
        return model_names[best_id]


    def get_fine_tuned_models(self):
        model_names= [x for x in list(self.models_params) if x is not 'ensemble_all']
        return [self.grid_res[x]['best_estimator'] for x in model_names]


    @staticmethod
    def get_model_config(model_type):
        if model_type == 'regression':
            return regressors
        elif model_type == 'classification':
            return classifiers
        else:
            raise ValueError("Model must be 'regression' or 'classification' ")

    def get_scoring_mtrics_options(self):
        if self.model_type == 'regression':
            return regressor_metrics
        elif self.model_type == 'classification':
            return classifier_metrics

    def get_all_model_results(self):
        res_pd = pd.DataFrame({"model": self.grid_res['model_name'],
                               "score": self.grid_res['best_score']})
        return res_pd.sort_values(by='score', ascending=False)


# ++++++++++++++++++++++++++++++++++++++++++++++++++
#           Model Configs for Grid Search and CV
# --------------------------------------------------
regressors = {
    'linear_lasso': {"model": Lasso(),
                     "params": {'alpha': [1e-3, 1e-2, 1e-1, 5, 10],
                                'normalize': [False],
                                'selection': ['random'],
                                'tol': [1e-4]
                                }
                     },
    'linear_ridge': {"model": Ridge(),
                     'params': {'alpha': [1e-4, 1e-3, 1e-2, 1e-1, 5, 10],
                                'normalize': [False],
                                'tol': [1e-4]
                                }
                     },
    "linear_support_vector": {"model": LinearSVR(),
                              'params': {"C": [1e-3, 1e-2, 1e-1, 1, 10],
                                         'loss': ["epsilon_insensitive", "squared_epsilon_insensitive"]
                                         }
                              },
    'elastic_net': {'model':ElasticNet(),
                    'params': {'alpha': [1e-1, 1e-2, 0.5, 1.0, 5.0, 10.0, 1.e2,1.e3],
                               'l1_ratio':[1e-1, 1e-2, 1e-3, 0.3,0.5,0.7,0.9]
                               }
                    },
    'bayes_ridge': { 'model': BayesianRidge(),
                     'params':{"alpha_1": [ 1e-6, 1e-7, 1e-5, 1e-3, 0.1],
                               'alpha_2': [ 1e-6, 1e-7, 1e-5, 1e-3, 0.1],
                               'lambda_1': [ 1e-6, 1e-7, 1e-5, 1e-3, 0.1],
                               'lambda_2': [ 1e-6, 1e-7, 1e-5, 1e-3, 0.1]
                               }

    },
    "random_forest": {'model': RandomForestRegressor(),
                      'params': {"n_estimators": [250],
                                 "max_features": ['auto', 'sqrt', 'log2'],
                                 'max_depth': [ 100 ]
                                 }
                      }
}



regressor_metrics = [
    'explained_variance',
    'neg_mean_absolute_error',
    'neg_mean_squared_error',
    'neg_mean_squared_log_error',
    'neg_median_absolute_error',
    'r2'
]

classifiers = {
    "navie_bayes_multi": {'model': MultinomialNB(),
                          'params': {"alpha": [1e-3, 1e-2, 1e-1, 1, 5, 10]
                                     }
                          },
    "navie_bayes_bern": {'model': BernoulliNB(),
                         'params': {"alpha": [1e-3, 1e-2, 1e-1, 1, 5, 10]
                                    }
                         },
    'knn': {'model': KNeighborsClassifier(),
            'params': {'n_neighbors': [3, 5, 7, 10],
                       'weights': ['uniform', 'distance'],
                       'p': [1, 2]  # 1 for manhattan dist, 2 for euclidean
                       }
            },
    'kncentroid': {'model': NearestCentroid(),
                   'params': {}},
    'linear_svm': {'model': LinearSVC(),
                   'params': {'penalty': ['l1', 'l2'],
                              'loss': ['hinge', 'squared_hinge'],
                              'tol': [1e-4],
                              'C': [1e-3, 1e-2, 0.1, 1, 5]
                              }
                   },
    'random_forest': {'model': RandomForestClassifier(),
                      'params': {'n_estimators': [500],
                                 'max_depth': [ 400 ],
                                 'criterion': ['gini'],
                                 'max_features': ['auto', 'sqrt', 'log2']}
                      }
}

classifier_metrics = [
    'accuracy',
    'average_precision',
    'f1',
    'f1_micro',
    'f1_macro',
    'f1_weighted',
    'f1_samples',
    'neg_log_loss',
]



if __name__ == '__main__':
    print("Configure pipelines before use")
    import numpy as np
    a = np.array([1,2,4,10,20,15])
    w = [0.4, 0.45, 0.5, 0.7, 0.9, 0.8]
    np.ma.average(a,weights=w)
    sum(a*w)/sum(w)
