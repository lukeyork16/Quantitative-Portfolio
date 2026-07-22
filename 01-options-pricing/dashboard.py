import streamlit as st
from blackscholes import price, delta, gamma, vega, theta, rho

st.title("Options Pricing Dashboard")
st.write("Adjust the sliders on the left and watch the price and Greeks update in real time.")

#sidebar sliders let you adjust every input and watch price/greeks update live
S=st.sidebar.slider("Stock Price", 50, 200, 100)
K=st.sidebar.slider("Strike Price", 50, 200, 100)
T=st.sidebar.slider("Time to Expiration (years)", 0.01, 2.0, 1.0)
r=st.sidebar.slider("Risk-Free Rate", 0.0, 0.10, 0.05)
sigma=st.sidebar.slider("Volatility", 0.05, 1.0, 0.20)
optiontype=st.sidebar.selectbox("Option Type", ["call", "put"])

#run all the pricing functions with whatever the sliders are set to
p=price(S,K,T,r,sigma,optiontype=optiontype)
d=delta(S,K,T,r,sigma,optiontype=optiontype)
g=gamma(S,K,T,r,sigma)
v=vega(S,K,T,r,sigma)
th=theta(S,K,T,r,sigma,optiontype=optiontype)
rh=rho(S,K,T,r,sigma,optiontype=optiontype)

st.metric("Price", f"{p:.2f}")
st.caption("The fair value of the option today, given everything set in the sidebar.")

col1,col2,col3=st.columns(3)
col1.metric("Delta", f"{d:.4f}")
col1.caption("How much the price moves for every $1 move in the stock. A 0.60 delta call behaves like owning 60 shares.")

col2.metric("Gamma", f"{g:.4f}")
col2.caption("How fast Delta itself changes. High gamma means your exposure shifts quickly as the stock moves.")

col3.metric("Vega", f"{v/100:.4f}")
col3.caption("How much the price changes for a 1 percentage point move in volatility (e.g. 20% to 21%).")

col4,col5=st.columns(2)
col4.metric("Theta (per day)", f"{th/365:.4f}")
col4.caption("How much value the option loses per day just from time passing, holding everything else fixed.")

col5.metric("Rho", f"{rh/100:.4f}")
col5.caption("How much the price changes for a 1 percentage point move in interest rates. Usually the smallest effect.")

#expandable section with the fuller explanation, so the dashboard stays clean but the depth is there if someone wants it
with st.expander("What is Black-Scholes actually doing?"):
    st.write("""
    Black-Scholes prices an option as an expected value: what you'd expect to receive at expiration
    (the stock, if it finishes above the strike for a call), minus what you'd expect to pay (the strike,
    discounted back to today), it is then weighted by the probability each of those things actually happens.

    It works by assuming the stock price moves randomly and can't go negative, with returns that are roughly
    symmetric in percentage terms. Volatility (sigma) is the main driver of how much the option is worth
    beyond its intrinsic value, since higher volatility means a wider range of possible outcomes.
    """)

with st.expander("Why does Theta only matter for Gamma?"):
    st.write("""
    Theta and Gamma are opposite sides of the same trade-off. An option with high Gamma reacts fast to
    stock moves, which is valuable, but the market charges you for that value every single day through
    Theta decay. This is why options are sometimes called a "wasting asset": you're paying rent on
    the possibility of a big move, whether or not it happens.
    """)
