import streamlit as st
from blackscholes import price, delta, gamma, vega, theta, rho

st.title("Options Pricing Dashboard")

#sidebar sliders let you adjust every input and watch price/greeks update live
S = st.sidebar.slider("Stock Price", 50, 200, 100)
K = st.sidebar.slider("Strike Price", 50, 200, 100)
T = st.sidebar.slider("Time to Expiration (years)", 0.01, 2.0, 1.0)
r = st.sidebar.slider("Risk-Free Rate", 0.0, 0.10, 0.05)
sigma = st.sidebar.slider("Volatility", 0.05, 1.0, 0.20)
optiontype = st.sidebar.selectbox("Option Type", ["call", "put"])

#run all the pricing functions with whatever the sliders are set to
p = price(S, K, T, r, sigma, optiontype=optiontype)
d = delta(S, K, T, r, sigma, optiontype=optiontype)
g = gamma(S, K, T, r, sigma)
v = vega(S, K, T, r, sigma)
th = theta(S, K, T, r, sigma, optiontype=optiontype)
rh = rho(S, K, T, r, sigma, optiontype=optiontype)

st.metric("Price", f"{p:.2f}")

col1, col2, col3 = st.columns(3)
col1.metric("Delta", f"{d:.4f}")
col2.metric("Gamma", f"{g:.4f}")
col3.metric("Vega", f"{v/100:.4f}")

col4, col5 = st.columns(2)
col4.metric("Theta (per day)", f"{th/365:.4f}")
col5.metric("Rho", f"{rh/100:.4f}")
