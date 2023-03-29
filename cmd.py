import requests


def get_proxy():
    data = requests.get("http://127.0.0.1:5010/get/").json()
    # print("成功获取代理地址: ", data.get("proxy"))
    return data

datas = []

if __name__ == '__main__':
    # 查询代理的数量
    for i in range(200):
        data = get_proxy()
        if data in datas:
            continue
        else:
            datas.append(data)
    print(len(datas))
    print(datas)