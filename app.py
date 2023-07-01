import pandas as pd
import seaborn as sns
import streamlit as st
import matplotlib.pyplot as plt

map_paises = {
    "Alemanha, República Democrática": "Alemanha",
    "Tcheca República": "República Tcheca"
}

# Analise dos dados de exportacao
df_exp_vinho = pd.read_csv('ExpVinho.csv', sep=';')
df_exp_vinho['País'] = df_exp_vinho['País'].map(lambda x: map_paises.get(x) if x in map_paises else x)

df_exp_vinho = df_exp_vinho.drop('Id', axis=1)
df_exp_vinho = df_exp_vinho.melt(id_vars=['País'], var_name='ano', value_name='valor')
df_exp_vinho['tipo'] = df_exp_vinho.apply(lambda row: 'Valor' if '.' in row['ano'] else 'Quantidade', axis=1)
df_exp_vinho['ano'] = pd.to_datetime(df_exp_vinho['ano'].apply(lambda x: x.replace('.1', ''))).dt.year
df_exp_vinho = df_exp_vinho[df_exp_vinho.ano >= 2007]
df_exp_vinho['valor'] = df_exp_vinho['valor'] / 1_000_000

df_exp_vinho_total = df_exp_vinho.groupby(['País', 'tipo']).sum().reset_index().drop('ano', axis=1)
df_exp_vinho_valor_total = df_exp_vinho_total[df_exp_vinho_total.tipo == 'Valor'].sort_values('valor', ascending=False)

# df_plot_1 = df_exp_vinho_valor_total.copy()
# df_plot_1 = df_plot_1.drop('tipo', axis=1).reset_index(drop=True)
# df_plot_1.columns = ['País', 'Valor (US$) (em milhões)']

df_plot_1 = df_exp_vinho_valor_total.copy()
df_plot_1 = df_plot_1.drop('tipo', axis=1).reset_index(drop=True)
df_plot_1.columns = ['País', 'Valor (US$) (em milhões)']
df_plot_1.style.background_gradient(cmap="RdYlGn", subset=['Valor (US$) (em milhões)'])

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

df_plot_5 = df_paises_maior_valor_por_litro.copy()

df_exp_vinho_quantidade = df_exp_vinho[df_exp_vinho.tipo == 'Quantidade']
df_exp_vinho_quantidade = df_exp_vinho_quantidade[df_exp_vinho_quantidade['País'].isin(paises_maior_valor_por_litro)]

df_plot_6 = df_exp_vinho_quantidade.copy()

df_exp_vinho_total_ano = df_exp_vinho_5_paises.groupby(['ano', 'tipo']).sum().reset_index()
df_exp_vinho_total_ano.tipo = df_exp_vinho_total_ano.tipo.apply(lambda x: 'Valor (US$)' if x == 'Valor' else 'Quantidade (L)')

df_plot_7 = df_exp_vinho_total_ano.copy()

# Analise dos dados de producao

df_producao_brasil = pd.read_csv('Producao.csv', sep=';')

df_producao_brasil = df_producao_brasil.T.reset_index().T
df_producao_brasil = df_producao_brasil.drop([0, 1], axis=1)

colunas = [ano for ano in range(1970, 2022)]
colunas.insert(0, 'Produto')
df_producao_brasil.columns = colunas
df_producao_brasil = df_producao_brasil.set_index('Produto')

df_producao_brasil = df_producao_brasil.astype(int)

lista_tipo_produto = []

tipo_produto = ''
for index in df_producao_brasil.index:
    if index.isupper():
        tipo_produto = index
    lista_tipo_produto.append(tipo_produto)

df_producao_brasil['tipo'] = lista_tipo_produto
df_producao_brasil = df_producao_brasil[~df_producao_brasil.index.str.isupper()]

df_producao_tipo = df_producao_brasil.groupby('tipo').agg(sum)
df_producao_tipo = df_producao_tipo.reset_index().melt(id_vars=['tipo'], var_name='ano', value_name='valor')
df_producao_tipo['valor'] = df_producao_tipo['valor'] / 1_000_000

df_plot_8 = df_producao_tipo.copy()

