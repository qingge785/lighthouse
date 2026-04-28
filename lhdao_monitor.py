import requests
import time
from typing import List, Dict, Optional

# ==================== 这里已经硬编码了你的 API Key ====================
API_KEY = "lh_live_vh3z42qKLoGmMJ0slYNoCHxHjdTfVTQK"   # ← 你已经填好了，不用改

class LHDaoViewer:
    def __init__(self, base_url: str = "https://service.lhdaobeta.top"):
        self.base_url = base_url.rstrip('/')
        self.headers = {
            "X-API-Key": API_KEY,          # 使用硬编码的 Key
            "Content-Type": "application/json"
        }

    # 下面代码和之前完全一样（只保留查看 + 价格监控功能）
    def list_campaigns(self, status: str = None, page: int = 1, page_size: int = 50) -> Optional[Dict]:
        params = {"page": page, "pageSize": page_size}
        if status:
            params["status"] = status.upper()
        resp = requests.get(f"{self.base_url}/open-api/v1/campaigns",
                            headers=self.headers, params=params)
        if resp.status_code == 200:
            data = resp.json()
            print(f"✅ 共找到 {data['total']} 个任务")
            for camp in data["items"]:
                self._print_campaign_price(camp)
            return data
        else:
            print(f"❌ 查询失败: {resp.text}")
            return None

    def get_campaign(self, campaign_id: str) -> Optional[Dict]:
        resp = requests.get(f"{self.base_url}/open-api/v1/campaigns/{campaign_id}",
                            headers=self.headers)
        if resp.status_code == 200:
            data = resp.json()
            self._print_campaign_price(data)
            return data
        else:
            print(f"❌ 查询任务 {campaign_id} 失败")
            return None

    def _print_campaign_price(self, camp: Dict):
        actions = camp["actions"][0]
        consumed = camp.get("consumedBudget", 0)
        total = camp.get("totalBudget", 0)
        remaining = camp.get("remainingPool", 0)
        progress = round(consumed / total * 100, 1) if total > 0 else 0

        print(f"\n📌 任务 ID: {camp['id']}")
        print(f"   类型: {actions['actionType']} | 状态: {camp['status']}")
        print(f"   目标: {actions['targetCount']} | 已完成: {actions.get('completedCount', 0)}")
        print(f"   总预算: {total} LUX | 已消耗: {consumed} LUX | 剩余: {remaining} LUX")
        print(f"   进度: {progress}% | 平台手续费: {camp.get('platformFee', 0)} LUX")

    def monitor_campaigns(self, campaign_ids: List[str] = None, interval: int = 5, timeout: int = 3600):
        if not campaign_ids:
            data = self.list_campaigns()
            if data:
                campaign_ids = [item["id"] for item in data["items"]]
        if not campaign_ids:
            print("没有找到任务")
            return

        start = time.time()
        print(f"🚀 开始实时监控 {len(campaign_ids)} 个任务的价格和进度...")

        while True:
            if time.time() - start > timeout:
                print("⏰ 监控超时！")
                break

            print(f"\n[{time.strftime('%H:%M:%S')}] ==================== 实时价格监控 ====================")
            all_done = True
            for cid in campaign_ids:
                data = self.get_campaign(cid)
                if data and data["status"] not in ["ENDED", "CLOSED"]:
                    all_done = False
            if all_done:
                print("\n🎉 所有任务已结束！")
                break
            time.sleep(interval)
