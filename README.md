# 有机电极材料论文周报收集工具

📚 **自动收集和整理有机电极材料相关的学术论文**

## 📖 项目概述

这是一个基于GitHub Actions的自动化工具，每周一早上8:00（北京时间）自动从全球顶级期刊中搜索有机电极材料相关的最新论文，并整理成易读的周报Markdown文件。

## 🎯 研究方向

关键词搜索涵盖：
- conjugated coordination polymer battery
- CCP sodium-ion battery
- conjugated polymer sodium-ion
- carbonyl organic electrode sodium
- organic proton storage
- organic aqueous battery zinc
- covalent organic framework sodium-ion
- conjugated ladder polymer battery

## 📰 覆盖期刊

### Tier 1（顶级期刊）
Nature / Science / JACS / Angew. Chem. / Energy Environ. Sci. / Adv. Mater. / Adv. Energy Mater. / Chem. Rev. / Acc. Chem. Res. / Nat. Commun. / Sci. Adv.

### Tier 2（高水平期刊）
Adv. Funct. Mater. / ACS Nano / Nano Lett. / ACS Energy Lett. / Chem. Sci. / J. Mater. Chem. A / SmartMat / eScience / EnergyChem

### Tier 3（重要期刊）
ACS Appl. Mater. Interfaces / Chem. Eng. J. / Chem. Commun. / Small / Mater. Today 及其他

## 📂 项目结构

```
organic-battery-papers/
├── .github/workflows/
│   └── fetch-papers.yml          # GitHub Actions工作流
├── scripts/
│   ├── fetch_papers.py           # 主爬虫脚本
│   └── requirements.txt           # Python依赖
├── weekly-reports/
│   └── 2026-week-26.md           # 每周生成的论文列表
├── README.md
└── .gitignore
```

## 📅 运行频率

- **时间**：每周一早上 08:00
- **时区**：北京时间（UTC+8）
- **输出**：`weekly-reports/2026-week-XX.md`

## 📝 论文列表格式

每周生成的Markdown文件包含：
- 周期信息（第X周，日期范围）
- 按期刊梯队分组的论文列表
- 每篇论文显示：**标题 | 作者 | 发表日期 | 简述 | 梯队 | 链接**

## 🔧 技术栈

- **数据来源**：Semantic Scholar API
- **自动化**：GitHub Actions
- **语言**：Python 3.x
- **调度**：Cron表达式

## 📊 示例输出

查看 `weekly-reports/` 目录下的Markdown文件查看论文周报格式。

---

**最后更新**：2026-06-23
