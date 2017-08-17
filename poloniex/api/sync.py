from datetime import datetime
from datetime import timedelta

import requests

from poloniex.error import PoloniexError
from poloniex.api.base import command_operator, BasePublicApi, BaseTradingApi

__author__ = 'andrew.shvv@gmail.com'


class PublicApi(BasePublicApi):
    url = "https://poloniex.com/public?"

    def api_call(self, *args, **kwargs):
        response = requests.get(self.url, *args, **kwargs)

        if response.status_code == 200:
            return response.json()
        else:
            raise PoloniexError('Got {} when calling {}.'.format(response.status_code, self.url))

    @command_operator
    def returnTicker(self):
        """
        Returns the ticker for all markets
        """
        pass

    @command_operator
    def return24hVolume(self):
        """
        Returns the 24-hour volume for all markets, plus totals for primary currencies.
        """
        pass

    @command_operator
    def returnOrderBook(self, currency_pair="all", depth=50):
        """
        Returns the order book for a given market, as well as a sequence number for use with the Push API and an indicator
        specifying whether the market is frozen. You may set currencyPair to "all" to get the order books of all markets
        """
        pass

    @command_operator
    def returnChartData(self,
                        currency_pair,
                        start=datetime.now() - timedelta(days=1),
                        end=datetime.now(),
                        period=300):
        """
        Returns candlestick chart data. Required GET parameters are "currencyPair", "period" (candlestick period in seconds;
        valid values are 300, 900, 1800, 7200, 14400, and 86400), "start", and "end". "Start" and "end" are given in UNIX
        timestamp format and used to specify the date range for the data returned.
        """
        pass

    @command_operator
    def returnCurrencies(self):
        """
        Returns information about currencies
        """
        pass

    @command_operator
    def returnTradeHistory(self,
                           currency_pair="all",
                           start=datetime.now() - timedelta(days=1),
                           end=datetime.now()):
        """
        Returns the past 200 trades for a given market, or up to 50,000 trades between a range specified in UNIX timestamps
        by the "start" and "end" GET parameters.
        """
        pass


