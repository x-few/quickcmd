#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import akshare as ak
import pandas as pd
from datetime import datetime, timedelta

default_cache_hours = 168

def get_stock_info_cn_cached(cache_file: str = 'stock_info_cache.json', cache_hours: int = default_cache_hours):
    """
    Get A-share stock basic information with local JSON cache support.

    Args:
        cache_file (str): Path to the cache file. Defaults to 'stock_info_cache.json'.
        cache_hours (int): Cache expiration time in hours. Defaults to default_cache_hours.

    Returns: List of stock information
        [
            {
                'code': str,    # Stock code
                'name': str     # Stock name
            },
            ...
        ]

    Raises:
        Exception: If failed to fetch data and no valid cache exists.
    """

    # Check if cache file exists
    if os.path.exists(cache_file):
        try:
            # Load cache file
            with open(cache_file, 'r', encoding='utf-8') as f:
                cache_data = json.load(f)

            # Check if cache has required fields
            if 'timestamp' in cache_data and 'data' in cache_data:
                # Parse cache timestamp
                cache_time = datetime.fromisoformat(cache_data['timestamp'])
                current_time = datetime.now()

                # Check if cache is still valid
                if current_time - cache_time < timedelta(hours=cache_hours):
                    print(f"Using cached data from {cache_data['timestamp']}")
                    return cache_data['data']
                else:
                    print(f"Cache expired (created at {cache_data['timestamp']})")
            else:
                print("Invalid cache format, will refresh data")

        except (json.JSONDecodeError, ValueError, KeyError) as e:
            print(f"Error reading cache file: {e}, will refresh data")
    else:
        print("Cache file not found, will fetch new data")

    # Fetch new data from akshare
    try:
        print("Fetching latest stock information...")
        stock_df = ak.stock_info_a_code_name()

        # Convert DataFrame to list of dictionaries
        stock_list = stock_df.to_dict('records')

        # Prepare cache data structure
        cache_data = {
            'timestamp': datetime.now().isoformat(),
            'data': stock_list
        }

        # Save to cache file
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(cache_data, f, ensure_ascii=False, indent=2)

        print(f"Data cached successfully to {cache_file}")
        print(f"Total stocks: {len(stock_list)}")

        return stock_list

    except Exception as e:
        print(f"Failed to fetch new data: {e}")

        # Try to use old cache if exists
        if os.path.exists(cache_file):
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    old_cache = json.load(f)
                print("Using old cache data due to fetch failure")
                return old_cache['data']
            except Exception as cache_error:
                print(f"Failed to load old cache: {cache_error}")

        # Re-raise the original exception if no fallback available
        raise e

