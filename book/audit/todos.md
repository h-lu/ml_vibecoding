### ML VibeCoding 书稿审核总计划（网络搜索 + Context7）

— 版本：2025-08 — 负责人：AI 助理（与作者协同）

---

## 1. 审核目标
- 明确每一小节是否严格基于第一性原理构建叙事与推导。
- 校验是否贯穿 Vibe Coding 原则（共情/故事、可玩性、心智模型、最小可行示例、视觉化）。
- 对齐 2024–2025 前沿与最佳实践（术语、API、论文/库、伦理与合规）。
- 输出每章成体系的审阅报告与可执行的修订任务清单。

## 2. 方法与工具
- 网络搜索（2025-08）
  - 验证事实与数据、SOTA 现状、术语标准、关键论文与行业动态。
  - 关注官方博客/白皮书、顶会论文、主流框架发布说明。
- Context7 MCP（官方文档检索）
  - 对齐库/框架/服务的当前版本 API、推荐实践、迁移指南与弃用项。
  - 典型目标：PyTorch/TF、scikit-learn、LangChain/LangGraph、FAISS/pgvector、OpenAI/Anthropic/阿里/Qwen 等。
- 本地静态检查
  - 资源可用性（`book/assets/chXX/` 引用）、外链有效性、代码块可读性与环境需求说明。
  - 术语一致性与跨章对齐（定义、符号、缩写）。

## 3. 评审量表（1–4 分）
- 第一性原理（FP）
  - 4：先定义后推导，边界条件清晰，反例与误区说明充分，可验证结论。
  - 3：总体自洽，关键假设与验证存在但略简。
  - 2：结论先行，论证链条不完整或跳步明显。
  - 1：比喻/口号大于推理，缺少可验证性。
- Vibe Coding 原则（VC）
  - 4：业务挑战牵引，最小可行示例可跑，心智模型与图示清晰，读者能“玩起来”。
  - 3：示例完整但互动性不足；心智模型或视觉化略弱。
  - 2：示例零散或可复现性差；缺乏“共情/故事”。
  - 1：讲概念不落地；无可玩性。
- 最佳实践（BP）
  - 4：内容与 2024–2025 一致；API/库/安全与合规/复现性俱佳并有参考链接。
  - 3：总体准确，少量时效或引用欠缺。
  - 2：存在过时描述或不推荐用法。
  - 1：明显错误或风险提示缺失。

## 4. 交付物
- 每章一份审阅报告：`book/audit/chXX.md`（固定结构，见附录模板）。
- 修订任务清单（按优先级 P0–P2），包含：问题、建议、影响范围、预估工时、负责人与截止时间。
- 变更记录与引用更新表（含网络搜索与 Context7 源链接）。

## 5. 里程碑与节奏（建议）
- M1（本周）：ch01–ch05 初审与快速修复（P0/P1）。
- M2（下周）：ch06–ch12 初审；M1 残留收口。
- M3（+1 周）：ch13–ch20 初审；全书一致性体检。
- M4（最终周）：打磨叙事与视觉、统一术语与引用风格、全文回归检查。

## 6. 工作流
1) 章节梳理（基于 `_quarto.yml`）→ 建立章节审阅任务。
2) 快速体检：
   - 资源引用有效性（HTML/图/代码）；外链 200 状态；图表是否可读。
   - 术语词表与跨章一致性（定义、符号、缩写）。
3) 逐节深审（网络搜索 + Context7）：
   - 先 FP 再 VC，最后 BP；记录证据与差距。
4) 产出 `audit/chXX.md` 与修订项；标注优先级与工时。
5) 执行修订并回归（链接/资源/构建/可复现性）。

## 7. 章节清单与进度（来自 `_quarto.yml`）

- [ ] 序言 `index.qmd`

- [x] ch01（5 节）
  - [x] ch01/1_1_crisis_opportunity.qmd
  - [x] ch01/1_2_player_to_designer.qmd
  - [x] ch01/1_3_vibe_coding_paradigm.qmd
  - [x] ch01/1_4_vibe_coding_practice.qmd
  - [x] ch01/1_5_exercises.qmd