df_producao_vinho_mesa = df_producao_brasil[df_producao_brasil.tipo == 'VINHO DE MESA.1']
df_producao_vinho_mesa = df_producao_vinho_mesa.drop('tipo', axis=1)
df_producao_vinho_mesa = df_producao_vinho_mesa.reset_index().melt(id_vars=['Produto'], var_name='ano', value_name='valor')
df_producao_vinho_mesa['valor'] = df_producao_vinho_mesa['valor'] / 1_000_000

df_plot_9 = df_producao_vinho_mesa.copy()

df_producao_total_ano = df_producao_brasil.drop('tipo', axis=1)
df_producao_total_ano = df_producao_total_ano.sum()
df_exp_vinho_total_ano['producao'] = df_exp_vinho_total_ano['ano'].map(df_producao_total_ano) / 1_000_000
df_exp_vinho_total_ano['valor'] = df_exp_vinho_total_ano['valor'] / df_exp_vinho_total_ano['valor'].mean()
df_exp_vinho_total_ano['producao'] = df_exp_vinho_total_ano['producao'] / df_exp_vinho_total_ano['producao'].mean()

df_exp_vinho_total_ano_quantidade = df_exp_vinho_total_ano[df_exp_vinho_total_ano.tipo == 'Quantidade (L)'].drop(['tipo', 'País'], axis=1)
df_exp_vinho_total_ano_valor = df_exp_vinho_total_ano[df_exp_vinho_total_ano.tipo == 'Valor (US$)'].drop(['tipo', 'País'], axis=1)

df_exp_vinho_total_ano_quantidade.columns = ['ano', 'Exportação', 'Produção']
df_exp_vinho_total_ano_valor.columns = ['ano', 'Exportação', 'Produção']

df_exp_vinho_total_ano_quantidade = df_exp_vinho_total_ano_quantidade.melt(id_vars=['ano'], var_name='Tipo', value_name='Valor')
df_exp_vinho_total_ano_valor = df_exp_vinho_total_ano_valor.melt(id_vars=['ano'], var_name='Tipo', value_name='Valor')

df_plot_10 = df_exp_vinho_total_ano_quantidade.copy()
df_plot_11 = df_exp_vinho_total_ano_valor.copy()

st.title('Análise Exploratória da Exportação do Vinho Brasileiro')
tab0, tab1, tab2, tab3, tab4 = st.tabs(["Geral", "Exportação", "Países Prioritários", "Países Potenciais", "Conclusão"])

# Dados produçao de vinho Europa

dados_producao = pd.read_excel('Production.xlsx')
dados_producao_filtrados = dados_producao.dropna()
dados_producao_top_continentes = dados_producao_filtrados[(dados_producao_filtrados["Region/Country"]=="Italy") | (dados_producao_filtrados["Region/Country"]=="France") | (dados_producao_filtrados["Region/Country"]=="Spain") | (dados_producao_filtrados["Region/Country"]=="Germany") | (dados_producao_filtrados["Region/Country"]=="Portugal")]
dados_producao_top_continentes.astype({"Year": int, "Quantity": int})
dados_producao_top_continentes = dados_producao_top_continentes.sort_values(by="Quantity", ascending=False)
dados_producao_top_continentes['Quantity'] = dados_producao_top_continentes['Quantity'] / 10

df_plot_12 = dados_producao_top_continentes.copy()

with tab0:
    """
    ## Exportação de Vinho Brasileiro (2007-2021)
    
    O vinho está entre os 100 produtos mais importados e exportados no mundo e movimenta bilhões de dólares anualmente. 
    O mercado de vinhos brasileiros passou por um crescimento significativo nas últimas décadas, tornando-se um setor 
    promissor para exportações.
    """
    st.subheader('Exportação de vinho brasileiro 2007-2021')
    # st.dataframe(df_plot_1, use_container_width=True)
    st.dataframe(df_plot_1.style.background_gradient(cmap='RdYlGn'))

    plt.figure()
    sns.set(style="whitegrid")
    sns.barplot(data=df_plot_1.head(10), x='País', y='Valor (US$) (em milhões)')
    plt.title('Exportação de vinho brasileiro 2007-2021')
    plt.ylabel('Valor (US$) (em milhões)')
    plt.xticks(rotation=65)
    st.pyplot(plt)

    """
    De 2007 a 2021, as exportações de vinhos brasileiros tiveram um aumento significativo, embora ainda representem uma 
    pequena parcela do mercado global. Dentre os países que mais importam o vinho brasileiro no período em questão, 
    destaque para o Paraguai com mais de 30 milhões de dólares, grande parte se deve a sua proximidade geográfica e às 
    relações comerciais entre os dois países. Rússia e China importantes parceiros do BRICS também fazem parte desta 
    lista, porém a Rússia com maior peso sendo a segunda maior importadora com cerca de 25 milhões de dólares, e em 
    terceiro o Estados Unidos aproximadamente 10 milhões de dólares, Reino Unido e alguns países da Europa também 
    fazem parte dessa lista.
    """


