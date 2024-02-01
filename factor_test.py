import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def cal_ICIR(data: pd.DataFrame, feild: str) -> tuple[float, float]:
    """
    data is a dataframe with columns: date, return, factor feild
    feild is the factor name
    return IC and IR
    """
    data = data.loc[data.loc[:, 'date'] < "2022-01-01", ['date', 'return', feild]]
    data.dropna(inplace=True)
    IC_dataframe = data.groupby('date').apply(lambda x: x.corr(method='spearman')[feild]['return'])
    return IC_dataframe.mean(), IC_dataframe.mean()/IC_dataframe.std()

def test_factor(ICIR: tuple[float, float]) -> str:
    """
    ICIR is a tuple of IC and IR
    return the test result
    """
    if abs(ICIR[0]) > 0.01 and abs(ICIR[1]) > 0.03:
        return 'pass'
    else:
        return 'fail'

if __name__ == '__main__':
    data = pd.read_csv('factor_pass6.csv', index_col=0)
    colname = data.columns.tolist()
    other_info = colname[:3]
    factorname = colname[3:]
    pass_list = []
    for i in factorname:
        if i == 'return':
            continue
        ICIR = cal_ICIR(data, i)
        print(i)
        print(ICIR)
        result = test_factor(ICIR)
        if result == 'pass':
            pass_list.append(i)
        print(result)
    data.loc[:, other_info + pass_list + ['return']].to_csv('factor_pass.csv')