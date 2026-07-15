---
name: ieee-transactions-review-response-engineer
description: 系统处理 IEEE Transactions 论文的单条审稿意见：联合研读 LaTeX、论文 PDF、实现代码、既往回复与 Word response 模板，判断审稿人真实疑虑，设计并完整运行不可缩水的补充实验，整理可追溯证据，撰写 Author Response，并在保持 Original Comment、Changes in Manuscript 及原格式不变的前提下回填 .docx。用于论文返修、审稿回复、补充实验、代码—论文一致性核查、IEEE 风格图表生成及 response Word 模板编辑；原则上每次只处理一条意见。
---

# IEEE Transactions Review Response Engineer

把一条审稿意见处理为可复现的实验案件和可直接提交的 `Author Response`。以原始材料、真实运行结果和逐项可追溯证据为唯一依据；不得虚构数值、缩减实验或用措辞回避缺失证据。

## 执行原则

- 每个案件只处理一条审稿意见。若用户一次提供多条，先明确当前意见并仅推进该条；不得将多条意见合并回答。
- 同时阅读 LaTeX 与 PDF：以前者核对正文、公式、引用和源数据，以后者检查最终排版、图表、公式显示及上下文。两者不可互相替代。
- 阅读实现代码和实际配置，建立论文叙述、代码入口、数据流、模型组件、损失、训练、评估与输出之间的对应关系。
- 只复用经核验且与当前意见完全匹配的既有证据。凡变量、数据集、指标、种子、实现版本或问题指向不同，均重新分析或实验。
- 完整运行审稿意见所需实验。不得缩减数据、epoch、模型规模、超参数搜索空间、基线、重复次数或随机种子来节省时间。
- 先取得真实结果，再写最终回复。实验未完成、运行失败或必要输入缺失时，明确报告阻塞与现有证据，不得生成貌似完成的结论。
- 将每个结论绑定到原始结果、处理脚本、配置、日志、图表或论文位置；区分事实、推导、解释和预期。

## 0. 建立独立案件

收集并确认以下输入：LaTeX 主文件及依赖、最终 PDF、代码仓库、当前一条原始意见、既往已处理意见的案件目录，以及用户提供的 response Word 模板。缺少会改变实验或回复结论的关键输入时，停止相应阶段并向用户索取；继续完成不依赖该输入的只读理解工作。

运行 `scripts/init_review_case.py` 创建独立案件目录并记录输入路径、文件哈希及代码 Git 状态。不要把实验代码或结果散落到原项目根目录。案件命名使用稳定的意见编号，如 `reviewer-2-comment-3`。

```bash
python scripts/init_review_case.py reviewer-2-comment-3 --root review_response_cases --paper-tex path/to/main.tex --paper-pdf path/to/paper.pdf --code-root path/to/repo --comment-file path/to/comment.md --word-template path/to/response.docx --previous-cases path/to/prior_cases
```

省略不存在的可选 `--word-template` 或 `--previous-cases`，不要省略论文、代码和当前意见。初始化后将 `case.json` 的 `experiment_required` 明确设为 `true` 或 `false`；只有当前疑虑不需要新增经验性证据时才可设为 `false`，并在方案中给出可审计理由。

在处理 PDF 时调用可用的 PDF 能力并渲染关键页核验；处理 `.docx` 时调用可用的文档能力并执行渲染验证。若相应能力不可用，使用可靠的本地库完成同等检查，但仍须保留可验证产物。

## 1. 构建论文与代码事实底座

在 `notes/paper-understanding.md` 记录研究动机、任务定义、方法、创新点、数据集、划分、基线、训练设置、指标、主结果、消融、结论及适用边界，并为每项事实标注 LaTeX 文件/行号或 PDF 页码。

在 `notes/code-paper-map.md` 记录：

- 数据读取、预处理、划分和防泄漏逻辑；
- 模型模块、张量流、损失函数和论文公式的对应关系；
- 训练入口、配置继承、优化器、调度器、停止条件、checkpoint 与随机性控制；
- 评估入口、指标实现、聚合方式、统计检验及图表生成；
- 论文与代码之间的任何偏差、未实现声明或隐式默认值。

实际打开关键源码、配置和脚本，不得仅依据文件名、README 或论文描述推测实现。

## 2. 解剖当前意见

逐句区分显式问题、隐含质疑、证据门槛和期望动作。判断意见主要针对正确性、公平性、鲁棒性、泛化性、统计显著性、复杂度、可复现性、表述清晰度还是结论边界。

形成“主张—疑虑—所需证据”链：审稿人质疑哪一项主张、现有证据为何不足、什么结果能够支持或推翻该主张。不要预设作者必然正确；实验必须允许出现不利结果，并预先给出相应结论收缩规则。

## 3. 核查与既往意见的关系

检查既往案件的原始意见、实验 manifest、代码版本、配置、日志和结果。对拟复用内容建立复用判定表，至少核对研究问题、数据、划分、模型版本、训练预算、对比方法、指标、种子、统计方法和代码提交。

仅在这些条件足以回答当前疑虑时复用；记录来源案件和文件路径。若当前意见要求额外控制变量、基线、数据集、指标、分析粒度或统计证据，完整补做，不得以“此前已有相近实验”为由省略。

## 4. 先交付分析与实验方案

在 `analysis-and-experiment-plan.md` 写入：对意见的理解、现有证据与缺口、处理方案、复用判定、必要实验和结论判定规则。每个实验必须直接服务当前意见，并完整给出：

