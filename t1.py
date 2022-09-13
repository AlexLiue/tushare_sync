# 导入tushare
import tushare as ts

# 初始化pro接口
pro = ts.pro_api('0727ee16a574094aefc773c03f505d48c692d8bb0dc22fbdf8b8038e')

# 拉取数据
df = pro.concept_detail(**{
    "id": "",
    "ts_code": "",
    "limit": "",
    "offset": ""
}, fields=[
    "id",
    "concept_name",
    "ts_code",
    "name"
])
print(df)

