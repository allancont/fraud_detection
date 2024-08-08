import streamlit as st
import pandas as pd
from pycaret.classification import load_model, predict_model
from datetime import datetime

st.title('MÓDULO DE DETECÇÃO DE FRAUDE')

# Carregar o modelo 
model_path = "Modelo_Final_Fraude"
# model_path = "E:\Meus Documentos\Allan\Clientes\Modelo_Final_Fraude"
# Carregar o modelo
saved_final_model = load_model(model_path)

st.subheader('Insira os detalhes da compra do cliente')

col1, col2 = st.columns(2)

with col1:
    qtitens = st.number_input('Quantidade de itens comprados', step=1)
with col2:
    venda_total = st.number_input('Valor da compra')

# Exibir 'cliente_recente' e 'rg_nulo' em duas colunas
col3, col4 = st.columns(2)

with col3:
    cliente_recente = st.radio('Cliente recente?', ['sim', 'não'])
with col4:
    rg_nulo = st.radio('RG nulo?', ['sim', 'não'])

col5, col6 = st.columns(2)

with col5:
    data_ultima_compra = st.date_input('Data da última compra', value=datetime.now().date(), format="DD/MM/YYYY")
    data_atual = datetime.now().date()
    dias_ultima_compra = (data_atual - data_ultima_compra).days

# Convertendo 'sim'/'não' para 1/0
cliente_recente = 1 if cliente_recente == 'sim' else 0
rg_nulo = 1 if rg_nulo == 'sim' else 0

# Dicionário com os inputs do usuário
data = {
    'qtitens': [qtitens],
    'venda_total': [venda_total],
    'cliente_recente': [cliente_recente],
    'rg_nulo': [rg_nulo],
    'dias_ultima_compra': [dias_ultima_compra]
}

# Convertendo os dados em um DataFrame
df = pd.DataFrame(data)

# Botão para fazer a predição
if st.button('VERIFICAR FRAUDE'):
    prediction = predict_model(saved_final_model, data=df)
    
    # Obter o nome das últimas colunas
    last_column = prediction.columns[-1]
    second_last_column = prediction.columns[-2]

    # Obter os valores da última linha das últimas colunas
    score = int(prediction[last_column].iloc[-1] * 100)
    label = int(prediction[second_last_column].iloc[-1])

    # Exibir o valor em Streamlit
    st.header(f'Score do resultado: {score}%')

    # Determinar o resultado da predição com base no valor da segunda última coluna
    resultado = 'Fraude' if label == 1 else 'Não é Fraude'

    # Alterar a cor do texto com base no resultado
    if resultado == 'Fraude':
        st.markdown(f'<h1 style="color:red;">{resultado}</h1>', unsafe_allow_html=True)
    else:
        st.title(f'{resultado}')

    # st.write(prediction.T)
