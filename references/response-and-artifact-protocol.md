# 回复、图表与 Word 原位更新协议

## 1. 按意见类型组织的 Author Response

严格分离内部推理和外部回复。`response-plan.md` 可以记录审稿人的核心疑虑、真实意图、证据门槛、候选解释、实验筹备和复用判断；最终 `Author Response` 不复述这些分析，只呈现审稿人作出判断所需的实际修改、证据、基于结果的解释和必要边界。

先判断当前意见的主要任务。类型可以组合，但首句和信息顺序应由最需要回应的任务决定：

- **明确增补（`explicit_addition`）**：审稿人明确要求新增实验、分析、证明、对比、统计或正文内容。采用“审稿人建议/要求 → 已完成的具体增补 → 必要的设置、方法或证明步骤 → 实际结果 → 基于结果的校准解释 → 论文修改位置与必要边界”。首句可写 `Following the reviewer’s suggestion, we added ...` 或 `In response to the reviewer’s request, we added ...`；这类句子说明已经完成的具体事实，不是应当删除的空泛过程性开场。
- **事实更正或缺失内容（`fact_correction_or_missing_content`）**：采用“直接指出更正/补充 → 支撑事实 → 论文中的实际修改”。如果补充内容同时是审稿人明确要求的，优先使用上一条的审稿人建议锚定开场。
- **主张判断或方法澄清（`claim_assessment_or_clarification`）**：可以在证据充分且能被紧随其后的证据直接支撑时给出校准后的直接回答；如果回答依赖新增分析，应先说明分析和结果，再给出解释，不强行结论先行。

不得默认使用以下防守型、泛泛认同或没有具体事实的过程型开场：

- `We thank the reviewer...`
- `We agree/acknowledge that...`
- `To address this concern...`
- `We would like to clarify...`
- `It is worth noting that...`
- `While we recognize..., we believe...`

对于非明确增补型意见，将这类句子替换为具体事实句。对于明确增补型意见，不要把审稿人建议视为必须删除的过程信息；优先写 `Following the reviewer’s suggestion, we added ...`，随后报告设置和实际结果。不要以 `The rank analysis proves that ...`、`The new experiment provides decisive evidence ...` 等未经结果支撑的定性句开场。只有确实需要承认事实错误或撤回主张时，才直接写明错误与修正，不用铺垫性自我辩护。

对于明确增补型意见，首段优先在两到四句内完成“已完成的增补 + 必要设置 + 实际结果”；对于主张判断型意见，才可在两到四句内完成“校准后的回答 + 最强证据”。实验设置只保留解释结果所必需的变量；完整训练细节留在方案文件、表注或论文修改中。避免多层 `although/while/however/nevertheless` 转折，不为每个结论机械添加限定语。若结果不支持原主张，直接陈述结果并收缩或撤回表述。

默认把整条 `Author Response` 写成一组连续段落，不用编号式或概念式小标题组织作者的分析过程。不得插入 `1) What is...`、`2) Additional experiment...`、`Scope of the evidence` 或同类标题。审稿意见包含多个问题时，按原意见顺序逐项回答，并用事实句自然过渡；表题和图注不属于此处所说的小标题。只有用户明确要求分项、期刊模板强制分项或不分项会造成指代歧义时才使用简短标签。

优先使用普通研究者会自然说出的具体句子。明确增补型意见先陈述“审稿人要求什么、我们新增了什么”，再报告结果并解释含义；其他意见先陈述更正或结果，再解释含义。例如：

- 不写 `These measurements confirm that, for the claim at issue, the original values were incomplete; at the same time, the new tests provide the previously missing evidence at both output boundaries.`
- 写 `The original approximately 1 ms timing omitted required online steps. With all steps included, the coefficient path has a worst p99 of 2.071 ms and the full-field path has a worst p99 of 22.576 ms.`
- 不写 `The rank analysis proves that the claim is correct.`
- 写 `Following the reviewer’s suggestion, we added a rank analysis of the learned predictors. The analysis yielded ... These results support the revised claim under ... .`
- 不写 `The evidence nevertheless has a clearly defined scope`、`the conclusion is supported only insofar as...` 或连续多句解释作者为何有资格保留某项主张。
- 写清“原表漏了什么、完整计时是多少、两种输出边界有什么区别”，然后只保留一句真正必要的适用范围。

