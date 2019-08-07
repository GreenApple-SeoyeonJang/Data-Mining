import pandas as pd
import cmath

train = pd.read_csv("train.csv")
test = pd.read_csv("test.csv")

train = train.drop(['PassengerId', 'Name', 'Ticket', 'Fare', 'Cabin'], axis=1)  #Feature Selection
test = test.drop(['Name', 'Ticket', 'Fare', 'Cabin'], axis=1)

sex_train = pd.get_dummies(train['Sex'])
sex_test = pd.get_dummies(test['Sex'])
sex_train.columns = ['Female', 'Male'] #sex -> Female / Male
sex_test.columns = ['Female', 'Male']
train.drop(['Sex'], axis=1, inplace=True)
test.drop(['Sex'], axis=1, inplace=True)
train = train.join(sex_train)
test = test.join(sex_test)

train["Age"].fillna(30, inplace=True)
test["Age"].fillna(30, inplace=True)

embarked_train = pd.get_dummies(train['Embarked'])
embarked_test = pd.get_dummies(test['Embarked'])
embarked_train.columns = ['C', 'Q', 'S'] #Embarked -> C / Q / S
embarked_test.columns = ['C', 'Q', 'S']
train.drop(['Embarked'], axis=1, inplace=True)
test.drop(['Embarked'], axis=1, inplace=True)

train = train.join(embarked_train)
test = test.join(embarked_test)

# w 랜덤값 지정
w0 = 0.4
w1 = 0.3
w2 = 0.3
w3 = 0.3
w4 = 0.3
w5 = 0.3
w6 = 0.3
w7 = 0.3
w8 = 0.3
w9 = 0.3

alpha = 0.001
count = 0
m = int(train.size/10)

while count <= 10000:
    count = count + 1
    sigma0 = 0
    sigma1 = 0
    sigma2 = 0
    sigma3 = 0
    sigma4 = 0
    sigma5 = 0
    sigma6 = 0
    sigma7 = 0
    sigma8 = 0
    sigma9 = 0

    for i in range(0, m): #편미분 구하는 FOR문
        z = w0 + (w1*train["Pclass"][i]) + (w2*train["Age"][i]) + (w3*train["SibSp"][i]) + (w4*train["Parch"][i]) + (w5*train["Female"][i]) + (w6*train["Male"][i]) + (w7*train["C"][i]) + (w8*train["S"][i]) + (w9*train["Q"][i])
        hxi = 1.0 / (1 + cmath.exp(-z))
        common = hxi - train["Survived"][i]
        sigma0 = sigma0 + common
        sigma1 = sigma1 + (common * train["Pclass"][i])
        sigma2 = sigma2 + (common * train["Age"][i])
        sigma3 = sigma3 + (common * train["SibSp"][i])
        sigma4 = sigma4 + (common * train["Parch"][i])
        sigma5 = sigma5 + (common * train["Female"][i])
        sigma6 = sigma6 + (common * train["Male"][i])
        sigma7 = sigma7 + (common * train["C"][i])
        sigma8 = sigma8 + (common * train["S"][i])
        sigma9 = sigma9 + (common * train["Q"][i])

#매개변수w 업데이트
    w0 = w0 - (alpha * (1 / m) * sigma0)
    w1 = w1 - (alpha * (1 / m) * sigma1)
    w2 = w2 - (alpha * (1 / m) * sigma2)
    w3 = w3 - (alpha * (1 / m) * sigma3)
    w4 = w4 - (alpha * (1 / m) * sigma4)
    w5 = w5 - (alpha * (1 / m) * sigma5)
    w6 = w6 - (alpha * (1 / m) * sigma6)
    w7 = w7 - (alpha * (1 / m) * sigma7)
    w8 = w8 - (alpha * (1 / m) * sigma8)
    w9 = w9 - (alpha * (1 / m) * sigma9)

s = int(test.size/10)
prediction = []

for j in range(0, s):
    p_z = w0 + (w1 * test["Pclass"][j]) + (w2 * test["Age"][j]) + (w3 * test["SibSp"][j]) + (w4 * test["Parch"][j]) + (w5 * test["Female"][j]) + (w6 * test["Male"][j]) + (w7 * test["C"][j]) + (w8 * test["S"][j]) + (w9 * test["Q"][j])
    py = 1.0 / (1 + cmath.exp(-p_z))
    if py.real >= 0.5:
        prediction.append(1)
    else:
        prediction.append(0)

submission = pd.DataFrame({ "PassengerId": test["PassengerId"], "Survived": prediction})
submission.to_csv('1610861.csv', index=False)