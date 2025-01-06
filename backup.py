import base64
import time
import requests
import json
from datetime import datetime
from datetime import timedelta
# 网站地址
website = "halo网址"
# halo2备份文件夹路径
backup_halo_path = "/opt/1panel/apps/halo/halo/data/backups"
backup_api = website + "/apis/migration.halo.run/v1alpha1/backups"
check_api = website + "/apis/migration.halo.run/v1alpha1/backups?sort=metadata.creationTimestamp%2Cdesc"
# 获取现在的时间 2023-09-24T13:14:18.650Z
now_time = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
ten_days_later = (datetime.now() + timedelta(minutes=2)).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'

print(now_time)
payload = json.dumps({
    "apiVersion": "migration.halo.run/v1alpha1",
    "kind": "Backup",
    "metadata": {
        "generateName": "backup-",
        "name": ""
    },
    "spec": {
        "expiresAt": ten_days_later,
    }
})
token = "你的token"
headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json'
}
response = requests.request("POST", backup_api, headers=headers, data=payload)
print(response.text)
if response.status_code == 201:
    print("备份请求成功！")
    new_backup_name = ""
    while True:
        check_response = requests.request("GET", check_api, headers=headers)
        if check_response.status_code == 200:
            backup_data = json.loads(check_response.text)
            items = backup_data.get("items", [])
            if items[0]["status"]["phase"] == "SUCCEEDED":
                print("备份完成！")
                new_backup_name = items[0]["status"]["filename"]
                break
            if items[0]["status"]["phase"] == "RUNNING":
                print("正在备份！")
                time.sleep(10)

        else:
            print(f"查询备份请求失败！错误代码：{check_response.status_code}")

else:
    print(f"备份请求失败！错误代码：{response.status_code}")
