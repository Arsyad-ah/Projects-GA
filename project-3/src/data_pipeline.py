import os
from sqlalchemy import create_engine
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler

def data_ingest():
    """To ingest csv file and write back to sqlite file"""
    pass

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean the data performing the following:
        1. Filtering for residential data
        2. Filling in NA with Nil and 0
        3. Creating dummy columns 
    """
    # remove non-residential house
    df = df[df['MSZoning'] != 'C (all)']

    if 'Id' in df.columns:
        df.drop('Id', axis=1, inplace=True)

    # get categorical columns
    house_cat = df[['MSZoning', 'Street', 'Alley', 'LotShape', 'LandContour',
        'Utilities', 'LotConfig', 'LandSlope', 'Neighborhood',
        'Condition1', 'Condition2', 'BldgType', 'HouseStyle', 'RoofStyle',
        'RoofMatl', 'Exterior1st', 'Exterior2nd', 'MasVnrType',
        'ExterQual', 'ExterCond', 'Foundation', 'BsmtQual', 'BsmtCond',
        'BsmtExposure', 'BsmtFinType1', 'BsmtFinType2', 'Heating',
        'HeatingQC', 'CentralAir', 'Electrical', 'KitchenQual',
        'Functional', 'FireplaceQu', 'GarageType', 'GarageFinish',
        'GarageQual', 'GarageCond', 'PavedDrive', 'PoolQC', 'Fence',
        'SaleType', 'SaleCondition', 'MSSubClass', 'MiscFeature']]

    # get numerical columns
    house_num = df[['LotFrontage', 'LotArea', 'YearBuilt', 'YearRemodAdd',
        'MasVnrArea', 'BsmtFinSF1', 'BsmtFinSF2', 'BsmtUnfSF',
        'TotalBsmtSF', '1stFlrSF', '2ndFlrSF', 'LowQualFinSF', 'GrLivArea',
        'GarageYrBlt', 'GarageArea', 'WoodDeckSF', 'OpenPorchSF',
        'EnclosedPorch', '3SsnPorch', 'ScreenPorch', 'PoolArea', 'MiscVal',
        'MoSold', 'YrSold', 'SalePrice']]

    # get ordinal columns
    house_ord = df.drop([house_cat, house_num], axis=1)

    house_cat.fillna('Nil', inplace=True)

    # dropping GarageYrBlt as it has high correlation with YearBuilt
    house_num.drop('GarageYrBlt', axis=1, inplace=True)

    # 0 if missing or not applicable
    house_num.fillna(0, inplace=True) 

    house_clean = pd.concat([house_num, house_cat, house_ord], axis=1)

    # house_clean['MSSubClass'] = house_clean['MSSubClass'].apply(lambda x: str(x))
    house_clean['MSSubClass'] = house_clean['MSSubClass'].apply(_change_to_string)

    house_clean['house_age'] = house_clean['YrSold'] - house_clean['YearBuilt']

    # get features to perform get dummies
    fixed_feat = house_clean[['MSSubClass', 'Street', 'LotConfig', 'Condition2', 'Foundation', 'HalfBath',
                    'MSZoning', 'BldgType', 'BsmtQual', 'BsmtFullBath', 'BedroomAbvGr', 'GarageType', 'PoolArea', 
                    'LotFrontage', 'Neighborhood', 'HouseStyle', 'TotalBsmtSF', 'BsmtHalfBath', 'KitchenAbvGr', 
                    'MiscFeature', 'LotShape', 'LandContour', 'Condition1', 'MasVnrType', '2ndFlrSF', 'TotRmsAbvGrd',
                    '1stFlrSF', 'FullBath', 'GrLivArea', 'GarageArea', 'MiscVal', 'LotArea', 'Utilities', 'GarageCars',
                    'MasVnrArea', 'BsmtFinSF1', 'BsmtFinSF2', 'Alley', 'LandSlope', 'house_age', 'YearRemodAdd',
                    'WoodDeckSF', 'OpenPorchSF', 'EnclosedPorch', '3SsnPorch', 'ScreenPorch', 'RoofStyle', 'Fireplaces'
                            ]]

    # creating dummy variable for categories cols
    fixed_feat_dummy = pd.get_dummies(fixed_feat, drop_first=True)

    house_1 = pd.concat([fixed_feat_dummy, df['YrSold'], df['SalePrice']], axis=1)

    return house_1


def data_split(df, column, value):
    """Customized train_test split based on sell date"""
    X_train = df[df[column] < value]
    X_train.drop(column, axis=1, inplace=True)
    X_train.sort_values(column, ascending=True, inplace=True)
    y_train = df[df[column] < value][column]

    X_test = df[df[column] == value]
    X_test.drop(column, axis=1, inplace=True)
    y_test = df[df[column] == value][column]

    return X_train, y_train, X_test, y_test


def data_preprocess(train, test):
    """Standardscale data"""
    ss = StandardScaler()
    ss.fit(train)

    Xs_train = pd.DataFrame(ss.transform(train), columns=train.columns.values)
    Xs_test = pd.DataFrame(ss.transform(test), columns=train.columns.values)

    return Xs_train, Xs_test




def _change_to_string(text):
    return str(text)