def get_stock_info_hk_cached(cache_file: str = 'stock_info_hk_cache.json', cache_hours: int = default_cache_hours):
    """
    Get Hong Kong stock basic information with local JSON cache support.

    Args:
        cache_file (str): Path to the cache file. Defaults to 'stock_info_hk_cache.json'.
        cache_hours (int): Cache expiration time in hours. Defaults to default_cache_hours.

    Returns: List of HK stock information [{'code': str, 'name': str}, ...]

    Raises:
        Exception: If failed to fetch data and no valid cache exists.
    """

    # Check if cache file exists
    if os.path.exists(cache_file):
        try:
            # Load cache file
            with open(cache_file, 'r', encoding='utf-8') as f:
                cache_data = json.load(f)

            # Check if cache has required fields
            if 'timestamp' in cache_data and 'data' in cache_data:
                # Parse cache timestamp
                cache_time = datetime.fromisoformat(cache_data['timestamp'])
                current_time = datetime.now()

                # Check if cache is still valid
                if current_time - cache_time < timedelta(hours=cache_hours):
                    print(f"Using cached HK stock data from {cache_data['timestamp']}")
                    return cache_data['data']
                else:
                    print(f"HK stock cache expired (created at {cache_data['timestamp']})")
            else:
                print("Invalid HK stock cache format, will refresh data")

        except (json.JSONDecodeError, ValueError, KeyError) as e:
            print(f"Error reading HK stock cache file: {e}, will refresh data")
    else:
        print("HK stock cache file not found, will fetch new data")

    # Fetch new data from akshare
    try:
        print("Fetching latest HK stock information...")
        stock_df = ak.stock_hk_spot_em()

        # Extract and rename columns to maintain consistency
        if '代码' in stock_df.columns and '名称' in stock_df.columns:
            stock_basic_df = stock_df[['代码', '名称']].copy()
            stock_basic_df.columns = ['code', 'name']
        else:
            # Fallback: try different column names
            possible_code_cols = ['代码', 'code', 'symbol', '股票代码']
            possible_name_cols = ['名称', 'name', '股票名称', '公司名称']

            code_col = None
            name_col = None

            for col in possible_code_cols:
                if col in stock_df.columns:
                    code_col = col
                    break

            for col in possible_name_cols:
                if col in stock_df.columns:
                    name_col = col
                    break

            if code_col and name_col:
                stock_basic_df = stock_df[[code_col, name_col]].copy()
                stock_basic_df.columns = ['code', 'name']
            else:
                raise ValueError(f"Cannot find code/name columns in HK stock data. Available columns: {list(stock_df.columns)}")

        # Convert DataFrame to list of dictionaries
        stock_list = stock_basic_df.to_dict('records')

        # Clean and format data
        cleaned_stock_list = []
        for stock in stock_list:
            code = str(stock.get('code', '')).strip()
            name = str(stock.get('name', '')).strip()

            # Skip empty records
            if code and name and code != 'nan' and name != 'nan':
                cleaned_stock_list.append({
                    'code': code,
                    'name': name
                })

        # Prepare cache data structure
        cache_data = {
            'timestamp': datetime.now().isoformat(),
            'market': 'HK',
            'data': cleaned_stock_list
        }

        # Save to cache file
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(cache_data, f, ensure_ascii=False, indent=2)

        print(f"HK stock data cached successfully to {cache_file}")
        print(f"Total HK stocks: {len(cleaned_stock_list)}")

        return cleaned_stock_list

    except Exception as e:
        print(f"Failed to fetch new HK stock data: {e}")

        # Try to use old cache if exists
        if os.path.exists(cache_file):
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    old_cache = json.load(f)
                print("Using old HK stock cache data due to fetch failure")
                return old_cache['data']
            except Exception as cache_error:
                print(f"Failed to load old HK stock cache: {cache_error}")

        # Re-raise the original exception if no fallback available
        raise e

def get_stock_info_us_cached(cache_file: str = 'stock_info_us_cache.json', cache_hours: int = default_cache_hours):
    """
    Get US stock basic information with local JSON cache support.

    Args:
        cache_file (str): Path to the cache file. Defaults to 'stock_info_us_cache.json'.
        cache_hours (int): Cache expiration time in hours. Defaults to default_cache_hours.

    Returns: List of US stock information [{'code': str, 'name': str}, ...]

    Raises:
        Exception: If failed to fetch data and no valid cache exists.
    """

    # Check if cache file exists
    if os.path.exists(cache_file):
        try:
            # Load cache file
            with open(cache_file, 'r', encoding='utf-8') as f:
                cache_data = json.load(f)

            # Check if cache has required fields
            if 'timestamp' in cache_data and 'data' in cache_data:
                # Parse cache timestamp
                cache_time = datetime.fromisoformat(cache_data['timestamp'])
                current_time = datetime.now()

                # Check if cache is still valid
                if current_time - cache_time < timedelta(hours=cache_hours):
                    print(f"Using cached US stock data from {cache_data['timestamp']}")
                    return cache_data['data']
                else:
                    print(f"US stock cache expired (created at {cache_data['timestamp']})")
            else:
                print("Invalid US stock cache format, will refresh data")

        except (json.JSONDecodeError, ValueError, KeyError) as e:
            print(f"Error reading US stock cache file: {e}, will refresh data")
    else:
        print("US stock cache file not found, will fetch new data")

    # Fetch new data from akshare
    try:
        print("Fetching latest US stock information...")
        stock_df = ak.stock_us_spot_em()

        # Extract and rename columns to maintain consistency
        if '代码' in stock_df.columns and '名称' in stock_df.columns:
            stock_basic_df = stock_df[['代码', '名称']].copy()
            stock_basic_df.columns = ['code', 'name']
        else:
            # Fallback: try different column names
            possible_code_cols = ['代码', 'code', 'symbol', '股票代码', 'Symbol']
            possible_name_cols = ['名称', 'name', '股票名称', '公司名称', 'Name']

            code_col = None
            name_col = None

            for col in possible_code_cols:
                if col in stock_df.columns:
                    code_col = col
                    break

            for col in possible_name_cols:
                if col in stock_df.columns:
                    name_col = col
                    break

            if code_col and name_col:
                stock_basic_df = stock_df[[code_col, name_col]].copy()
                stock_basic_df.columns = ['code', 'name']
            else:
                raise ValueError(f"Cannot find code/name columns in US stock data. Available columns: {list(stock_df.columns)}")

        # Convert DataFrame to list of dictionaries
        stock_list = stock_basic_df.to_dict('records')

        # Clean and format data
        cleaned_stock_list = []
        for stock in stock_list:
            code = str(stock.get('code', '')).strip()
            name = str(stock.get('name', '')).strip()

            # Skip empty records
            if code and name and code != 'nan' and name != 'nan':
                cleaned_stock_list.append({
                    'code': code,
                    'name': name
                })

        # Prepare cache data structure
        cache_data = {
            'timestamp': datetime.now().isoformat(),
            'market': 'US',
            'data': cleaned_stock_list
        }

        # Save to cache file
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(cache_data, f, ensure_ascii=False, indent=2)

        print(f"US stock data cached successfully to {cache_file}")
        print(f"Total US stocks: {len(cleaned_stock_list)}")

        return cleaned_stock_list

    except Exception as e:
        print(f"Failed to fetch new US stock data: {e}")

        # Try to use old cache if exists
        if os.path.exists(cache_file):
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    old_cache = json.load(f)
                print("Using old US stock cache data due to fetch failure")
                return old_cache['data']
            except Exception as cache_error:
                print(f"Failed to load old US stock cache: {cache_error}")

        # Re-raise the original exception if no fallback available
        raise e


