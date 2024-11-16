import pandas as pd
df = pd.read_csv("resources/Ticker_IDs.csv")
import yfinance as yf



def calculate_financial_health(ticker):
    stock = yf.Ticker(ticker)
    balance_sheet = stock.balance_sheet
    cash_flow = stock.cashflow
    income_statement = stock.financials
    for year in years:
        year = pd.Timestamp(year)
        # Extract values
    current_assets = balance_sheet.loc['Current Assets', year]
    current_liabilities = balance_sheet.loc['Current Liabilities', year]
    inventory = balance_sheet.loc['Inventory', year]
    total_assets = balance_sheet.loc['Total Assets', year]
    total_debt = balance_sheet.loc['Total Debt', year]
    shareholders_equity = balance_sheet.loc['Stockholders Equity', year]
    cash_equiv = balance_sheet.loc['Cash And Cash Equivalents', year]

    net_income = income_statement.at['Net Income', year]
    total_revenue = income_statement.at['Total Revenue', year]

    # Calculate Liquidity Ratios
    current_ratio = current_assets / current_liabilities if current_liabilities != 0 else np.nan
    quick_ratio = (current_assets - inventory) / current_liabilities if current_liabilities != 0 else np.nan
    working_capital = current_assets - current_liabilities

    # Calculate Leverage Ratios
    debt_to_equity = total_debt / shareholders_equity if shareholders_equity != 0 else np.nan
    debt_to_assets = total_debt / total_assets if total_assets != 0 else np.nan

    # Calculate Efficiency Ratios
    asset_turnover = total_revenue / total_assets if total_assets != 0 else np.nan

    # Calculate Profitability Ratios
    roa = (net_income / total_assets) * 100 if total_assets != 0 else np.nan
    roe = (net_income / shareholders_equity) * 100 if shareholders_equity != 0 else np.nan

    # Calculate Net Debt
    net_debt = total_debt - cash_equiv
    metrics.loc[str(year.date()), 'Current Ratio'] = round(current_ratio, 2)
    metrics.loc[str(year.date()), 'Quick Ratio'] = round(quick_ratio, 2)
    metrics.loc[str(year.date()), 'Working Capital'] = round(working_capital, 2)
    metrics.loc[str(year.date()), 'Debt to Equity Ratio'] = round(debt_to_equity, 2)
    metrics.loc[str(year.date()), 'Debt to Assets Ratio'] = round(debt_to_assets, 2)
    metrics.loc[str(year.date()), 'Asset Turnover Ratio'] = round(asset_turnover, 2)
    metrics.loc[str(year.date()), 'Return on Assets (ROA) (%)'] = round(roa, 2)
    metrics.loc[str(year.date()), 'Return on Equity (ROE) (%)'] = round(roe, 2)
    metrics.loc[str(year.date()), 'Net Debt'] = round(net_debt, 2)
    print(metrics.T)
    metrics = metrics.T


import dash
from dash import dcc, html
import plotly.graph_objects as go
import pandas as pd


# Function to create a formatted table using Plotly
def create_metrics_table():
    header = ["Metric"] + metrics.columns.tolist()
    rows = [
        [metric] + [f"{value:,.2f}" if isinstance(value, float) else f"{value:,}" for value in metrics.loc[metric]]
        for metric in metrics.index
    ]

    fig = go.Figure(data=[go.Table(
        header=dict(values=header, fill_color='paleturquoise', align='left', font=dict(size=12, color='black')),
        cells=dict(values=list(zip(*rows)), fill_color='lavender', align='left', font=dict(size=10))
    )])
    fig.update_layout(title="Financial Metrics Overview", title_x=0.5)
    return fig

# Function to create a bar chart for Debt to Equity Ratio
def create_bar_chart():
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=metrics.columns,
        y=metrics.loc['Debt to Equity Ratio'],
        name='Debt to Equity Ratio',
        marker_color='skyblue'
    ))
    fig.update_layout(
        title="Debt to Equity Ratio Over Time",
        xaxis_title="Year",
        yaxis_title="Debt to Equity Ratio",
        template="plotly_white",
        hovermode="x"
    )
    return fig

# Function to create a line chart for any selected metric
def create_line_chart(metric_name):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=metrics.columns,
        y=metrics.loc[metric_name],
        mode='lines+markers',
        marker=dict(size=8, color='royalblue'),
        line=dict(color='royalblue', width=2),
        name=metric_name
    ))
    fig.update_layout(
        title=f"{metric_name} Trend Over Time",
        xaxis_title="Year",
        yaxis_title=metric_name,
        template="plotly_white",
        hovermode="x"
    )
    return fig

# Initialize the Dash app
app = dash.Dash(__name__)

# Layout of the app
app.layout = html.Div([
    html.H1("Financial Metrics Dashboard", style={'textAlign': 'center'}),

    # Display the table
    dcc.Graph(figure=create_metrics_table(), style={'margin-bottom': '50px'}),

    # Dropdown for selecting a metric
    html.Label("Select a Metric:"),
    dcc.Dropdown(
        id='metric-dropdown',
        options=[{'label': metric, 'value': metric} for metric in metrics.index],
        value='Current Ratio'  # Default selected value
    ),

    # Line chart for the selected metric
    dcc.Graph(id='line-chart', style={'margin-top': '20px'}),

    # Bar chart for Debt to Equity Ratio
    dcc.Graph(figure=create_bar_chart(), style={'margin-top': '50px'})
])

# Callback to update the line chart based on the selected metric
@app.callback(
    dash.dependencies.Output('line-chart', 'figure'),
    [dash.dependencies.Input('metric-dropdown', 'value')]
)
def update_line_chart(selected_metric):
    return create_line_chart(selected_metric)

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True
