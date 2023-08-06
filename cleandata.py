import numpy as np
import pandas as pd

def unify_datetime(d):
    if 'Unnamed: 0' in d.columns:
        d['fecha_hora'] = d['Unnamed: 0'].fillna(d['Fecha_Hora'])
        del d['Unnamed: 0']
    elif 'Fecha_Hora' in d.columns:
        d['fecha_hora'] = d['Fecha_Hora']
    elif 'Unnamed: 0' in d.columns:
        d['fecha_hora'] = d['Unnamed: 0']
    
    d.index = pd.to_datetime(d['fecha_hora'])
    del d['Fecha_Hora']
    del d['fecha_hora']

def cleandata(file, porcentaje, datos):
    with open("DIEGO_DATA_PCA/" + file) as f:
        station = f.read().splitlines()

    frames = [pd.read_csv('DIEGO_DATA_PCA/' + s) for s in station]
    d = pd.concat(frames)

    if datos == 1:
        unify_datetime(d)

        k = abs((d[d == -9999.0]).sum()) / 9999.0
        to_delete = k >= len(d) * (porcentaje / 100)

        for i, delete in enumerate(to_delete):
            if delete:
                del d[d.columns[i]]
                del d[d.columns[i + 1]]

        d = d[~(d == -9999.0).any(axis=1)]
        calidad_columns = [col for col in d.columns if 'calidad' in col]

        for col in calidad_columns:
            d = d[~((d[col] >= 2.6) | (d[col] != 1.0))]

    elif datos == 2:
        unify_datetime(d)
        d = d[d.index.minute == 0]

        k = abs((d[d == -999.0]).sum()) / 999.0
        to_delete = k >= len(d) * (porcentaje / 100)

        for i, delete in enumerate(to_delete):
            if delete:
                del d[d.columns[i]]
                del d[d.columns[i + 1]]

        d = d[~(d == -999.0).any(axis=1)]
        calidad_columns = [col for col in d.columns if 'Calidad' in col]

        for col in calidad_columns:
            d = d[~((d[col] != 1.0))]

    elif datos == 3:
        unify_datetime(d)
        d = d[['pm25', 'calidad_pm25']]
        d = d[~(d['pm25'] == -9999.0)]
        d = d[~(d['calidad_pm25'] >= 2.6)]

    return d