经验性实验或分析之后的解释必须校准证据强度。默认使用 `supports`、`indicates` 或 `is consistent with`；只有形式证明或预先定义且满足的判定标准，才使用 `proves`、`establishes`、`confirms`、`demonstrates` 或“决定性证据”。作者应说明证据支持和不支持的范围，而不是在证据出现前替审稿人宣布其是否足以证明主张。

一个段落只承担一个主要任务：界定事实、说明实验、报告结果、解释含义或给出边界。若一句话包含多层分号、三个以上转折或需要读者回看才能找到主语，拆成两到三句。报告完关键数字后，直接用一句话说明它们意味着什么；不要在后续段落用不同措辞重复同一结论。

Markdown 草稿不是默认交付物。可在内存或临时文件中组织回复，最终直接写入用户指定 Word；需要保留的来源映射放入 `response-plan.md`。

写入 Word 前执行一次直接性检查：

- 第一有效句是否直接进入当前意见的事实：明确增补型意见是否点明审稿人建议和具体新增内容，其他意见是否给出可由后文证据支撑的事实或校准回答；
- 删除开场句是否不损失任何事实；若是，删除该句；
- 是否按照意见类型组织顺序：明确增补型意见先写增补和结果，再写解释；必要边界是否放在证据和修改之后；
- 是否存在没有实际作用的致谢、认同、担忧复述或自我辩护；
- 每个比较级、因果词、显著性词、范围词和数值是否可绑定实际证据；
- 是否只保留会改变审稿人判断的信息。
- 是否存在可以用更短、更具体的事实句表达的抽象措辞；
- 是否出现为组织作者思考过程而设置的小标题；
- 是否在不同段落重复同一个限定或结论。
- 是否在实验、分析或证明的实际内容之前使用 `prove`、`confirm`、`establish`、`demonstrate` 或“决定性证据”等未经支撑的强结论；

## 2. 关联意见、复用证据与自包含

完整审稿意见用于发现相关证据，不用于在最终回复中建立审稿人之间的阅读关系。其他意见的编号、审稿人身份、处理顺序和“此前已经回答”的事实只写入 `response-plan.md`。最终 `Author Response` 不得出现：

- `R1C7`、`R2C6`、`Reviewer 2` 等其他意见标识；
- `as shown/discussed in our response to...`；
- `the feature-importance results in R2C... lead to the same conclusion`；
- 要求当前审稿人前往另一条回复查看实验、图表或结论的表达。

条件完全匹配的既往实验结果可以复用，但必须在当前回复中提供理解该证据所需的最小完整信息：测试对象、关键变量、评价指标、决定性数值和直接结论。不要重复实验筹备过程，也不要宣称该实验是专门为当前意见新增的，除非事实确实如此。

复用图表时执行以下判定：

1. **默认不复制**：图表只起辅助作用时，在正文中报告最关键的数值和结论。
2. **优先使用修订稿**：修订稿已经包含同一图表且读者无需查看其他审稿回复即可理解时，引用修订稿中的图号或表号。
3. **必要时自包含嵌入**：当前意见明确要求可靠性图、阈值曲线、敏感性图等可视化，且文字或修订稿中的证据不足时，从原始实验产物重新嵌入；不得从另一条回复截图。
4. **保持来源透明**：在 `response-plan.md` 中记录原始结果与复用关系；若嵌入当前回复，使用当前意见的图表编号和能够独立理解的图注，不保留其他意见编号，也不把同一运行描述成新的独立实验。
5. **控制重复长度**：同一图表已经在回复信其他位置完整出现时，只有其对当前意见不可替代才再次嵌入；否则改用一段数值摘要或修订稿引用。

公式和数学符号在逻辑草稿、实验结果、表格、图注以及最终 Word 中统一采用 TeX 格式；写入 Word 时也保留 TeX 源码和公式分隔符，不得改写成 Office Math、Word 原生公式或其他原生文本表达。

- **行内公式**：使用 `$...$`，例如 `$L_2$`、`$p<0.05$`。
- **独立公式**：使用单独成行的 `\[...\]`，不要使用 `$$...$$` 或 `\(...\)` 代替。
- **可直接输入的符号**：对于可以直接输入的独立 Unicode 符号，直接使用符号本身，例如 `℃`；不要写成 `$℃$`、`\\degree C` 或 `degrees C`。
- **禁止原生文本代替数学表达**：`L2`、`degrees C` 等写法不合规，应分别写成 `$L_2$`、`℃`。同一符号在正文、表格、图和论文中保持含义、大小写、上下标及字体语义一致；新符号首次出现时应在正文中定义。

