import requests
import time
from datetime import datetime

# ================== 配置区 ==================
API_KEY = "lh_live_vI6rDHTL-gEL-6FDScjt2uZc4BZA9eNz"                    # ←←← 这里填你的 Lighthouse API Key

CHECK_INTERVAL = 60          # 秒，轮询间隔（建议 30~300 秒）
VALUE_THRESHOLD = 10.0       # 只有大于这个值的任务才会输出报告

STATUS_FILTER = "ACTIVE"     # 只监控进行中的任务，可改成 None 监控全部
# ===========================================

BASE_URL = "https://service.lhdaobeta.top/open-api/v1"

def get_campaigns():
    url = f"{BASE_URL}/campaigns"
    headers = {"X-API-Key": API_KEY}
    params = {
        "status": STATUS_FILTER,
        "page": 1,
        "pageSize": 50
    }
    try:
        resp = requests.get(url, headers=headers, params=params, timeout=15)
        if resp.status_code == 200:
            return resp.json()
        else:
            print(f"[{datetime.now()}] ❌ API 请求失败: {resp.status_code}")
            return None
    except Exception as e:
        print(f"[{datetime.now()}] ❌ 请求异常: {e}")
        return None

notified_ids = set()   # 防止同一个任务重复输出报告

print("🚀 Lighthouse 任务监控脚本已启动")
print(f"   报告触发条件：价值 > {VALUE_THRESHOLD} LUX")
print(f"   检查间隔：{CHECK_INTERVAL} 秒 | 状态筛选：{STATUS_FILTER or '全部'}")
print("=" * 80)

while True:
    print(f"[{datetime.now()}] 🔍 正在检查任务列表...")

    data = get_campaigns()
    
    if data and "items" in data:
        report_printed = False
        
        for campaign in data["items"]:
            cid = campaign.get("id")
            if not cid or cid in notified_ids:
                continue

            high_value_details = []
            
            # 检查每个 action 的 baseReward 是否 > 10 LUX
            for action in campaign.get("actions", []):
                reward = action.get("baseReward", 0)
                if reward > VALUE_THRESHOLD:
                    high_value_details.append(
                        f"   • {action.get('actionType', '未知')} → {reward} LUX "
                        f"(目标次数: {action.get('targetCount', 0)})"
                    )
            
            # ================== 只有价值 > 10 LUX 才输出完整报告 ==================
            if high_value_details:
                report_printed = True
                notified_ids.add(cid)
                
                print("\n" + "=" * 60)
                print("🚨 高价值任务报告")
                print("=" * 60)
                print(f"任务 ID     : {cid}")
                print(f"状态         : {campaign.get('status')}")
                print(f"剩余池       : {campaign.get('remainingPool', 0)} LUX")
                print(f"目标链接     : {campaign.get('targetUrl', '无')}")
                print(f"创建时间     : {campaign.get('createdAt', '')}")
                print(f"过期时间     : {campaign.get('expiresAt', '')}")
                print("-" * 40)
                print("奖励详情（价值 > 10 LUX）：")
                for detail in high_value_details:
                    print(detail)
                print("=" * 60)
                print(f"[{datetime.now()}] 报告结束 — 请立即处理\n")
        
        if not report_printed:
            print(f"[{datetime.now()}] 本次检查未发现价值 > {VALUE_THRESHOLD} LUX 的任务")
    
    time.sleep(CHECK_INTERVAL)
