#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import requests
from datetime import datetime, timedelta
from pathlib import Path
import pandas as pd

# 搜索关键词
SEARCH_KEYWORDS = [
    "conjugated coordination polymer battery",
    "CCP sodium-ion battery",
    "conjugated polymer sodium-ion",
    "carbonyl organic electrode sodium",
    "organic proton storage",
    "organic aqueous battery zinc",
    "covalent organic framework sodium-ion",
    "conjugated ladder polymer battery",
]

# 期刊分类
JOURNAL_TIERS = {
    "Tier 1": [
        "Nature",
        "Science",
        "JACS",
        "Angewandte Chemie",
        "Chemical Communications",
        "Energy & Environmental Science",
        "Advanced Materials",
        "Advanced Energy Materials",
        "Chemical Reviews",
        "Accounts of Chemical Research",
        "Nature Communications",
        "Science Advances",
        "Nature Energy",
    ],
    "Tier 2": [
        "Advanced Functional Materials",
        "ACS Nano",
        "Nano Letters",
        "ACS Energy Letters",
        "Chemical Science",
        "Journal of Materials Chemistry A",
        "SmartMat",
        "eScience",
        "EnergyChem",
    ],
    "Tier 3": [
        "ACS Applied Materials & Interfaces",
        "Chemical Engineering Journal",
        "Small",
        "Materials Today",
        "Journal of Power Sources",
        "Electrochimica Acta",
    ],
}

def get_week_info():
    """获取当前周信息"""
    now = datetime.now()
    year, week, _ = now.isocalendar()
    week_start = now - timedelta(days=now.weekday())
    week_end = week_start + timedelta(days=6)
    return year, week, week_start, week_end

