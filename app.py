import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title='Daily Expense Manager', page_icon='💰', layout='wide')

CATEGORIES = ['Food', 'Travel', 'Shopping', 'Bills', 'Health', 'Education', 'Entertainment', 'Other']
PAYMENT_METHODS = ['Cash', 'UPI', 'Card', 'Bank Transfer', 'Other']
COLUMNS = ['Date', 'Category', 'Description', 'Amount', 'Payment Method']

if 'expenses' not in st.session_state:
    st.session_state.expenses = pd.DataFrame(columns=COLUMNS)

st.title('💰 Daily Expense Manager')
st.caption('Practice Streamlit app for tracking everyday expenses.')

with st.sidebar:
    st.header('Add Expense')
    expense_date = st.date_input('Date', value=date.today())
    category = st.selectbox('Category', CATEGORIES)
    description = st.text_input('Description', placeholder='e.g. Lunch')
    amount = st.number_input('Amount (₹)', min_value=0.0, step=10.0, format='%.2f')
    payment = st.selectbox('Payment Method', PAYMENT_METHODS)
    if st.button('Add Expense', type='primary', use_container_width=True):
        if amount <= 0:
            st.error('Enter an amount greater than ₹0.')
        elif not description.strip():
            st.error('Enter a short description.')
        else:
            row = pd.DataFrame([{
                'Date': expense_date.isoformat(),
                'Category': category,
                'Description': description.strip(),
                'Amount': float(amount),
                'Payment Method': payment,
            }])
            st.session_state.expenses = pd.concat([st.session_state.expenses, row], ignore_index=True)
            st.success('Expense added.')

expenses = st.session_state.expenses.copy()
if not expenses.empty:
    expenses['Amount'] = pd.to_numeric(expenses['Amount'], errors='coerce').fillna(0.0)
    expenses['Date'] = pd.to_datetime(expenses['Date']).dt.date

total = float(expenses['Amount'].sum()) if not expenses.empty else 0.0
today_total = float(expenses.loc[expenses['Date'] == date.today(), 'Amount'].sum()) if not expenses.empty else 0.0
count = len(expenses)

c1, c2, c3 = st.columns(3)
c1.metric('Total Expenses', f'₹{total:,.2f}')
c2.metric("Today's Spending", f'₹{today_total:,.2f}')
c3.metric('Transactions', f'{count}')

st.subheader('Expense History')
if expenses.empty:
    st.info('No expenses yet. Add your first expense from the sidebar.')
else:
    display = expenses.sort_values('Date', ascending=False).reset_index(drop=False).rename(columns={'index':'Record'})
    st.dataframe(display[COLUMNS], use_container_width=True, hide_index=True)

    left, right = st.columns(2)
    with left:
        st.subheader('Spending by Category')
        category_totals = expenses.groupby('Category', as_index=True)['Amount'].sum().sort_values(ascending=False)
        st.bar_chart(category_totals)
    with right:
        st.subheader('Daily Spending')
        daily_totals = expenses.groupby('Date', as_index=True)['Amount'].sum().sort_index()
        st.line_chart(daily_totals)

    st.subheader('Manage Data')
    record_to_delete = st.selectbox(
        'Select a transaction to delete',
        options=list(range(len(expenses))),
        format_func=lambda i: f"{expenses.iloc[i]['Date']} — {expenses.iloc[i]['Description']} — ₹{expenses.iloc[i]['Amount']:,.2f}",
    )
    b1, b2, b3 = st.columns(3)
    if b1.button('Delete Selected', use_container_width=True):
        st.session_state.expenses = st.session_state.expenses.drop(st.session_state.expenses.index[record_to_delete]).reset_index(drop=True)
        st.rerun()
    if b2.button('Clear All', use_container_width=True):
        st.session_state.expenses = pd.DataFrame(columns=COLUMNS)
        st.rerun()
    csv_data = expenses.to_csv(index=False).encode('utf-8')
    b3.download_button('Download CSV', data=csv_data, file_name='daily_expenses.csv', mime='text/csv', use_container_width=True)

st.divider()
st.caption('Note: This practice version uses Streamlit session storage. Data resets when the app/session restarts.')
