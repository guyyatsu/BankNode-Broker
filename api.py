"""
"""
#!/bin/python3
import requests
import alpaca_trade_api as AlpacaTradeAPI
from alpaca_trade_api.rest import REST, TimeFrame


class DataHeist():
  def __init__(
                self
                       ):
    self.api = REST()

  def GetIRM(self):
    print(self.api.get_bars("IRM", TimeFrame.Minute, "2022-09-15", "2022-09-15", adjustment='raw'))


class Alpaca:
  def __init__(
                self,
                key,
                secret,
                # The SDK uses the live API by default...
                url="https://paper-api.alpaca.markets"
                                                       ):

    self.Connection = AlpacaTradeAPI.REST(key, secret, url)


  def Get_Account():
    return self.Connection\
               .get_account()


  def Get_Order_By_Client_ID(
                              self,
                              client_order_id
                                              ):

    return self.Connection\
               .get_order_by_client_order_id(client_order_id)


  def List_Orders(
                   self,
                   status=None,
                   limit=None,
                   after=None,
                   until=None,
                   direction=None,
                   params=None,
                   nested=None,
                   symbols=None,
                   side=None
                                  ):

    return self.Connection\
               .list_orders(
                             status=status,
                             limit=limit,
                             after=after,
                             until=until,
                             direction=direction,
                             params=params,
                             nested=nested,
                             symbols=symbols,
                             side=side
                                            )


  def Submit_Order( 
                    self,
                    symbol,
                    qty=None,
                    side="buy",
                    type="market",
                    time_in_force="day",
                    limit_price=None,
                    stop_price=None,
                    client_order_id=None,
                    order_class=None,
                    take_profit=None,
                    stop_loss=None,
                    trail_price=None,
                    trail_percent=None,
                    notional=None
                                         ):

    return self.Connection\
               .submit_order( 
                              symbol=symbol,
                              qty=qty,
                              side=side,
                              type=type,
                              time_in_force=time_in_force,
                              limit_price=limit_price,
                              stop_price=stop_price,
                              client_order_id=client_order_id,
                              order_class=order_class,
                              take_profit=take_profit,
                              stop_loss=stop_loss,
                              trail_price=trail_price,
                              trail_percent=trail_percent,
                              notional=notional
                                                   )


  def Get_Order(
                 self,
                 order_id
                          ):
    return self.Connection\
               .get_order(order_id=order_id)


  def Cancel_Order(
                    self,
                    order_id
                             ):
    return self.Connection\
               .cancel_order(order_id=order_id)


  def Cancel_All_Orders(self):
    return self.Connection\
               .cancel_all_orders()


  def List_Positions(self):
    return self.Connection\
               .list_positions()


  def Get_Position(
                    self,
                    symbol
                           ):
    return self.Connection\
               .get_position(symbol=symbol)


  def List_Assets(
                   self,
                   status=None,
                   asset_class=None
                                    ):
    return self.Connection\
               .list_assets(
                             status=status,
                             asset_class=asset_class
                                         )


  def Get_Assets(
                  self,
                  symbol
                         ):
    return self.Connection\
               .get_assets(symbol=symbol)


  def Get_Clock(self):
    return self.Connection\
               .get_clock()


  def Get_Calendar(
                    self,
                    start=None,
                    end=None
                                ):
    return self.Connection\
               .get_calendar(
                              start=start,
                              end=end
                                           )


  def Get_Portfolio_History(
                             date_start=None,
                             date_end=None,
                             period=None,
                             timeframe=None,
                             extended_hours=None
                                                 ):
    return self.Connection\
               .get_portfolio_history(
                                       date_start=date_start,
                                       date_end=date_end,
                                       period=period,
                                       timeframe=timeframe,
                                       extended_hours=extended_hours
                                                                     )