with tab1:
    plt.figure()
    sns.lineplot(data=df_plot_7[df_plot_7.tipo == 'Quantidade (L)'], x='ano', y='valor')
    plt.xlabel('Ano')
    plt.ylabel('Quantidade (L) (em milhões)')
    plt.title('Exportação Total com o decorrer do tempo')
    st.pyplot(plt)

    """
    Em 2009, o país teve um bom aumento no volume de exportações devido às exportações do vinho de mesa e vinhos finos 
    de baixo valor agregado. O aumento das exportações de vinhos deveu-se às políticas do governo federal por meio do 
    Programa de Escoamento da Produção (PEP), especialmente quando exportados para a Rússia e ao programa de exportação 
    “Wines from Brazil.” Conforme vemos no gráfico, a Rússia importou em 2009 cerca de 20 milhões de litros de vinho 
    brasileiro. De 2014 até 2021 temos um grande crescimento das exportações para o Paraguai.
    """

    plt.figure()
    sns.lineplot(data=df_plot_3[df_plot_3.tipo == 'Quantidade'], x='ano', y='valor', hue='País')
    plt.title('Exportação de vinho com o decorrer do tempo')
    plt.xlabel('Ano')
    plt.ylabel('Quantidade (L) (em milhões)')
    st.pyplot(plt)

    """
    Alguns vinhos brasileiros têm recebido prêmios e reconhecimento em competições internacionais, o que contribui para 
    a reputação do setor. A entrada de investidores estrangeiros na indústria vinícola brasileira tem impulsionado o 
    desenvolvimento e a promoção dos vinhos brasileiros no exterior.
    """

    # plt.figure()
    # plt.title('Exportação de vinho com o decorrer do tempo')
    # plt.xlabel('Ano')
    # plt.ylabel('Valor (US$) (em milhões)')
    # sns.lineplot(data=df_plot_3[df_plot_3.tipo == 'Valor'], x='ano', y='valor', hue='País')
    # st.pyplot(plt)

with tab2:
    plt.figure()
    sns.barplot(data=df_plot_2, x='País', y='valor', hue='tipo')
    plt.title('Exportação de vinho brasileiro 2007-2021')
    plt.legend(title='Tipo')
    plt.ylabel('Valor (US$) (em milhões)')
    plt.xticks(rotation=30)
    st.pyplot(plt)

    """
    Países com crescente interesse em vinhos, como China, Rússia e Índia, representam uma oportunidade para as 
    exportações brasileiras. Mercados tradicionais de vinho como Reino Unido e Alemanha, têm potencial para a 
    expansão das exportações brasileiras devido ao seu alto consumo e países em que tanto a produção quanto o consumo 
    são crescentes, como os Estados Unidos, a Austrália e a África do Sul também são importantes players de mercado para 
    as exportações, visto que suas produções não são o suficiente para o mercado aquecido de consumo de vinhos.
    """

    # plt.figure()
    # sns.lineplot(data=df_plot_8[df_plot_8.ano >= 2007], x='ano', y='valor', hue='tipo')
    # plt.xlabel('Ano')
    # plt.ylabel('Valor (em milhões)')
    # plt.title('Produção com o decorrer do tempo')
    # st.pyplot(plt)
    #
    # plt.figure()
    # sns.lineplot(data=df_plot_9[df_plot_9.ano >= 2007], x='ano', y='valor', hue='Produto')
    # plt.xlabel('Ano')
    # plt.ylabel('Valor (em milhões)')
    # plt.title('Produção de Vinho de Mesa com o decorrer do tempo')
    # st.pyplot(plt)

    # plt.figure()
    # plt.title('Valor por litro do vinho com o decorrer do tempo')
    # plt.xlabel('Ano')
    # plt.ylabel('Valor (US$)')
    # sns.lineplot(data=df_plot_5, x='ano', y='valor_por_litro', hue='País')
    # st.pyplot(plt)
    #
    # plt.figure()
    # sns.lineplot(data=df_plot_6, x='ano', y='valor', hue='País')
    # plt.title('Exportação de vinho brasileiro em decorrer com o tempo')
    # plt.xlabel('Ano')
    # plt.ylabel('Quantidade (L) (em milhões)')
    # st.pyplot(plt)

