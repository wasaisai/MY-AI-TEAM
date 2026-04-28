#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量处理职位信息脚本
读取 jobs 目录下的职位信息，进行匹配度分析，生成沟通信息
"""

import json
import os
from datetime import datetime
from typing import Dict, List


class JobProcessor:
    """职位处理器"""

    def __init__(self, base_dir: str = ".."):
        self.base_dir = base_dir
        self.jobs_dir = os.path.join(base_dir, "jobs")
        self.analysis_dir = os.path.join(base_dir, "analysis")
        self.messages_dir = os.path.join(base_dir, "messages")
        self.config_file = os.path.join(base_dir, "config.json")
        self.resume_file = os.path.join(base_dir, "resume.json")

        # 确保目录存在
        os.makedirs(self.analysis_dir, exist_ok=True)
        os.makedirs(self.messages_dir, exist_ok=True)

        # 加载配置和简历
        self.config = self._load_json(self.config_file)
        self.resume = self._load_json(self.resume_file)

    def _load_json(self, filepath: str) -> Dict:
        """加载 JSON 文件"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"加载文件失败 {filepath}: {e}")
            return {}

    def _save_json(self, data: Dict, filepath: str):
        """保存 JSON 文件"""
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"已保存: {filepath}")
        except Exception as e:
            print(f"保存文件失败 {filepath}: {e}")

    def load_jobs(self, source: str = None) -> List[Dict]:
        """
        加载职位信息

        Args:
            source: 来源（zhilian/lagou），None 表示加载所有

        Returns:
            职位列表
        """
        jobs = []

        if source:
            search_dir = os.path.join(self.jobs_dir, source)
        else:
            search_dir = self.jobs_dir

        # 遍历目录查找 JSON 文件
        for root, dirs, files in os.walk(search_dir):
            for file in files:
                if file.endswith('.json') and file != 'job-template.json':
                    filepath = os.path.join(root, file)
                    job = self._load_json(filepath)
                    if job:
                        jobs.append(job)

        print(f"加载了 {len(jobs)} 个职位")
        return jobs

    def calculate_match_score(self, job: Dict) -> Dict:
        """
        计算匹配度

        Args:
            job: 职位信息

        Returns:
            分析结果
        """
        if not self.resume or not self.config:
            print("简历或配置文件未加载")
            return {}

        weights = self.config.get('matching_weights', {})

        # 技能匹配度（40%）
        skills_score = self._calculate_skills_match(job)

        # 经验匹配度（30%）
        experience_score = self._calculate_experience_match(job)

        # 薪资匹配度（20%）
        salary_score = self._calculate_salary_match(job)

        # 其他因素（10%）
        other_score = self._calculate_other_factors(job)

        # 总分
        total_score = (
            skills_score * weights.get('skills', 0.4) +
            experience_score * weights.get('experience', 0.3) +
            salary_score * weights.get('salary', 0.2) +
            other_score * weights.get('other', 0.1)
        )

        analysis = {
            'job_id': job.get('job_id', ''),
            'company_name': job.get('company', {}).get('name', ''),
            'position_title': job.get('position', {}).get('title', ''),
            'match_score': round(total_score, 2),
            'breakdown': {
                'skills_match': round(skills_score, 2),
                'experience_match': round(experience_score, 2),
                'salary_match': round(salary_score, 2),
                'other_factors': round(other_score, 2)
            },
            'strengths': self._identify_strengths(job),
            'weaknesses': self._identify_weaknesses(job),
            'recommendations': self._generate_recommendations(total_score),
            'analyzed_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        return analysis

    def _calculate_skills_match(self, job: Dict) -> float:
        """计算技能匹配度"""
        # 这里需要实现实际的技能匹配逻辑
        # 示例：简单的关键词匹配
        required_skills = job.get('requirements', {}).get('skills', [])
        user_skills = self.resume.get('skills', [])

        if not required_skills or not user_skills:
            return 50.0  # 默认分数

        # 简单匹配逻辑
        matched = 0
        for req_skill in required_skills:
            for user_skill in user_skills:
                if user_skill.lower() in req_skill.lower():
                    matched += 1
                    break

        score = (matched / len(required_skills)) * 100 if required_skills else 50
        return min(score, 100)

    def _calculate_experience_match(self, job: Dict) -> float:
        """计算经验匹配度"""
        required_years = job.get('requirements', {}).get('experience_years', '')
        user_years = self.config.get('user_info', {}).get('years_of_experience', 0)

        # 解析要求的年限（如 "3-5年"）
        try:
            if '-' in required_years:
                min_years, max_years = map(int, required_years.replace('年', '').split('-'))
                if min_years <= user_years <= max_years:
                    return 100.0
                elif user_years < min_years:
                    return max(0, 100 - (min_years - user_years) * 20)
                else:
                    return 90.0  # 超出要求也是好事
        except:
            pass

        return 70.0  # 默认分数

    def _calculate_salary_match(self, job: Dict) -> float:
        """计算薪资匹配度"""
        job_salary = job.get('salary', {})
        expected_salary = self.config.get('job_preferences', {}).get('salary_range', {})

        job_min = job_salary.get('min', 0)
        job_max = job_salary.get('max', 0)
        expected_min = expected_salary.get('min', 0)
        expected_max = expected_salary.get('max', 0)

        if not job_min or not expected_min:
            return 70.0  # 默认分数

        # 计算重叠度
        overlap_min = max(job_min, expected_min)
        overlap_max = min(job_max, expected_max)

        if overlap_max >= overlap_min:
            # 有重叠
            overlap_range = overlap_max - overlap_min
            expected_range = expected_max - expected_min
            score = (overlap_range / expected_range) * 100 if expected_range > 0 else 100
            return min(score, 100)
        elif job_max < expected_min:
            # 低于期望
            gap = expected_min - job_max
            return max(0, 100 - gap / expected_min * 100)
        else:
            # 高于期望
            return 100.0

    def _calculate_other_factors(self, job: Dict) -> float:
        """计算其他因素"""
        score = 70.0  # 基础分

        # 公司规模匹配
        company_size = job.get('company', {}).get('size', '')
        preferred_sizes = self.config.get('job_preferences', {}).get('company_size', [])
        if company_size in preferred_sizes:
            score += 10

        # 工作地点匹配
        location = job.get('position', {}).get('work_location', '')
        preferred_locations = self.config.get('job_preferences', {}).get('locations', [])
        if any(loc in location for loc in preferred_locations):
            score += 10

        # 公司类型匹配
        company_type = job.get('company', {}).get('type', '')
        preferred_types = self.config.get('job_preferences', {}).get('company_type', [])
        if company_type in preferred_types:
            score += 10

        return min(score, 100)

    def _identify_strengths(self, job: Dict) -> List[str]:
        """识别优势"""
        strengths = []
        # 这里可以实现更复杂的逻辑
        strengths.append("技能匹配度高")
        strengths.append("经验符合要求")
        return strengths

    def _identify_weaknesses(self, job: Dict) -> List[str]:
        """识别劣势"""
        weaknesses = []
        # 这里可以实现更复杂的逻辑
        weaknesses.append("某些技能需要加强")
        return weaknesses

    def _generate_recommendations(self, score: float) -> List[str]:
        """生成建议"""
        recommendations = []

        if score >= 80:
            recommendations.append("强烈推荐申请此职位")
            recommendations.append("准备详细的项目案例")
        elif score >= 60:
            recommendations.append("可以尝试申请")
            recommendations.append("突出相关经验")
        else:
            recommendations.append("匹配度较低，建议谨慎考虑")
            recommendations.append("补充相关技能后再申请")

        return recommendations

    def save_analysis(self, analysis: Dict):
        """保存分析结果"""
        if not analysis or 'job_id' not in analysis:
            return

        filename = f"{analysis['job_id']}_{datetime.now().strftime('%Y%m%d')}.json"
        filepath = os.path.join(self.analysis_dir, filename)
        self._save_json(analysis, filepath)

    def generate_message(self, job: Dict, analysis: Dict) -> str:
        """
        生成沟通信息

        Args:
            job: 职位信息
            analysis: 分析结果

        Returns:
            沟通信息文本
        """
        if analysis.get('match_score', 0) < 70:
            print(f"匹配度过低 ({analysis.get('match_score')}分)，跳过生成沟通信息")
            return ""

        # 获取配置
        user_info = self.config.get('user_info', {})
        message_style = self.config.get('message_style', {})

        # 基本信息
        name = user_info.get('name', '求职者')
        title = user_info.get('current_title', '工程师')
        years = user_info.get('years_of_experience', 0)

        position_title = job.get('position', {}).get('title', '该职位')
        company_name = job.get('company', {}).get('name', '贵公司')

        # 生成消息（使用模板）
        message = f"""您好！

我在{company_name}招聘的{position_title}职位中看到了与我技能高度匹配的要求。我是{name}，有{years}年的{title}经验。

根据职位要求，我的优势包括：
"""

        # 添加优势
        for i, strength in enumerate(analysis.get('strengths', [])[:3], 1):
            message += f"{i}. {strength}\n"

        message += f"""
我对{company_name}的业务非常感兴趣，相信我的经验能够为团队带来价值。

附上我的简历供您参考，期待您的回复！

此致
敬礼

{name}
"""

        return message

    def save_message(self, job_id: str, message: str):
        """保存沟通信息"""
        if not message:
            return

        filename = f"{job_id}_{datetime.now().strftime('%Y%m%d')}.txt"
        filepath = os.path.join(self.messages_dir, filename)

        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(message)
            print(f"已保存沟通信息: {filepath}")
        except Exception as e:
            print(f"保存沟通信息失败: {e}")

    def process_all(self, source: str = None, min_score: float = 60):
        """
        批量处理所有职位

        Args:
            source: 来源（zhilian/lagou），None 表示处理所有
            min_score: 最低匹配分数
        """
        print("=" * 50)
        print("开始批量处理职位")
        print("=" * 50)
        print()

        # 加载职位
        jobs = self.load_jobs(source)

        if not jobs:
            print("没有找到职位信息")
            return

        # 处理每个职位
        results = []
        for i, job in enumerate(jobs, 1):
            print(f"处理第 {i}/{len(jobs)} 个职位...")

            # 分析匹配度
            analysis = self.calculate_match_score(job)

            if not analysis:
                print("分析失败，跳过")
                continue

            # 保存分析结果
            self.save_analysis(analysis)

            # 如果匹配度足够高，生成沟通信息
            if analysis.get('match_score', 0) >= min_score:
                message = self.generate_message(job, analysis)
                if message:
                    self.save_message(job.get('job_id', ''), message)

            results.append({
                'job_id': job.get('job_id', ''),
                'company': job.get('company', {}).get('name', ''),
                'position': job.get('position', {}).get('title', ''),
                'score': analysis.get('match_score', 0)
            })

            print(f"匹配度: {analysis.get('match_score', 0)}分")
            print("-" * 50)

        # 输出汇总
        print()
        print("=" * 50)
        print("处理完成！")
        print("=" * 50)
        print()
        print("匹配度排名：")
        results.sort(key=lambda x: x['score'], reverse=True)
        for i, result in enumerate(results[:10], 1):
            print(f"{i}. {result['company']} - {result['position']}: {result['score']}分")


def main():
    """主函数"""
    print("=" * 50)
    print("批量处理职位信息")
    print("=" * 50)
    print()

    processor = JobProcessor()

    # 选择来源
    print("请选择职位来源：")
    print("1. 智联招聘")
    print("2. 拉钩招聘")
    print("3. 所有来源")
    choice = input("请输入选项（1-3）: ").strip()

    source_map = {
        '1': 'zhilian',
        '2': 'lagou',
        '3': None
    }
    source = source_map.get(choice)

    # 最低匹配分数
    min_score = input("请输入最低匹配分数（默认60）: ").strip()
    min_score = float(min_score) if min_score else 60.0

    print()
    print("=" * 50)

    # 开始处理
    processor.process_all(source, min_score)


if __name__ == "__main__":
    main()
