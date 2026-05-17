import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

# ============================================
# LOAD DATA
# ============================================

df = pd.read_csv(
    r"C:\Users\rajpu\Downloads\olist_dataset.csv\final_dashboard_data.csv"
)

# ============================================
# DATETIME CONVERSION
# ============================================

df['order_purchase_timestamp'] = pd.to_datetime(
    df['order_purchase_timestamp']
)

# ============================================
# CREATE MONTH COLUMN
# ============================================

df['purchase_month'] = (
    df['order_purchase_timestamp']
    .dt.month_name()
)

# ============================================
# KPI VALUES
# ============================================

TOTAL_ORDERS = df['order_id'].nunique()

TOTAL_REVENUE = round(
    df['price'].sum(),
    2
)

AVG_REVIEW = round(
    df['review_score'].mean(),
    2
)

AVG_DELIVERY = round(
    df['delivery_days'].mean(),
    2
)

# ============================================
# CREATE APP
# ============================================

app = Dash(__name__)

app.title = "Olist Dashboard"

# ============================================
# APP LAYOUT
# ============================================

app.layout = html.Div([

    # TITLE

    html.H1(
        "Olist E-Commerce Dashboard",
        style={
            'textAlign': 'center',
            'marginBottom': '30px'
        }
    ),

    # ============================================
    # DROPDOWN FILTER
    # ============================================

    html.Div([

        html.Label("Select Month"),

        dcc.Dropdown(

            id='month_filter',

            options=[
                {
                    'label': month,
                    'value': month
                }

                for month in sorted(
                    df['purchase_month']
                    .dropna()
                    .unique()
                )
            ],

            multi=True,

            placeholder='Select Month'
        )

    ], style={
        'width': '40%',
        'margin': 'auto',
        'marginBottom': '30px'
    }),

    # ============================================
    # KPI CARDS
    # ============================================

    html.Div([

        # TOTAL ORDERS

        html.Div([

            html.H3("Total Orders"),

            html.H2(f"{TOTAL_ORDERS:,}")

        ], style={
            'border': '1px solid lightgray',
            'padding': '20px',
            'borderRadius': '10px',
            'width': '22%',
            'textAlign': 'center',
            'backgroundColor': '#F8F9FA'
        }),

        # TOTAL REVENUE

        html.Div([

            html.H3("Total Revenue"),

            html.H2(f"${TOTAL_REVENUE:,}")

        ], style={
            'border': '1px solid lightgray',
            'padding': '20px',
            'borderRadius': '10px',
            'width': '22%',
            'textAlign': 'center',
            'backgroundColor': '#F8F9FA'
        }),

        # AVG REVIEW

        html.Div([

            html.H3("Average Review"),

            html.H2(f"{AVG_REVIEW}")

        ], style={
            'border': '1px solid lightgray',
            'padding': '20px',
            'borderRadius': '10px',
            'width': '22%',
            'textAlign': 'center',
            'backgroundColor': '#F8F9FA'
        }),

        # AVG DELIVERY

        html.Div([

            html.H3("Avg Delivery Days"),

            html.H2(f"{AVG_DELIVERY}")

        ], style={
            'border': '1px solid lightgray',
            'padding': '20px',
            'borderRadius': '10px',
            'width': '22%',
            'textAlign': 'center',
            'backgroundColor': '#F8F9FA'
        })

    ], style={
        'display': 'flex',
        'justifyContent': 'space-between',
        'marginBottom': '40px'
    }),

    # ============================================
    # CHARTS
    # ============================================

    dcc.Graph(id='monthly_sales_chart'),

    dcc.Graph(id='top_categories_chart'),

    dcc.Graph(id='review_distribution_chart'),

    dcc.Graph(id='payment_method_chart')

], style={
    'padding': '20px',
    'fontFamily': 'Arial'
})

# ============================================
# CALLBACK
# ============================================

@app.callback(

    [
        Output('monthly_sales_chart', 'figure'),

        Output('top_categories_chart', 'figure'),

        Output('review_distribution_chart', 'figure'),

        Output('payment_method_chart', 'figure')
    ],

    [
        Input('month_filter', 'value')
    ]

)

def update_dashboard(selected_months):

    filtered_df = df.copy()

    # ============================================
    # FILTER DATA
    # ============================================

    if selected_months:

        filtered_df = filtered_df[
            filtered_df['purchase_month']
            .isin(selected_months)
        ]

    # ============================================
    # MONTHLY SALES CHART
    # ============================================

    sales_data = (

        filtered_df
        .groupby('purchase_month')['price']
        .sum()
        .reset_index()

    )

    monthly_sales_fig = px.line(

        sales_data,

        x='purchase_month',

        y='price',

        title='Monthly Sales Trend',

        markers=True
    )

    # ============================================
    # TOP PRODUCT CATEGORIES
    # ============================================

    top_categories = (

        filtered_df['product_category_name']
        .value_counts()
        .head(10)
        .reset_index()

    )

    top_categories.columns = [
        'Category',
        'Orders'
    ]

    top_categories_fig = px.bar(

        top_categories,

        x='Category',

        y='Orders',

        title='Top 10 Product Categories'
    )

    # ============================================
    # REVIEW DISTRIBUTION
    # ============================================

    review_fig = px.histogram(

        filtered_df,

        x='review_score',

        title='Review Score Distribution'
    )

    # ============================================
    # PAYMENT METHOD CHART
    # ============================================

    payment_data = (

        filtered_df['payment_type']
        .value_counts()
        .reset_index()

    )

    payment_data.columns = [
        'Payment Type',
        'Count'
    ]

    payment_fig = px.pie(

        payment_data,

        names='Payment Type',

        values='Count',

        title='Payment Method Usage'
    )

    return (

        monthly_sales_fig,

        top_categories_fig,

        review_fig,

        payment_fig
    )

# ============================================
# RUN APP
# ============================================

if __name__ == '__main__':
    app.run(debug=True)