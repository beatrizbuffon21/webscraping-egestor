# =============================== #

import locale
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import pandas as pd
import plotly.graph_objects as go
import plotly.figure_factory as ff
import dash_bootstrap_components as dbc
from dash import html, dcc, Output, Input
from app import app
import dash

# =============================== #
locale.setlocale(locale.LC_ALL, 'pt_BR.utf8')  

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_name('arquivojson.json', scope)
client = gspread.authorize(credentials)
spreadsheet = client.open_by_key('chave-planilha')
sheet = spreadsheet.get_worksheet(0)
values = sheet.get_all_values()
sublistas_selecionadas = values[2:]

# =============================== #

df = pd.DataFrame()
for sublista in sublistas_selecionadas:
    if len(sublista) > 0: 
        nome_coluna = sublista[0]
        valores_coluna = sublista[1:] 
        df[nome_coluna] = valores_coluna
        
lista1 = sublistas_selecionadas[0]

lista2 = sublistas_selecionadas[1]
solicitacoes_retencao = lista2[:4]
renovaram_financeiro = lista2[9:]

lista3 = sublistas_selecionadas[2]
cancelados_retencao = lista3[:4]
nao_pagou_financeiro = lista3[9:]

lista4 = sublistas_selecionadas[3]
revertidos_retencao = lista4[:4]
renovou_downsol_financeiro = lista4[9:]

lista5 = sublistas_selecionadas[4]
mrr_revertido_retencao = lista5[:4] 
cancelou_retencao_financeiro = lista5[9:]

lista6 = sublistas_selecionadas[5]
mrr_cancelado_retencao = lista6[:4] 
mrr_renovado_financeiro = lista6[9:]

lista7 = sublistas_selecionadas[6]
mrr_revertidoHS_retencao = lista7[:4] 
mrr_renovado_downsel_financeiro = lista7[9:]

lista8 = sublistas_selecionadas[7]
porcentag_reversao_retencao = lista8[:4] 
mrr_nao_pago_financeiro = lista8[9:]

lista9 = sublistas_selecionadas[8]
upsell_mrr_retencao = lista9[:4] 
mrr_cancelou_financeiro = lista9[9:] 

lista10 = sublistas_selecionadas[9]
total_mrr_retencao = lista10[:4] 
mrr_certificados_vencidos_financeiro = lista10[9:] 

lista12 = sublistas_selecionadas[10]
negociacoes_pagas_mrr = lista12[9:] 

lista13 = sublistas_selecionadas[11]
negociacoes_nao_pagas_mrr = lista13[9:] 

lista16 = sublistas_selecionadas[12]
total_MRR_feito = lista16[9:] 

lista14 = sublistas_selecionadas[13]
descontos_renovacoesARR_financeiro = lista14[9:] 

lista15 = sublistas_selecionadas[14]
descontos_renovacoesMRR_financeiro = lista15[9:] 

# ============= Financeiro ================== #

listas = [renovaram_financeiro, nao_pagou_financeiro, renovou_downsol_financeiro,
          cancelou_retencao_financeiro, mrr_renovado_financeiro,
          mrr_renovado_downsel_financeiro, mrr_nao_pago_financeiro,
          mrr_cancelou_financeiro, mrr_certificados_vencidos_financeiro, negociacoes_pagas_mrr,
          negociacoes_nao_pagas_mrr, total_MRR_feito,
          descontos_renovacoesARR_financeiro,descontos_renovacoesMRR_financeiro]
listas_resultantes = []

for lista in listas: 
    primeiros_elementos = lista[1:4]
    listas_resultantes.append(primeiros_elementos)
 
