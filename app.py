import pandas as pd
import seaborn as sns
import streamlit as st
import matplotlib.pyplot as plt

st.title('Análise de exportação de vinho brasileiro.')

tab0, tab1 = st.tabs(["Importadores", "Exportação"])

df_exp_vinho = pd.read_csv('ExpVinho.csv', sep=';')

df_exp_vinho = df_exp_vinho.drop('Id', axis=1)
df_exp_vinho = df_exp_vinho.melt(id_vars=['País'], var_name='ano', value_name='valor')
df_exp_vinho['tipo'] = df_exp_vinho.apply(lambda row: 'Valor' if '.' in row['ano'] else 'Quantidade', axis=1)
df_exp_vinho['ano'] = pd.to_datetime(df_exp_vinho['ano'].apply(lambda x: x.replace('.1', ''))).dt.year
df_exp_vinho = df_exp_vinho[df_exp_vinho.ano >= 2007]
df_exp_vinho['valor'] = df_exp_vinho['valor'] / 1_000_000

df_exp_vinho_total = df_exp_vinho.groupby(['País', 'tipo']).sum().reset_index().drop('ano', axis=1)
df_exp_vinho_valor_total = df_exp_vinho_total[df_exp_vinho_total.tipo == 'Valor'].sort_values('valor', ascending=False)

df_plot_1 = df_exp_vinho_valor_total.copy()

paises_principais = df_exp_vinho_valor_total.head(5)['País'].to_list()
df_exp_vinho_total = df_exp_vinho_total[df_exp_vinho_total['País'].isin(paises_principais)]

df_exp_vinho_total['tipo_valor'] = df_exp_vinho_total['tipo'].apply(lambda x: 0 if x == 'Valor' else 1)
df_exp_vinho_total = df_exp_vinho_total.sort_values(['tipo_valor', 'valor'], ascending=[True, False])

df_exp_vinho_total.tipo = df_exp_vinho_total.tipo.apply(lambda x: 'Valor (US$)' if x == 'Valor' else 'Quantidade (L)')

df_plot_2 = df_exp_vinho_total.copy()

df_exp_vinho_5_paises = df_exp_vinho[df_exp_vinho['País'].isin(paises_principais)]

df_plot_3 = df_exp_vinho_5_paises.copy()

df_exp_vinho_pais_anos = df_exp_vinho.groupby(['ano', 'País']).agg(list)
df_exp_vinho_pais_anos['valor_por_litro'] = df_exp_vinho_pais_anos.apply(lambda x: x['valor'][1] / x['valor'][0] if x['valor'][0] else 0, axis=1)

df_media_valor_por_litro = df_exp_vinho_pais_anos.reset_index()[['País', 'valor_por_litro']]
df_media_valor_por_litro = df_media_valor_por_litro.groupby(['País']).mean().reset_index().sort_values('valor_por_litro', ascending=False).head(5)

df_plot_4 = df_media_valor_por_litro.copy()

df_exp_vinho_pais_anos = df_exp_vinho_pais_anos.reset_index()
paises_maior_valor_por_litro = df_media_valor_por_litro['País'].to_list()
df_paises_maior_valor_por_litro = df_exp_vinho_pais_anos[df_exp_vinho_pais_anos['País'].isin(paises_maior_valor_por_litro)]

with tab0:
    """
    ## Título do texto
    
    Texto...
    """

    plt.figure()
    sns.set(style="whitegrid")
    sns.barplot(data=df_plot_1.head(10), x='País', y='valor')
    plt.title('Exportação de vinho brasileiro 2007-2021')
    plt.ylabel('Valor (US$) (em milhões)')
    plt.xticks(rotation=90)
    st.pyplot(plt)

    plt.figure()
    sns.barplot(data=df_plot_2, x='País', y='valor', hue='tipo')
    plt.title('Exportação de vinho brasileiro 2007-2021')
    plt.legend(title='Tipos')
    plt.ylabel('Valor (em milhões)')
    st.pyplot(plt)

    plt.figure()
    sns.barplot(data=df_plot_4, x='País', y='valor_por_litro')
    plt.title('Média do valor por litro do vinho')
    plt.ylabel('Valor (US$)')
    plt.xticks(rotation=45)
    st.pyplot(plt)


with tab1:
    """
    ## Título do texto

    Texto...
    """

    plt.figure()
    sns.lineplot(data=df_plot_3[df_plot_3.tipo == 'Quantidade'], x='ano', y='valor', hue='País')
    plt.title('Exportação de vinho com o decorrer do tempo')
    plt.xlabel('Ano')
    plt.ylabel('Quantidade (L) (em milhões)')
    st.pyplot(plt)

    plt.figure()
    plt.title('Exportação de vinho com o decorrer do tempo')
    plt.xlabel('Ano')
    plt.ylabel('Valor (US$) (em milhões)')
    sns.lineplot(data=df_plot_3[df_plot_3.tipo == 'Valor'], x='ano', y='valor', hue='País')
    st.pyplot(plt)
