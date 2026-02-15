#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import akshare as ak
import pandas as pd
from iniparser import IniParser
from quickcmd_color import QuickCmdColor
from fzf import FuzzyFinder
from datetime import datetime, timedelta
from stock_info import get_stock_info_cn_cached, \
    get_stock_info_hk_cached, \
    get_stock_info_us_cached, \
    get_stock_individual_info, \
    get_stock_quote

class FactorManager:
    def __init__(self, config_path, stock_code, stock_name, industry):
        self.config_path = config_path
        self.stock_code = stock_code
        self.stock_name = stock_name
        self.industry = industry
        self.parser = IniParser(self.config_path) if os.path.exists(self.config_path) else None
        self.qcc = QuickCmdColor()

    def _get_value(self, section, key):
        if not self.parser:
            return None
        # Use get_config which is the method in the provided iniparser.py
        config = self.parser.get_config(section, key)
        return config[1] if config else None

    def get_factor(self):
        # 1. Check company by code
        factor = self._get_value('company', self.stock_code)
        if factor:
            return float(factor)

        # 2. Check company by name
        factor = self._get_value('company', self.stock_name)
        if factor:
            return float(factor)

        # 3. Check industry
        factor = self._get_value('industry', self.industry)
        if factor:
            return float(factor)

        # 4. Check default
        factor = self._get_value('default', 'factor')
        if factor:
            return float(factor)

        # 5. Prompt user
        while True:
            try:
                factor_input = self.qcc.green_input(f"No factor found for {self.stock_name}. Please enter a factor (e.g., 0.85): ")
                return float(factor_input)
            except (ValueError, TypeError):
                self.qcc.red_print("Invalid input. Please enter a number.")

    def get_payout_ratio(self):
        # This logic needs to be adapted to how you want to store payout ratios in the ini.
        # For now, let's assume a simple lookup similar to factor.
        ratio = self._get_value('company', f"{self.stock_code}_payout_ratio") or \
                self._get_value('company', f"{self.stock_name}_payout_ratio") or \
                self._get_value('industry', f"{self.industry}_payout_ratio") or \
                self._get_value('default', 'payout_ratio')

        return float(ratio) if ratio else 0.5 # Default to 0.5 if not found


class StockAnalyzer:
    def __init__(self, stock_code, stock_name, stock_share):
        self.stock_code = stock_code
        self.stock_name = stock_name
        self.stock_share = stock_share
        self.qcc = QuickCmdColor()
        self.data = {}

    def _format_value(self, value):
        if isinstance(value, (int, float)):
            return f"{value / 100_000_000:.2f} 亿"
        return "N/A"

    def analyze(self):
        if self.stock_share not in ["A-Share", "HK-Stock"]:
            self.qcc.red_print(f"Unsupported stock share: {self.stock_share}")
            return None

        try:
            self.qcc.blue_print(f"Fetching data for {self.stock_name} ({self.stock_code}, {self.stock_share})...")

            # Fetch all necessary data
            self.data['profile'] = get_stock_individual_info(stock_code=self.stock_code, stock_share=self.stock_share)
            self.data['quote'] =get_stock_quote(stock_code=self.stock_code, stock_share=self.stock_share)
            print(f"---isshe---: profile: {self.data['profile']}, quote: {self.data['quote']}")
            #
            self.data['cash_flow'] = ak.stock_cash_flow_sheet_by_report_em(symbol=self.stock_code)
            self.data['balance_sheet'] = ak.stock_balance_sheet_by_report_em(symbol=self.stock_code)
            self.data['income_statement'] = ak.stock_financial_analysis_indicator(symbol=self.stock_code)

            # Extract key values
            industry = self.data['profile'].loc[self.data['profile']['item'] == '行业'].iloc[0, 1]
            market_cap = self.data['quote']['总市值'].iloc[0]

            # Get latest annual data
            latest_annual_report_date = self.data['income_statement']['报告期'].iloc[0]

            net_profit = self.data['income_statement'][self.data['income_statement']['报告期'] == latest_annual_report_date]['净利润 (元)'].iloc[0]

            cash_flow_latest = self.data['cash_flow'][self.data['cash_flow']['REPORT_DATE'].str.contains('12-31')].iloc[0]
            op_cash_flow = cash_flow_latest['NET_CASH_FLOWS_OPER_ACT']
            capex = cash_flow_latest['NET_CASH_FLOWS_INV_ACT']

            balance_sheet_latest = self.data['balance_sheet'][self.data['balance_sheet']['REPORT_DATE'].str.contains('12-31')].iloc[0]
            financial_expenses = balance_sheet_latest.get('FIN_EXP', 0) # Use .get for safety
            total_cash = balance_sheet_latest['MONETARY_CAPITAL']
            current_liabilities = balance_sheet_latest['TOTAL_CURRENT_LIAB']

            # Initialize FactorManager
            config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'stock_factors.ini')
            factor_mgr = FactorManager(config_path, self.stock_code, self.stock_name, industry)
            investment_factor = factor_mgr.get_factor()
            payout_ratio = factor_mgr.get_payout_ratio()

            # Calculations
            conservative_net_profit = net_profit * investment_factor
            estimated_dividend = conservative_net_profit * payout_ratio
            penetration_return_rate = (estimated_dividend / market_cap) * 100 if market_cap else 0

            real_controllable_cash_flow = op_cash_flow + capex - (financial_expenses or 0)
            cash_reserve = total_cash - current_liabilities

            # Target price for 5% return
            target_market_cap_5_percent = estimated_dividend / 0.05
            current_price = self.data['quote']['最新价'].iloc[0]
            current_total_shares = market_cap / current_price if current_price else 0
            target_price_5_percent = target_market_cap_5_percent / current_total_shares if current_total_shares else 0

            # Print report
            self.qcc.light_green_print("\n--- Stock Analysis Report ---")
            self.qcc.white_print(f"  {self.stock_name} ({self.stock_code}) - {industry}")
            self.qcc.light_green_print("-----------------------------")

            self.qcc.white_print(f"  Market Cap: {self._format_value(market_cap)}")
            self.qcc.white_print(f"  Last Year Net Profit: {self._format_value(net_profit)}")

            self.qcc.light_green_print("\n--- Penetration Return Rate ---")
            self.qcc.white_print(f"  Investment Factor: {investment_factor:.2f}")
            self.qcc.white_print(f"  Assumed Payout Ratio: {payout_ratio:.2f}")
            self.qcc.cyan_print(f"  Conservative Est. Dividend: {self._format_value(estimated_dividend)}")
            self.qcc.yellow_print(f"  Estimated Penetration Return Rate: {penetration_return_rate:.2f}%")

            self.qcc.light_green_print("\n--- Sustainability Check ---")
            self.qcc.white_print(f"  Real Controllable Cash Flow: {self._format_value(real_controllable_cash_flow)}")
            self.qcc.white_print(f"  Cash Reserve (Cash - Current Liab.): {self._format_value(cash_reserve)}")
            if real_controllable_cash_flow > estimated_dividend:
                self.qcc.green_print("  Cash flow can cover estimated dividend.")
            else:
                self.qcc.red_print("  Warning: Cash flow may NOT cover estimated dividend.")

            self.qcc.light_green_print("\n--- Investment Valuation ---")
            self.qcc.white_print(f"  Target Price for 5% Return: {target_price_5_percent:.2f} CNY")
            self.qcc.light_green_print("-----------------------------\n")

        except Exception as e:
            self.qcc.red_print(f"An error occurred during analysis: {e}")
            self.qcc.red_print("This might be due to data availability for the selected stock (e.g., non-A-shares, new listings).")


