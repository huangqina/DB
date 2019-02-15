import pandas as pd

print('input defects')
defect = input()
data = pd.DataFrame(eval(defect))
data.to_csv('./csv/defects.csv',encoding='utf-8')
