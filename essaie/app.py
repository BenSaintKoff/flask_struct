import pandas as pd
import numpy as np
import os
from flask import *


main = Blueprint('main', __name__)

maladies = pd.read_csv(r'./essaie/data/arret.csv', sep=';')
all_agent = pd.read_csv(r'./essaie/data/matricule_ges.txt', sep=';', encoding='latin')
conges = pd.read_excel(r'./essaie/data/conges.xlsx')
df_maladie = maladies
df_maladie.rename(columns={'idArret': 'Code client', 'datecreation': 'Date de creation', 'datedebut': 'Date de debut',
                   'datefin': 'Date de fin', 'nombrejour': 'Nombre de jour', 'datereprise': 'Date de reprise',
                   'agent_matricule': 'Matricule'}, inplace=True)



@main.route('/')
def index():
    return {"hello": "world"}


@main.route('/api/arret/maladie', methods=['GET'])
def api_maladies():
    if os.path.isfile('./essaie/data/arret.csv'):
        # df = maladies.loc[maladies['agent_matricule'].astype(str).isin(all_agent['CUTI_S'].astype(str).str.strip().unique())]
        df = maladies
        df.rename(columns={'idArret': 'Code client', 'datecreation': 'Date de creation', 'datedebut': 'Date de debut', 'datefin': 'Date de fin', 'nombrejour': 'Nombre de jour', 'datereprise': 'Date de reprise', 'agent_matricule': 'Matricule'}, inplace=True)
        col = ['Code client', 'Date de creation', 'Date de debut', 'Date de fin', 'Nombre de jour', 'Date de reprise', 'Matricule']
        columns = [{'Header': c, 'accessor': c} for c in col]
        data = df[col].fillna('null').to_dict(orient='records')
        return jsonify({'columns': columns, 'data': data}), 200


@main.route('/api/top/conges')
def api_conges():
    df = conges
    df.rename(columns={'ID': 'Code client', 'Nom et Prénoms du salarié': 'Nom et Prenom du salarie', 'Date de début': 'Date de debut', 'Nombre de jour ': 'Nombre de jour'}, inplace=True)
    col = ['Code client', 'Matricule', 'Nom et Prenom du salarie', 'Date de debut', 'Date de fin', 'Date de reprise', 'Nombre de jour', 'Service', 'Direction']
    columns = [{'Header': c, 'accessor': c} for c in col]
    data = df[col].fillna('null').to_dict(orient='records')
    return jsonify({'columns': columns, 'data': data}), 200


def search_agent_malade(code):
    #df = maladies
    #df.rename(columns={'idArret': 'Code client', 'datecreation': 'Date de creation', 'datedebut': 'Date de debut', 'datefin': 'Date de fin', 'nombrejour': 'Nombre de jour', 'datereprise': 'Date de reprise', 'agent_matricule': 'Matricule'}, inplace=True)
    df_maladie = maladies
    df_maladie.rename(columns={'idArret': 'Code client', 'datecreation': 'Date de creation', 'datedebut': 'Date de debut', 'datefin': 'Date de fin', 'nombrejour': 'Nombre de jour', 'datereprise': 'Date de reprise', 'agent_matricule': 'Matricule'}, inplace=True)
    malade_code = df_maladie['Code client']
    filename=''
    for f in malade_code.values:

        if int(f) == int(code):
            filename = f
            break
        if filename!='':
            break
    return filename


@main.route('/api/post/maladie', methods=['POST'])
def agent_malade():
    PostJson = request.get_json()
    file = PostJson.get('file')
    url = PostJson.get('url')
    print('test',file)

    # file = int(file)
    filename = search_agent_malade(file)
    print('test2',filename)

    if filename != '':
        print(filename)
        print(file)
        codeclient = str(df_maladie.loc[df_maladie['Code client'].astype(int)==int(file), 'Code client'].iloc[0])
        #print(codeclient)
        datecreation = str(df_maladie.loc[df_maladie['Code client'].astype(int)==int(file), 'Date de creation'].iloc[0])
        datedebut = str(df_maladie.loc[df_maladie['Code client'].astype(int)==int(file), 'Date de debut'].iloc[0])
        datefin = str(df_maladie.loc[df_maladie['Code client'].astype(int)==int(file), 'Date de fin'].iloc[0])
        nombrejour = str(df_maladie.loc[df_maladie['Code client'].astype(int)==int(file), 'Nombre de jour'].iloc[0])
        datereprise = str(df_maladie.loc[df_maladie['Code client'].astype(int)==int(file), 'Date de reprise'].iloc[0])
        matricule = str(df_maladie.loc[df_maladie['Code client'].astype(int)==int(file), 'Matricule'].iloc[0])

    elif filename == '':
        codeclient=''
        datecreation=''
        datedebut=''
        datefin=''
        nombrejour=''
        datereprise=''
        matricule=''

    return jsonify({'Code client': codeclient, 'Date de creation': datecreation, 'Date de debut': datedebut, 'Date de fin': datefin, 'Nombre de jour': nombrejour, 'Date de reprise': datereprise, 'Matricule': matricule})


if __name__ == "__main__":
    main.run(debug=True)

