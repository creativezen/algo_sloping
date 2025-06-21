class Endpoints:

    def request(self, *_, **__):
        pass

    def get_broker_earnings(self, biz_type=None, start_time=None, end_time=None, limit=None,
                            cursor=None):
        return self.request(False, "/v5/broker/earning-record", True, bizType=biz_type,
                            startTime=start_time, endTime=end_time, limit=limit, cursor=cursor)

    def enable_ut_for_sub_uid(self, sub_member_ids):
        return self.request(True, "/v5/asset/transfer/save-transfer-sub-member", True,
                            subMemberIds=sub_member_ids)

    def get_account_info(self):
        return self.request(False, "/v5/account/info", True)

    def batch_set_collateral_coin(self, request):
        return self.request(True, "/v5/account/set-collateral-switch-batch", True,
                            request=request)

    def get_borrow_history(self, currency=None, start_time=None, end_time=None, limit=None,
                           cursor=None):
        return self.request(False, "/v5/account/borrow-history", True, currency=currency,
                            startTime=start_time, endTime=end_time, limit=limit, cursor=cursor)

    def get_coin_greeks(self, base_coin=None):
        return self.request(False, "/v5/asset/coin-greeks", True, baseCoin=base_coin)

    def get_collateral_info(self, currency=None):
        return self.request(False, "/v5/account/collateral-info", True, currency=currency)

    def get_contract_transaction_log(self, currency=None, base_coin=None, type=None,
                                     start_time=None, end_time=None, limit=None, cursor=None):
        return self.request(False, "/v5/account/contract-transaction-log", True,
                            currency=currency, baseCoin=base_coin, type=type,
                            startTime=start_time, endTime=end_time, limit=limit, cursor=cursor)

    def get_fee_rate(self, category=None, symbol=None, base_coin=None):
        return self.request(False, "/v5/account/fee-rate", True, category=category, symbol=symbol,
                            baseCoin=base_coin)

    def get_mmp_state(self, base_coin):
        return self.request(False, "/v5/account/mmp-state", True, baseCoin=base_coin)

    def repay_liability(self, coin=None):
        return self.request(True, "/v5/account/quick-repayment", True, coin=coin)

    def reset_mmp(self, base_coin):
        return self.request(True, "/v5/account/mmp-reset", True, baseCoin=base_coin)

    def set_collateral_coin(self, coin, collateral_switch):
        return self.request(True, "/v5/account/set-collateral-switch", True, coin=coin,
                            collateralSwitch=collateral_switch)

    def set_margin_mode(self, set_margin_mode):
        return self.request(True, "/v5/account/set-margin-mode", True,
                            setMarginMode=set_margin_mode)

    def set_mmp(self, base_coin, window, frozen_period, qty_limit, delta_limit):
        return self.request(True, "/v5/account/mmp-modify", True, baseCoin=base_coin,
                            window=window, frozenPeriod=frozen_period, qtyLimit=qty_limit,
                            deltaLimit=delta_limit)

    def get_transaction_log(self, category=None, account_type=None, currency=None, base_coin=None,
                            type=None, start_time=None, end_time=None, limit=None, cursor=None):
        return self.request(False, "/v5/account/transaction-log", True, category=category,
                            accountType=account_type, currency=currency, baseCoin=base_coin,
                            type=type, startTime=start_time, endTime=end_time, limit=limit,
                            cursor=cursor)

    def get_transferable_amount(self, coin_name=None):
        return self.request(False, "/v5/account/withdrawal", True, coinName=coin_name)

    def upgrade_to_unified_account(self):
        return self.request(True, "/v5/account/upgrade-to-uta", True)

    def get_wallet_balance(self, account_type, coin=None):
        return self.request(False, "/v5/account/wallet-balance", True, accountType=account_type,
                            coin=coin)

    def get_affiliate_user_info(self, uid):
        return self.request(False, "/v5/user/aff-customer-info", True, uid=uid)

    def get_single_coin_balance(self, account_type, coin, member_id=None, to_member_id=None,
                                to_account_type=None, with_bonus=None,
                                with_transfer_safe_amount=None,
                                with_ltv_transfer_safe_amount=None):
        return self.request(False, "/v5/asset/transfer/query-account-coin-balance", True,
                            accountType=account_type, coin=coin, memberId=member_id,
                            toMemberId=to_member_id, toAccountType=to_account_type,
                            withBonus=with_bonus,
                            withTransferSafeAmount=with_transfer_safe_amount,
                            withLtvTransferSafeAmount=with_ltv_transfer_safe_amount)

    def get_all_coins_balance(self, account_type, member_id=None, coin=None, with_bonus=None):
        return self.request(False, "/v5/asset/transfer/query-account-coins-balance", True,
                            accountType=account_type, memberId=member_id, coin=coin,
                            withBonus=with_bonus)

    def get_spot_asset_info(self, account_type, coin=None):
        return self.request(False, "/v5/asset/transfer/query-asset-info", True,
                            accountType=account_type, coin=coin)

    def get_withdrawable_amount(self, coin):
        return self.request(False, "/v5/asset/withdraw/withdrawable-amount", True, coin=coin)

    def get_coin_info(self, coin=None):
        return self.request(False, "/v5/asset/coin/query-info", True, coin=coin)

    def get_option_delivery_record(self, category=None, symbol=None, start_time=None,
                                   end_time=None, exp_date=None, limit=None, cursor=None):
        return self.request(False, "/v5/asset/delivery-record", True, category=category,
                            symbol=symbol, startTime=start_time, endTime=end_time,
                            expDate=exp_date, limit=limit, cursor=cursor)

    def get_allowed_deposit_coin_info(self, coin=None, chain=None, limit=None, cursor=None):
        return self.request(False, "/v5/asset/deposit/query-allowed-list", True, coin=coin,
                            chain=chain, limit=limit, cursor=cursor)

    def get_deposit_records(self, coin=None, start_time=None, end_time=None, limit=None,
                            cursor=None):
        return self.request(False, "/v5/asset/deposit/query-record", True, coin=coin,
                            startTime=start_time, endTime=end_time, limit=limit, cursor=cursor)

    def get_internal_deposit_records(self, tx_i_d=None, start_time=None, end_time=None, coin=None,
                                     cursor=None, limit=None):
        return self.request(False, "/v5/asset/deposit/query-internal-record", True, txID=tx_i_d,
                            startTime=start_time, endTime=end_time, coin=coin, cursor=cursor,
                            limit=limit)

    def get_master_deposit_address(self, coin, chain_type=None):
        return self.request(False, "/v5/asset/deposit/query-address", True, coin=coin,
                            chainType=chain_type)

    def set_deposit_account(self, account_type):
        return self.request(True, "/v5/asset/deposit/deposit-to-account", True,
                            accountType=account_type)

    def get_sub_deposit_address(self, coin, chain_type, sub_member_id):
        return self.request(False, "/v5/asset/deposit/query-sub-member-address", True, coin=coin,
                            chainType=chain_type, subMemberId=sub_member_id)

    def get_coin_exchange_records(self, from_coin=None, to_coin=None, limit=None, cursor=None):
        return self.request(False, "/v5/asset/exchange/order-record", True, fromCoin=from_coin,
                            toCoin=to_coin, limit=limit, cursor=cursor)

    def get_usdc_contract_settlement(self, category=None, symbol=None, start_time=None,
                                     end_time=None, limit=None, cursor=None):
        return self.request(False, "/v5/asset/settlement-record", True, category=category,
                            symbol=symbol, startTime=start_time, endTime=end_time, limit=limit,
                            cursor=cursor)

    def get_sub_uid(self):
        return self.request(False, "/v5/asset/transfer/query-sub-member-list", True)

    def create_internal_transfer(self, transfer_id, coin, amount, from_account_type,
                                 to_account_type):
        return self.request(True, "/v5/asset/transfer/inter-transfer", True,
                            transferId=transfer_id, coin=coin, amount=amount,
                            fromAccountType=from_account_type, toAccountType=to_account_type)

    def get_transferable_coin(self, from_account_type, to_account_type):
        return self.request(False, "/v5/asset/transfer/query-transfer-coin-list", True,
                            fromAccountType=from_account_type, toAccountType=to_account_type)

    def create_universal_transfer(self, transfer_id, coin, amount, from_member_id, to_member_id,
                                  from_account_type, to_account_type):
        return self.request(True, "/v5/asset/transfer/universal-transfer", True,
                            transferId=transfer_id, coin=coin, amount=amount,
                            fromMemberId=from_member_id, toMemberId=to_member_id,
                            fromAccountType=from_account_type, toAccountType=to_account_type)

    def cancel_withdrawal(self, id):
        return self.request(True, "/v5/asset/withdraw/cancel", True, id=id)

    def get_withdrawal_records(self, withdraw_i_d=None, tx_i_d=None, coin=None,
                               withdraw_type=None, start_time=None, end_time=None, limit=None,
                               cursor=None):
        return self.request(False, "/v5/asset/withdraw/query-record", True,
                            withdrawID=withdraw_i_d, txID=tx_i_d, coin=coin,
                            withdrawType=withdraw_type, startTime=start_time, endTime=end_time,
                            limit=limit, cursor=cursor)

    def withdraw(self, coin, address, amount, timestamp, chain=None, tag=None, force_chain=None,
                 account_type=None, fee_type=None, request_id=None, beneficiary=None):
        return self.request(True, "/v5/asset/withdraw/create", True, coin=coin, address=address,
                            amount=amount, timestamp=timestamp, chain=chain, tag=tag,
                            forceChain=force_chain, accountType=account_type, feeType=fee_type,
                            requestId=request_id, beneficiary=beneficiary)

    def get_exchange_broker_earnings(self, biz_type=None, begin=None, end=None, uid=None,
                                     limit=None, cursor=None):
        return self.request(False, "/v5/broker/earnings-info", True, bizType=biz_type,
                            begin=begin, end=end, uid=uid, limit=limit, cursor=cursor)

    def get_leveraged_token_info(self, lt_coin=None):
        return self.request(False, "/v5/spot-lever-token/info", False, ltCoin=lt_coin)

    def get_leveraged_token_market(self, lt_coin):
        return self.request(False, "/v5/spot-lever-token/reference", False, ltCoin=lt_coin)

    def get_purchase_redemption_records(self, lt_coin=None, order_id=None, start_time=None,
                                        end_time=None, limit=None, lt_order_type=None,
                                        serial_no=None):
        return self.request(False, "/v5/spot-lever-token/order-record", True, ltCoin=lt_coin,
                            orderId=order_id, startTime=start_time, endTime=end_time, limit=limit,
                            ltOrderType=lt_order_type, serialNo=serial_no)

    def purchase(self, lt_coin, lt_amount, serial_no=None):
        return self.request(True, "/v5/spot-lever-token/purchase", True, ltCoin=lt_coin,
                            ltAmount=lt_amount, serialNo=serial_no)

    def redeem(self, lt_coin, quantity, serial_no=None):
        return self.request(True, "/v5/spot-lever-token/redeem", True, ltCoin=lt_coin,
                            quantity=quantity, serialNo=serial_no)

    def get_option_delivery_price(self, category=None, symbol=None, base_coin=None, limit=None,
                                  cursor=None):
        return self.request(False, "/v5/market/delivery-price", False, category=category,
                            symbol=symbol, baseCoin=base_coin, limit=limit, cursor=cursor)

    def get_funding_rate_history(self, symbol, category=None, start_time=None, end_time=None,
                                 limit=None):
        return self.request(False, "/v5/market/funding/history", False, symbol=symbol,
                            category=category, startTime=start_time, endTime=end_time,
                            limit=limit)

    def get_index_price_kline(self, symbol, interval, category=None, start=None, end=None,
                              limit=None):
        return self.request(False, "/v5/market/index-price-kline", False, symbol=symbol,
                            interval=interval, category=category, start=start, end=end,
                            limit=limit)

    def get_instruments_info(self, category=None, symbol=None, status=None, base_coin=None,
                             limit=None, cursor=None):
        return self.request(False, "/v5/market/instruments-info", False, category=category,
                            symbol=symbol, status=status, baseCoin=base_coin, limit=limit,
                            cursor=cursor)

    def get_insurance(self, coin=None):
        return self.request(False, "/v5/market/insurance", False, coin=coin)

    def get_historical_volatility(self, category=None, base_coin=None, quote_coin=None,
                                  period=None, start_time=None, end_time=None):
        return self.request(False, "/v5/market/historical-volatility", False, category=category,
                            baseCoin=base_coin, quoteCoin=quote_coin, period=period,
                            startTime=start_time, endTime=end_time)

    def get_kline(self, symbol, interval, category=None, start=None, end=None, limit=None):
        return self.request(False, "/v5/market/kline", False, symbol=symbol, interval=interval,
                            category=category, start=start, end=end, limit=limit)

    def get_long_short_ratio(self, symbol, period, category=None, start_time=None, end_time=None,
                             limit=None, cursor=None):
        return self.request(False, "/v5/market/account-ratio", False, symbol=symbol,
                            period=period, category=category, startTime=start_time,
                            endTime=end_time, limit=limit, cursor=cursor)

    def get_mark_price_kline(self, symbol, interval, category=None, start=None, end=None,
                             limit=None):
        return self.request(False, "/v5/market/mark-price-kline", False, symbol=symbol,
                            interval=interval, category=category, start=start, end=end,
                            limit=limit)

    def get_open_interest(self, symbol, interval_time, category=None, start_time=None,
                          end_time=None, limit=None, cursor=None):
        return self.request(False, "/v5/market/open-interest", False, symbol=symbol,
                            intervalTime=interval_time, category=category, startTime=start_time,
                            endTime=end_time, limit=limit, cursor=cursor)

    def get_orderbook(self, symbol, category=None, limit=None):
        return self.request(False, "/v5/market/orderbook", False, symbol=symbol,
                            category=category, limit=limit)

    def get_premium_index_price_kline(self, symbol, interval, category=None, start=None, end=None,
                                      limit=None):
        return self.request(False, "/v5/market/premium-index-price-kline", False, symbol=symbol,
                            interval=interval, category=category, start=start, end=end,
                            limit=limit)

    def get_public_trading_history(self, category=None, symbol=None, base_coin=None,
                                   option_type=None, limit=None):
        return self.request(False, "/v5/market/recent-trade", False, category=category,
                            symbol=symbol, baseCoin=base_coin, optionType=option_type,
                            limit=limit)

    def get_risk_limit(self, category=None, symbol=None, cursor=None):
        return self.request(False, "/v5/market/risk-limit", False, category=category,
                            symbol=symbol, cursor=cursor)

    def get_tickers(self, category=None, symbol=None, base_coin=None, exp_date=None):
        return self.request(False, "/v5/market/tickers", False, category=category, symbol=symbol,
                            baseCoin=base_coin, expDate=exp_date)

    def get_server_time(self):
        return self.request(False, "/v5/market/time", False)

    def amend_order(self, symbol, category=None, order_id=None, order_link_id=None, order_iv=None,
                    trigger_price=None, qty=None, price=None, tpsl_mode=None, take_profit=None,
                    stop_loss=None, tp_trigger_by=None, sl_trigger_by=None, trigger_by=None,
                    tp_limit_price=None, sl_limit_price=None):
        return self.request(True, "/v5/order/amend", True, symbol=symbol, category=category,
                            orderId=order_id, orderLinkId=order_link_id, orderIv=order_iv,
                            triggerPrice=trigger_price, qty=qty, price=price, tpslMode=tpsl_mode,
                            takeProfit=take_profit, stopLoss=stop_loss, tpTriggerBy=tp_trigger_by,
                            slTriggerBy=sl_trigger_by, triggerBy=trigger_by,
                            tpLimitPrice=tp_limit_price, slLimitPrice=sl_limit_price)

    def batch_amend_order(self, request, category=None):
        return self.request(True, "/v5/order/amend-batch", True, request=request,
                            category=category)

    def batch_cancel_order(self, request, category=None):
        return self.request(True, "/v5/order/cancel-batch", True, request=request,
                            category=category)

    def batch_place_order(self, request, category=None):
        return self.request(True, "/v5/order/create-batch", True, request=request,
                            category=category)

    def cancel_all_orders(self, category=None, symbol=None, base_coin=None, settle_coin=None,
                          order_filter=None, stop_order_type=None):
        return self.request(True, "/v5/order/cancel-all", True, category=category, symbol=symbol,
                            baseCoin=base_coin, settleCoin=settle_coin, orderFilter=order_filter,
                            stopOrderType=stop_order_type)

    def cancel_order(self, symbol, category=None, order_id=None, order_link_id=None,
                     order_filter=None):
        return self.request(True, "/v5/order/cancel", True, symbol=symbol, category=category,
                            orderId=order_id, orderLinkId=order_link_id, orderFilter=order_filter)

    def place_order(self, symbol, side, order_type, qty, category=None, is_leverage=None,
                    market_unit=None, slippage_tolerance_type=None, slippage_tolerance=None,
                    price=None, trigger_direction=None, order_filter=None, trigger_price=None,
                    trigger_by=None, order_iv=None, time_in_force=None, position_idx=None,
                    order_link_id=None, take_profit=None, stop_loss=None, tp_trigger_by=None,
                    sl_trigger_by=None, reduce_only=None, close_on_trigger=None, smp_type=None,
                    mmp=None, tpsl_mode=None, tp_limit_price=None, sl_limit_price=None,
                    tp_order_type=None, sl_order_type=None):
        return self.request(True, "/v5/order/create", True, symbol=symbol, side=side,
                            orderType=order_type, qty=qty, category=category,
                            isLeverage=is_leverage, marketUnit=market_unit,
                            slippageToleranceType=slippage_tolerance_type,
                            slippageTolerance=slippage_tolerance, price=price,
                            triggerDirection=trigger_direction, orderFilter=order_filter,
                            triggerPrice=trigger_price, triggerBy=trigger_by, orderIv=order_iv,
                            timeInForce=time_in_force, positionIdx=position_idx,
                            orderLinkId=order_link_id, takeProfit=take_profit, stopLoss=stop_loss,
                            tpTriggerBy=tp_trigger_by, slTriggerBy=sl_trigger_by,
                            reduceOnly=reduce_only, closeOnTrigger=close_on_trigger,
                            smpType=smp_type, mmp=mmp, tpslMode=tpsl_mode,
                            tpLimitPrice=tp_limit_price, slLimitPrice=sl_limit_price,
                            tpOrderType=tp_order_type, slOrderType=sl_order_type)

    def set_dcp(self, time_window, product=None):
        return self.request(True, "/v5/order/disconnected-cancel-all", True,
                            timeWindow=time_window, product=product)

    def get_executions(self, category=None, symbol=None, order_id=None, order_link_id=None,
                       base_coin=None, start_time=None, end_time=None, exec_type=None, limit=None,
                       cursor=None):
        return self.request(False, "/v5/execution/list", True, category=category, symbol=symbol,
                            orderId=order_id, orderLinkId=order_link_id, baseCoin=base_coin,
                            startTime=start_time, endTime=end_time, execType=exec_type,
                            limit=limit, cursor=cursor)

    def get_open_orders(self, category=None, symbol=None, base_coin=None, settle_coin=None,
                        order_id=None, order_link_id=None, open_only=None, order_filter=None,
                        limit=None, cursor=None):
        return self.request(False, "/v5/order/realtime", True, category=category, symbol=symbol,
                            baseCoin=base_coin, settleCoin=settle_coin, orderId=order_id,
                            orderLinkId=order_link_id, openOnly=open_only,
                            orderFilter=order_filter, limit=limit, cursor=cursor)

    def get_order_history(self, category=None, symbol=None, base_coin=None, settle_coin=None,
                          order_id=None, order_link_id=None, order_filter=None, order_status=None,
                          start_time=None, end_time=None, limit=None, cursor=None):
        return self.request(False, "/v5/order/history", True, category=category, symbol=symbol,
                            baseCoin=base_coin, settleCoin=settle_coin, orderId=order_id,
                            orderLinkId=order_link_id, orderFilter=order_filter,
                            orderStatus=order_status, startTime=start_time, endTime=end_time,
                            limit=limit, cursor=cursor)

    def get_borrow_quota(self, symbol, side, category=None):
        return self.request(False, "/v5/order/spot-borrow-check", True, symbol=symbol, side=side,
                            category=category)

    def bind_or_unbind_uid(self, uid, operate):
        return self.request(True, "/v5/ins-loan/association-uid", True, uid=uid, operate=operate)

    def get_loan_orders(self, order_id=None, start_time=None, end_time=None, limit=None):
        return self.request(False, "/v5/ins-loan/loan-order", True, orderId=order_id,
                            startTime=start_time, endTime=end_time, limit=limit)

    def get_ltv(self):
        return self.request(False, "/v5/ins-loan/ltv-convert", True)

    def get_margin_coin_info(self, product_id=None):
        return self.request(False, "/v5/ins-loan/ensure-tokens-convert", False,
                            productId=product_id)

    def get_product_info(self, product_id=None):
        return self.request(False, "/v5/ins-loan/product-infos", False, productId=product_id)

    def get_repayment_orders(self, start_time=None, end_time=None, limit=None):
        return self.request(False, "/v5/ins-loan/repaid-history", True, startTime=start_time,
                            endTime=end_time, limit=limit)

    def set_auto_add_margin(self, symbol, auto_add_margin, category=None, position_idx=None):
        return self.request(True, "/v5/position/set-auto-add-margin", True, symbol=symbol,
                            autoAddMargin=auto_add_margin, category=category,
                            positionIdx=position_idx)

    def get_closed_pnl(self, category=None, symbol=None, start_time=None, end_time=None,
                       limit=None, cursor=None):
        return self.request(False, "/v5/position/closed-pnl", True, category=category,
                            symbol=symbol, startTime=start_time, endTime=end_time, limit=limit,
                            cursor=cursor)

    def switch_margin_mode(self, symbol, trade_mode, buy_leverage, sell_leverage, category=None):
        return self.request(True, "/v5/position/switch-isolated", True, symbol=symbol,
                            tradeMode=trade_mode, buyLeverage=buy_leverage,
                            sellLeverage=sell_leverage, category=category)

    def set_leverage(self, symbol, buy_leverage, sell_leverage, category=None):
        return self.request(True, "/v5/position/set-leverage", True, symbol=symbol,
                            buyLeverage=buy_leverage, sellLeverage=sell_leverage,
                            category=category)

    def add_margin(self, symbol, margin, category=None, position_idx=None):
        return self.request(True, "/v5/position/add-margin", True, symbol=symbol, margin=margin,
                            category=category, positionIdx=position_idx)

    def switch_position_mode(self, mode, category=None, symbol=None, coin=None):
        return self.request(True, "/v5/position/switch-mode", True, mode=mode, category=category,
                            symbol=symbol, coin=coin)

    def get_positions(self, category=None, symbol=None, base_coin=None, settle_coin=None,
                      limit=None, cursor=None):
        return self.request(False, "/v5/position/list", True, category=category, symbol=symbol,
                            baseCoin=base_coin, settleCoin=settle_coin, limit=limit,
                            cursor=cursor)

    def set_risk_limit(self, symbol, risk_id, category=None, position_idx=None):
        return self.request(True, "/v5/position/set-risk-limit", True, symbol=symbol,
                            riskId=risk_id, category=category, positionIdx=position_idx)

    def set_tp_sl_mode(self, symbol, tp_sl_mode, category=None):
        return self.request(True, "/v5/position/set-tpsl-mode", True, symbol=symbol,
                            tpSlMode=tp_sl_mode, category=category)

    def set_trading_stop(self, symbol, tpsl_mode, position_idx, category=None, take_profit=None,
                         stop_loss=None, trailing_stop=None, tp_trigger_by=None,
                         sl_trigger_by=None, active_price=None, tp_size=None, sl_size=None,
                         tp_limit_price=None, sl_limit_price=None, tp_order_type=None,
                         sl_order_type=None):
        return self.request(True, "/v5/position/trading-stop", True, symbol=symbol,
                            tpslMode=tpsl_mode, positionIdx=position_idx, category=category,
                            takeProfit=take_profit, stopLoss=stop_loss,
                            trailingStop=trailing_stop, tpTriggerBy=tp_trigger_by,
                            slTriggerBy=sl_trigger_by, activePrice=active_price, tpSize=tp_size,
                            slSize=sl_size, tpLimitPrice=tp_limit_price,
                            slLimitPrice=sl_limit_price, tpOrderType=tp_order_type,
                            slOrderType=sl_order_type)

    def get_pre_upgrade_closed_pnl(self, symbol, category=None, start_time=None, end_time=None,
                                   limit=None, cursor=None):
        return self.request(False, "/v5/pre-upgrade/position/closed-pnl", True, symbol=symbol,
                            category=category, startTime=start_time, endTime=end_time,
                            limit=limit, cursor=cursor)

    def get_pre_upgrade_option_delivery_record(self, category=None, symbol=None, exp_date=None,
                                               limit=None, cursor=None):
        return self.request(False, "/v5/pre-upgrade/asset/delivery-record", True,
                            category=category, symbol=symbol, expDate=exp_date, limit=limit,
                            cursor=cursor)

    def get_pre_upgrade_trade_history(self, category=None, symbol=None, order_id=None,
                                      order_link_id=None, base_coin=None, start_time=None,
                                      end_time=None, exec_type=None, limit=None, cursor=None):
        return self.request(False, "/v5/pre-upgrade/execution/list", True, category=category,
                            symbol=symbol, orderId=order_id, orderLinkId=order_link_id,
                            baseCoin=base_coin, startTime=start_time, endTime=end_time,
                            execType=exec_type, limit=limit, cursor=cursor)

    def get_pre_upgrade_order_history(self, category=None, symbol=None, base_coin=None,
                                      order_id=None, order_link_id=None, order_filter=None,
                                      order_status=None, start_time=None, end_time=None,
                                      limit=None, cursor=None):
        return self.request(False, "/v5/pre-upgrade/order/history", True, category=category,
                            symbol=symbol, baseCoin=base_coin, orderId=order_id,
                            orderLinkId=order_link_id, orderFilter=order_filter,
                            orderStatus=order_status, startTime=start_time, endTime=end_time,
                            limit=limit, cursor=cursor)

    def get_pre_upgrade_usdc_session_settlement(self, category=None, symbol=None, limit=None,
                                                cursor=None):
        return self.request(False, "/v5/pre-upgrade/asset/settlement-record", True,
                            category=category, symbol=symbol, limit=limit, cursor=cursor)

    def get_pre_upgrade_transaction_log(self, category=None, base_coin=None, type=None,
                                        start_time=None, end_time=None, limit=None, cursor=None):
        return self.request(False, "/v5/pre-upgrade/account/transaction-log", True,
                            category=category, baseCoin=base_coin, type=type,
                            startTime=start_time, endTime=end_time, limit=limit, cursor=cursor)

    def normal_get_loan_account_info(self):
        return self.request(False, "/v5/spot-cross-margin-trade/account", True)

    def normal_get_borrow_order_detail(self, start_time=None, end_time=None, coin=None,
                                       status=None, limit=None):
        return self.request(False, "/v5/spot-cross-margin-trade/orders", True,
                            startTime=start_time, endTime=end_time, coin=coin, status=status,
                            limit=limit)

    def normal_borrow(self, coin, qty):
        return self.request(True, "/v5/spot-cross-margin-trade/loan", True, coin=coin, qty=qty)

    def normal_get_borrowable_coin_info(self, coin=None):
        return self.request(False, "/v5/spot-cross-margin-trade/borrow-token", False, coin=coin)

    def normal_get_interest_quota(self, coin):
        return self.request(False, "/v5/spot-cross-margin-trade/loan-info", True, coin=coin)

    def normal_get_margin_coin_info(self, coin=None):
        return self.request(False, "/v5/spot-cross-margin-trade/pledge-token", False, coin=coin)

    def normal_get_repayment_order_detail(self, start_time=None, end_time=None, coin=None,
                                          limit=None):
        return self.request(False, "/v5/spot-cross-margin-trade/repay-history", True,
                            startTime=start_time, endTime=end_time, coin=coin, limit=limit)

    def normal_repay(self, coin, qty=None, complete_repayment=None):
        return self.request(True, "/v5/spot-cross-margin-trade/repay", True, coin=coin, qty=qty,
                            completeRepayment=complete_repayment)

    def normal_toggle_margin_trade(self, switch):
        return self.request(True, "/v5/spot-cross-margin-trade/switch", True, switch=switch)

    def normal_get_vip_margin_data(self, vip_level=None, currency=None):
        return self.request(False, "/v5/spot-cross-margin-trade/data", False, vipLevel=vip_level,
                            currency=currency)

    def historical_interest(self, currency, vip_level=None, start_time=None, end_time=None):
        return self.request(False, "/v5/spot-margin-trade/interest-rate-history", True,
                            currency=currency, vipLevel=vip_level, startTime=start_time,
                            endTime=end_time)

    def set_leverage_spot(self, leverage):
        return self.request(True, "/v5/spot-margin-trade/set-leverage", True, leverage=leverage)

    def status_and_leverage(self):
        return self.request(False, "/v5/spot-margin-trade/state", True)

    def toggle_margin_trade(self, spot_margin_mode):
        return self.request(True, "/v5/spot-margin-trade/switch-mode", True,
                            spotMarginMode=spot_margin_mode)

    def vip_margin_data(self, vip_level=None, currency=None):
        return self.request(False, "/v5/spot-margin-trade/data", False, vipLevel=vip_level,
                            currency=currency)

    def get_api_key_information(self):
        return self.request(False, "/v5/user/query-api", True)

    def create_sub_api_key(self, subuid, read_only, permissions, note=None, ips=None):
        return self.request(True, "/v5/user/create-sub-api", True, subuid=subuid,
                            readOnly=read_only, permissions=permissions, note=note, ips=ips)

    def create_sub_uid(self, username, member_type, password=None, switch=None, is_uta=None,
                       note=None):
        return self.request(True, "/v5/user/create-sub-member", True, username=username,
                            memberType=member_type, password=password, switch=switch,
                            isUta=is_uta, note=note)

    def freeze_sub_uid(self, subuid, frozen):
        return self.request(True, "/v5/user/frozen-sub-member", True, subuid=subuid,
                            frozen=frozen)

    def get_all_sub_api_keys(self, sub_member_id, limit=None, cursor=None):
        return self.request(False, "/v5/user/sub-apikeys", True, subMemberId=sub_member_id,
                            limit=limit, cursor=cursor)

    def modify_master_api_key(self, read_only=None, ips=None, permissions=None):
        return self.request(True, "/v5/user/update-api", True, readOnly=read_only, ips=ips,
                            permissions=permissions)

    def modify_sub_api_key(self, apikey=None, read_only=None, ips=None, permissions=None):
        return self.request(True, "/v5/user/update-sub-api", True, apikey=apikey,
                            readOnly=read_only, ips=ips, permissions=permissions)

    def delete_master_api_key(self):
        return self.request(True, "/v5/user/delete-api", True)

    def delete_sub_api_key(self, apikey=None):
        return self.request(True, "/v5/user/delete-sub-api", True, apikey=apikey)

    def delete_sub_uid(self, sub_member_id):
        return self.request(True, "/v5/user/del-submember", True, subMemberId=sub_member_id)

    def get_sub_uid_list(self):
        return self.request(False, "/v5/user/query-sub-members", True)

    def get_uid_wallet_type(self, member_ids=None):
        return self.request(False, "/v5/user/get-member-type", True, memberIds=member_ids)
