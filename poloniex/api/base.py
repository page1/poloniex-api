import hashlib
import hmac
import time
import urllib
from inspect import signature, iscoroutinefunction

from poloniex import constants
from poloniex.error import PoloniexError, AddressAlreadyExist
from poloniex.logger import getLogger
from poloniex.utils import switch

__author__ = "andrew.shvv@gmail.com"

logger = getLogger(__name__)


def apply_defaults(func, *args, **kwargs):
    kwargs = signature(func).bind_partial(*args, **kwargs)
    kwargs.apply_defaults()
    return dict(kwargs.arguments)


def command_operator(func):
    if iscoroutinefunction(func):
        async def async_decorator(self, *args, **kwargs):
            kwargs = apply_defaults(func, *args, **kwargs)
            method, params = self.get_params(func.__name__, **kwargs)

            if method == "post":
                response = await self.api_call(data=params)
            elif method == "get":
                response = await self.api_call(params=params)
            else:
                raise PoloniexError("Not available method '{}'".format(method))

            return self.response_handler(response, command=func.__name__)

        return async_decorator
    else:
        def decorator(self, *args, **kwargs):
            kwargs = apply_defaults(func, *args, **kwargs)
            method, params = self.get_params(func.__name__, **kwargs)

            if method == "post":
                response = self.api_call(data=params)
            elif method == "get":
                response = self.api_call(params=params)
            else:
                raise PoloniexError("Not available method '{}'".format(method))

            return self.response_handler(response, command=func.__name__)

        return decorator


class BasePublicApi:
    url = "https://poloniex.com/public?"

    def api_call(self, *args, **kwargs):
        raise NotImplementedError("'api_call' method should be implemented.")

    def get_params(self, command, **kwargs):
        currency_pair = kwargs.get("currency_pair")

        depth = kwargs.get("depth")

        start = kwargs.get("start")
        if start:
            start = start.timestamp()

        end = kwargs.get("end")
        if end:
            end = end.timestamp()

        period = kwargs.get("period")
        if period and period not in constants.CHART_DATA_PERIODS:
            raise PoloniexError("Period '{}' not available.".format(period))

        for case in switch(command):
            if case("returnTicker"):
                method = "get"
                params = {"command": command}
                break

            if case("return24hVolume"):
                method = "get"
                params = {"command": command}
                break

            if case("returnOrderBook"):
                method = "get"
                params = {
                    "command": command,
                    "currencyPair": currency_pair,
                    "depth": depth
                }
                break

            if case("returnChartData"):
                method = "get"
                params = {
                    "command": command,
                    "currencyPair": currency_pair,
                    "period": period,
                    "start": start,
                    "end": end
                }
                break

            if case("returnCurrencies"):
                method = "get"
                params = {"command": command}
                break

            if case("returnTradeHistory"):
                method = "get"
                params = {
                    "command": command,
                    "currencyPair": currency_pair,
                    "start": start,
                    "end": end
                }
                break

            if case():
                raise NotImplementedError("There is no command '{}'.".format(command))

        return method, params

    def response_handler(self, response, **kwargs):
        if ("error" in response) and (response["error"] is not None):
            raise PoloniexError(response["error"])

        return response


