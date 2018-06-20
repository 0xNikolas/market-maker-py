import math
import matplotlib.pyplot as plt

def printBuyInfo(smartTokens, connectorTokens, effectivePrice, tokenBalance, connectorBalance):
    print("==========================================")
    print(f"          ---- BUY ORDER ----            ")
    print("==========================================")
    print(f" - Tokens Bought: {smartTokens}")
    print(f" - ETH paid: {connectorTokens}")
    print(f" - Effective Price: {effectivePrice}")
    print(f" - Token balance: {tokenBalance}")
    print(f" - Connector balance: {connectorBalance}")
    print("==========================================")


def printSellInfo(smartTokens, connectorTokens, effectivePrice, tokenBalance, connectorBalance):
    print("==========================================")
    print(f"          ---- SELL ORDER ----           ")
    print("==========================================")
    print(f" - Tokens Sold: {smartTokens}")
    print(f" - ETH received: {connectorTokens}")
    print(f" - Effective Price: {effectivePrice}")
    print(f" - Token balance: {tokenBalance}")
    print(f" - Connector balance: {connectorBalance}")
    print("==========================================")


class MarketMakerFormula:
    connectorWeight = 0.5
    tokenPrice = 1
    tokenBalance = 1000
    connectorBalance = 250

    def __init__(self):
        self.setPrice()

    def buyTokens(self, eth):
        emittedSmartTokens = self.emitSmartTokens(eth)
        effectivePrice = self.getEffectivePrice(emittedSmartTokens, eth)
        self.increaseTokenBalance(emittedSmartTokens)
        self.decreaseEthBalance(eth)
        self.computeCurrentState()

        return emittedSmartTokens, eth, effectivePrice

    def sellTokens(self, smartTokens):
        eth = self.emitEth(smartTokens)
        effectivePrice = self.getEffectivePrice(smartTokens, eth)
        self.increaseEthBalance(eth)
        self.decreaseTokenBalance(smartTokens)
        self.computeCurrentState()

        return smartTokens, eth, effectivePrice,

    def emitSmartTokens(self, eth):
        emittedSmartTokens = self.tokenBalance * (math.pow((1 + eth / self.connectorBalance), self.connectorWeight) - 1)

        return emittedSmartTokens

    def emitEth(self, smartTokens):
        eth = self.connectorBalance * (math.pow((1 + smartTokens / self.tokenBalance),  1 / self.connectorWeight) - 1)

        return eth

    def setPrice(self):
        if self.connectorBalance != 0:
            self.tokenPrice = self.connectorBalance / (self.tokenBalance * self.connectorWeight)

    def computeCurrentState(self):
        self.setPrice()
        totalValue = self.tokenPrice * self.tokenBalance
        self.connectorWeight = self.connectorBalance / totalValue

    def decreaseTokenBalance(self, howMuch):
        self.tokenBalance -= howMuch

    def increaseTokenBalance(self, howMuch):
        self.tokenBalance += howMuch

    def decreaseEthBalance(self, howMuch):
        self.connectorBalance -= howMuch

    def increaseEthBalance(self, howMuch):
        self.connectorBalance += howMuch

    def getEffectivePrice(self, smartTokens, connectorTokens):
        return connectorTokens / smartTokens


def printMarketMakerStatus(marketMaker: MarketMakerFormula):
    print("==========================================")
    print(f"      ---- MARKET-MAKER STATUS ----      ")
    print("==========================================")
    print(f"    - Token Price: {marketMaker.tokenPrice}")
    print(f"    - Token Balance: {marketMaker.tokenBalance}")
    print(f"    - Connector Balance: {marketMaker.connectorBalance}")
    print("==========================================")


def testMarketMaker(tries):
    marketMaker = MarketMakerFormula()
    orderQuantity = 100
    tokenBalances = []
    tokenPrices = []

    for i in range(0, tries):
        # Buy order
        smartTokens, eth, effectivePrice = marketMaker.buyTokens(orderQuantity)
        orderQuantity = smartTokens
        printBuyInfo(smartTokens, eth, effectivePrice, marketMaker.tokenBalance, marketMaker.connectorBalance)
        tokenBalances.append(marketMaker.tokenBalance)
        tokenPrices.append(marketMaker.tokenPrice)

    for i in range(0, tries):
        # Sell order
        smartTokens, eth, effectivePrice = marketMaker.sellTokens(orderQuantity)
        printSellInfo(smartTokens, eth, effectivePrice, marketMaker.tokenBalance, marketMaker.connectorBalance)
        orderQuantity = eth
        tokenBalances.append(marketMaker.tokenBalance)
        tokenPrices.append(marketMaker.tokenPrice)

    return tokenBalances, tokenPrices


supply, price = testMarketMaker(tries=100)


# Note that using plt.subplots below is equivalent to using
# fig = plt.figure() and then ax = fig.add_subplot(111)
fig, ax = plt.subplots()
ax.plot(supply, price)

ax.set(xlabel='Token Supply', ylabel='Price',
       title='Market Maker')
ax.grid()

plt.show()
