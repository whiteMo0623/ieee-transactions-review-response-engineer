---
name: ieee-transactions-review-response-engineer
description: 以精简但严谨的方式处理 IEEE Transactions 论文的单条审稿意见：联合阅读 LaTeX、PDF、实现代码和完整 review_comments，先从全部意见中筛选与当前意见相关的条目，再按需核查已处理案件及可复用证据；在一个 Markdown 中完成意见理解、相关论文/代码证据、回复思路、实验设计与实际结果映射；仅在需要新增实验、分析或必要图表时创建一个实验目录；根据意见类型组织 Author Response：对明确要求新增实验、分析、证明或内容的意见，先说明已按建议完成的修改，再报告证据和基于结果的谨慎解释；对要求判断现有主张的意见，才在证据充分时使用结论优先；写入用户指定的 response Word 文件，并在原位修改前创建一份相邻备份。用于论文返修、补充实验、代码—论文一致性核查、IEEE 图表与 Author Response 写作；默认只保留回复方案、实验代码/结果/图表和最终 Word 三类核心产物，每次只处理一条意见。
---

# IEEE Transactions Review Response Engineer

把一条审稿意见处理为充分、可复现且不繁琐的证据链。默认只保留三类核心产物：一个回复方案 Markdown、一个按需创建的实验目录，以及用户指定位置的 response Word；其余日志、渲染页、结构差异和临时脚本均放入临时目录并在成功后清理。

## 核心约束

- 每次只处理一条意见。
- 先识别当前意见的主要任务：是明确要求新增或修正内容，还是要求判断现有主张；回复开场和证据—解释顺序随意见类型变化，不把“结论优先”作为所有意见的硬规则。
- 完整读取一次 `review_comments` 以了解所有审稿意见；只对其中与当前意见在疑虑、主张、方法模块或所需证据上相关的条目继续检查。
- 同时核对 LaTeX、最终 PDF 和实际实现代码，但只记录与当前意见直接相关的事实，不另建通用论文摘要或代码地图。
- 只复用条件完全匹配且来源可核验的既往证据；当前意见需要的新控制变量、基线、数据、指标或统计分析必须完整完成。
- 不得为节省成本擅自缩减已确定正式方案的数据、epoch 上限、模型规模、搜索空间、必要基线、重复次数或种子。预定的验证集早停不属于缩减预算；具体训练、随机种子和 GPU 使用遵循用户及项目约定。
- 先得到真实结果，再写最终回复；不得虚构、挑选或夸大证据。
- 将“核心疑虑、真实意图、证据门槛、实验筹备过程和复用判断”限制在内部 `response-plan.md`；回复只呈现与当前意见相关的修改内容、真实证据、基于结果的校准解释，以及仅在会改变当前结论解释时才需要的最短边界。正文修改的完成时态与实际落实状态按下述两阶段流程区分。
- 对审稿人明确要求新增实验、分析、证明、对比、统计或正文内容的意见，首句说明审稿人的建议/要求及具体增补；实验、分析和证明必须实际完成，正文编辑可按下述两阶段流程预写完成时态。`Following the reviewer’s suggestion, we added ...` 和 `In response to the reviewer’s request, we added ...` 不是空泛的过程性开场。
- 对经验性实验或分析，先报告新增内容、方法和实际结果，再说明结果支持的具体主张；除非存在形式证明或预先定义且满足的判定标准，默认不使用 `prove`、`confirm`、`establish`、`demonstrate` 或“决定性证据”等过强表述。
- 最终回复遵循“正向证据优先、最小必要边界”原则：围绕已经完成的修改、实际结果和结果支持的结论组织内容，不主动罗列未覆盖的布局、配置、设施、真实测量数据、不能替代的验证、未认证的能力或后续工作。除非审稿人直接询问适用范围、泛化性、样本独立性等问题，或不加限定会使当前结果明显被误读为更强主张，否则删除这类防御性免责声明；若确需避免误解，只保留一条与当前意见直接相关的最短事实限定，并放在证据之后。不要用“不能……”“不应被解释为……”“仍需……”“未来工作……”等句式作为惯常收尾，也不要主动引入论文并未声称的通用性主张。
- 回复等人类可读内容中的公式和数学符号统一使用 TeX 格式，即使最终写入 Word 也保留 TeX 表达：行内公式使用 `$...$`，独立公式使用单独成行的 `\[...\]`。对于行内“数学符号=普通数值”的表达，只将数学符号置于 `$...$` 中，等号和数值置于定界符外；例如应写作 `$\rho$=0.50`，不得写作 `$\rho=0.50$`。可直接输入的独立符号（例如 `℃`）直接使用 Unicode 符号，不写成 LaTeX 或英文名称；不得使用 `L2`、`degrees C` 等原生文本代替，应写成 `$L_2$`、`℃`，也不得用 Office Math 或其他 Word 原生公式格式替代 TeX 源码。
- 本次新增或修改的回复正文使用 Times New Roman 11 pt；图题和表题使用 Times New Roman 10 pt、居中、加粗；图题置于对应图的下方，表题置于对应表的上方；表格内文字使用 Times New Roman 10 pt；数据表格统一采用三线表，只保留顶线、表头分隔线和底线。保留模板的封面、Reviewer/Comment 标题层级和红/蓝/绿段落边框与底色；三段区域是段落样式，不适用数据表格的三线表规则。
- 最终 `Author Response` 默认使用连续段落，不插入 `1) ...`、`What is...`、`Additional experiment...` 等组织作者思考过程的小标题；只有用户明确要求或既有模板强制时例外。
- 其他审稿意见的编号、结论出处和处理过程只保留在内部方案中；最终回复不得要求当前审稿人阅读或关注其他审稿人的意见。
- 回复阶段默认只修改当前意见的 `Author Response`，保留 `Original Comment`、`Changes in Manuscript`、其他意见和格式；正文同步阶段再按用户要求更新当前意见的 `Changes in Manuscript` 及回复中受影响的定位和措辞。

