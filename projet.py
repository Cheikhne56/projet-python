import pandas as pd
import matplotlib.pyplot as plt
import gradio as gr
import gradio.inputs as gr_inputs
import gradio.outputs as gr_outputs
import numpy as np
from matplotlib.dates import DateFormatter

# Charger les données du marché boursier en utilisant pandas
df = pd.read_csv('donner.csv')
df['Date'] = pd.to_datetime(df['Date'])  # Convertir la colonne 'Date' en type datetime
df = df.sort_values('Date')  # Trier les données par la colonne 'Date'

def analyse_interactive_marche_boursier(start_date, end_date):
    # Filtrer les données dans la plage de dates spécifiée
    df_filtre = df[(df['Date'] >= pd.to_datetime(start_date)) & (df['Date'] <= pd.to_datetime(end_date))]

    # Créer le graphique avec deux sous-graphiques
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

    ax1.plot(df_filtre['Date'], df_filtre['Close'], label='Close', color='blue')
    ax1.set_ylabel("Close", color='blue')
    ax1.legend(loc='upper left')

    ax2.plot(df_filtre['Date'], df_filtre['Volume'], label='Volume', color='green')
    ax2.set_ylabel("Volume", color='green')
    ax2.legend(loc='upper right')

    # Configurer les formats de date sur l'axe des x
    date_format = DateFormatter("%Y-%m-%d")
    ax2.xaxis.set_major_formatter(date_format)
    plt.xticks(rotation=45)

    # Configurer la mise en page et l'apparence du graphique
    plt.title(f"Variation du volume et du prix de clôture entre {start_date} et {end_date}")
    plt.tight_layout()

    # Convertir le graphique en tableau numpy
    fig.canvas.draw()
    graph_array = np.array(fig.canvas.renderer.buffer_rgba())

    return graph_array

# Créer l'interface Gradio
interface = gr.Interface(
    fn=analyse_interactive_marche_boursier,
    inputs=[
        gr_inputs.Textbox(label='Date de début (AAAA-MM-JJ)', lines=1, type='text'),
        gr_inputs.Textbox(label='Date de fin (AAAA-MM-JJ)', lines=1, type='text')
    ],
    outputs=gr_outputs.Image(type="numpy", label="Graphique du marché boursier"),
    title="Analyse interactive du marché boursier",
    description="Visualisez la variation du volume et du prix de clôture entre deux dates.",
    examples=[['2020-01-01', '2021-12-31']]
)

# Lancer l'interface
interface.launch()
