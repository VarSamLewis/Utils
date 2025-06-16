import numpy as np
import pandas as pd

def reduce_df_mem_usage(df: pd.DataFrame, float16_as32: bool = True) -> pd.DataFrame:
    """
    Reduces memory usage of a pandas DataFrame by downcasting numeric columns
    to smaller data types where possible.

    Parameters:
        df (pd.DataFrame): The input DataFrame.
        float16_as32 (bool): If True, use float32 instead of float16 for better precision.

    Returns:
        pd.DataFrame: Optimized DataFrame with reduced memory usage.
    """

    start_mem = df.memory_usage(deep=True).sum() / 1024**2
    print(f"Memory usage of dataframe is {start_mem:.2f} MB")

    for col in df.columns:
        col_type = df[col].dtype

        # Skip object, category, and boolean columns
        if str(col_type) in ['object', 'category', 'bool']:
            continue

        c_min = df[col].min()
        c_max = df[col].max()

        if str(col_type)[:3] == 'int':
            if c_min > np.iinfo(np.int8).min and c_max < np.iinfo(np.int8).max:
                df[col] = df[col].astype(np.int8)
            elif c_min > np.iinfo(np.int16).min and c_max < np.iinfo(np.int16).max:
                df[col] = df[col].astype(np.int16)
            elif c_min > np.iinfo(np.int32).min and c_max < np.iinfo(np.int32).max:
                df[col] = df[col].astype(np.int32)
            elif c_min > np.iinfo(np.int64).min and c_max < np.iinfo(np.int64).max:
                df[col] = df[col].astype(np.int64)
        else:
            if c_min > np.finfo(np.float16).min and c_max < np.finfo(np.float16).max:
                if float16_as32:
                    df[col] = df[col].astype(np.float32)
                else:
                    df[col] = df[col].astype(np.float16)
            elif c_min > np.finfo(np.float32).min and c_max < np.finfo(np.float32).max:
                df[col] = df[col].astype(np.float32)
            else:
                df[col] = df[col].astype(np.float64)

    end_mem = df.memory_usage(deep=True).sum() / 1024**2
    print(f"Memory usage after optimization is: {end_mem:.2f} MB")
    print(f"Decreased by {(100 * (start_mem - end_mem) / start_mem):.1f}%")

    return df