## 有机电极材料期刊文章周报收集工具

📚 **Weekly Organic Battery Electrode Materials Paper Collection**

使用 **Semantic Scholar API** 和 **CrossRef API** 自动化收集有机电极材料领域的最新研究论文，按期刊梯队分类输出。

### 🎯 功能特性

✨ **核心功能**
- 基于Semantic Scholar和CrossRef API的双引擎搜索
- 自动论文去重与梯队分类
- 每周自动执行，生成周报
- Markdown和JSON两种格式输出
- 按梯队、发表日期排序

📰 **期刊梯队分类**

**Tier 1** (顶级期刊)
- Nature / Science 系列
- JACS / Angewandte Chemie / Chemical Communications
- Energy & Environmental Science
- Advanced Materials / Advanced Energy Materials
- Chemical Reviews / Accounts of Chemical Research
- Nature Communications / Science Advances

**Tier 2** (高水平期刊)
- Advanced Functional Materials / ACS Nano / Nano Letters
- ACS Energy Letters / Chemical Science
- Journal of Materials Chemistry A
- SmartMat / eScience / EnergyChem

**Tier 3** (其他期刊)
- ACS Applied Materials & Interfaces
- Chemical Engineering Journal / Small / Materials Today
- Journal of Power Sources / Electrochimica Acta

🔑 **监控关键词**
```
- conjugated coordination polymer battery
- CCP sodium-ion battery
- conjugated polymer sodium-ion
- carbonyl organic electrode sodium
- organic proton storage
- organic aqueous battery zinc
- covalent organic framework sodium-ion
- conjugated ladder polymer battery
```

### 📋 安装

```bash
# 克隆仓库
git clone https://github.com/YY-888-YY/organic-battery-papers.git
cd organic-battery-papers

# 安装依赖
pip install -r requirements.txt
```

### 🚀 使用方法

#### 单次运行

```bash
python paper_collector.py
```

输出文件自动保存到 `weekly-reports/` 目录：
- `2026-week-26.md` - Markdown格式周报
- `2026-week-26.json` - JSON格式数据

#### 输出示例

**Markdown格式** (`2026-week-26.md`)

```markdown
# 有机电极材料期刊文章周报

**第 26 周** | 2026-06-22 ~ 2026-06-28

*本周收集论文总数: 45*

---

## 梯队分布

| 梯队 | 数量 |
|------|------|
| Tier 1 | 12 |
| Tier 2 | 18 |
| Tier 3 | 15 |

## Tier 1 (12)

### 1. High-Performance Organic Cathode Materials with Conjugated Ladder Polymers

- **作者**: John Smith, Sarah Johnson, ...
- **期刊**: Nature Energy
- **发表日期**: 2026-06-25
- **梯队**: Tier 1
- **来源**: Semantic Scholar
- **摘要**: This study demonstrates a novel approach to designing organic cathode materials...
- **链接**: [https://doi.org/10.1038/s41560-026-xxxxx](https://doi.org/10.1038/s41560-026-xxxxx)

...
```

**JSON格式** (`2026-week-26.json`)

```json
{
  "week": 26,
  "year": 2026,
  "week_start": "2026-06-22T00:00:00",
  "week_end": "2026-06-28T00:00:00",
  "total_papers": 45,
  "papers": [
    {
      "title": "High-Performance Organic Cathode Materials...",
      "authors": "John Smith, Sarah Johnson, ...",
      "venue": "Nature Energy",
      "tier": "Tier 1",
      "year": 2026,
      "publication_date": "2026-06-25",
      "abstract": "This study demonstrates a novel approach...",
      "url": "https://doi.org/10.1038/s41560-026-xxxxx",
      "source": "Semantic Scholar"
    },
    ...
  ]
}
```

### ⏰ 定期运行配置

#### GitHub Actions 自动化（推荐）

工作流已配置在 `.github/workflows/collect-papers.yml`

**运行时间**：每周一 8:00（北京时间 UTC+8）

工作流会自动：
1. 运行论文收集脚本
2. 生成周报文件
3. 提交并推送到仓库

手动触发：在GitHub仓库Actions标签页点击 "Run workflow"

#### Linux/macOS - Cron 任务

```bash
# 编辑 crontab
crontab -e

# 添加以下行（每周一 8:00 UTC+8 = 00:00 UTC）
0 0 * * 1 cd /path/to/organic-battery-papers && python paper_collector.py >> logs/collection.log 2>&1
```

#### Windows - Task Scheduler

1. 打开 Task Scheduler
2. 创建基本任务
   - 名称：Weekly Paper Collection
   - 触发器：每周一 08:00
   - 操作：启动程序 `python.exe`
   - 参数：`C:\path\to\paper_collector.py`
   - 工作目录：`C:\path\to\organic-battery-papers`

### 🔧 自定义配置

编辑 `paper_collector.py` 可修改：

**添加/修改搜索关键词**
```python
SEARCH_KEYWORDS = [
    "你的关键词1",
    "你的关键词2",
    ...
]
```

**调整期刊分类**
```python
JOURNAL_TIERS = {
    "Tier 1": [
        "期刊名1", "期刊名2", ...
    ],
    ...
}
```

### 📊 API 信息

#### Semantic Scholar API
- 无需密钥
- 免费使用
- 文档：https://api.semanticscholar.org
- 每秒请求限制：约100请求/秒

#### CrossRef API
- 无需密钥
- 免费使用
- 文档：https://github.com/CrossRef/rest-api-doc
- 推荐添加邮箱以获得更好的服务

### 📁 项目结构

```
organic-battery-papers/
├── README.md                           # 项目说明
├── requirements.txt                    # Python依赖
├── paper_collector.py                  # 主程序
├── .github/
│   └── workflows/
│       └── collect-papers.yml          # GitHub Actions工作流
└── weekly-reports/                     # 输出报告目录
    ├── 2026-week-25.md
    ├── 2026-week-25.json
    ├── 2026-week-26.md
    └── 2026-week-26.json
```

### ❓ 常见问题

**Q: 如何增加搜索的论文数量？**
A: 修改 `paper_collector.py` 中 `search_semantic_scholar()` 和 `search_crossref()` 函数的 `limit` 参数。

**Q: 能否集成其他数据源（如PubMed、arXiv）？**
A: 可以，修改 `collect_papers()` 方法添加新的搜索函数即可。

**Q: 如何只搜索特定时间段的论文？**
A: CrossRef API支持日期过滤，可在 `params` 中添加 `from-pub-date` 和 `until-pub-date`。

**Q: JSON格式中没有某些字段怎么办？**
A: 不同的期刊/API返回的字段不同，已在代码中处理并设为 'N/A'。

**Q: 如何本地测试GitHub Actions工作流？**
A: 安装 `act` 工具：`https://github.com/nektos/act`，然后运行 `act`。

### 🤝 贡献

欢迎提交Issue和Pull Request！

### 📄 许可证

MIT License

---

**最后更新**: 2026-06-23
**维护者**: @YY-888-YY
