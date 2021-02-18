from gql import gql

CURRENT_BUYCOINS_PRICE = gql(
    """
    query {
      buycoinsPrices(side: buy, mode: standard, cryptocurrency: bitcoin){
        buyPricePerCoin
        cryptocurrency
        id
        maxBuy
        maxSell
        minBuy
        minCoinAmount
        minSell
        mode
        sellPricePerCoin
        status
      }
    }
"""
)

GET_ORDERS = gql(
    """
    query getOrders($status: GetOrdersStatus!){
        getOrders(status: $status) {
            dynamicPriceExpiry
            orders {
                edges {
                    node {
                        id
                        cryptocurrency
                        coinAmount
                        side
                        status
                        createdAt
                        pricePerCoin
                        priceType
                        staticPrice
                        dynamicExchangeRate
                    }
                }
            }
        }
    }
"""
)

GET_MARKET_BOOK_DEFAULT = gql(
    """
    query {
      getMarketBook {
        dynamicPriceExpiry
        orders {
          edges {
            node {
              id
              cryptocurrency
              coinAmount
              side
              status 
              createdAt
              pricePerCoin
              priceType
              staticPrice
              dynamicExchangeRate
            }
          }
        }
      }
    }
"""
)

GET_MARKET_BOOK = gql(
    """
    query {
      getMarketBook {
        dynamicPriceExpiry
        orders {
          edges {
            node {
              id
              cryptocurrency
              coinAmount
              side
              status 
              createdAt
              pricePerCoin
              priceType
              staticPrice
              dynamicExchangeRate
            }
          }
        }
      }
    }
"""
)


CURRENT_GET_PRICES = gql(
    """
    query GetBuyCoinsPrices($side: OrderSide, $currency: Cryptocurrency) {
        getPrices(side: $side, cryptocurrency: $currency){
            buyPricePerCoin
            cryptocurrency
            id
            maxBuy
            maxSell
            minBuy
            minCoinAmount
            minSell
            sellPricePerCoin
            status
        }
    }
"""
)

GET_PRICES = gql(
    """
    query{
      getPrices{
        id
        cryptocurrency
        sellPricePerCoin
        buyPricePerCoin
        minBuy
        maxBuy
        expiresAt
      }
    }
"""
)

GET_ESTIMATED_NETWORK_FEE = gql(
    """
    query getEstimatedNetworkFee($cryptocurrency: Cryptocurrency, $amount: BigDecimal!) {
        getEstimatedNetworkFee(cryptocurrency: $cryptocurrency, amount: $amount) {
            estimatedFee
            total
        }
    }
"""
)

GET_BALANCES_ = gql(
    """
    query($cryptocurrency: Cryptocurrency) {
        getBalances(cryptocurrency: $cryptocurrency) {
            id
            cryptocurrency
            confirmedBalance
        }
    }
"""
)

GET_BALANCES = gql(
    """
    query {
        getBalances{
            id
            cryptocurrency
            confirmedBalance
        }
    }
"""
)
