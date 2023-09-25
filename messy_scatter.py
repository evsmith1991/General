import numpy as np
import matplotlib.pyplot as plt

df = datasets["Raw Data"] #pulling data from Mode dataset
print(df.head(5))

x=df.months_post_first_transfer
y=df.adjusted_perf

# Calculate mean and standard deviation
mean_y = np.mean(y)
std_y = np.std(y)

# Create scatter plot
plt.scatter(x, y, label='Data Points', color='b')

# Add mean and standard deviation box
bbox_props = dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.5)
plt.text(0.5, np.max(y) - 2, f"Mean: {mean_y:.2f}\nStd: {std_y:.2f}", bbox=bbox_props)

# Add mean line
plt.axhline(mean_y, color='r', linestyle='--', linewidth=0.8, label='Mean')

# Add 1 std deviation band
plt.fill_between(x, mean_y - std_y, mean_y + std_y, color='gray', alpha=0.2, label='1 Std Dev')

# Label the plot
plt.xlabel('Time')
plt.ylabel('Value')
plt.title('Scatterplot Over Time with Mean and Std Dev')
plt.legend()

plt.show()
