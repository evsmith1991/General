import plotly.express as px

df = datasets["Raw Data"]
print(df.head(5))

fig = px.scatter(x=df.days_post_first_transfer, y=df.adjusted_perf)
fig.show()

fig = px.box(x=df.months_post_first_transfer, y=df.adjusted_perf)
fig.show()
