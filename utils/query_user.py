

import tushare as ts

if __name__ == '__main__':
    pro = ts.pro_api()

    # 设置你的token
    df = pro.user(token='0727ee16a574094aefc773c03f505d48c692d8bb0dc22fbdf8b8038e')

    print(df)


