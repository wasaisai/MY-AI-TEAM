#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智联招聘职位信息爬虫脚本
注意：此脚本仅供学习参考，使用前请确保遵守网站的 robots.txt 和服务条款
"""

import json
import time
import os
from datetime import datetime
from typing import List, Dict
import requests
from bs4 import BeautifulSoup

class ZhilianScraper:
    """智联招聘爬虫"""

    def __init__(self, output_dir: str = "../jobs/zhilian"):
        self.base_url = "https://www.zhaopin.com"
        self.output_dir = output_dir
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        }

        # 确保输出目录存在
        os.makedirs(output_dir, exist_ok=True)

    def search_jobs(self, keyword: str, city: str = "北京", page: int = 1) -> List[Dict]:
        """
        搜索职位

        Args:
            keyword: 搜索关键词（如"前端工程师"）
            city: 城市名称
            page: 页码

        Returns:
            职位列表
        """
        print(f"正在搜索: {keyword} - {city} - 第{page}页")

        # 这里需要根据实际的智联招聘 API 或页面结构来实现
        # 以下是示例代码结构

        search_url = f"{self.base_url}/search"
        params = {
            'jl': city,
            'kw': keyword,
            'p': page
        }

        try:
            # 注意：实际使用时需要处理登录、验证码等问题
            response = requests.get(search_url, params=params, headers=self.headers, timeout=10)
            response.raise_for_status()

            # 解析页面
            jobs = self._parse_job_list(response.text)

            # 延迟，避免请求过快
            time.sleep(2)

            return jobs

        except Exception as e:
            print(f"搜索失败: {e}")
            return []

    def _parse_job_list(self, html: str) -> List[Dict]:
        """解析职位列表页面"""
        jobs = []

        # 这里需要根据实际页面结构来解析
        # 以下是示例结构
        soup = BeautifulSoup(html, 'html.parser')

        # 示例：查找职位卡片
        job_cards = soup.find_all('div', class_='job-card')

        for card in job_cards:
            try:
                job = {
                    'job_id': card.get('data-job-id', ''),
                    'title': card.find('h3').text.strip() if card.find('h3') else '',
                    'company': card.find('div', class_='company-name').text.strip() if card.find('div', class_='company-name') else '',
                    'salary': card.find('span', class_='salary').text.strip() if card.find('span', class_='salary') else '',
                    'location': card.find('span', class_='location').text.strip() if card.find('span', class_='location') else '',
                    'url': self.base_url + card.find('a')['href'] if card.find('a') else '',
                }
                jobs.append(job)
            except Exception as e:
                print(f"解析职位卡片失败: {e}")
                continue

        return jobs

    def get_job_detail(self, job_url: str) -> Dict:
        """
        获取职位详情

        Args:
            job_url: 职位详情页 URL

        Returns:
            职位详细信息
        """
        print(f"正在获取职位详情: {job_url}")

        try:
            response = requests.get(job_url, headers=self.headers, timeout=10)
            response.raise_for_status()

            job_detail = self._parse_job_detail(response.text, job_url)

            time.sleep(2)

            return job_detail

        except Exception as e:
            print(f"获取职位详情失败: {e}")
            return {}

    def _parse_job_detail(self, html: str, url: str) -> Dict:
        """解析职位详情页面"""
        soup = BeautifulSoup(html, 'html.parser')

        # 这里需要根据实际页面结构来解析
        # 以下是示例结构
        job_detail = {
            'job_id': url.split('/')[-1],
            'source': 'zhilian',
            'url': url,
            'collected_date': datetime.now().strftime('%Y-%m-%d'),
            'status': 'pending',
            'company': {},
            'position': {},
            'salary': {},
            'requirements': {},
            'responsibilities': [],
            'benefits': [],
            'tech_stack': [],
        }

        # 解析各个字段（需要根据实际页面结构调整）
        try:
            # 职位标题
            title_elem = soup.find('h1', class_='job-title')
            if title_elem:
                job_detail['position']['title'] = title_elem.text.strip()

            # 公司名称
            company_elem = soup.find('div', class_='company-name')
            if company_elem:
                job_detail['company']['name'] = company_elem.text.strip()

            # 薪资
            salary_elem = soup.find('span', class_='salary')
            if salary_elem:
                salary_text = salary_elem.text.strip()
                # 解析薪资范围（如 "20K-30K"）
                job_detail['salary'] = self._parse_salary(salary_text)

            # 职位描述
            desc_elem = soup.find('div', class_='job-description')
            if desc_elem:
                job_detail['responsibilities'] = [p.text.strip() for p in desc_elem.find_all('p')]

            # 职位要求
            req_elem = soup.find('div', class_='job-requirements')
            if req_elem:
                job_detail['requirements']['skills'] = [li.text.strip() for li in req_elem.find_all('li')]

        except Exception as e:
            print(f"解析职位详情失败: {e}")

        return job_detail

    def _parse_salary(self, salary_text: str) -> Dict:
        """解析薪资文本"""
        salary = {
            'min': 0,
            'max': 0,
            'currency': 'CNY',
            'period': 'monthly',
            'note': salary_text
        }

        # 简单的薪资解析逻辑（需要根据实际格式调整）
        try:
            # 示例: "20K-30K" 或 "20000-30000"
            if 'K' in salary_text:
                parts = salary_text.replace('K', '').split('-')
                if len(parts) == 2:
                    salary['min'] = int(parts[0]) * 1000
                    salary['max'] = int(parts[1]) * 1000
        except Exception as e:
            print(f"解析薪资失败: {e}")

        return salary

    def save_job(self, job: Dict):
        """保存职位信息到文件"""
        if not job or 'job_id' not in job:
            print("职位信息无效，跳过保存")
            return

        filename = f"{job['job_id']}_{datetime.now().strftime('%Y%m%d')}.json"
        filepath = os.path.join(self.output_dir, filename)

        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(job, f, ensure_ascii=False, indent=2)
            print(f"已保存: {filepath}")
        except Exception as e:
            print(f"保存失败: {e}")

    def run(self, keyword: str, city: str = "北京", max_pages: int = 3):
        """
        运行爬虫

        Args:
            keyword: 搜索关键词
            city: 城市
            max_pages: 最大爬取页数
        """
        print(f"开始爬取: {keyword} - {city}")
        print(f"最大页数: {max_pages}")
        print("-" * 50)

        all_jobs = []

        for page in range(1, max_pages + 1):
            # 搜索职位列表
            jobs = self.search_jobs(keyword, city, page)

            if not jobs:
                print(f"第{page}页没有找到职位，停止爬取")
                break

            print(f"第{page}页找到 {len(jobs)} 个职位")

            # 获取每个职位的详情
            for job in jobs:
                if job.get('url'):
                    detail = self.get_job_detail(job['url'])
                    if detail:
                        self.save_job(detail)
                        all_jobs.append(detail)

            print(f"第{page}页处理完成")
            print("-" * 50)

        print(f"爬取完成！共获取 {len(all_jobs)} 个职位")
        return all_jobs


def main():
    """主函数"""
    print("=" * 50)
    print("智联招聘职位爬虫")
    print("=" * 50)
    print()

    # 配置参数
    keyword = input("请输入搜索关键词（如：前端工程师）: ").strip() or "前端工程师"
    city = input("请输入城市（如：北京）: ").strip() or "北京"
    max_pages = input("请输入最大爬取页数（默认3）: ").strip()
    max_pages = int(max_pages) if max_pages.isdigit() else 3

    print()
    print("=" * 50)

    # 创建爬虫实例
    scraper = ZhilianScraper()

    # 运行爬虫
    scraper.run(keyword, city, max_pages)

    print()
    print("=" * 50)
    print("提示：")
    print("1. 此脚本仅供学习参考")
    print("2. 实际使用需要处理登录、验证码、反爬虫等问题")
    print("3. 请遵守网站的 robots.txt 和服务条款")
    print("4. 建议使用官方 API 或手动复制职位信息")
    print("=" * 50)


if __name__ == "__main__":
    main()
