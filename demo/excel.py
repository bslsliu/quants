import pandas as pd
df = pd.read_excel(r"C:\Users\hspcadmin\Documents\demo\\coy-company_match.xlsx");
ods_k = df.dropna(subset="keyword")
df = df.fillna("")
datas = set(df["company"])
def convert(k) :
    hit = ""
    for data in datas:
      if k in data:
        hit=data
        break
    return f"{k} match {hit}"
matchOr = list(map(lambda x: convert(x), ods_k["keyword"]))
print(matchOr)
print(len(matchOr))