# Michael大麦哥 Combined Skill

一个面向 Codex 和其他支持 `SKILL.md` 的 Agent 的联合检索与蒸馏适配层。

它不重复爬取抖音，也不重新下载整套视频，而是复用已经公开存在的字幕、带时间点的字幕摘录和发布文案来源，把三者的检索入口统一起来。

## 包含什么

- 13 个跨视频能力框架：自我价值、接纳、低谷、认知、习惯、身体、关系、自由、时间、职业、意义、独立思考、创作
- 一个离线词面检索脚本
- 来源优先级与证据等级
- 覆盖边界、版权说明和可复现的来源清单
- 对缺失来源的安全降级：只使用本地实际存在的语料

## 不包含什么

本仓库**不打包**视频、音频、截图、完整 SRT 字幕或第三方知识库正文。

你需要自行确认并安装可选来源：

- [feiyuaq/michael-damaige-skill](https://github.com/feiyuaq/michael-damaige-skill)
- [qwer3021/douyin-Michael-DaMaiGe-skill](https://github.com/qwer3021/douyin-Michael-DaMaiGe-skill)
- [wangjs-jacky/michael-damaige-gallery](https://github.com/wangjs-jacky/michael-damaige-gallery)

三个来源的授权状态不同。安装公开仓库不等于获得重新发布其中内容的授权，请先阅读 [CONTENT_RIGHTS.md](CONTENT_RIGHTS.md)。

## 安装

```bash
git clone https://github.com/zhao007577/github-program.git \
  "${CODEX_HOME:-$HOME/.codex}/skills/michael-damaige-combined"
```

Windows PowerShell：

```powershell
git clone https://github.com/zhao007577/github-program.git "$HOME\.codex\skills\michael-damaige-combined"
```

开启新会话后即可使用 `$michael-damaige-combined`。

## 配置可选来源

默认会从 Codex 技能目录查找：

```text
<CODEX_HOME>/skills/feiyuaq-michael-damaige
<CODEX_HOME>/skills/qwer-michael-damaige
<CODEX_HOME>/skills/michael-damaige-gallery/public/catalog.json
```

也可以显式设置路径：

```text
MICHAEL_DAMAI_TRANSCRIPT_DIR
MICHAEL_DAMAI_METADATA_DIR
MICHAEL_DAMAI_GALLERY_CATALOG
```

没有安装某个来源时，脚本会跳过它，并在 `source_available` 中返回可用状态。

## 使用

检索低谷、内耗和自我接纳：

```bash
python scripts/search_all.py "低谷 放过自己" --limit 5
```

只查完整字幕：

```bash
python scripts/search_all.py "爱情 沟通" --source transcript --limit 5
```

查询工作与焦虑：

```bash
python scripts/search_all.py "工作 焦虑" --limit 5
```

脚本输出 UTF-8 JSON，不依赖第三方 Python 包，需要 Python 3.10+。

## 覆盖边界

目标抖音账号当前显示 209 个作品。三个来源合并后约有 135 个唯一长视频标题：

- 19 个有完整字幕
- 121 个有带时间点的字幕摘录
- 39 个有发布文案与元数据

这些来源彼此重叠，并不是 209 个作品的完整逐字档案。未登录的抖音页面也只会公开显示部分作品。因此本项目不会声称“所有视频已经完整蒸馏”。

详细记录见 [references/coverage.md](references/coverage.md) 和 [references/source-manifest.json](references/source-manifest.json)。

## 设计原则

- 先找现成实现，再补缺，不从零重复劳动
- 直接引文与自己的理解分开
- 时间戳、标题和来源必须可追溯
- 健康、心理、财务等观点必须作为个人观点呈现，除非另有独立证据
- 不把单个视频中的一句话夸大为人物整体立场

## 授权

本项目原创的代码、技能说明和蒸馏框架采用 [MIT License](LICENSE)。第三方视频、字幕、文案、图片、名称和商标不包含在该授权中，详见 [CONTENT_RIGHTS.md](CONTENT_RIGHTS.md)。

本项目不是 Michael大麦哥 的官方产品，也不代表其背书。