df_financeiro = pd.DataFrame({'Renovaram': listas_resultantes[0],
                   'Não Pagou': listas_resultantes[1],
                   'Renovou com Downsell': listas_resultantes[2],
                   'Cancelou': listas_resultantes[3],
                   'MRR renovado': listas_resultantes[4],
                   'MRR renovado com Downsell': listas_resultantes[5],
                   'MRR não pago': listas_resultantes[6],
                   'MRR cancelou': listas_resultantes[7],
                   'MRR - Certificados vencidos': listas_resultantes[8],
                   'Negociações pagas - Em MRR': listas_resultantes[9],
                   'Negociações não pagas - Em MRR': listas_resultantes[10],
                   'Total de MRR feito': listas_resultantes[11],
                   'Desconto dado para as renovações - ARR': listas_resultantes[12],
                   'Desconto dado para as renovações - MRR': listas_resultantes[13]})
nomes = ['Pessoa1', 'Pesso2', 'Pessoa3']
df_financeiro.insert(0, 'Nome', nomes)

colunas_monetarias = ['MRR renovado', 'MRR renovado com Downsell', 'MRR não pago', 'Renovou com Downsell',
                      'MRR cancelou', 'Negociações pagas - Em MRR', 'Negociações não pagas - Em MRR',
                      'MRR - Certificados vencidos', 'Total de MRR feito', 'Desconto dado para as renovações - ARR', 'Desconto dado para as renovações - MRR']

for coluna in colunas_monetarias:
    df_financeiro[coluna] = df_financeiro[coluna].str.replace('R\$ ', '', regex=True)
    df_financeiro[coluna] = df_financeiro[coluna].str.replace('.', '').str.replace(',', '.', regex=True)
for coluna in colunas_monetarias:
    df_financeiro[coluna] = pd.to_numeric(df_financeiro[coluna], errors='coerce')
df_financeiro = df_financeiro.fillna(0)

# ============== Retenção ================= #

listas_retencao = [solicitacoes_retencao, cancelados_retencao,
                   revertidos_retencao, mrr_revertido_retencao,
                   mrr_cancelado_retencao, mrr_revertidoHS_retencao,
                   porcentag_reversao_retencao, upsell_mrr_retencao, total_mrr_retencao]
listas_resultantes_retencao = []

for lista in listas_retencao: # para cada lista
    primeiros_elementos = lista[1:4] # selecionar apenas o elemento 0 ao 4
    listas_resultantes_retencao.append(primeiros_elementos) # junta os elementos em uma lista

df_retencao = pd.DataFrame({'Solicitações': listas_resultantes_retencao[0],
                   'Cancelados': listas_resultantes_retencao[1],
                   'Revertidos': listas_resultantes_retencao[2],
                   'MRR Revertido': listas_resultantes_retencao[3],
                   'MRR Cancelado': listas_resultantes_retencao[4],
                   'MRR revertido HS': listas_resultantes_retencao[5],
                   '% de reversão': listas_resultantes_retencao[6],
                   'Upsell MRR': listas_resultantes_retencao[7],
                   'Total MRR Retenção': listas_resultantes_retencao[8],})
nomes = ['Pessoa4', 'Pessoa5', 'Pesssoa6']
df_retencao.insert(0, 'Nome', nomes)
df_retencao.fillna(0)

colunas_monetarias2 = ['MRR Revertido', 'MRR Cancelado', 'MRR revertido HS', 'Upsell MRR', 'Total MRR Retenção']

for coluna in colunas_monetarias2:
    df_retencao[coluna] = df_retencao[coluna].str.replace('R\$ ', '', regex=True)
    df_retencao[coluna] = df_retencao[coluna].str.replace('.', '').str.replace(',', '.', regex=True)
for coluna in colunas_monetarias2:
    df_retencao[coluna] = pd.to_numeric(df_retencao[coluna], errors='coerce')
    df_retencao.fillna(0)

df_retencao = df_retencao.fillna(0)

df_retencao['% de reversão'] = [value.replace("%", "").replace(".", ",") for value in df_retencao['% de reversão']]
df_retencao['% de reversão'] = [
    float(value.replace(",", ".")) if value else None
    for value in df_retencao['% de reversão']
]
df_retencao['Reversão do Time'] = (df_retencao['% de reversão'].sum() / 3).round(2)


# ============== Somatório das variáveis ================= #