def search_stocks(keyword, us=False):
    """
    Search for stocks across different markets.
    """
    qcc = QuickCmdColor()
    qcc.blue_print(f"Searching for '{keyword}'...")
    try:
        all_results = []
        keyword_lower = keyword.lower()

        # A-shares
        stock_a_list = get_stock_info_cn_cached()
        result_a = [
            stock for stock in stock_a_list
            if keyword_lower in str(stock['code']).lower() or
            keyword_lower in str(stock['name']).lower()
        ]
        if result_a:
            # list is not empty
            result_df = pd.DataFrame(result_a)
            result_df['market'] = 'A-Share'
            all_results.append(result_df[['code', 'name', 'market']])

        # HK-Stock
        stock_hk_list = get_stock_info_hk_cached()
        result_hk = [
            stock for stock in stock_hk_list
            if keyword_lower in str(stock['code']).lower() or
            keyword_lower in str(stock['name']).lower()
        ]
        if result_hk:
            result_df = pd.DataFrame(result_hk)
            result_df['market'] = 'HK-Stock'
            all_results.append(result_df[['code', 'name', 'market']])

        if us:
            # US-Stock
            stock_us_list = get_stock_info_us_cached()
            result_us = [
                stock for stock in stock_us_list
                if keyword_lower in str(stock['code']).lower() or
                keyword_lower in str(stock['name']).lower()
            ]
            if result_us:
                result_df = pd.DataFrame(result_us)
                result_df['market'] = 'US-Stock'
                all_results.append(result_df[['code', 'name', 'market']])

        if not all_results:
            return []

        combined_results = pd.concat(all_results, ignore_index=True)

        return [f"{row['code']} - {row['name']} - {row['market']}" for index, row in combined_results.iterrows()]

    except Exception as e:
        qcc.red_print(f"An error occurred during stock search: {e}")
        return []

def run_stock_analysis_workflow():
    qcc = QuickCmdColor()
    keyword = qcc.green_input("Enter stock keyword (name or code) to search: ")
    if not keyword:
        qcc.red_print("Search keyword cannot be empty.")
        return

    results = search_stocks(keyword)
    if not results:
        qcc.red_print(f"No stock found for keyword: {keyword}")
        return

    fzf = FuzzyFinder()
    fzf.prepare_files(results)
    fzf.run()
    index = fzf.parse_output()

    print(index)

    if index is not None and index < len(results):
        selected = results[index]
        print(selected)
        parts = selected.split(' - ')
        stock_code = parts[0]
        stock_name = parts[1]
        stock_share = parts[2]
        analyzer = StockAnalyzer(stock_code, stock_name, stock_share)
        analyzer.analyze()