## 固定模板与两阶段工作流

默认使用 [assets/response-template.docx](assets/response-template.docx) 的三段结构：`Original Comment` → `Author Response` → `Changes in Manuscript`。首次创建回复文件、扩展意见块或进入正文同步阶段时，读取 [references/template-and-revision-workflow.md](references/template-and-revision-workflow.md)。用户已提供 response Word 时直接编辑该文件，不用空白模板覆盖；需要新建时先复制模板到用户指定位置，再初始化案件。

1. **先完成回复**：逐条完成必要实验和分析并写入 `Author Response`。按最终提交口吻使用 `We have added/revised ...`，不使用“我们将/我们准备”。尚未落实的正文编辑只在 `response-plan.md` 记录具体内容、拟修改位置、与其他意见的重叠关系及状态；不虚构实验结果、正文摘录或未确定的页码/行号/图表编号。新文档的 `Changes in Manuscript` 保持标题和空白区域，已有内容则暂时保留。
2. **正文修改后同步**：用户要求统一修改正文或补充修改记录时，合并相关意见的重叠要求；依据实际修订稿填写 `Changes in Manuscript` 的位置、原文摘录和必要图表，并校正 `Author Response` 中受影响的陈述与定位。正文编辑权限及范围以用户本次任务为准；正文已由用户修改时直接核验后同步，不重复改写。

在现有方案中分别记录回复完成、正文落实和修改记录同步状态。回复阶段允许完成 Word 写入与 QA；只有正文和两段作者内容一致后才标记为可提交。通常仍逐条处理意见，仅在用户要求统一修改正文时合并涉及的相关案件，不自动扩展其他意见。

## 最小案件结构

默认只创建：

```text
<comment-id>/
├── response-plan.md
└── experiment/                 # 新增实验/分析或必要的复用图表需要时创建
    ├── run_*.py                # 或复用原项目的入口与配置
    ├── config.*                # 仅在原框架或复现需要时保留
    ├── results.json/csv        # 机器可读实际结果
    ├── table.*                 # 最终回复真正使用的表
    └── figure.pdf/png          # 最终回复真正使用的图
```

不要默认创建 `case.json`、`inputs/`、`notes/`、`response/`、`delivery/`、`qa/`、独立证据账本、独立 case summary、渲染页集合或预览 PDF。若用户明确要求其中某项，再创建。