公式写入 Word 后，回读时检查 `$...$` 与 `\[...\]` 是否保留、是否正确区分行内和独立公式，以及是否存在 `L2`、`degrees C` 等原生文本替代。

表格只保留当前论证需要的列，明确单位、方向、均值/离散度、种子数和最佳值规则。小数位与测量精度一致；表格由实验结果直接生成或逐项核验。

图按最终单栏或双栏尺寸生成，使用 Times New Roman；在最终尺寸下保证轴、刻度、图例和标注可读；颜色不是唯一编码。多子图在下方居中放置 `(a)`、`(b)`、`(c)`。只保留进入回复的矢量版本和 Word 使用的高分辨率版本。

## 4. 指定 Word 的唯一备份与原位写入

把用户指定的 response Word 视为最终文件，不在案件目录创建 delivery 副本。

在修改前创建相邻备份：`<word-stem>.before-<comment-id>.docx`。如果该备份已存在，停止并核实，不得覆盖。备份用于失败恢复；不要仅为常规验收对整份文档执行结构差异比较。

采用安全原位流程：

1. 从当前 Word 创建临时 staging 文件；
2. 通过原始意见精确文本、稳定编号或唯一书签定位目标块；
3. 只修改目标 `Author Response`；
4. 从 staging 回读目标块，核对目标块的定位锚点、内容、表格、图片和样式；
5. 使用 Microsoft Word 的只读导出能力生成临时 QA PDF，只渲染目标块实际占用的页面并完成视觉检查；必要时扩大到前后相邻页；
6. 全部通过后用原子替换写回用户指定路径；
7. 删除 staging、渲染页和临时 PDF。

保留 `Original Comment`、`Changes in Manuscript`、其他意见、标题层级、段落/字符样式、编号、节属性、页眉页脚、脚注尾注、超链接、批注和修订标记。目标无法唯一定位时不得写入。

插入表格时继承模板样式并防止溢出；插入图片时直接使用 `experiment/` 中的最终图片，嵌入媒体、锁定宽高比并按栏宽设置，不复制到其他目录。

## 5. 面向修改区域的局部 QA

在 Windows 且本机安装 Microsoft Word 时，必须使用 Microsoft Word 自身的排版引擎生成 QA PDF：创建独立的隐藏 Word COM 实例，以 `ReadOnly=True`、`AddToRecentFiles=False` 打开最终 Word，调用 `ExportAsFixedFormat` 导出到临时目录，随后以 `wdDoNotSaveChanges` 关闭文档并退出本次创建的 Word 实例。不得保存文档，不得附着、复用或关闭用户已经打开的 Word 实例。

不得默认使用 LibreOffice，也不得在 Microsoft Word 导出失败后静默回退。若本机 Microsoft Word 不存在或 COM 导出无法使用，停止 QA，向用户说明原因；只有获得用户明确同意后，才可使用 LibreOffice。使用 LibreOffice 时必须明确记录该 QA 仅为近似检查，其分页、字体、表格和图片布局不能代表 Microsoft Word 的最终效果。

完成后定位目标 `Author Response` 在最终 Word 中实际占用的页面，只渲染这些页面并检查布局。若目标块跨页，检查其覆盖的全部页面；若目标块紧邻分页边界、局部渲染显示溢出/错位/异常分页，或修改明显挤压相邻内容，再增加前一页或后一页。修正后只重新渲染受影响页面，不做默认全文渲染。

渲染 PNG/PDF 和自动化检查日志均写入系统或项目临时目录。成功后删除；只有失败且用户需要排查时才报告临时位置，不把它们纳入案件产物。不要默认生成全文像素差分或结构差异 JSON。

从最终 Word 重新读取目标 `Author Response`，核对正文、表格和图中的数字、符号、随机种子数及统计描述；同时确认用于定位该块的前后锚点仍存在且顺序正确。局部回读与目标页渲染通过后即可交付；只有出现定位异常、分页连锁变化或文件损坏迹象时，才扩大检查范围。

交付前对目标块执行一次自包含检查：搜索其他 reviewer/comment 编号和 `response to`、`as shown in`、`as discussed in` 等交叉回复措辞；确认回复不依赖其他审稿意见才能理解。再执行一次图表必要性检查：每张图表是否直接回答当前意见，是否可以由更短的数值摘要或修订稿引用替代，以及是否错误保留了其他意见的编号或图注。