soma_mrr_feito_retencao = df_retencao['Total MRR Retenção'].sum() # soma total retenção
soma_mrr_feito_retencao1 = soma_mrr_feito_retencao.round(2) # arredondamento em 2
soma_mrr_feito_retencao1 = '{:,.2f}'.format(soma_mrr_feito_retencao1).replace(',', ' ').replace('.', ',').replace(' ', '.') # substituições
soma_mrr_feito_retencao1 = f'R$ {soma_mrr_feito_retencao1}' #formata adicionando R$ na frente 

reversao_retencao = df_retencao['Reversão do Time'][1] 
reversao_retencao = f"{reversao_retencao} %"

mrr_revertido_financeiro = df_financeiro['Total de MRR feito'].sum() # soma total financeiro
mrr_revertido_financeiro = round(mrr_revertido_financeiro, 2)  # arredondamento em 2
mrr_revertido_financeiro = '{:,.2f}'.format(mrr_revertido_financeiro).replace(',', ' ').replace('.', ',').replace(' ', '.') # substituições
mrr_revertido_financeiro = f'R$ {mrr_revertido_financeiro}'  #formata adicionando R$ na frente 

# ================================= #

solicitacoes_ret = df_retencao['Solicitações'].astype(int).sum()
cancelados_ret = df_retencao['Cancelados'].astype(int).sum()
revertidos_ret = df_retencao['Revertidos'].astype(int).sum()
mrr_revertido_ret = df_retencao['MRR Revertido'].sum()
mrr_revertido_ret = mrr_revertido_ret.round(2)
mrr_cancelado_ret = df_retencao['MRR Cancelado'].sum()
mrr_cancelado_ret = mrr_cancelado_ret.round(2)
mrr_revertido_hs_ret = df_retencao['MRR revertido HS'].sum()
mrr_revertido_hs_ret = mrr_revertido_hs_ret.round(2)
upsell_mrr_ret = df_retencao['Upsell MRR'].sum()
upsell_mrr_ret = upsell_mrr_ret.round(2)
total_mrr_ret = df_retencao['Total MRR Retenção'].sum()
total_mrr_ret = total_mrr_ret.round(2)

data_retencao = {
    'MRR': ["Total MRR Retenção", "MRR revertido HS", "MRR Revertido", "MRR Cancelado", "Upsell MRR"],
    'Valor': [total_mrr_ret, mrr_revertido_hs_ret, mrr_revertido_ret, mrr_cancelado_ret, upsell_mrr_ret],
    'Cor': ['#04ad43', '#04ad43', '#04ad43', '#f50909', '#04ad43']  # Cores específicas
}

data_retencao_sorted = sorted(zip(data_retencao['MRR'], data_retencao['Valor'], data_retencao['Cor']),  key=lambda x: x[1], reverse=True)
data_retencao['MRR'] = [item[0] for item in data_retencao_sorted]
data_retencao['Valor'] = [item[1] for item in data_retencao_sorted]
data_retencao['Cor'] = [item[2] for item in data_retencao_sorted]

# =========  Gráfico Geral Retenção - 1 =========== #

fig_retencao = go.Figure()
for mrr, valor, cor in zip(data_retencao['MRR'], data_retencao['Valor'], data_retencao['Cor']):
    fig_retencao.add_trace(go.Bar(
        x=[valor],
        y=[mrr],
        orientation='h',
        marker={"color": cor},
        hoverinfo="none"
    ))
fig_retencao.update_layout(
    height=400,
    width=700,
    template="plotly_white",
    margin={"l": 20, "r": 20, "t": 20, "b": 20},
    xaxis={"showticklabels": False}
)
fig_retencao.update_yaxes(tickfont=dict(size=18, color='black'))
for data_index, bar in enumerate(fig_retencao.data):
    x_value = bar.x[0]
    y_value = bar.y[0]
    fig_retencao.add_annotation(
        x=x_value + 400,  # Ajuste horizontal da posição do texto
        y=y_value,
        text=f"{x_value:.2f}",  # Formatação do valor com duas casas decimais
        showarrow=False,  # Não mostrar seta
        font=dict(size=18, color="black", family="Arial, sans-serif")  # Estilo da fonte do texto
    )