运行 `scripts/init_review_case.py` 可生成仅含 `response-plan.md` 的案件骨架。先将 `SKILL_DIR` 设为本 Skill 的绝对目录，脚本按该目录定位，输入/输出相对路径仍以当前任务工作目录解析；使用 Python 3.9+，macOS 有 bundled Python 时优先使用。初始化只记录路径和可用的 Git revision；Git 不可用或尚无提交时记录 null，不扫描/哈希整个代码树来补偿。已有案件直接读取续作，或用 `python "$SKILL_DIR/scripts/init_review_case.py" R2-C4 --root response_exp --resume` 定位原方案；该命令不重写方案、Word 或备份。

```bash
python "$SKILL_DIR/scripts/init_review_case.py" R2-C4 --root response_exp --paper-tex path/to/main.tex --paper-pdf path/to/paper.pdf --code-root path/to/repo --review-comments path/to/review_comments.docx --comment-text "当前审稿意见原文" --word-file path/to/response.docx
```

## 1. 在一个文件中完成理解与方案

完整读取 `review_comments`；核对论文相关章节及上下文，并追踪当前意见涉及的数据、模型、训练和评估代码路径。发现依赖或一致性问题时再扩大范围，不要求通读整个代码仓库。先确认目标意见、输入路径与版本：缺失材料只阻塞依赖该材料的步骤；LaTeX 与 PDF 不一致时记录差异及各自版本，明确哪个版本用于事实核验、哪个用于修订定位，不能混用页码或编号。只把回答当前意见所需内容写入 `response-plan.md`：

先完整读取 `review_comments`，按意见编号筛选与当前意见可能相关的条目。对每个候选条目，先判断对应案件是否已经处理：未处理时只记录关联及其可能共享的证据需求；已处理时只打开该案件的 `response-plan.md`，并仅在准备复用时继续读取其中明确引用的结果、配置或代码文件。不得遍历全部既往案件，也不得为复用判定扫描整个代码树。

复用判断必须区分“复用实验事实”和“复制回复产物”。在 `response-plan.md` 中记录原始结果文件、条件匹配情况及采用方式（正文数值、紧凑表格、必要图片或修订稿引用）。最终 `Author Response` 不写其他 reviewer/comment 编号，不写 `as shown in the response to...`、`the results in R2C...` 等交叉引用，也不把复用来源伪装成当前意见新增的独立实验。

把 `response-plan.md` 视为内部工作文件。可以在其中充分分析审稿人的疑虑和证据缺口，但不得把“我们如何理解意见、如何设计流程、如何消除担忧”等元叙述直接搬入最终 `Author Response`。

- 原始意见；
- 意见类型与开场模式（是否明确要求新增/修正内容，以及对应的首句和证据—解释顺序）；
- 核心疑虑、真实意图与证据门槛；
- 相关论文位置、代码文件/行号、配置和现有结果；
- 与既往意见的关联及逐项复用判定；
- 回复思路；
- 必要实验的目的、对比方法、变量、数据集、指标、训练配置、随机种子、预期结果和预先判定规则；
- 实际结果、来源文件/字段、基于结果的校准解释句和结论边界；
- Word 写入位置、备份位置；回复状态、正文落实状态、修改记录同步状态，以及待落实的具体正文改动与重叠关系。

不要把这些内容再拆成 `paper-understanding.md`、`code-paper-map.md`、`evidence-summary.md`、`evidence-ledger.json` 或 `case-summary.md`。详细实验规则见 [references/experiment-and-evidence-protocol.md](references/experiment-and-evidence-protocol.md)。

`experiment_required` 表示是否需要新增经验性实验或分析：需要时设为 `true`，否则设为 `false` 并说明依据。直接复用既有结果、重绘相同数据而不作新分析可为 `false`，并允许在 `experiment/` 保存必要图表；新增统计量或新的分析则为 `true`。不要从目录是否非空推断实验需求。代码入口、结果路径及用户明确要求的产物例外记录在方案 frontmatter 的 `code_files`、`result_files`、`approved_artifacts` 中，格式与旧案件补填规则见实验协议。

## 2. 只完成直接服务当前意见的实验

