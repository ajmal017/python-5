from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
import pandas as pd

def train_test_val(X, y, test_size):
     X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=7)
     X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.2, random_state=7)

     return X_train, X_test, X_val, y_val, y_train, y_test

def evaluate_acc(model, test_features, test_labels):
    """[Evaluate the accurarcy]
    
    Arguments:
        model {[Enter the model]} -- [description]
        test_features {[Enter the test features]} -- [description]
        test_labels {[enter the test labels]} -- [description]
    """

    predictions = model.predict(test_features)
    acc = accuracy_score(test_labels, predictions)
    print('Model Performance')
    print('Accuracy = {}%.'.format(acc))
    return(acc)

def rf_feature_importances(data, model):
    """[Plot all feature importances]
    
    Arguments:
        data {[Pandas DatasFrame]} -- [Enter the DataFrame with all features and labeled columns.]
        model {[RandomForrest Model]} -- [Enter the RandomForrest Model or the GridSearch optimized model.]
    """

    feats_rf = {} # a dict to hold feature_name: feature_importance
    
    for feature, importance in zip(data.columns, model.feature_importances_):
        feats_rf[feature] = importance #add the name/value pair 

    importances_rf = pd.DataFrame.from_dict(feats_rf, orient='index').rename(columns={0: 'Gini-importance'})
    importances_rf = importances_rf.sort_values(by='Gini-importance', ascending=False)

    import seaborn as sns
    fig = sns.barplot(x = importances_rf.index, y = importances_rf)

    return fig

def rf_compare_base(X_train, y_train, X_test, y_test, model):
    """[RF comapred to basemodel]
    
    Arguments:
        X_train {[Trainings data]} -- [description]
        y_train {[Trainings data]} -- [description]
        X_test {[Test data]} -- [description]
        y_test {[Test data]} -- [description]
        model {[RandomForest Model]} -- [Can be a GridSearch result or a normal model.]
    
    Returns:
        [Accuracy] -- [Uses the Accuracy function to print the calculated accuracy.]
    """

    from sklearn.ensemble import RandomForestClassifier

    # Create a RandomForest Base-Model
    base_model = RandomForestClassifier(n_estimators = 10, random_state = 7)
    base_model.fit(X_train, y_train)
    base_accuracy = evaluate_acc(base_model, X_test, y_test)

    try: 
        best_random = model.best_estimator_
        acc = evaluate_acc(best_random, X_test, y_test)
        return print('Improvement of {:0.2f}%.'.format( 100 * (acc - base_accuracy) / base_accuracy))

    except:
        acc = evaluate_acc(model, X_test, y_test)
        return print('Improvement of {:0.2f}%.'.format( 100 * (acc - base_accuracy) / base_accuracy))