- [x] ch02（5 节）
  - [x] ch02/2_1_business_challenge.qmd
  - [x] ch02/2_2_definition_framework.qmd
  - [x] ch02/2_3_ml_problem_types.qmd
  - [x] ch02/2_4_vibe_coding_practice.qmd
  - [x] ch02/2_5_exercises.qmd

- [ ] ch03（5 节）
  - [x] ch03/3_1_vector_space.qmd
  - [x] ch03/3_2_probability.qmd
  - [x] ch03/3_3_optimization.qmd
  - [x] ch03/3_4_vibe_coding_practice.qmd
  - [x] ch03/3_5_exercises.qmd

- [ ] ch04（5 节）
  - [x] ch04/4_1_beyond_charts.qmd
  - [x] ch04/4_2_human_vision.qmd
  - [x] ch04/4_3_insight_framework.qmd
  - [x] ch04/4_4_vibe_coding_practice.qmd
  - [x] ch04/4_5_exercises.qmd

- [ ] ch05（6 节）
  - [x] ch05/5_1_business_challenge.qmd
  - [x] ch05/5_2_linear_regression.qmd
  - [x] ch05/5_3_overfitting_regularization.qmd
  - [x] ch05/5_4_xai.qmd
  - [x] ch05/5_5_vibe_coding_practice.qmd
  - [x] ch05/5_6_exercises.qmd

- [ ] ch06（6 节）
  - [x] ch06/6_1_business_challenge.qmd
  - [x] ch06/6_2_probability_vs_geometry.qmd
  - [x] ch06/6_3_kernel_trick.qmd
  - [x] ch06/6_4_xai.qmd
  - [x] ch06/6_5_vibe_coding_practice.qmd
  - [x] ch06/6_6_exercises.qmd

- [ ] ch07（8 节）
  - [x] ch07/7_1_business_challenge.qmd
  - [x] ch07/7_2_decision_tree.qmd
  - [x] ch07/7_3_ensemble_philosophy.qmd
  - [x] ch07/7_4_random_forest.qmd
  - [x] ch07/7_5_gradient_boosting.qmd
  - [x] ch07/7_6_xai_for_trees.qmd
  - [x] ch07/7_7_vibe_coding_practice.qmd
  - [x] ch07/7_8_exercises.qmd

- [ ] ch08（6 节）
  - [x] ch08/8_1_business_challenge.qmd
  - [x] ch08/8_2_kmeans.qmd
  - [x] ch08/8_3_beyond_kmeans.qmd
  - [x] ch08/8_4_clustering_evaluation.qmd
  - [x] ch08/8_5_vibe_coding_practice.qmd
  - [x] ch08/8_6_exercises.qmd

- [ ] ch09（8 节）
  - [x] ch09/9_1_challenge.qmd
  - [x] ch09/9_2_history.qmd
  - [x] ch09/9_3_neuron_activation.qmd
  - [x] ch09/9_4_fully_connected_network.qmd
  - [x] ch09/9_5_training_engine.qmd
  - [x] ch09/9_6_deep_learning_gears.qmd
  - [x] ch09/9_7_vibe_coding_practice.qmd
  - [x] ch09/9_8_exercises.qmd

- [ ] ch10（6 节）
  - [x] ch10/10_1_challenge.qmd
  - [x] ch10/10_2_word_embeddings.qmd
  - [x] ch10/10_3_rag_architecture.qmd
  - [x] ch10/10_4_transformer_attention.qmd
  - [x] ch10/10_5_vibe_coding_practice.qmd
  - [x] ch10/10_6_exercises.qmd

- [ ] ch11（5 节）
  - [x] ch11/11_1_challenge.qmd
  - [x] ch11/11_2_attention_mechanism.qmd
  - [x] ch11/11_3_transformer_architecture.qmd
  - [x] ch11/11_4_vibe_coding_practice.qmd
  - [x] ch11/11_5_exercises.qmd

- [ ] ch12（5 节）
  - [x] ch12/12_1_business_challenge.qmd
  - [x] ch12/12_2_cnn.qmd
  - [x] ch12/12_3_vit.qmd
  - [x] ch12/12_4_vibe_coding_practice.qmd
  - [x] ch12/12_5_exercises.qmd