with tab3:
    plt.figure()
    sns.barplot(data=df_plot_4, x='País', y='valor_por_litro')
    plt.title('Média do valor por litro do vinho (2007-2021)')
    plt.ylabel('Valor (US$)')
    plt.xticks(rotation=30)
    st.pyplot(plt)

    """
    Países nos quais o consumo é expressivo mas a produção pequena ou inexistente, como os da Europa Setentrional, 
    pagam um valor agregado maior pelos vinhos brasileiros conforme o gráfico, chegando até U$7/L o valor pago pela 
    Suíça. Esse grupo e o anterior constituem-se nos mercados mais dinâmicos, responsáveis não só por grande parte do 
    crescimento do consumo de vinhos finos, mas também por muitas características desse consumo. São países que possuem 
    grande potencial para exportação.
    """

    # plt.figure()
    # sns.lineplot(data=df_plot_10, x='ano', y='Valor', hue='Tipo')
    # plt.xlabel('Ano')
    # plt.ylabel('Quantidade (proporcional à média)')
    # plt.title('Exportação x Produção de vinho em decorrer com o tempo')
    # st.pyplot(plt)
    #
    # plt.figure()
    # sns.lineplot(data=df_plot_11, x='ano', y='Valor', hue='Tipo')
    # plt.xlabel('Ano')
    # plt.ylabel('Valor (proporcional à média)')
    # plt.title('Exportação x Produção de vinho em decorrer com o tempo')
    # st.pyplot(plt)

with tab4:
    """
    É importante destacar que a exportação de vinhos brasileiros ainda enfrenta desafios. Um deles é a concorrência com 
    países tradicionalmente reconhecidos pela produção de vinhos, como França, Itália, Espanha e Argentina. Essas nações 
    têm uma longa tradição na indústria vinícola e já possuem uma reputação estabelecida.
    """

    plt.figure()
    ax = sns.lineplot(data=df_plot_12, x='Year', y='Quantity', hue='Region/Country')
    plt.title('Produção de vinho em top países europeus')
    plt.ylabel('Quantidade (L) (em milhões)')
    plt.xlabel('Ano')
    sns.move_legend(ax, "upper left", bbox_to_anchor=(1, 1))
    st.pyplot(plt)

    """
    Os vinhos brasileiros ainda são pouco conhecidos e reconhecidos internacionalmente, o que dificulta sua penetração 
    em mercados já estabelecidos. Em comparação com países com longa tradição vitivinícola, o Brasil ainda é considerado 
    um novo produtor, o que pode afetar a percepção de qualidade por parte dos consumidores internacionais.

    Além disso, questões relacionadas a impostos e barreiras comerciais também podem dificultar a exportação de 
    vinhos brasileiros. Cada país tem suas próprias regulamentações e taxas de importação, o que pode impactar o preço 
    final do produto e torná-lo menos competitivo em alguns mercados.

    Apesar dos desafios, a exportação de vinhos brasileiros tem apresentado um crescimento constante ao longo dos anos. 
    De 2014 para 2021 tivemos um crescimento quase constante da exportação. Isso demonstra o potencial do Brasil como 
    produtor de vinhos de qualidade e a capacidade do setor em conquistar espaço em âmbito internacional. Com o contínuo 
    investimento em tecnologia, inovação e promoção, é possível que as exportações de vinhos brasileiros continuem a 
    crescer nos próximos anos.
    """
