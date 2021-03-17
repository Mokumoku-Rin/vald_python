from vald_client import ValdClient
import numpy as np
import random
import string
import yaml

# 環境変数を読み込み
with open("./vald_config/config.yaml", "r") as f:
    config = yaml.safe_load(f)
vector_dimension = config["ngt"]["dimension"]  # ベクトルの次元

vc = ValdClient(ip="127.0.0.1", port="8081")  # valdに接続

# idを生成
id_length, vector_num = 5, 10
dat = string.digits + string.ascii_lowercase + string.ascii_uppercase
ids = ["".join([random.choice(dat) for i in range(id_length)]) for _ in range(vector_num)]

""" 挿入"""
for i in ids:
    v = np.random.rand(vector_dimension)  # 挿入されるデータ
    vc.insert(data_id=i, data=v)

""" indexを生成"""
vc.create_index(pool_size=vector_num)

""" 検索"""
target = np.random.rand(vector_dimension)  # 検索対象
result = vc.search(data=target, result_num=2)
print(result)

""" 削除"""
for i in ids:
    vc.delete(data_id=i)
