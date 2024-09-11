Trading Strategies Using Python

This project implements several trading strategies using historical stock data downloaded from Yahoo Finance (yfinance), with backtesting provided by the Backtesting Python library. The strategies include moving average crossover, breakout strategies, mean reversion, and trend-following techniques. Each strategy generates buy/sell signals based on technical indicators and evaluates performance through backtesting.

Key Features
Historical Data Retrieval: Fetches historical stock data using yfinance.
Technical Indicators: Calculates moving averages, standard deviations, and other metrics for decision-making.
Backtesting: Simulates trading strategies and evaluates their performance using the Backtesting library.
Optimization: Allows parameter optimization for improved strategy performance.
Requirements
Before running the code, make sure to install the necessary Python libraries:

bash
Copy code
pip install numpy pandas yfinance matplotlib seaborn backtesting
How to Use
Download Historical Data:

The script downloads daily stock data and Implement Trading Strategies:

Moving Average Crossover: Compares short-term and long-term moving averages to generate buy/sell signals.
Breakout Strategy: Detects potential breakouts based on volatility and price movement.
Mean Reversion: Buys when the stock price is below its average and sells when above.
Trend Following: Buys during an uptrend and sells during a downtrend based on moving averages.
Run Backtesting:

Each strategy is backtested using the Backtesting library to simulate trades and calculate performance metrics such as return, Sharpe ratio, and maximum drawdown.
Optimization:

For the Mean Reversion Buy strategy, optimization is available, adjusting parameters to maximize returns.
Trading Strategies
1. Moving Average Crossover
    # Computes 3-day and 14-day moving averages.
    # Generates buy signals when the 3-day MA crosses above the 14-day MA.
    # Generates sell signals when the 3-day MA crosses below the 14-day MA.
2. Breakout Strategy (Upward)
    # Identifies upward breakouts based on the price crossing the 14-day moving average.
    # Uses volatility comparison between the 14-day and 30-day standard deviation for additional signal filtering.
3. Breakout Strategy (Downward)
    # Identifies downward breakouts when the price falls below the 14-day moving average.
    # Similar volatility comparison as BreakoutUp.
4. Mean Reversion (Buy)
    # Buys when the stock price is below the 14-day moving average.
    # Sells when the price rises above a certain threshold of standard deviation.
    # Includes an optimization process to maximize returns.
5. Mean Reversion (Sell)
    # Sells when the stock price is significantly below its 14-day moving average.
    # Closes the position when the price reverts to the mean.
6. Trend Following
    # Buys when the stock is in an uptrend (i.e., when the 7-day MA is above the 100-day MA).
    # Sells when the stock is in a downtrend (i.e., when the 7-day MA is below the 100-day MA).

Example Usage
To run the Trend Following strategy on Microsoft (MSFT) stock:

python
Copy code
TrendFollowing(MSFT)
To run the Mean Reversion Buy strategy:

python
Copy code
MeanReversionBuy(MSFT)
Visualizing Results
The Backtesting library will automatically plot the results of the strategy, including the portfolio performance, equity curve, and buy/sell signals.

Conclusion
This project provides a set of trading strategies that can be applied to various financial assets. It includes technical analysis and backtesting to validate the performance of these strategies. Users can further modify and optimize the strategies based on their requirements.
