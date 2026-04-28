import requests
import time
from typing import List, Dict, Optional

class LHDaoViewer:
    def __init__(self, api_key: str, base_url: str = "https://service.lhdaobeta.top"):
        self.base_url = base_url.rstrip('/')
        self.headers = {
            "X-API-Key": lh_live_vh3z42qKLoGmMJ0slYNoCHxHjdTfVTQK,
            "Content-Type": "application/json"
        }

    def list_campaigns(self, status: str = None, page: int = 1, page_size: int = 50) -> Optional[Dict]:
        """列出所有任务（支持按状态筛选）"""
        params = {"page": page, "pageSize": page_size}
        if status:
            params["status"] = status.upper()

        resp = requests.get(f"{self.base_url}/open-api/v1/campaigns",
                            headers=self.headers, params=params)
        
        if resp.status_code == 200:
            data = resp.json()
            print(f"✅ 共找到 {data['total']} 个任务（第 {data['page']} 页）")
            for camp in data["items"]:
                self._print_campaign_price(camp)
            return data
        else:
            print(f"❌ 查询任务列表失败: {resp.text}")
            return None

    def get_campaign(self, campaign_id: str) -> Optional[Dict]:
        """查看单个任务详情（重点显示价格）"""
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
        """统一打印任务的价格和状态信息"""
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
        print(f"   创建时间: {camp['createdAt']} | 过期时间: {camp.get('expiresAt', 'N/A')}")

    def monitor_campaigns(self, campaign_ids: List[str] = None, interval: int = 5, timeout: int = 3600):
        """实时轮询任务状态和价格（不传 ID 则监控所有任务）"""
        if not campaign_ids:
            print("🔍 未指定任务ID，正在查询所有任务...")
            data = self.list_campaigns()
            if data:
                campaign_ids = [item["id"] for item in data["items"]]

        if not campaign_ids:
            print("没有找到任何任务")
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
                data = self.get_campaign(cid)  # 会自动打印价格
                if data and data["status"] not in ["ENDED", "CLOSED"]:
                    all_done = False

            if all_done:
                print("\n🎉 所有任务已结束！")
                break

            time.sleep(interval)
