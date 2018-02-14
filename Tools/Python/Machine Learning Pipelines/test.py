from sklearn.metrics import r2_score, mean_squared_error
from sklearn.mixture import GaussianMixture, BayesianGaussianMixture
from sklearn.model_selection import StratifiedShuffleSplit
import pandas as pd
import numpy as np
from Build_Pipeline import *


dat = pd.read_csv("housing.csv")
dat['median_income_group'] = np.ceil(dat.median_income/1.5)

splitter = StratifiedShuffleSplit(n_splits=1, test_size=0.9,random_state=1)

for train_index, test_index in splitter.split(dat, dat.median_income_group):
    dat_train = dat.loc[train_index]
    dat_test = dat.loc[test_index]

for set in (dat, dat_train, dat_test):
    set.drop("median_income_group", axis=1,inplace=True)

dat_train_Y = dat_train['median_house_value']
dat_train = dat_train.drop(['median_house_value'], axis=1)

dat_test_Y = dat_test['median_house_value']
dat_test = dat_test.drop(['median_house_value'], axis=1)


pipe = DataProcessingPipe()
dat_train = pipe.fit_transform(dat_train)
dat_test = pipe.transform(dat_test)

model = ModelFittingPipe('regression')
model.fit(dat_train, dat_train_Y, scoring_metric='r2')
predict = model.predict(dat_train)

model.SLB_avg_fit(dat_train, dat_train_Y)

predict_test = model.predict(dat_test)
pred_test = model.SLB_avg_predict(dat_test)
r2_score(dat_test_Y,predict_test)
r2_score(dat_test_Y,pred_test)


from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR

find_tuned_m = model.get_fine_tuned_models()
model_pred = [x.predict(dat_train) for x in find_tuned_m]
model_pred = np.array(model_pred).T
model_pred_test = [x.predict(dat_test) for x in find_tuned_m]
model_pred_test = np.array(model_pred_test).T

grid = GridSearchCV(SVR(), param_grid={"C":[1e-3,1e-1,1e-5],
                                       "kernel":['sigmoid']},scoring='r2',
                    n_jobs=-1, cv=5)
grid.fit(model_pred, dat_train_Y)
grid.best_estimator_
SVR_pred = grid.predict(model_pred)
SVR_pred_test = grid.predict(model_pred_test)
r2_score(dat_train_Y, SVR_pred)
r2_score(dat_test_Y, SVR_pred_test)

lm = LinearRegression(n_jobs=-1,normalize=True)
lm.fit(X=model_pred, y=dat_train_Y)
lm_pre = lm.predict(model_pred_test)
r2_score(dat_test_Y, lm_pre)

