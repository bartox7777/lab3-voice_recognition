import pandas as pd
import matplotlib.pyplot as plt

ALGS = ["1-Evol-RS", "1-Coev-RS", "2-Coev-RS", "1-Coev", "2-Coev"]
FILES = ["1c.csv", "1crs.csv", "1ers.csv", "2c.csv", "2crs.csv"]
FILES = [f"dane/{file}" for file in FILES]

dataframes = [pd.read_csv(file) for file in FILES]

# First plot
plt.subplot(1, 2, 1)
for df in dataframes:
    plt.plot(df["effort"]/1000, df.iloc[:, 2:].mean(axis=1)*100)
plt.xlabel(r"Rozegranych gier ($\times$ 1000)")
plt.ylabel(r"Odsetek wygranych gier ($\%$)")
plt.legend(ALGS)

# Second plot
plt.subplot(1, 2, 2)
for df in dataframes:
    plt.plot(df["effort"], df.iloc[:, 2:].max(axis=1))
plt.xlabel("Rozegranych gier")
plt.ylabel("Maksymalny odsetek wygranych gier")
plt.legend(ALGS)

plt.show()