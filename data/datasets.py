import plotly.graph_objects as go


def temperature_chart(df, second_variable="pressure"):
    """
    Cria um gráfico de linhas mostrando temperatura e uma segunda variável com escalas separadas.
    """
    

    if df.empty:
        raise ValueError("O DataFrame está vazio. Não é possível criar o gráfico.")
    
    # Cria o gráfico com duas escalas
    fig = go.Figure()

    # Adiciona a linha de temperatura
    fig.add_trace(
        go.Scatter(
            x=df["date"],
            y=df["temperature"],
            mode="lines",
            name="Temperatura (°C)",
            line={"color":"red"},
            yaxis="y1"  # Associa à escala da esquerda
        )
    )

    # Adiciona a linha da segunda variável (pressure ou humidity)
    fig.add_trace(
        go.Scatter(
            x=df["date"],
            y=df[second_variable],
            mode="lines",
            name="Pressão (hPa)" if second_variable == "pressure" else "Umidade (%)",
            line={"color":"blue"},
            yaxis="y2"  # Associa à escala da direita
        )
    )

    # Configura os eixos
    fig.update_layout(
    title="Variação de Temperatura e Variável Selecionada ao Longo do Tempo",
    xaxis={'title': 'Data'},
    yaxis={
        'title': {'text': 'Temperatura (°C)', 'font': {'color': 'red'}},  
        'tickfont': {'color': 'red'}      
    },
    yaxis2={
        'title': {
            'text': 'Pressão (hPa)' if second_variable == 'pressure' else 'Umidade (%)',
            'font': {'color': 'blue'}
        },   
        'overlaying': 'y',  # Sobrepõe ao eixo y
        'tickfont': {'color': 'blue'},
        'side': 'right'  # Coloca o eixo à direita
    },
    legend={'x': 0, 'y': 1},
    )

    return fig