# Suppressing all FutureWarnings because they are cluttering the console.
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
from pathlib import Path
# INF601 - Advanced Programming in Python
# Michael DeGan
# Mini Project 1

# (5/5 points) Initial comments with your name, class and project at the top of your .py file.
# (5/5 points) Proper import of packages used.
# (20/20 points) Using an API of your choice (yfinance works), collect the closing price of 5 of your favorite stock
# tickers for the last 10 trading days.
# (10/10 points) Store this information in a list that you will convert to an array in NumPy.
# (10/10 points) Plot these 5 graphs. Feel free to add as much information to the graphs as you like exploring the
# documentation for matplotlib. At minimum it just needs to show 10 data points.
# (10/10 points) Save these graphs in a folder called charts as PNG files. Do not upload these to your project folder,
# the project should save these when it executes. You may want to add this folder to your .gitignore file.
# (10/10 points) There should be a minimum of 5 commits on your project, be sure to commit often!
# (10/10 points) I will be checking out the main branch of your project. Please be sure to include a requirements.txt
# file which contains all the packages that need installed. You can create this fille with the output of pip freeze at
# the terminal prompt.
# (20/20 points) There should be a README.md file in your project that explains what your project is, how to install
# the pip requirements, and how to execute the program. Please use the GitHub flavor of Markdown.


def getClosing(ticker):
    # Get the closing price for the last 10 trading days
    stock = yf.Ticker(ticker)
    # get historical market data
    hist = stock.history(period="10d")

    closingList = []

    for price in hist['Close']:
        closingList.append(price)

    return closingList

def printGraph(stock):
    stockClosing = np.array(getClosing(stock))
    # This conditional had to be added to account for all of the errors that Ticker throws, as well as the fact that
    # getClosing() will just return an empty array for invalid symbols, which leads to index errors.
    if stockClosing.size == 0:
        print("10 day closing prices for this stock are unavailable. Graphing operation failed.")
        return

    days = list(range(1, len(stockClosing) + 1))

    # This plots the graph
    plt.plot(days, stockClosing)

    # Get our min and max for y
    prices = getClosing(stock)
    prices.sort()
    low_price = prices[0]
    high_price = prices[-1]

    # Set our x-axis min and max
    plt.axis([1, 10, low_price - 2, high_price + 2])

    # Set our labels for the graph
    plt.xlabel("Days")
    plt.ylabel("Closing Price")
    plt.title(f"{stock} Closing Price")

    # Saves plot
    saveFile = "charts/" + stock + ".png"
    plt.savefig(saveFile)

    # Show the graph
    plt.show()

# Old getStocks() function to collect user input.
# def getStocks():
#     stocks = []
#
#     print("Please enter 5 stocks to graph:")
#     for i in range(1, 6):
#         while True:
#             print("Enter stock ticker " + str(i))
#             userValue = input("> ")
#             stock = yf.Ticker(userValue)
#             print("Checking ticker...")
#
#             # This section had to be refactored because try-except statements cannot handle the various types of errors
#             # that Ticker.info throws. Note: stock.info will always have 1 entry, even for invalid ticker symbols.
#             if len(stock.info) > 1:
#                 stocks.append(userValue)
#                 print("Valid input.")
#                 break
#             else:
#                 print("Invalid ticker. Please try again.")
#
#     return stocks

# Start of program
try:
    #Create our charts folder.
    Path("charts").mkdir()
except FileExistsError:
    pass

#Collect and validate symbols from end-user, output as graphs, store in directory "charts."

theStocks = ["GOOG", "COST", "WMT", "SMSN.L", "LYFT"]

for stock in theStocks:
    getClosing(stock)
    printGraph(stock)