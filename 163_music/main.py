"""
@author: Alex
@contact: 1272296763@qq.com or jakinmili@gmail.com
@file: main.py
@time: 2019/9/10 17:43
"""
str = """
一来送菜，
二来遮阳，
三来观景，
颇有滋味，

成长一月又几，窗台略显杂乱，斟酌数次
今日，
摘
洗
炒
品
.....
而后，余根弃之，略有不舍，但窗台瞬间变得整洁而内心舒适。
"""
str = str.strip().replace(' ', '').replace('\n', '').replace('\t', '').replace('\r', '').strip()
print(str)