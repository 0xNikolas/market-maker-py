import math
import matplotlib.pyplot as plt

def printBuyInfo(smartTokens, connectorTokens, effectivePrice, tokenBalance, connectorBalance, iteration):
    print("==========================================")
    print(f"      ---- BUY ORDER {iteration + 1} ----")
    print("==========================================")
    print(f" - Tokens Bought: {smartTokens}")
    print(f" - ETH paid: {connectorTokens}")
    print(f" - Effective Price: {effectivePrice}")
    print(f" - Token balance: {tokenBalance}")
    print(f" - Connector balance: {connectorBalance}")
    print("==========================================")


def printSellInfo(smartTokens, connectorTokens, effectivePrice, tokenBalance, connectorBalance, iteration):
    print("==========================================")
    print(f"     ---- SELL ORDER {iteration + 1} ----")
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
    tokenSupply = 1000
    connectorBalance = 250

    def __init__(self):
        self.setPrice()

    def buyTokens(self, eth):
        emittedSmartTokens = self.emitSmartTokens(eth)
        effectivePrice = self.getEffectivePrice(emittedSmartTokens, eth)
        self.increaseTokenSupply(emittedSmartTokens)
        self.increaseEthBalance(eth)
        self.computeCurrentState()

        return emittedSmartTokens, eth, effectivePrice

    def sellTokens(self, smartTokens):
        eth = self.emitEth(smartTokens)
        effectivePrice = self.getEffectivePrice(smartTokens, eth)
        self.decreaseTokenSupply(smartTokens)
        self.decreaseEthBalance(eth)
        self.computeCurrentState()

        return smartTokens, eth, effectivePrice,

    def emitSmartTokens(self, eth):
        emittedSmartTokens = self.tokenSupply * (math.pow((1 + eth / self.connectorBalance), self.connectorWeight) - 1)

        return emittedSmartTokens

    def emitEth(self, smartTokens):
        eth = self.connectorBalance * (math.pow((1 + smartTokens / self.tokenSupply), 1 / self.connectorWeight) - 1)

        return eth

    def setPrice(self):
        if self.connectorBalance != 0:
            self.tokenPrice = self.connectorBalance / (self.tokenSupply * self.connectorWeight)

    def computeCurrentState(self):
        self.setPrice()
        totalValue = self.tokenPrice * self.tokenSupply
        self.connectorWeight = self.connectorBalance / totalValue

    def decreaseTokenSupply(self, howMuch):
        self.tokenSupply -= howMuch

    def increaseTokenSupply(self, howMuch):
        self.tokenSupply += howMuch

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
    print(f"    - Token Balance: {marketMaker.tokenSupply}")
    print(f"    - Connector Balance: {marketMaker.connectorBalance}")
    print("==========================================")


def testMarketMaker(tries):
    marketMaker = MarketMakerFormula()
    orderQuantity = 100
    tokenBalances = []
    tokenPrices = []

    # Buy order
    for i in range(0, tries):
        smartTokens, eth, effectivePrice = marketMaker.buyTokens(100)
        orderQuantity = smartTokens
        printBuyInfo(smartTokens, eth, effectivePrice, marketMaker.tokenSupply, marketMaker.connectorBalance, i)
        tokenBalances.append(marketMaker.tokenSupply)
        tokenPrices.append(marketMaker.tokenPrice)

    # Sell order
    for i in range(0, tries):
        smartTokens, eth, effectivePrice = marketMaker.sellTokens(100)
        printSellInfo(smartTokens, eth, effectivePrice, marketMaker.tokenSupply, marketMaker.connectorBalance, i)
        orderQuantity = eth
        tokenBalances.append(marketMaker.tokenSupply)
        tokenPrices.append(marketMaker.tokenPrice)

    return tokenBalances, tokenPrices


supply, price = testMarketMaker(tries=10000)


# Note that using plt.subplots below is equivalent to using
# fig = plt.figure() and then ax = fig.add_subplot(111)
fig, ax = plt.subplots()
ax.plot(supply, price)

ax.set(xlabel='Token Supply', ylabel='Price',
       title='Market Maker')
ax.grid()

plt.show()