fig_retencao.update_xaxes(tickformat=".2f")
fig_retencao.update_layout(showlegend=False)  # Remove a legenda
fig_retencao.update_xaxes(showgrid=False)
fig_retencao.update_yaxes(showgrid=False)

# ========= Tabelas =========== #

data_matrix = [['% de Reversão', 'Solicitações', 'Cancelados', 'Revertidos']]
percentage_value = df_retencao[df_retencao['Nome'] == 'Pessoa1']['% de reversão'].iloc[0]
formatted_percentage = f"{percentage_value / 1:.2f}%"

fig_matrix.append([
                    formatted_percentage,
                    df_retencao[df_retencao['Nome'] == 'Pessoa1']['Solicitações'].iloc[0],
                    df_retencao[df_retencao['Nome'] == 'Pessoa1']['Cancelados'].iloc[0],
                    df_retencao[df_retencao['Nome'] == 'Pessoa1']['Revertidos'].iloc[0]])

colorscale = [[0, '#ab1216'],[.5, '#8a8a8a'],[1, '#e5e5e5']]
fig_matrix = ff.create_table(data_matrix, height_constant=20, colorscale=colorscale)
fig_matrix.layout.width=600
for i in range(len(fig_matrix.layout.annotations)):
    fig_matrix.layout.annotations[i].font.size = 18

# =========  Layout  =========== #
layout = dbc.Col([
    dbc.Row([
        dbc.Col([
            dbc.CardGroup([
                dbc.Card([
                    html.Legend('MRR revertido Retenção', style={'font-weight': 'bold', 'color': 'black'}),
                    html.H5(soma_mrr_feito_retencao1, id='p-saldo-dashboards', style={'font-weight': 'bold', 'font-size':'25px', 'color':'rgb(235, 50, 55)'})
                ], style={'padding-left': '20px', 'padding-top': '10px'}),
                dbc.Card(
                    html.Div(className='fa fa-line-chart ', style=card_icon),
                    color= 'black',
                    style={'maxWidth': 75, 'height': 100, 'margin-left': '-10px'}
                )
            ])
        ], width=4),

        dbc.Col([       
            dbc.CardGroup([
                dbc.Card([
                    html.Legend('Reversão do time de Retenção', style={'font-weight': 'bold', 'color': 'black'}),
                    html.H5(reversao_retencao, id='p-receita-dashboards', style={'font-weight': 'bold', 'font-size':'25px', 'color':'rgb(235, 50, 55)'})
                ], style={'padding-left': '20px', 'padding-top': '10px'}),
                dbc.Card(
                    html.Div(className='fa fa-line-chart ', style=card_icon),
                    color= 'black',
                    style={'maxWidth': 75, 'height': 100, 'margin-left': '-10px'}
                )
            ])
        ], width=4),
        
        dbc.Col([ 
            dbc.CardGroup([
                dbc.Card([
                    html.Legend('MRR Revertido Financeiro', style={'font-weight': 'bold', 'color': 'black'}),
                    html.H5(mrr_revertido_financeiro, id='p-despesa-dashboards', style={'font-weight': 'bold', 'font-size':'25px', 'color':'rgb(235, 50, 55)'})
                ], style={'padding-left': '20px', 'padding-top': '10px'}),
                dbc.Card(
                    html.Div(className='fa fa-line-chart ', style=card_icon),
                    color= 'black',
                    style={'maxWidth': 75, 'height': 100, 'margin-left': '-10px'}
                )
            ])
        ], width=4),
    ], style={'margin': '30px'}),
    
    dbc.Row([       
        dbc.Col([
            dbc.CardGroup([
                dbc.Card([
                html.Label("Período de análise", style={"margin-top": "10px"}),
                dcc.Dropdown(
                    id="dropdown-despesa",
                    clearable=False,
                    style={"width": "100%"},
                    persistence=True,
                    persistence_type="session",
                    multi=True
                )
            ], style={'height':"70%", 'padding': '20px', 'margin-left': '30px'})
            ])
            ], width=4),
        dbc.Col([
             dbc.Button("Pessoa1", id='img-pessoa-1', className='teste1', n_clicks=0),
             dbc.Button("Pessoa2", id='img-pessoa-2', className='teste1', n_clicks=0),
             dbc.Button("Pessoa3", id='img-pessoa-3',className='teste1', n_clicks=0),
             dbc.Button("Pessoa4", id='img-pessoa-4',className='teste1',  n_clicks=0),
             dbc.Button("Pessoa5", id='img-pessoa-5',  className='teste1', n_clicks=0),
             dbc.Button("Pessoa6", id='img-pessoa-6',className='teste1', n_clicks=0),
        ], className = 'teste2'),
    ]),
    dbc.Row([
        dbc.Col(
            dbc.Card(dcc.Graph(id='graph2'), style={'padding-left': '30px', 'width': '100%'}), width=6),
        dbc.Col([
             dbc.Card(dcc.Graph(id='graph3'), style={'margin-left': '50px', 'margin-top': '30px', 'width': '100%'}),
             dbc.Card(dcc.Graph(id='graph4'), style={'margin-left': '50px', 'margin-top': '30px', 'width': '100%'}),
    ], width=6),
])
])

