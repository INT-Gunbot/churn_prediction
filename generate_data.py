import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# 固定随机种子，保证数据可复现
np.random.seed(2025)
random.seed(2025)

# 生成10万条用户数据
n = 100000
data = {
    "user_id": np.arange(10001, 10001 + n),
    # 基础属性
    "age": np.random.randint(18, 65, n),
    "gender": np.random.choice([0, 1], n, p=[0.48, 0.52]),  # 0女1男
    "city_level": np.random.choice([1,2,3,4], n, p=[0.2,0.3,0.3,0.2]),
    
    # 行为数据
    "login_days": np.random.randint(1, 31, n),
    "browse_times": np.random.poisson(15, n),
    "cart_add_times": np.random.poisson(5, n),
    "purchase_times": np.random.poisson(3, n),
    
    # 关键特征（项目核心：优惠券、支付卡顿）
    "coupon_remind": np.random.choice([0,1], n, p=[0.65, 0.35]),  # 0未提醒1已提醒
    "pay_lag": np.random.choice([0,1], n, p=[0.7, 0.3]),  # 0无卡顿1有卡顿
    
    # 消费数据
    "total_amount": np.round(np.random.uniform(50, 5000, n), 2),
    "last_login_days": np.random.randint(1, 90, n),
    
    # 标签：1=流失用户，0=留存用户
    "is_churn": np.nan
}

df = pd.DataFrame(data)

# 构建流失规则（贴合业务：支付卡顿+无优惠券提醒 → 流失率大幅提升）
def calc_churn(row):
    base = 0
    # 支付卡顿：流失概率+40%
    if row["pay_lag"] == 1:
        base += 0.4
    # 无优惠券提醒：流失概率+30%
    if row["coupon_remind"] == 0:
        base += 0.3
    # 长期未登录：流失概率+20%
    if row["last_login_days"] > 30:
        base += 0.2
    return 1 if random.random() < base else 0

df["is_churn"] = df.apply(calc_churn, axis=1)

# 手动插入缺失值、异常值（模拟真实脏数据，用于数据清洗）
df.loc[np.random.choice(df.index, 3000), "total_amount"] = np.nan
df.loc[df.index[:1500], "age"] = -1  # 异常年龄
df.loc[df.index[1500:3000], "browse_times"] = 999  # 异常浏览数

# 保存数据
df.to_csv("user_churn_data.csv", index=False, encoding="utf-8-sig")
print("10万行用户数据已生成：user_churn_data.csv")
print(f"流失用户占比：{df['is_churn'].mean():.2%}")