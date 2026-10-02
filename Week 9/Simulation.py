import numpy as np
n = 10000
sales = np.random.choice([80000, 100000, 120000], n, p=[0.3, 0.5, 0.2])
price = np.random.choice([42, 45, 48], n, p=[0.4, 0.4, 0.2])
cost = np.random.choice([36, 38, 40], n, p=[1/6, 4/6, 1/6])
investment = 500000
profit = sales * (price - cost) - investment
print("Mean profit:", profit.mean())
print("Standard deviation:", profit.std())
print("Probability profit > 0:", (profit > 0).mean())