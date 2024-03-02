#!/usr/bin/env python
# coding: utf-8

# In[18]:


import numpy as np
import pandas as pd
import datetime as dt
import yfinance as yf
import matplotlib.pyplot as plt
from scipy.stats import norm


# In[3]:


#assigning the time frame 

years = 15

endDate = dt.datetime.now()
startDate  = endDate-dt.timedelta(days=365*years)


# In[4]:


# assigning the tickers for the etf of which we want the data

tickers = ['SPY','BND','GLD','QQQ','VTI']


# In[5]:


# adjusted daily close price for the tickers 
# adjusted close prices account for dividends or the stock splits

adj_close_df = pd.DataFrame()

for ticker in tickers:
    data = yf.download(ticker,start = startDate, end = endDate)
    adj_close_df[ticker] = data['Adj Close']
print(adj_close_df)


# In[7]:


# daily log returns
# log return are easier for calculation

log_returns = np.log(adj_close_df/adj_close_df.shift(1))
log_returns = log_returns.dropna()

log_returns


# In[8]:


# now we will create equally weighted portfolio

portfolio_value = 1000000
weights = np.array([1/len(tickers)]*len(tickers))
print(weights)


# In[10]:


#now we will calculate the historical portfolio return

historical_returns = (log_returns*weights).sum(axis = 1)
print(historical_returns)


# In[11]:


# now we find X-days historical returns
# the window here is like the average of the previous days on the each date
# example on 16/03/2009 the average returns is
# the sum of all previous 5 days returns
# (here we have 5 previous days)

days = 5

range_returns = historical_returns.rolling(window = days).sum()
range_returns = range_returns.dropna()
print(range_returns)


# In[ ]:


# now lets specify the confidence interval and var calculation


# In[24]:


confidence_interval = 0.95 #this confidence is of var not 

VaR = np.percentile(range_returns,(100-confidence_interval*100))*portfolio_value
print("The Value at risk in Dollar is:" ,VaR)


# In[25]:


return_window  = days
range_returns = historical_returns.rolling(window = return_window).sum()
range_returns = range_returns.dropna()

range_returns_dollar = range_returns*portfolio_value

plt.hist(range_returns_dollar.dropna(),bins = 50,density = True)
plt.xlabel(f'{return_window}-Day Portfolio Return (Dollar Value)')
plt.ylabel('Frequency')
plt.title(f'Distribution of portfolio {return_window}- Day Return(Dollar Value)')
plt.axvline(VaR, color='r',linestyle='dashed',linewidth = 2, label = f'Var at {confidence_interval:.0%} confidence level')
plt.legend()
plt.show()


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




