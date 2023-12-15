from HouseDAO import HouseDAO
import pandas as pd
import matplotlib.pyplot as plt

file = "house.csv"
name = "houses"
house = HouseDAO(file, name)
df = pd.read_csv(file)

# df.info()
x = df["center_distance"]
y = df["price"]

plt.scatter(x, y)
# plt.figure()
plt.xlabel("center_distance")
plt.ylabel("Price")
plt.title("Real State prices")
plt.legend()
plt.show()
