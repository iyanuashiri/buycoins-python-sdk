from gql import gql

CREATE_DEPOSIT_ACCOUNT = gql(
    """
    mutation createDepositAccount($accountName: String!) {
        createDepositAccount(accountName: $accountName) {
            accountNumber
            accountName
            accountType
            bankName
            accountReference
        }
    }
"""
)

POST_LIMIT_ORDER = gql(
    """
    mutation postLimitOrder($orderSide: OrderSide!, $coinAmount: BigDecimal!, $cryptocurrency: Cryptocurrency, $staticPrice: BigDecimal, $priceType: PriceType!){
        postLimitOrder(orderSide: $orderSide, coinAmount: $coinAmount, cryptocurrency: $cryptocurrency, staticPrice: $staticPrice, priceType: $priceType) {
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
"""
)

POST_MARKET_ORDER = gql(
    """
    mutation postMarketOrder($orderSide: OrderSide!, $coinAmount: BigDecimal!, $cryptocurrency: Cryptocurrency){
        postMarketOrder(orderSide: $orderSide, coinAmount: $coinAmount, cryptocurrency: $cryptocurrency){
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
"""
)

BUY = gql(
    """
    mutation buy($price: ID!, $coin_amount: BigDecimal!, $cryptocurrency: Cryptocurrency){
        buy(price: $price, coin_amount: $coin_amount, cryptocurrency: $cryptocurrency) {
            id
            cryptocurrency
            status
            totalCoinAmount
            side
        }
    }
"""
)

SELL = gql(
    """
    mutation sell($price: ID!, $coin_amount: BigDecimal!, $cryptocurrency: Cryptocurrency){
        sell(price: $price, coin_amount: $coin_amount, cryptocurrency: $cryptocurrency) {
            id
            cryptocurrency
            status
            totalCoinAmount
            side
        }
    }
"""
)

SEND = gql(
    """
    mutation send($amount: BigDecimal!, $cryptocurrency: Cryptocurrency, $address: String!){
        send(cryptocurrency: $cryptocurrency, amount: $amount, address: $address) {
            id
            address
            amount
            cryptocurrency
            fee
            status
            transaction {
                txhash
                id
            }
        }
    }
"""

)

CREATE_ADDRESS = gql(
    """
    mutation createAddress($cryptocurrency: Cryptocurrency) {
        createAddress(cryptocurrency: $cryptocurrency) {
            cryptocurrency
            address
        }
    }
"""
)