优先调用原项目的数据、模型、训练和评估入口。将本意见新增的运行代码、必要配置、机器可读结果以及最终回复真正使用的图/表放在 `experiment/`；允许按原项目需要建立少量子目录，但不要机械地分出 `raw/processed/logs/configs/src/figures` 六层结构。

正式命令、环境、数据版本、全部运行、种子和失败重跑记录写入 `response-plan.md` 或机器可读结果本身。运行日志默认写入临时目录；成功后删除，失败时仅保留定位问题所需日志。冒烟测试只验证接口，不作为证据。

只生成进入最终证据链的图表。不得因为某项结果已经用于其他审稿意见，就自动把对应图表复制到当前回复。先判断图表对当前意见是否不可替代：辅助性证据只在正文中报告关键数值；修订稿已经包含且能够独立支撑当前结论时，优先引用修订稿中的图表；当当前意见明确要求该类可视化，或文字/数值及修订稿现有证据不足以完成论证时，才从原始实验产物重新嵌入自包含图表。不得从其他回复截图或复制带有其他意见编号的图表。图按最终栏宽生成并使用 Times New Roman；图题采用 Times New Roman 10 pt、居中加粗并置于图下方；灰度可辨；多子图在下方标注 `(a)`、`(b)`、`(c)`；保留矢量版本与 Word 使用的高分辨率版本，不再复制到第二个 response 目录。新增或复用的表格均采用三线表，表题采用 Times New Roman 10 pt、居中加粗并置于表上方，表内文字采用 Times New Roman 10 pt。

## 3. 将 Author Response 直接写入指定 Word

本节默认用于回复阶段；正文同步阶段按模板协议更新 `Changes in Manuscript`，复用同样的定位、备份、回读及视觉 QA 要求。模板的三个固定标签属于文档结构，不属于禁止的回复内部小标题。

不要把最终 Word 复制到案件的 `delivery/`。使用用户指定的 response Word 路径作为最终文件：

1. 精确定位当前 `Original Comment` 对应的 `Author Response`；若不能唯一定位，停止并请求定位。
2. 首次修改时在同一目录创建且只创建一份备份：`<word-stem>.before-<comment-id>.docx`。不得覆盖已有备份；同案件续作及正文同步时核验归属后续用。
3. 从当前 Word 在同目录隐藏 staging 文件中完成局部编辑。
4. 回复阶段默认只修改目标 `Author Response`；从 staging 回读本阶段目标块，核对其定位锚点、内容、表格、图片和样式。不要默认执行整篇 Word 的结构差异比较。
5. 在 macOS 上先调用工作区依赖加载工具 `load_workspace_dependencies`，使用其返回的 bundled Python 和文档处理依赖；用 bundled `render_docx.py` 渲染 staging Word，设置稳定且可写的 `TMPDIR`（优先 `/private/tmp`），并使用 `--emit_pdf` 生成临时 PDF 与 `page-<N>.png`。先用 `python-docx` 根据 Reviewer/Comment、原始意见和区域标签定位本阶段目标块，再用 `pdftotext`/`pdfinfo` 从渲染 PDF 确定实际页码，最后用 `view_image` 检查目标块覆盖的全部页面；仅在分页边界、局部版式异常或影响相邻内容时扩大检查。renderer 不支持页码筛选时允许全文渲染。不得写死意见编号或页码。渲染失败时记录原因并修正后重试；通过 QA、确认目标未被其他操作更新后原子替换指定 Word，再回读核验。成功后删除 staging、临时 PDF、PNG 和日志，不删除 bundled renderer。

最终 `Author Response` 不采用对所有意见一刀切的开场顺序，而是先根据意见类型组织信息：

