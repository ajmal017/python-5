def data_clean(data):
    data["Age"]=data["Age"].fillna(data["Age"].dropna().median())

    # male und femal in 1 und 0 umwandeln

    data.loc[data["Sex"]=="male", "Sex"] = 0
    data.loc[data["Sex"]=="female", "Sex"] = 1

    data["Embarked"] = data["Embarked"].fillna("S")
    data.loc[data["Embarked"]=="S", "Embarked"] = 0
    data.loc[data["Embarked"]=="C", "Embarked"] = 1
    data.loc[data["Embarked"]=="Q", "Embarked"] = 2