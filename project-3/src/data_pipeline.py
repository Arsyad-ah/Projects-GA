import numpy as np
import pandas as pd



def clean_data(df: pd.DataFrame) -> pd.DataFrame:

    # remove non-residential house
    df = df[df['MSZoning'] != 'C (all)']

    if 'Id' in df.columns:
        df.drop('Id', axis=1, inplace=True)

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


    house_num = df[['LotFrontage', 'LotArea', 'YearBuilt', 'YearRemodAdd',
       'MasVnrArea', 'BsmtFinSF1', 'BsmtFinSF2', 'BsmtUnfSF',
       'TotalBsmtSF', '1stFlrSF', '2ndFlrSF', 'LowQualFinSF', 'GrLivArea',
       'GarageYrBlt', 'GarageArea', 'WoodDeckSF', 'OpenPorchSF',
       'EnclosedPorch', '3SsnPorch', 'ScreenPorch', 'PoolArea', 'MiscVal',
       'MoSold', 'YrSold', 'SalePrice']]

    house_ord = df.drop([house_cat, house_num], axis=1)

    house_cat.fillna('Nil', inplace=True)

    house_num.drop('GarageYrBlt', axis=1, inplace=True)

    house_num.fillna(0, inplace=True)

    house_clean = pd.concat([house_num, house_cat, house_ord], axis=1)

    house_clean['MSSubClass'] = house_clean['MSSubClass'].apply(lambda x: str(x))

    house_clean['house_age'] = house_clean['YrSold'] - house_clean['YearBuilt']
