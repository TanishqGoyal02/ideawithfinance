import yfinance as yf
import numpy as np

def calculate_intrinsic_value(ticker):
    # Download the financial data for the company
    stock = yf.Ticker(ticker)

    # Fetch the financial statements
    balance_sheet = stock.balance_sheet
    income_statement = stock.financials
    cash_flow = stock.cashflow

    # Extract relevant financial data
    revenue = income_statement.loc['Total Revenue'].iloc[0] if 'Total Revenue' in income_statement.index else 0
    ebit = income_statement.loc['EBIT'].iloc[0] if 'EBIT' in income_statement.index else 0
    tax_expense = income_statement.loc['Tax Provision'].iloc[0] if 'Tax Provision' in income_statement.index else 0

    # Extract values using the correct labels from the cash flow statement
    depreciation = cash_flow.loc['Depreciation & Amortization'].iloc[0] if 'Depreciation & Amortization' in cash_flow.index else 0
    capex = cash_flow.loc['Capital Expenditures'].iloc[0] if 'Capital Expenditures' in cash_flow.index else 0
    change_in_working_capital = cash_flow.loc['Change in Working Capital'].iloc[0] if 'Change in Working Capital' in cash_flow.index else 0

    # Extract values from the balance sheet
    total_debt = balance_sheet.loc['Total Debt'].iloc[0] if 'Total Debt' in balance_sheet.index else 0
    cash = balance_sheet.loc['Cash & Equivalents'].iloc[0] if 'Cash & Equivalents' in balance_sheet.index else 0

    # Calculate key financial metrics
    tax_rate = tax_expense / ebit if ebit != 0 else 0
    nopat = ebit * (1 - tax_rate)  # Net Operating Profit After Taxes
    fcf = nopat + depreciation - capex - change_in_working_capital  # Free Cash Flow

    # DCF assumptions
    wacc = 0.08  # Discount rate (8%)
    terminal_growth_rate = 0.02  # Terminal growth rate (2%)
    growth_rate = 0.03  # Future FCF growth rate (3%)
    years = 5  # Projection period

    # Forecast future Free Cash Flows
    future_fcfs = [fcf * (1 + growth_rate)**i for i in range(1, years + 1)]

    # Calculate the Terminal Value using the perpetual growth method
    terminal_value = future_fcfs[-1] * (1 + terminal_growth_rate) / (wacc - terminal_growth_rate)

    # Discount future Free Cash Flows to present value
    discounted_fcfs = [fcf / (1 + wacc)**i for i, fcf in enumerate(future_fcfs, start=1)]
    pv_terminal_value = terminal_value / (1 + wacc)**years

    # Calculate Enterprise Value
    enterprise_value = sum(discounted_fcfs) + pv_terminal_value

    # Calculate Equity Value
    equity_value = enterprise_value - total_debt + cash

    # Get the number of shares outstanding
    shares_outstanding = stock.info['sharesOutstanding'] if 'sharesOutstanding' in stock.info else 1  # Avoid division by zero

    # Calculate Intrinsic Value per Share
    intrinsic_value_per_share = equity_value / shares_outstanding

    # Return the intrinsic value
    return intrinsic_value_per_share