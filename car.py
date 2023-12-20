import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Load the dataset
file_path = 'Auto_Sales_data.csv'
data = pd.read_csv(file_path)

# Convert ORDERDATE to datetime
data['ORDERDATE'] = pd.to_datetime(data['ORDERDATE'], format='%d/%m/%Y')

# Preparing the data
sales_by_country_date = data.groupby(['COUNTRY', data['ORDERDATE'].dt.to_period("M")]).agg({'SALES': 'sum', 'PRICEEACH': 'mean', 'QUANTITYORDERED': 'sum'}).reset_index()
sales_by_country_date['ORDERDATE'] = sales_by_country_date['ORDERDATE'].dt.to_timestamp()

# Unique list of countries
countries = sales_by_country_date['COUNTRY'].unique()

# Create subplots
fig = make_subplots(rows=3, cols=1, subplot_titles=('Sales', 'Average Price', 'Quantity Ordered'))

# Custom color palette
colors = ['blue', 'green', 'red']

# Add traces for each subplot
for i, country in enumerate(countries):
    filtered_data = sales_by_country_date[sales_by_country_date['COUNTRY'] == country]
    
    # Sales subplot
    fig.add_trace(
        go.Scatter(
            x=filtered_data['ORDERDATE'], 
            y=filtered_data['SALES'], 
            name=f"Sales in {country}",
            line=dict(color=colors[i % len(colors)], width=2, dash='dash'),
            mode='lines+markers',
            marker=dict(size=6)
        ),
        row=1, col=1
    )

    # Average Price subplot
    fig.add_trace(
        go.Scatter(
            x=filtered_data['ORDERDATE'],
            y=filtered_data['PRICEEACH'],
            name=f"Average Price in {country}",
            line=dict(color=colors[i % len(colors)], width=2, dash='dot'),
            mode='lines+markers',
            marker=dict(size=6, symbol='diamond')
        ),
        row=2, col=1
    )

    # Quantity Ordered subplot
    fig.add_trace(
        go.Scatter(
            x=filtered_data['ORDERDATE'],
            y=filtered_data['QUANTITYORDERED'],
            name=f"Quantity Ordered in {country}",
            line=dict(color=colors[i % len(colors)], width=2),
            mode='lines+markers',
            marker=dict(size=6, symbol='square')
        ),
        row=3, col=1
    )

# Create dropdown buttons
dropdown_buttons = [
    {
        'label': country,
        'method': 'update',
        'args': [
            {'visible': [country == c for c in countries for _ in range(3)]},  # Control visibility per subplot
            {'title': f'Sales, Average Price, and Quantity Ordered Over Time: {country}'}
        ]
    } for country in countries
]

# Set the initial state to hidden for all plots
for i in range(len(fig.data)):
    fig.data[i].visible = False

# Update layout with dropdown
fig.update_layout(
    updatemenus=[{
        'buttons': dropdown_buttons,
        'direction': 'down',
        'showactive': True,
        'x': 0.5,
        'y': 1.2
    }],
    template='plotly_dark',  # Use a template
    hovermode='x unified',  # Unified hover labels
    title=dict(text='Sales Data by Country', font=dict(size=20,color = 'black')),
    margin=dict(l=20, r=20, t=40, b=20),
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(color='black'),
)
# Enhance axes with black text color
fig.update_xaxes(title_text='Date', title_font=dict(color='black'), tickfont=dict(color='black'))
fig.update_yaxes(title_text='Value', title_font=dict(color='black'), tickfont=dict(color='black'))

# Update subplot titles to black
for i in fig['layout']['annotations']:
    i['font'] = dict(size=12, color='black')

# Show figure
fig.show()