- 对明确要求新增实验、分析、证明、对比、统计或正文内容的意见，采用“审稿人建议/要求 → 已完成的新增内容 → 必要的设置、方法或证明步骤 → 实际结果 → 基于结果的校准解释 → 论文修改位置与必要边界”。首句可写 `Following the reviewer’s suggestion, we added ...` 或 `In response to the reviewer’s request, we added ...`；这类句子说明已经完成的具体事实，不是应当删除的空泛过程性开场。不要在新增内容和实际结果之前先写“该分析证明了……”或“该分析提供了决定性证据”。
- 对事实更正或缺失内容，采用“直接指出更正/补充 → 支撑事实 → 论文中的实际修改”；若补充内容同时是审稿人明确要求的，优先使用上一条的审稿人建议锚定开场。
- 对要求判断现有主张是否成立、或要求澄清方法选择的意见，只有在答案可以被紧随其后的证据直接支撑时才使用结论优先；如果答案依赖新增分析，应先说明分析和结果，再给出解释。经验性结果默认使用 `supports`、`indicates` 或 `is consistent with` 等校准表达，不使用 `prove`、`confirm`、`establish`、`demonstrate` 或“决定性证据”等过强表述，除非存在形式证明或预先定义且满足的判定标准。
- 回复应在实际结果及其直接含义处收束，不默认添加“不能替代其他验证”“不应被解释为全面能力”“仍是重要的后续工作”等限制性尾句；只有当前意见直接涉及范围、泛化、独立性，或不加限定会造成明显误读时，才保留上一条所述的最短必要限定。

对实质性审稿意见，无论意见类型如何，第一句都应直接进入当前意见的事实，不以致谢、泛泛认同、担忧复述或没有具体修改内容的 `To address this concern...` 开场。疑虑分析和实验筹备留在 `response-plan.md`，不得泄漏成防守型回复。用连续段落组织论证，不用编号式或概念式小标题切分回复；涉及多项问题时按审稿意见的顺序自然过渡。公式和数学符号统一使用 TeX：行内使用 `$...$`，独立公式使用单独成行的 `\[...\]`；对于行内“数学符号=普通数值”的表达，只将数学符号置于 `$...$` 中，等号和数值写在定界符外，例如应写作 `$\rho$=0.50`，不得写作 `$\rho=0.50$`；可直接输入的符号如 `℃` 直接使用，禁止用 `L2`、`degrees C` 等原生文本代替 `$L_2$`、`℃`，也禁止用 Office Math 替代 TeX。每个经验性结果数值必须来自本案件或已核验的外部原始结果，并在 `response-plan.md` 标明来源文件/字段；论文中的维度、数据规模等事实按论文/代码来源核验，页码和编号按对应版本核验。无需复制外部结果来满足目录要求。JSON/CSV 等结果文件保持数值类型与可计算结构，TeX 规则仅用于人类可读的表达。交付前执行直接性、自然表达、自包含和图表必要性检查，完整规则见 [references/response-and-artifact-protocol.md](references/response-and-artifact-protocol.md)。

## 4. 集中验收

本阶段工作完成后，先清理本次 staging、渲染页、预览 PDF、`__pycache__` 和成功日志；失败定位所需日志按需暂存。然后集中执行轻量审计，失败时修复并重跑，不逐步反复审计：

```bash
python "$SKILL_DIR/scripts/audit_review_case.py" path/to/R2-C4
```

审计检查必需章节存在且非空、实验需求已明确、显式引用的代码/结果可访问、支持的结果文件有基本内容、默认冗余产物及用户要求的例外、指定 Word 与备份的基本包结构及文件差异。文件有差异只说明字节发生变化，不能证明目标回复已更新。审计不判断证据真实性、论证完整性、正文是否落实或可提交状态，也不替代目标块回读和视觉 QA；各阶段状态与核验结论写在方案中。

通过后报告核心方案文件、实际使用的实验图表/结果、指定 Word 及备份位置，并准确说明本次完成的是回复阶段还是正文同步阶段。

## 资源

- `assets/response-template.docx`：从用户指定 Word 提取的可复用三段空白模板，正文修改区初始留空。
- `references/template-and-revision-workflow.md`：模板样式、意见块定位、占位符使用和两阶段同步规则。
- `scripts/init_review_case.py`：创建单文件方案骨架，不扫描或复制大目录。
- `scripts/audit_review_case.py`：集中检查产物契约，修复问题后可重跑。
- `references/experiment-and-evidence-protocol.md`：完整实验与紧凑证据映射规则。
- `references/response-and-artifact-protocol.md`：Author Response、IEEE 图表和 Word 原位更新规则。
