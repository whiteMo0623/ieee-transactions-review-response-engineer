---
name: ieee-transactions-review-response-engineer
description: 以精简但严谨的方式处理 IEEE Transactions 论文的单条审稿意见：联合阅读 LaTeX、PDF、实现代码和既往意见，在一个 Markdown 中完成意见理解、相关论文/代码证据、回复思路、实验设计与实际结果映射；仅在需要时创建一个实验目录；基于真实结果直接写入用户指定的 response Word 文件，并在原位修改前创建一份相邻备份。用于论文返修、补充实验、代码—论文一致性核查、IEEE 图表与 Author Response 写作；默认只保留回复方案、实验代码/结果/图表和最终 Word 三类核心产物，每次只处理一条意见。
---

# IEEE Transactions Review Response Engineer

把一条审稿意见处理为充分、可复现且不繁琐的证据链。默认只保留三类核心产物：一个回复方案 Markdown、一个按需创建的实验目录，以及用户指定位置的 response Word；其余日志、渲染页、结构差异和临时脚本均放入临时目录并在成功后清理。

## 核心约束

- 每次只处理一条意见。
- 同时核对 LaTeX、最终 PDF 和实际实现代码，但只记录与当前意见直接相关的事实，不另建通用论文摘要或代码地图。
- 只复用条件完全匹配且来源可核验的既往证据；当前意见需要的新控制变量、基线、数据、指标或统计分析必须完整完成。
- 不缩减数据、epoch、模型规模、搜索空间、基线、重复次数或随机种子。
- 先得到真实结果，再写最终回复；不得虚构、挑选或夸大证据。
- 默认只修改 Word 中当前意见的 `Author Response`，保留 `Original Comment`、`Changes in Manuscript`、其他意见和格式。

## 最小案件结构

默认只创建：

```text
<comment-id>/
├── response-plan.md
└── experiment/                 # 仅当确实需要新增实验/分析时创建
    ├── run_*.py                # 或复用原项目的入口与配置
    ├── config.*                # 仅在原框架或复现需要时保留
    ├── results.json/csv        # 机器可读实际结果
    ├── table.*                 # 最终回复真正使用的表
    └── figure.pdf/png          # 最终回复真正使用的图
```

不要默认创建 `case.json`、`inputs/`、`notes/`、`response/`、`delivery/`、`qa/`、独立证据账本、独立 case summary、渲染页集合或预览 PDF。若用户明确要求其中某项，再创建。

运行 `scripts/init_review_case.py` 可生成仅含 `response-plan.md` 的案件骨架。初始化只记录路径和可用的 Git revision；不要对论文目录、整个代码树或既往案件目录做全量哈希。

```bash
python scripts/init_review_case.py R2-C4 --root response_exp --paper-tex path/to/main.tex --paper-pdf path/to/paper.pdf --code-root path/to/repo --comment-file path/to/comment.md --word-file path/to/response.docx --previous-cases path/to/response_exp
```

## 1. 在一个文件中完成理解与方案

完整读取论文与代码，但只把回答当前意见所需内容写入 `response-plan.md`：

- 原始意见；
- 核心疑虑、真实意图与证据门槛；
- 相关论文位置、代码文件/行号、配置和现有结果；
- 与既往意见的关联及逐项复用判定；
- 回复思路；
- 必要实验的目的、对比方法、变量、数据集、指标、训练配置、随机种子、预期结果和预先判定规则；
- 实际结果、来源文件/字段和结论边界；
- Word 写入位置、备份位置与完成状态。

不要把这些内容再拆成 `paper-understanding.md`、`code-paper-map.md`、`evidence-summary.md`、`evidence-ledger.json` 或 `case-summary.md`。详细实验规则见 [references/experiment-and-evidence-protocol.md](references/experiment-and-evidence-protocol.md)。

若当前意见不需要新增经验性证据，将 `experiment_required` 设为 `false` 并说明理由；不要为了流程完整而制造无关实验。若需要实验，将其设为 `true` 并创建 `experiment/`。

## 2. 只完成直接服务当前意见的实验

优先调用原项目的数据、模型、训练和评估入口。将本意见新增的运行代码、必要配置、机器可读结果以及最终回复真正使用的图/表放在 `experiment/`；允许按原项目需要建立少量子目录，但不要机械地分出 `raw/processed/logs/configs/src/figures` 六层结构。

正式命令、环境、数据版本、全部运行、种子和失败重跑记录写入 `response-plan.md` 或机器可读结果本身。运行日志默认写入临时目录；成功后删除，失败时仅保留定位问题所需日志。冒烟测试只验证接口，不作为证据。

只生成进入最终证据链的图表。图使用 Times New Roman，按最终栏宽保证可读，灰度可辨；多子图在下方标注 `(a)`、`(b)`、`(c)`；保留矢量版本与 Word 使用的高分辨率版本，不再复制到第二个 response 目录。

## 3. 将 Author Response 直接写入指定 Word

不要把最终 Word 复制到案件的 `delivery/`。使用用户指定的 response Word 路径作为最终文件：

1. 精确定位当前 `Original Comment` 对应的 `Author Response`；若不能唯一定位，停止并请求定位。
2. 在同一目录创建且只创建一份备份：`<word-stem>.before-<comment-id>.docx`。不得覆盖已有备份。
3. 在临时目录或同目录隐藏临时文件中完成局部编辑；验证成功后原子替换用户指定 Word。
4. 默认只修改目标 `Author Response`；结构比较必须确认其他正文、表格、关系和 `Changes in Manuscript` 未变化。
5. 渲染最终 Word 做视觉 QA。渲染 PNG/PDF、结构差异 JSON 和临时编辑脚本均为内部临时产物，成功后删除，不放入案件目录。

最终回复直接从核心结论切入，不写客套开场。用文字、`$...$` LaTeX 公式、紧凑表格和必要图片形成连续证据链；每个数值必须来自 `experiment/` 的实际结果，并在 `response-plan.md` 的实际结果区标明来源。完整写作与 Word 规则见 [references/response-and-artifact-protocol.md](references/response-and-artifact-protocol.md)。

## 4. 一次性验收

完成全部工作后只运行一次轻量审计：

```bash
python scripts/audit_review_case.py path/to/R2-C4
```

审计检查：单一方案文件已完成、实验需求已明确、必要实验代码与机器可读结果存在、案件目录无默认冗余产物、指定 Word 与相邻备份存在且不同。审计不替代对 Word 的结构比较和全页视觉检查。

通过后清理临时目录、渲染页、预览 PDF、`__pycache__` 和成功运行日志。最终向用户只报告核心方案文件、实验图表/结果、已更新的指定 Word 及备份位置。

## 资源

- `scripts/init_review_case.py`：创建单文件方案骨架，不扫描或复制大目录。
- `scripts/audit_review_case.py`：执行一次精简产物审计。
- `references/experiment-and-evidence-protocol.md`：完整实验与紧凑证据映射规则。
- `references/response-and-artifact-protocol.md`：Author Response、IEEE 图表和 Word 原位更新规则。
