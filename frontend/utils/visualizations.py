import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

COLORS = {
    'temperature': {'label': 'Temperatura', 'unit': '°C', 'range': '#3498db', 'mean': '#2980b9'},
    'pressure': {'label': 'Pressão', 'unit': 'hPa', 'range': '#e67e22', 'mean': '#d35400'},
    'humidity': {'label': 'Umidade', 'unit': '%', 'range': '#2ecc71', 'mean': '#27ae60'}
}

DELTA_LABELS = {
    'humidity': {1: 4.5, 7: 5, 30: 5},
    'pressure': {1: 0.5, 7: 1, 30: 1},
    'temperature': {1: 1, 7: 1, 30: 1.5}
}


def _add_labels(ax, x, values, variable, days):
    """Adiciona os rótulos das médias no gráfico."""
    for pos, row in enumerate(values.itertuples(index=False)):
        try:
            delta = DELTA_LABELS[variable][days]
            if pos > 0 and row.mean > values.iloc[pos - 1]['mean']:
                delta = -delta
            fontsize = 6 if days != 7 else 8

            ax.text(
                x[pos], row.mean + delta, f"{row.mean:.1f}",
                ha='center', va='center', color='white', fontsize=fontsize, weight='bold',
                bbox=dict(facecolor=COLORS[variable]['mean'], alpha=0.25, boxstyle='round', pad=0.2)
            )
        except Exception:
            continue  # Ignora rótulos problemáticos silenciosamente


def plot_historic_data(df, variable, days=7):
    if variable not in COLORS:
        raise ValueError("Variável inválida. Use: 'temperature', 'pressure' ou 'humidity'.")

    plt.style.use('dark_background')
    sns.set_theme(style="white", palette="deep")

    df = df.copy()
    df['date'] = pd.to_datetime(df['date'])

    fig, ax = plt.subplots(figsize=(6.5, 3), facecolor='none')
    ax.set_facecolor('none')

    if days == 1:
        # Filtra os dados para as últimas 24 horas
        last_24_hours = df[df['date'] >= df['date'].max() - pd.Timedelta(hours=24)]
        last_24_hours['hour'] = last_24_hours['date'].dt.floor('H')
        last_24_hours['dia'] = last_24_hours['date'].dt.date  # Arredonda para a hora inteira
        grouped = (
            last_24_hours.groupby([last_24_hours['dia'], last_24_hours['hour']])[variable]
            .agg(['min', 'max', 'mean'])
            .reset_index()
        )
        grouped['hour_label'] = grouped['hour'].dt.strftime('%H')  # Formata as horas para exibição lógica
        x = np.arange(len(grouped))
        ax.set_xticks(x)
        ax.set_xticklabels([f"{h}h" for h in grouped['hour_label']], rotation=45, color="white")

    else:
        df['dia'] = df['date'].dt.date
        grouped = (
            df.groupby('dia')[variable]
            .agg(['min', 'max', 'mean'])
            .reset_index()
            .sort_values(by='dia', ascending=False)
            .head(days)
            .sort_values(by='dia', ascending=True)
        )
        x = np.arange(len(grouped))
        ax.set_xticks(x)
        ax.set_xticklabels([d.strftime('%d/%m') for d in grouped['dia']], rotation=45, color="white")

    # Plotagem
    ax.bar(x, grouped['max'] - grouped['min'], bottom=grouped['min'],
           width=0.6, color=COLORS[variable]['range'], alpha=0.4, edgecolor='none', linewidth=0)
    ax.plot(x, grouped['mean'], 'o-', color=COLORS[variable]['mean'], linewidth=1)
    _add_labels(ax, x, grouped, variable, days)

    # Ajuste de limites
    y_padding = 1 if variable == 'humidity' else 0.2
    ax.set_ylim(bottom=grouped['min'].min() - y_padding, top=grouped['max'].max() + y_padding)
    ax.set_xlim(-0.5, len(x) - 0.5)

    # Estilo e texto
    ax.set_ylabel(f"{COLORS[variable]['label']} ({COLORS[variable]['unit']})", fontsize=6, color="white")
    ax.grid(True, linestyle='-', alpha=0.1, color="gray", axis='y')
    ax.set_title(f"{COLORS[variable]['label']} - {'Últimas' if days == 1 else 'Últimos'} {days if days != 1 else 24} {'Horas' if days == 1 else 'Dias'}",
                 fontsize=14, fontweight='bold', color="white", pad=30)
    ax.tick_params(axis='both', colors='white', labelsize=8 if days == 7 else 6, pad=15)

    for spine in ax.spines.values():
        spine.set_visible(False)

    plt.tight_layout()
    return fig
