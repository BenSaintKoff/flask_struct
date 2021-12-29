from flask import *
import numpy as np
import pandas as pd
import datetime
import os
from sqlalchemy import create_engine
from flask_jwt_extended import (JWTManager, create_access_token,create_refresh_token, jwt_required,get_jwt_identity)
#,jwt_refresh_token_required,

maladies = pd.read_csv(r'./essaie/data/arret.csv', sep=';')
conges = pd.read_excel(r'./essaie/data/conges.xlsx')
all_agent = pd.read_csv(r'./essaie/data/matricule_ges.txt', sep=';', encoding='latin')
take_all = all_agent.shape[0]
#print(take_all)


pilotage = Blueprint('pilotage', __name__)


'''@pilotage.route('/api/get/stat/top/conges', methods=['GET'])
def get_conges():
    all_agent['CUTI_S'] = all_agent['CUTI_S'].astype(str).str.strip()
    df = all_agent.loc[all_agent['CUTI_S'].isin(conges['Matricule'].astype(str).unique())]
    take_one = df.shape[0]
    print(take_one)
    x = 100
    y = int((take_one * 100) / take_all)
    z = x - y
    z = int(z)
    stat = {'x': x, 'y': y, 'z': z}
    return jsonify({'stat': stat}), 200'''


@pilotage.route('/api/get/stat/top/conges', methods=['GET'])
def get_conges():
    all_agent['CUTI_S'] = all_agent['CUTI_S'].astype(str).str.strip()
    stat = {'x': [], 'y': [], 'z': []}
    df = all_agent.loc[all_agent['CUTI_S'].isin(conges['Matricule'].astype(str).unique())]
    take_one = df.shape[0]
    print(take_one)
    # taux_un = all_agent.loc[(all_agent['CUTI_S'].isin(conges['Matricule'])) & (conges['Statut congé'] == 'VALIDE')].shape[0]
    # taux_deux = all_agent.shape[0]
    result_one = int((take_one * 100) / take_all)
    result_two = (take_one * 1) / take_all
    x = ['conges', 'pas conges']
    y = [round(result_one, 2), round(100 - result_one, 2)]
    z = [round(result_two, 2), round(1 - result_two, 2)]
    stat['x'].append(x)
    stat['y'].append(y)
    stat['z'].append(z)
    return jsonify({'stat': stat}), 200


@pilotage.route('/api/get/stat/arret/maladie', methods=['GET'])
def get_maladies():
    # if os.path.isfile('./essaie/Data/controleur_stat.csv'):
    # stat = {'name': [], 'non controlé': [], 'rejet': [], 'valider': [], 'non_traite_montant': [], 'rejet_montant': [], 'valider_montant': []}
    all_agent['CUTI_S'] = all_agent['CUTI_S'].astype(str).str.strip()
    stat = {'x': [], 'y': [], 'z': []}
    df = all_agent.loc[all_agent['CUTI_S'].isin(maladies['agent_matricule'].astype(str).unique())]
    take_one = df.shape[0]
    print(take_one)
    result_one = int((take_one * 100) / take_all)
    result_two = (take_one * 1) / take_all
    x = ['malade', 'non malade']
    y = [result_one, 100 - result_one]
    z = [round(result_two, 2), round(1 - result_two, 2)]
    stat['x'].append(x)
    stat['y'].append(y)
    stat['z'].append(z)
    return jsonify({'stat': stat}), 200


'''@pilotage.route('/api/get/stat/arret/maladie', methods=['GET'])
def get_maladies():
    # if os.path.isfile('./essaie/Data/controleur_stat.csv'):
    # stat = {'name': [], 'non controlé': [], 'rejet': [], 'valider': [], 'non_traite_montant': [], 'rejet_montant': [], 'valider_montant': []}
    all_agent['CUTI_S'] = all_agent['CUTI_S'].astype(str).str.strip()
    df = all_agent.loc[all_agent['CUTI_S'].isin(maladies['agent_matricule'].astype(str).unique())]
    take_one = df.shape[0]
    print(take_one)
    x = 100
    y = int((take_one * 100) / take_all)
    z = x - y
    z = int(z)
    stat = {'x': x, 'y': y, 'z': z}
    return jsonify({'stat': stat}), 200'''


