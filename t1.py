# 导入tushare
import tushare as ts

# 初始化pro接口
pro = ts.pro_api('0727ee16a574094aefc773c03f505d48c692d8bb0dc22fbdf8b8038e')

# 拉取数据



df = pro.bak_basic(trade_date='20211012', fields='trade_date,ts_code,name,industry,pe')
print(df)

