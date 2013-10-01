'''
Created on Sep 26, 2013

@author: kapild
'''
import numpy as np
import sklearn.linear_model as lm
from sklearn import svm
from sklearn import metrics,preprocessing,cross_validation
import pandas as p
from sklearn.ensemble import RandomForestRegressor
from sklearn.naive_bayes import MultinomialNB

rd = lm.LogisticRegression(penalty='l2', dual=True, tol=0.0001, 
                             C=1, fit_intercept=True, intercept_scaling=1.0, 
                             class_weight=None, random_state=None)

#my_svm =svm.SVC(kernel='linear', gamma=10, C=1,)
my_svm =svm.LinearSVC(penalty='l2', loss='l2', )


#rf = RandomForestRegressor(n_estimators=1000,verbose=2,n_jobs=20,min_samples_split=5,random_state=1034324)

naive = MultinomialNB(alpha=0.5)
trainer  = [ 
    ['lr' , rd],
    ['svm' , my_svm],
#    ['naive', naive], 
]


def run_cross_validation(X_train, y_train, X_test, cv=10):

#    raw_input('Press enter to run CV:')
    print "running cross validation on all methods:"
    best_method = None
    best_score = None
#    best_method_name  =None
    for name, method in trainer:
        print '\nrunning method:' + name
        score = np.mean(cross_validation.cross_val_score(method, X_train, y_train, cv=cv))
        print 'CV score for: ' + name + ' ' + str(score)
#        save_methods_accuracy_score( exp_type, name , score)
        if best_score is None or score > best_score:
            best_score = score
            best_method = method
#            best_method_name = name 
            print 'best method:' + name


    best_method.fit(X_train,y_train)

    pred = best_method.predict(X_test)
    exp_type = '_'
    testfile = p.read_csv('../data/test.tsv', sep="\t", na_values=['?'], index_col=1)
    pred_df = p.DataFrame(pred, index=testfile.index, columns=['label'])
    pred_df.to_csv("../data/results/" + exp_type + 'benchmark.csv')
    print "submission file created.."



if __name__ == '__main__':
    pass