import matplotlib.pyplot as plt
import pandas as pd

x = [1, 2, 3, 4]
y = [10, 20, 15, 30]

plt.figure(figsize=(6, 4))
plt.plot(x, y)
plt.xlabel("x")
plt.ylabel("y")
plt.title("Test simple")
plt.show()