@app.callback(
    [Output('img-pessoa-1', 'className'),
     Output('img-pessoa-2', 'className'),
     Output('img-pessoa-3', 'className'),
     Output('img-pessoa-4', 'className'),
     Output('img-pessoa-5', 'className'),
     Output('img-pessoa-6', 'className'),
     Output('graph2', 'figure'),
     Output('graph3', 'figure'),
     Output('graph4', 'figure')], 
   [Input('img-pessoa-1', 'n_clicks'),
    Input('img-pessoa-2', 'n_clicks'),
    Input('img-pessoa-3', 'n_clicks'),
    Input('img-pessoa-4', 'n_clicks'),
    Input('img-pessoa-5', 'n_clicks'),
    Input('img-pessoa-6', 'n_clicks')],
    prevent_initial_call=True
)

def update_card(img1, img2, img3, img4, img5, img6):
    figura = go.Figure()
    figura2 = go.Figure()
    figura3 = go.Figure()

    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    
    class_pessoa1, class_pessoa2, class_pessoa3, class_pessoa4, class_pessoa5, class_pessoa6 = \
        'teste1', 'teste1', 'teste1', 'teste1', 'teste1', 'teste1'

    if 'img-pessoa-1' in changed_id:
        figura = fig_pessoa1
        figura2 = fig_pessoa11
        figura3 = data_matrix
        class_pessoa1 = 'teste1-active'
    elif 'img-pessoa-2' in changed_id:
        figura = fig_pessoa2
        figura2 = fig_pessoa22
        figura3 = data_matrix
        class_pessoa2 = 'teste1-active'
    elif 'img-pessoa-3' in changed_id:
        figura = fig_pessoa3
        figura2 = fig_pessoa33
        figura3 = data_matrix
        class_pessoa3 = 'teste1-active'
    elif 'img-pessoa-4' in changed_id:
        figura = fig_pessoa4
        figura2 = fig_pessoa44
        figura3 = fig_pessoa444
        class_pessoa4 = 'teste1-active'
    elif 'img-pessoa-5' in changed_id:
        figura = fig_pessoa5
        figura2 = fig_pessoa55
        figura3 = fig_pessoa555
        class_pessoa5 = 'teste1-active'
    elif 'img-pessoa-6' in changed_id:
        figura = fig_pessoa6
        figura2 = fig_pessoa66
        figura3 = fig_pessoa666
        class_pessoa6 = 'teste1-active'

    return class_pessoa1, class_pessoa2, class_pessoa3, class_pessoa4, class_pessoa5, class_pessoa6, figura, figura2, figura3