def get_stock_individual_info(stock_code: str, stock_share: str):
    """
    Get individual stock information based on stock market type.

    Args:
        stock_code (str): Stock code/symbol
        stock_share (str): Stock market type - 'A-Share', 'HK-Stock', 'US-Stock'

    Returns: Stock individual information DataFrame, None if failed

    Raises:
        ValueError: If unsupported stock_share type is provided
        Exception: If API call fails
    """

    try:
        if stock_share == 'A-Share':
            # A 股个股信息查询 - 东方财富
            print(f"Fetching A-Share info for {stock_code}")
            return ak.stock_individual_info_em(symbol=stock_code)

        elif stock_share == 'HK-Stock':
            # 港股个股信息查询 - 雪球
            print(f"Fetching HK stock info for {stock_code}")
            return ak.stock_individual_basic_info_hk_xq(symbol=stock_code)

        elif stock_share == 'US-Stock':
            # 美股个股信息查询 - 雪球
            print(f"Fetching US stock info for {stock_code}")
            return ak.stock_individual_basic_info_us_xq(symbol=stock_code)

        else:
            raise ValueError(f"Unsupported stock_share type: {stock_share}. "
                           f"Supported types: 'A-Share', 'HK-Stock'")

    except Exception as e:
        print(f"Error fetching stock info for {stock_code} ({stock_share}): {e}")
        return None


def get_stock_quote(stock_code: str, stock_share: str):
    """
    Get stock real-time quote based on stock market type.

    Args:
        stock_code (str): Stock code/symbol
        stock_share (str): Stock market type - 'A-Share' or 'HK-Stock'

    Returns:
        Optional[pd.Series]: Stock quote information as Series, None if failed

    Raises:
        ValueError: If unsupported stock_share type is provided
    """

    try:
        if stock_share == 'A-Share':
            # A 股实时行情
            print(f"Fetching A-Share quote for {stock_code}")
            spot_df = ak.stock_zh_a_spot_em()

            # Filter by stock code
            quote_data = spot_df[spot_df['代码'] == stock_code]
            if not quote_data.empty:
                return quote_data.iloc[0]  # Return first match as Series
            else:
                print(f"No A-Share data found for code: {stock_code}")
                return None

        elif stock_share == 'HK-Stock':
            # 港股实时行情
            print(f"Fetching HK stock quote for {stock_code}")
            spot_df = ak.stock_hk_spot_em()

            # Filter by stock code
            quote_data = spot_df[spot_df['代码'] == stock_code]
            if not quote_data.empty:
                return quote_data.iloc[0]  # Return first match as Series
            else:
                print(f"No HK stock data found for code: {stock_code}")
                return None

        else:
            raise ValueError(f"Unsupported stock_share type: {stock_share}. "
                           f"Supported types: 'A-Share', 'HK-Stock'")

    except Exception as e:
        print(f"Error fetching quote for {stock_code} ({stock_share}): {e}")
        return None
