from pathlib import Path
import pandas as pd
try:
    import matplotlib.pyplot as plt
except ImportError:
    plt = None

ROOT = Path(__file__).parent
DATA = ROOT / 'data' / 'sales.csv'
OUT = ROOT / 'outputs'
OUT.mkdir(exist_ok=True)

df = pd.read_csv(DATA)
required_columns = {
    'order_date', 'category', 'region', 'quantity', 'unit_price', 'unit_cost',
}
missing_columns = required_columns.difference(df.columns)
if missing_columns:
    missing = ', '.join(sorted(missing_columns))
    raise SystemExit(f'Missing required columns in {DATA}: {missing}')

df['order_date'] = pd.to_datetime(df['order_date'])
df = df.drop_duplicates().copy()
df['revenue'] = df['quantity'] * df['unit_price']
df['cost'] = df['quantity'] * df['unit_cost']
df['profit'] = df['revenue'] - df['cost']
df['month'] = df['order_date'].dt.to_period('M').astype(str)

total_revenue = df['revenue'].sum()
total_profit = df['profit'].sum()
profit_margin = round(total_profit / total_revenue * 100, 2) if total_revenue else 'N/A'

print('ROWS:', len(df))
print('TOTAL REVENUE:', round(total_revenue, 2))
print('TOTAL PROFIT:', round(total_profit, 2))
print('PROFIT MARGIN (%):', profit_margin)
print('\nREVENUE BY CATEGORY')
print(df.groupby('category', as_index=False)['revenue'].sum().sort_values('revenue', ascending=False).to_string(index=False))
print('\nREVENUE BY REGION')
print(df.groupby('region', as_index=False)['revenue'].sum().sort_values('revenue', ascending=False).to_string(index=False))

if plt is not None:
    monthly = df.groupby('month', as_index=False)[['revenue', 'profit']].sum()
    monthly.plot(x='month', y=['revenue', 'profit'], marker='o', title='Monthly Revenue and Profit', figsize=(9, 5))
    plt.ylabel('Amount')
    plt.tight_layout()
    plt.savefig(OUT / 'monthly_revenue_profit.png', dpi=160)
    plt.close()

    category = df.groupby('category', as_index=False)['revenue'].sum().sort_values('revenue')
    category.plot.barh(x='category', y='revenue', legend=False, title='Revenue by Category', figsize=(8, 4))
    plt.xlabel('Revenue')
    plt.tight_layout()
    plt.savefig(OUT / 'revenue_by_category.png', dpi=160)
    plt.close()
else:
    print('\nCharts skipped: install dependencies from requirements.txt to generate PNG visualizations.')

print('\nRECOMMENDATIONS')
print('- Prioritize Furniture and Technology bundles because they produce higher-value orders.')
print('- Review low-margin products and negotiate supplier costs where possible.')
print('- Use monthly trend monitoring to identify periods requiring promotional support.')