class BaseTradingApi:
    url = "https://poloniex.com/tradingApi?"

    def __init__(self, api_key, api_sec):
        if type(api_key) is not str:
            raise Exception("API_KEY must be string")

        if type(api_sec) is not str:
            raise Exception("SECRET_KEY must be string")

        self.api_key = api_key
        self.api_sec = api_sec.encode()

    @property
    def nonce(self):
        return int(time.time() * 1000)

    def secure_request(self, data, headers):
        data.update(nonce=self.nonce)

        e = urllib.parse.urlencode(data).encode()
        auth = {
            "Sign": hmac.new(self.api_sec, e, hashlib.sha512).hexdigest(),
            "Key": self.api_key
        }

        headers.update(**auth)
        return data, headers

    def get_params(self, command, **kwargs):
        currency_pair = kwargs.get("currency_pair")
        lending_rate = kwargs.get("lending_rate")

        currency = kwargs.get("currency")
        duration = kwargs.get("duration")
        auto_renew = kwargs.get("auto_renew")

        start = kwargs.get("start")
        if start:
            start = start.timestamp()

        end = kwargs.get("end")
        if end:
            end = end.timestamp()

        rate = kwargs.get("rate")
        amount = kwargs.get("amount")
        address = kwargs.get("address")
        order_number = kwargs.get("order_number")

        for case in switch(command):
            if case("returnBalances"):
                method = "post"
                params = {"command": command}
                break

            if case("returnCompleteBalances"):
                method = "post"
                params = {"command": command}
                break

            if case("returnDepositAddresses"):
                method = "post"
                params = {"command": command}
                break

            if case("generateNewAddress"):
                method = "post"
                params = {
                    "command": command,
                    "currency": currency
                }
                break

            if case("returnDepositsWithdrawals"):
                method = "post"
                params = {
                    "command": command,
                    "start": start,
                    "end": end
                }
                break

            if case("returnOpenOrders"):
                method = "post"
                params = {
                    "command": command,
                    "currencyPair": currency_pair
                }
                break

            if case("returnTradeHistory"):
                method = "post"
                params = {
                    "command": command,
                    "currencyPair": currency_pair,
                    "start": start,
                    "end": end
                }
                break

            if case("returnOrderTrades"):
                method = "post"
                params = {
                    "command": command,
                    "orderNumber": order_number
                }
                break

            if case("buy"):
                method = "post"
                params = {
                    "command": command,
                    "currencyPair": currency_pair,
                    "rate": rate,
                    "amount": amount
                }
                break

            if case("sell"):
                method = "post"
                params = {
                    "command": command,
                    "currencyPair": currency_pair,
                    "rate": rate,
                    "amount": amount
                }
                break

            if case("cancelOrder"):
                method = "post"
                params = {
                    "command": command,
                    "orderNumber": order_number
                }
                break

            if case("moveOrder"):
                method = "post"
                params = {
                    "command": command,
                    "currencyPair": currency_pair,
                    "rate": rate,
                    "amount": amount
                }
                break

            if case("withdraw"):
                method = "post"
                params = {
                    "command": command,
                    "currency": currency,
                    "amount": amount,
                    "address": address
                }
                break

            if case("returnFeeInfo"):
                method = "post"
                params = {
                    "command": command
                }
                break

            if case("returnAvailableAccountBalances"):
                method = "post"
                params = {
                    "command": command
                }
                break

            if case("returnTradableBalances"):
                method = "post"
                params = {
                    "command": command
                }
                break

            if case("returnMarginAccountSummary"):
                method = "post"
                params = {
                    "command": command
                }
                break

            if case("marginBuy"):
                method = "post"
                params = {
                    "command": command,
                    "currencyPair": currency_pair,
                    "rate": rate,
                    "amount": amount,
                    "lendingRate": lending_rate
                }
                break

            if case("marginSell"):
                method = "post"
                params = {
                    "command": command,
                    "currencyPair": currency_pair,
                    "rate": rate,
                    "amount": amount,
                    "lendingRate": lending_rate
                }
                break

            if case("getMarginPosition"):
                method = "post"
                params = {
                    "command": command,
                    "currencyPair": currency_pair
                }
                break

            if case("closeMarginPosition"):
                method = "post"
                params = {
                    "command": command,
                    "currencyPair": currency_pair
                }
                break

            if case("createLoanOffer"):
                method = "post"
                params = {
                    "command": command,
                    "currency": currency,
                        "amount": amount,
                        "duration": duration,
                        "autoRenew": auto_renew,
                        "lendingRate": lending_rate
                }
                break

            if case("cancelLoanOffer"):
                method = "post"
                params = {
                    "command": command,
                    "orderNumber": order_number
                }
                break

            if case("returnOpenLoanOffers"):
                method = "post"
                params = {
                    "command": command
                }
                break

            if case("returnActiveLoans"):
                method = "post"
                params = {
                    "command": command
                }
                break

            if case("returnLendingHistory"):
                method = "post"
                params = {
                    "command": command,
                    "start": start,
                    "end": end
                }
                break

            if case("toggleAutoRenew"):
                method = "post"
                params = {
                    "command": command,
                    "orderNumber": order_number
                }
                break

            if case():
                raise NotImplementedError("There is no command '{}'.".format(command))

        return method, params

    def response_handler(self, response, command, **kwargs):
        if ("error" in response) and (response["error"] is not None):
            raise PoloniexError(response["error"])

        for case in switch(command):
            if case("generateNewAddress"):
                if response["success"] == 0:
                    if "address" in response:
                        raise AddressAlreadyExist("Address [{}] already exist".format(response["address"]))
                    elif "response" in response:
                        raise PoloniexError(response["response"])

        return response