- [ ] ch13（6 节）
  - [x] ch13/13_1_business_challenge.qmd
  - [x] ch13/13_2_transfer_learning_intro.qmd
  - [x] ch13/13_3_finetuning_techniques.qmd
  - [x] ch13/13_4_transformer_architectures.qmd
  - [x] ch13/13_5_vibe_coding_practice.qmd
  - [x] ch13/13_6_exercises.qmd

- [ ] ch14（6 节）
  - [x] ch14/14_1_business_challenge.qmd
  - [x] ch14/14_2_generative_adversarial_networks.qmd
  - [x] ch14/14_3_diffusion_models.qmd
  - [x] ch14/14_4_autoregressive_models.qmd
  - [x] ch14/14_5_vibe_coding_practice.qmd
  - [x] ch14/14_6_exercises.qmd

- [ ] ch15（6 节）
  - [x] ch15/15_1_business_challenge.qmd
  - [x] ch15/15_2_first_principle.qmd
  - [x] ch15/15_3_rag_foundation.qmd
  - [x] ch15/15_4_chunking.qmd
  - [x] ch15/15_5_vibe_coding_practice.qmd
  - [x] ch15/15_6_exercises.qmd

- [ ] ch16（6 节）
  - [x] ch16/16_1_business_challenge.qmd
  - [x] ch16/16_2_first_principle.qmd
  - [x] ch16/16_3_alignment_paths.qmd
  - [x] ch16/16_4_safe_rlhf.qmd
  - [x] ch16/16_5_vibe_coding_practice.qmd
  - [x] ch16/16_6_exercises.qmd

- [ ] ch17（6 节）
  - [x] ch17/17_1_business_challenge.qmd
  - [x] ch17/17_2_agent_architectures.qmd
  - [x] ch17/17_3_agent_pillars.qmd
  - [x] ch17/17_4_stateful_langgraph.qmd
  - [x] ch17/17_5_vibe_coding_practice.qmd
  - [x] ch17/17_6_exercises.qmd

- [ ] ch18（5 节）
  - [x] ch18/18_1_business_challenge.qmd
  - [x] ch18/18_2_first_principles.qmd
  - [x] ch18/18_3_framework_comparison.qmd
  - [x] ch18/18_4_vibe_coding_practice.qmd
  - [x] ch18/18_5_exercises.qmd

- [ ] ch19（7 节）
  - [x] ch19/19_1_business_challenge.qmd
  - [x] ch19/19_2_first_principle.qmd
  - [x] ch19/19_3_safety_and_alignment.qmd
  - [x] ch19/19_4_embodied_ai.qmd
  - [x] ch19/19_5_governance.qmd
  - [x] ch19/19_6_vibe_coding_practice.qmd
  - [x] ch19/19_7_architects_reflection.qmd

- [ ] ch20（5 节）
  - [x] ch20/20_1_challenge.qmd
  - [x] ch20/20_2_architecture_design.qmd
  - [x] ch20/20_3_vibe_coding_mvp.qmd
  - [x] ch20/20_4_pitch_day.qmd
  - [x] ch20/20_5_reflection.qmd

## 8. 下一步（本次迭代）
- [ ] 建立审阅模板文件：`book/audit/_template_chapter.md`。
- [ ] 生成 `book/audit/ch01.md`–`ch20.md` 的空白结构文件（引用模板）。
- [ ] 从 ch01 开始执行：完成 FP/VC/BP 三维打分与首轮修订建议。

---

## 附录：每章审阅报告模板（draft）

文件：`book/audit/chXX.md`

1) 概览
   - 章节：chXX（标题）
   - 小节清单与定位（源自 `_quarto.yml`）
   - 总体评估：FP/VC/BP（各 1–4 分）与一句话结论

2) 证据与问题（按小节）
   - 结构：
     - 小节名
     - 关键论断（需可验证）
     - 证据链接（网络搜索 / Context7）
     - 风险与边界（误用、常见坑）

3) 修订建议与优先级
   - P0（阻断阅读/错误/过时）
   - P1（重要提升/一致性）
   - P2（打磨/风格）

4) 资源与可复现性
   - 代码/数据/环境需求与替代方案
   - 资产检查（图/HTML/外链）

5) 术语与引用
   - 术语表更新、跨章统一项
   - 参考文献与官方链接（标注访问日期）

6) 状态与动作
   - 审核状态：未开始 / 进行中 / 已完成
   - 责任人 / 截止时间 / 变更记录


