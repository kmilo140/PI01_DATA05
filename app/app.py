from fastapi import FastAPI
import pandas as pd

app = FastAPI()

data = pd.read_csv('https://raw.githubusercontent.com/kmilo140/PI01_DATA05/master/Datasets/data_string.csv')

def listaPalabrasDicFrec(listaPalabras):
    frecuenciaPalab = [listaPalabras.count(p) for p in listaPalabras]
    return dict(list(zip(listaPalabras, frecuenciaPalab)))

def ordenaDicFrec(dicFrec):
    aux = [(dicFrec[key], key) for key in dicFrec]
    aux.sort()
    aux.reverse()
    return aux

@app.get("/get_max_duration")
def get_max_duration(anio:int, plataforma:str, tipo:str):
    data.Duration = pd.to_numeric(data.Duration, errors='coerce')
    data.Release_year = pd.to_numeric(data.Release_year, errors='coerce')
    query1 = data[(data['Release_year'] == anio) & (data['Platform'] == plataforma) & (data['Type_duration'] == tipo) ]
    query1 = query1.sort_values('Duration', ascending = False)
    reply = query1.head(1)
    reply = reply .Title.to_list()

    return 'El contenido que mas dura es: ', str(''.join(reply))

@app.get("/get_count_plataform")
def get_count_plataform(plataforma:str):
    query2 = data['Platform'] == plataforma
    count_query2 = data[query2]['Type_duration'].value_counts()

    return {'Plataforma':plataforma,
            'Movies':str(count_query2[0]),
            'Tv show':str(count_query2[1]+count_query2[2])
            }

@app.get("/get_listedin")
def get_listedin(genero:str):
    plataforma = ''
    plats = data.Platform.unique()
    max = 0
    for plat in plats:
        if data[data.Platform == plat].Genre.str.count(genero).sum() > max:
            max = data[data.Platform == plat].Genre.str.count(genero).sum()
            plataforma = plat
    return (f'La plataforma con mas titulos listados en el genero {genero} es: {plataforma} con un total {max}')

@app.get("/get_actor")
def get_actor(plataforma:str, anio:int):
    act = data[(data['Platform'] == plataforma) & (data['Release_year'] == anio)].Cast.str.split(',')
    act = act.dropna()

    actores_año = []
    for actores in act:
        for actor in actores:
            actor = actor.rstrip()
            actor = actor.lstrip()
            if actor != 'undetermined':
                actores_año.append(actor)

    actor = listaPalabrasDicFrec(actores_año)
    actor = ordenaDicFrec(actor)
            
    return f'El actor que mas se repite en: {plataforma} en el año: {anio} es: {actor[0][1]} con un total de {actor[0][0]} '