def search_semantic_scholar(keyword, limit=10):
    """从 Semantic Scholar API 搜索论文"""
    papers = []
    url = "https://api.semanticscholar.org/graph/v1/paper/search"
    params = {
        "query": keyword,
        "limit": limit,
        "fields": "title,authors,venue,publicationDate,abstract,url,externalIds",
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        for paper in data.get("data", []):
            paper_info = {
                "title": paper.get("title", "N/A"),
                "authors": ", ".join([a.get("name", "Unknown") for a in paper.get("authors", [])]),
                "venue": paper.get("venue", "N/A"),
                "publication_date": paper.get("publicationDate", "N/A"),
                "abstract": paper.get("abstract", "N/A"),
                "url": paper.get("url", "N/A"),
                "source": "Semantic Scholar",
            }
            papers.append(paper_info)
    except Exception as e:
        print(f"Error searching Semantic Scholar for '{keyword}': {e}")
    
    return papers

def search_crossref(keyword, limit=10):
    """从 CrossRef API 搜索论文"""
    papers = []
    url = "https://api.crossref.org/works"
    params = {
        "query": keyword,
        "rows": limit,
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        for item in data.get("message", {}).get("items", []):
            authors = []
            for author in item.get("author", []):
                name = f"{author.get('given', '')} {author.get('family', '')}".strip()
                if name:
                    authors.append(name)
            
            publication_date = "N/A"
            if item.get("published", {}).get("date-parts"):
                publication_date = "-".join(map(str, item.get("published", {}).get("date-parts")[0]))
            
            paper_info = {
                "title": item.get("title", ["N/A"])[0] if item.get("title") else "N/A",
                "authors": ", ".join(authors) if authors else "N/A",
                "venue": ", ".join(item.get("container-title", ["N/A"])),
                "publication_date": publication_date,
                "abstract": "N/A",
                "url": item.get("URL", "N/A"),
                "source": "CrossRef",
            }
            papers.append(paper_info)
    except Exception as e:
        print(f"Error searching CrossRef for '{keyword}': {e}")
    
    return papers

def classify_paper(paper):
    """根据期刊名称分类论文"""
    venue = paper.get("venue", "").lower()
    
    for tier, journals in JOURNAL_TIERS.items():
        for journal in journals:
            if journal.lower() in venue:
                return tier
    
    return "Tier 3"

def deduplicate_papers(papers):
    """去重论文"""
    seen_titles = set()
    unique_papers = []
    
    for paper in papers:
        title_lower = paper.get("title", "").lower()
        if title_lower not in seen_titles:
            seen_titles.add(title_lower)
            paper["tier"] = classify_paper(paper)
            unique_papers.append(paper)
    
    return unique_papers

def generate_markdown_report(papers, year, week, week_start, week_end):
    """生成 Markdown 格式的周报"""
    papers_by_tier = {}
    for paper in papers:
        tier = paper.get("tier", "Tier 3")
        if tier not in papers_by_tier:
            papers_by_tier[tier] = []
        papers_by_tier[tier].append(paper)
    
    md_content = f"""# 有机电极材料期刊文章周报

**第 {week} 周** | {week_start.strftime('%Y-%m-%d')} ~ {week_end.strftime('%Y-%m-%d')}

*本周收集论文总数: {len(papers)}*

---

## 梯队分布

| 梯队 | 数量 |
|------|------|
| Tier 1 | {len(papers_by_tier.get("Tier 1", []))} |
| Tier 2 | {len(papers_by_tier.get("Tier 2", []))} |
| Tier 3 | {len(papers_by_tier.get("Tier 3", []))} |

"""
    
    for tier in ["Tier 1", "Tier 2", "Tier 3"]:
        papers_in_tier = papers_by_tier.get(tier, [])
        if papers_in_tier:
            md_content += f"\n## {tier} ({len(papers_in_tier)})\n\n"
            for idx, paper in enumerate(papers_in_tier, 1):
                md_content += f"### {idx}. {paper.get('title', 'N/A')}\n\n"
                md_content += f"- **作者**: {paper.get('authors', 'N/A')}\n"
                md_content += f"- **期刊**: {paper.get('venue', 'N/A')}\n"
                md_content += f"- **发表日期**: {paper.get('publication_date', 'N/A')}\n"
                md_content += f"- **来源**: {paper.get('source', 'N/A')}\n"
                md_content += f"- **摘要**: {paper.get('abstract', 'N/A')}\n"
                md_content += f"- **链接**: [{paper.get('url', 'N/A')}]({paper.get('url', 'N/A')})\n\n"
    
    return md_content

def generate_json_report(papers, year, week, week_start, week_end):
    """生成 JSON 格式的数据"""
    json_data = {
        "week": week,
        "year": year,
        "week_start": week_start.isoformat(),
        "week_end": week_end.isoformat(),
        "total_papers": len(papers),
        "papers": papers,
    }
    return json_data

def main():
    """主程序"""
    print("开始收集有机电极材料论文...")
    
    year, week, week_start, week_end = get_week_info()
    print(f"当前周期: {year} 年第 {week} 周")
    
    all_papers = []
    for keyword in SEARCH_KEYWORDS:
        print(f"搜索关键词: {keyword}")
        papers_ss = search_semantic_scholar(keyword, limit=5)
        all_papers.extend(papers_ss)
        print(f"  - Semantic Scholar: {len(papers_ss)} 篇")
        
        papers_cr = search_crossref(keyword, limit=5)
        all_papers.extend(papers_cr)
        print(f"  - CrossRef: {len(papers_cr)} 篇")
    
    papers = deduplicate_papers(all_papers)
    print(f"\n去重后论文总数: {len(papers)}")
    
    output_dir = Path("weekly-reports")
    output_dir.mkdir(exist_ok=True)
    
    md_report = generate_markdown_report(papers, year, week, week_start, week_end)
    json_report = generate_json_report(papers, year, week, week_start, week_end)
    
    md_file = output_dir / f"{year}-week-{week:02d}.md"
    json_file = output_dir / f"{year}-week-{week:02d}.json"
    
    with open(md_file, "w", encoding="utf-8") as f:
        f.write(md_report)
    print(f"\n✓ Markdown 报告已保存: {md_file}")
    
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(json_report, f, ensure_ascii=False, indent=2)
    print(f"✓ JSON 报告已保存: {json_file}")
    
    print("\n论文收集完成！")

if __name__ == "__main__":
    main()