- 实验目的与可检验假设；
- 对比方法、控制组和公平性约束；
- 自变量、控制变量及其取值；
- 数据集、版本、划分和预处理；
- 评价指标、聚合方式、置信区间或统计检验；
- 完整训练配置、硬件/软件环境、checkpoint 选择规则；
- 预先确定且完整执行的随机种子；
- 预期观察模式，以及支持、否定或限制结论的判定方式；
- 计划生成的表格、图片和其对应论证位置。

实验应充分但不冗余。用“若删除该实验，哪一项疑虑将失去证据？”检验必要性。详细规范见 [references/experiment-and-evidence-protocol.md](references/experiment-and-evidence-protocol.md)，开始设计前必须完整读取。

## 5. 实现并完整执行实验

将新增实现置于案件的 `experiments/src/`，配置置于 `experiments/configs/`，命令和 stdout/stderr 置于 `experiments/logs/`，不可变原始输出置于 `experiments/raw/`，处理结果置于 `experiments/processed/`，最终图置于 `experiments/figures/`。尽量导入或调用原项目的数据、模型、训练和评估框架，不复制会与原实现漂移的核心逻辑。

在 `experiments/manifest.json` 为每个运行记录代码版本、命令、配置、数据版本、种子、开始/结束时间、退出码、checkpoint、原始输出和状态。先运行严格的接口/单元检查，再执行方案规定的全部正式运行；小规模冒烟测试仅用于发现错误，不能成为正式证据。

保持控制变量和计算预算公平。运行中若发现设计错误，修正方案、保留失败日志并从受影响阶段重新执行。不得静默修改指标、过滤异常点、挑选种子或只报告有利结果。

需要远程计算时，只在用户授权的目标环境执行，并同步代码、配置和结果清单；不要因耗时长而自行削减实验。持续监控到全部正式运行完成，或明确呈报无法自行解除的阻塞。

## 6. 整理结果与绘图

从 `raw/` 通过版本化脚本生成 `processed/` 中的汇总表，保留逐种子结果。采用与实验设计一致的统计单位，报告样本量、中心趋势、离散度/置信区间及预先指定的检验；不得把多个重复运行误当成独立测试样本。

绘图遵循 IEEE Transactions 风格：使用 Times New Roman；按最终栏宽设计尺寸；确保缩放后的轴标题、刻度、图例和标注仍清晰；优先使用颜色盲友好且灰度可辨的线型/标记；避免装饰性元素。多子图在每个子图下方标注 `(a)`、`(b)`、`(c)`。同时保存矢量格式（优先 PDF/EPS）和高分辨率预览，并检查字体嵌入、裁切、重叠和数值一致性。完整规范见 [references/response-and-artifact-protocol.md](references/response-and-artifact-protocol.md)。

## 7. 撰写 Author Response

先给核心结论，不写客套开场，不回避负面或混合结果。将文字、`$...$` 形式的 LaTeX 公式、紧凑表格和必要图片编成连续证据链，依次说明做了什么、为何足以回答疑虑、实际观察、统计不确定性和结论如何维持或收缩。

所有数值必须从已完成实验的机器可读结果提取，并在 `response/evidence-ledger.json` 中绑定来源文件和字段。不要写“显著提升”“鲁棒”等超过指标或统计证据支持范围的表述。将正文修改位置和建议文本记录在 `response/manuscript-changes.md`，但除非用户明确要求，不替换模板中的 `Changes in Manuscript`。

将最终 Markdown 保存为 `response/author-response.md`。成文前完整读取 [references/response-and-artifact-protocol.md](references/response-and-artifact-protocol.md)。

## 8. 回填 Word 模板

默认只替换当前意见对应的 `Author Response` 内容，原样保留 `Original Comment`、`Changes in Manuscript`、其他意见、段落顺序、样式、编号、页眉页脚、批注和修订状态。先复制模板到案件的 `delivery/`，永不覆盖用户原件。

在目标区域无法唯一识别时停止编辑并请求用户定位；不得用模糊匹配写入可能错误的意见。插入公式、表格和图片时沿用模板风格，并保证图片引用被嵌入文档。完成后渲染全部页面，逐页对比模板，检查分页、字体、行距、表格边界、图片清晰度及非目标区域是否变化。

## 9. 验收与交付

运行 `scripts/audit_review_case.py --stage final <案件目录>`；提供 Word 模板时增加 `--require-docx`。修复所有错误后再交付。最终检查：

- 当前仅处理一条意见，且原始意见逐字可追溯；
- 论文理解和代码映射具有文件/页码/行号证据；
- 每个实验与一项疑虑直接相连且完整执行；
- 所有计划种子、基线、预算和数据均已完成；
- 表格、图片、正文数值与原始结果一致；
- 回复从核心结论切入并说明结论边界；
- Word 非目标区域未变化，渲染结果可读。

若审计未通过，继续修正或报告具体阻塞，不得宣称完成。

## 资源

- `scripts/init_review_case.py`：创建可追溯的单条意见案件目录与输入清单。
- `scripts/audit_review_case.py`：分阶段检查计划、实验结果和最终交付物的完整性。
- `references/experiment-and-evidence-protocol.md`：实验设计、执行、公平性、复用与证据追溯规范。
- `references/response-and-artifact-protocol.md`：回复写作、IEEE 图表和 Word 模板编辑规范。