class TradingApi(BaseTradingApi):
    url = "https://poloniex.com/tradingApi?"

    def api_call(self, *args, **kwargs):
        data, headers = self.secure_request(kwargs.get('data', {}), kwargs.get('headers', {}))

        kwargs['data'] = data
        kwargs['headers'] = headers

        response = requests.post(self.url, *args, **kwargs)
        if response.status_code == 200:
            return response.json()
        else:
            raise PoloniexError('Got {} when calling {}.'.format(response.status_code, self.url))

    @command_operator
    def returnBalances(self):
        """
        Returns all of your available balances
        """
        pass

    @command_operator
    def returnCompleteBalances(self):
        """
        Returns all of your balances, including available balance, balance on orders, and the estimated BTC value of your balance.
        """
        pass

    @command_operator
    def returnDepositAddresses(self):
        """
        Returns all of your deposit addresses.
        """
        pass

    @command_operator
    def generateNewAddress(self, currency):
        """
        Generates a new deposit address for the specified currency.
        """
        pass

    @command_operator
    def returnDepositsWithdrawals(self,
                                  start=datetime.now() - timedelta(days=1),
                                  end=datetime.now()):
        """
        Returns your deposit and withdrawal history within a range, specified by the "start" and "end" POST parameters,
        both of which should be given as UNIX timestamps
        """
        pass

    @command_operator
    def returnOpenOrders(self, currency_pair="all"):
        """
        Returns your open orders for a given market, specified by the "currencyPair" POST parameter, e.g. "BTC_XCP".
        Set "currencyPair" to "all" to return open orders for all markets.
        """
        pass

    @command_operator
    def returnTradeHistory(self,
                           currency_pair="all",
                           start=datetime.now() - timedelta(days=1),
                           end=datetime.now()):
        """
        Returns your trade history for a given market, specified by the "currencyPair" POST parameter.
        You may specify "all" as the currencyPair to receive your trade history for all markets. You may optionally
        specify a range via "start" and/or "end" POST parameters, given in UNIX timestamp format; if you do not specify
        a range, it will be limited to one day.
        """
        pass

    @command_operator
    def returnOrderTrades(self, order_number):
        """
        Returns all trades involving a given order, specified by the "orderNumber" POST parameter. If no trades for the order
        have occurred or you specify an order that does not belong to you, you will receive an error.
        """

    @command_operator
    def buy(self,
            currency_pair,
            rate,
            amount):
        """
        Places a limit buy order in a given market. Required POST parameters are "currencyPair", "rate", and "amount".
        If successful, the method will return the order number
        """
        pass

    @command_operator
    def sell(self,
             currency_pair,
             rate,
             amount):
        """
        Places a sell order in a given market
        """
        pass

    @command_operator
    def cancelOrder(self, order_number):
        """
        Cancels an order you have placed in a given market. Required POST parameter is "orderNumber"
        """
        pass

    @command_operator
    def moveOrder(self, order_number, rate, amount):
        """
        Cancels an order and places a new one of the same type in a single atomic transaction, meaning either both
        operations will succeed or both will fail. Required POST parameters are "orderNumber" and "rate"; you may
        optionally specify "amount" if you wish to change the amount of the new order.
        TODO: "postOnly" or "immediateOrCancel" may be specified for exchange orders, but will have no effect on margin orders.
        """
        pass

    @command_operator
    def withdraw(self, currency, amount, address):
        """
        Immediately places a withdrawal for a given currency, with no email confirmation. In order to use this method,
        the withdrawal privilege must be enabled for your API key. Required POST parameters are "currency", "amount",
        and "address". For XMR withdrawals, you may optionally specify "paymentId".
        """
        pass

    @command_operator
    def returnFeeInfo(self):
        """
        If you are enrolled in the maker-taker fee schedule, returns your current trading fees and trailing 30-day volume in BTC.
        This information is updated once every 24 hours.
        """
        pass

    @command_operator
    def returnAvailableAccountBalances(self):
        """
        Returns your balances sorted by account.
        TODO: You may optionally specify the "account" POST parameter if you wish to fetch only the balances of one account.
        Please note that balances in your margin account may not be accessible if you have any open margin positions or orders.
        """
        pass

    @command_operator
    def returnTradableBalances(self):
        """
        Returns your current tradable balances for each currency in each market for which margin trading is enabled.
        Please note that these balances may vary continually with market conditions.
        """
        pass

    @command_operator
    def returnMarginAccountSummary(self):
        """
        Returns a summary of your entire margin account. This is the same information you will find in the
        Margin Account section of the Margin Trading page, under the Markets list.
        """
        pass

    @command_operator
    def marginBuy(self,
                  currency_pair,
                  rate,
                  amount,
                  lending_rate=1):
        """
        Places a margin buy order in a given market.
        Required POST parameters are "currencyPair", "rate", and "amount".
        You may optionally specify a maximum lending rate using the "lendingRate" parameter.
        If successful, the method will return the order number and any trades immediately resulting from your order.
        """
        pass

    @command_operator
    def marginSell(self,
                  currency_pair,
                  rate,
                  amount,
                  lending_rate=1):
        """
        Places a margin sell order in a given market.
        Parameters and output are the same as for the marginBuy method.
        """
        pass

    @command_operator
    def getMarginPosition(self, currency_pair):
        """
        Returns information about your margin position in a given market, specified by the "currencyPair" POST parameter.
        You may set "currencyPair" to "all" if you wish to fetch all of your margin positions at once.
        If you have no margin position in the specified market, "type" will be set to "none". "liquidationPrice"
        is an estimate, and does not necessarily represent the price at which an actual forced liquidation will occur. If you have no liquidation price, the value will be -1.
        """
        pass

    @command_operator
    def closeMarginPosition(self, currency_pair):
        """
        Closes your margin position in a given market (specified by the "currencyPair" POST parameter) using a market order.
        This call will also return success if you do not have an open position in the specified market.
        """
        pass

    @command_operator
    def createLoanOffer(self,
                        currency,
                        amount,
                        duration,
                        auto_renew,
                        lending_rate):
        """
        Creates a loan offer for a given currency.
        Required POST parameters are "currency", "amount", "duration", "autoRenew" (0 or 1), and "lendingRate".
        """
        pass

    @command_operator
    def cancelLoanOffer(self, order_number):
        """
        Cancels a loan offer specified by the "orderNumber" POST parameter.
        """
        pass

    @command_operator
    def returnOpenLoanOffers(self):
        """
        Returns your open loan offers for each currency
        """
        pass

    @command_operator
    def returnActiveLoans(self):
        """
        Returns your active loans for each currency
        """
        pass

    @command_operator
    def returnLendingHistory(self,
                             start=datetime.now() - timedelta(days=1),
                             end=datetime.now(),
                             limit=0):
        """
        Returns your lending history within a time range specified by the "start" and "end" POST parameters as UNIX timestamps.
        TODO: "limit" may also be specified to limit the number of rows returned.
        """
        pass

    @command_operator
    def toggleAutoRenew(self, order_number):
        """
        Toggles the autoRenew setting on an active loan, specified by the "orderNumber" POST parameter.
        If successful, "message" will indicate the new autoRenew setting.
        """
        pass