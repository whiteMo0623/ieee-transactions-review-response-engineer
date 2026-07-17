# 回复、图表与 Word 原位更新协议

## 1. 结果优先的 Author Response

严格分离内部推理和外部回复。`response-plan.md` 可以记录审稿人的核心疑虑、真实意图、证据门槛、候选解释、实验筹备和复用判断；最终 `Author Response` 不复述这些分析，只呈现审稿人作出判断所需的结论和证据。

先判断当前意见属于经验性质疑、事实澄清、方法选择、错误修正或缺失内容，再按以下顺序写作：

1. **直接结论**：第一句明确回答“是否成立、结果是什么、采用了什么修正”，并能脱离上下文独立成立；
2. **决定性证据**：紧接最能回答意见的实际数值、比较、公式、表格或图片；
3. **实际修改**：说明论文中新增、修正或收缩了什么；
4. **必要边界**：只有边界会实质改变结论适用范围时才保留，放在证据和修改之后，通常只用一句话。

不得默认使用以下防守型或过程型开场：

- `We thank the reviewer...`
- `We agree/acknowledge that...`
- `To address this concern...`
- `We would like to clarify...`
- `It is worth noting that...`
- `While we recognize..., we believe...`

将这类句子替换为事实句。例如，不写 “To address this concern, we conducted an additional experiment”，直接写 “The additional experiment shows that ...”。只有确实需要承认事实错误或撤回主张时，才直接写明错误与修正，不用铺垫性自我辩护。

首段优先在两到四句内完成“结论 + 最强证据”。实验设置只保留解释结果所必需的变量；完整训练细节留在方案文件、表注或论文修改中。避免多层 `although/while/however/nevertheless` 转折，不为每个结论机械添加限定语。若结果不支持原主张，直接陈述结果并收缩或撤回表述。

默认把整条 `Author Response` 写成一组连续段落，不用编号式或概念式小标题组织作者的分析过程。不得插入 `1) What is...`、`2) Additional experiment...`、`Scope of the evidence` 或同类标题。审稿意见包含多个问题时，按原意见顺序逐项回答，并用事实句自然过渡；表题和图注不属于此处所说的小标题。只有用户明确要求分项、期刊模板强制分项或不分项会造成指代歧义时才使用简短标签。

优先使用普通研究者会自然说出的具体句子。先陈述遗漏、修正或结果，再解释含义。例如：

- 不写 `These measurements confirm that, for the claim at issue, the original values were incomplete; at the same time, the new tests provide the previously missing evidence at both output boundaries.`
- 写 `The original approximately 1 ms timing omitted required online steps. With all steps included, the coefficient path has a worst p99 of 2.071 ms and the full-field path has a worst p99 of 22.576 ms.`
- 不写 `The evidence nevertheless has a clearly defined scope`、`the conclusion is supported only insofar as...` 或连续多句解释作者为何有资格保留某项主张。
- 写清“原表漏了什么、完整计时是多少、两种输出边界有什么区别”，然后只保留一句真正必要的适用范围。

一个段落只承担一个主要任务：界定事实、说明实验、报告结果、解释含义或给出边界。若一句话包含多层分号、三个以上转折或需要读者回看才能找到主语，拆成两到三句。报告完关键数字后，直接用一句话说明它们意味着什么；不要在后续段落用不同措辞重复同一结论。

Markdown 草稿不是默认交付物。可在内存或临时文件中组织回复，最终直接写入用户指定 Word；需要保留的来源映射放入 `response-plan.md`。

写入 Word 前执行一次直接性检查：

- 第一有效句是否已经回答当前意见，而不是描述作者态度或处理过程；
- 删除开场句是否不损失任何事实；若是，删除该句；
- 是否先给结论和证据，再给限制条件；
- 是否存在没有实际作用的致谢、认同、担忧复述或自我辩护；
- 每个比较级、因果词、显著性词、范围词和数值是否可绑定实际证据；
- 是否只保留会改变审稿人判断的信息。
- 是否存在可以用更短、更具体的事实句表达的抽象措辞；
- 是否出现为组织作者思考过程而设置的小标题；
- 是否在不同段落重复同一个限定或结论。

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

## 3. 公式、表格与图片

逻辑草稿中的符号和公式使用 `$...$`；写入 Word 时使用模板支持的 Office Math 或清晰的原生文本表达。符号定义与论文保持一致。

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
