# 会话执行日志（追加，禁止覆盖历史）

> 请在每轮 Codex 会话结束追加一个新条目。首次初始化不等于学习开始。

## 每轮记录模板

### YYYY-MM-DD HH:mm（时区） | Session N | Stage NN
- **起始状态**：
- **本轮唯一目标**：
- **实际完成（OBSERVED）**：
- **代码变更（Codex 实现 / 用户独立设计、审查或验收）**：
- **实际命令、退出码、日志与证据路径**：
- **新获得的概念理解（仅实际被考核的）**：
- **面试题、独立回答与得分**：
- **误区和变式复测要求**：
- **阻塞 / 未执行 / API 预算与授权**：
- **更新过的记录文件**：
- **下次唯一任务**：
- **是否正在等待用户批准进入下一阶段**：

### 2026-10-29 18:06（Asia/Shanghai） | Session 1 | Stage 00
- **起始状态**：NOT_STARTED；工作区只有计划、模板、离线脚本，无 Git 仓库和官方源码 checkout。
- **本轮唯一目标**：恢复状态，完成 Stage 00 第一小节环境盘点，布置用户动手练习。
- **实际完成（OBSERVED）**：读取启动文件、进度记录、Stage 00 笔记及 Gate；核对本地文件；为 `AGENTS.md` 加入阶段 branch、及时 commit/push、Gate 后 PR 与 merge 核验规则。Stage 00 进入 IN_PROGRESS；尚无 Demo 或 Benchmark 运行。
- **代码变更（用户亲写 / AI 生成 / 共同修改）**：用户尚未写代码；Codex 修改规则和学习记录，未编写核心项目代码。
- **实际命令、退出码、日志与证据路径**：`python scripts/resume.py` exit 0（修改前报 Stage 00 NOT_STARTED）；`python scripts/check_workspace.py` exit 0（修改前）；`git status --short --branch` exit 1、`git remote -v` exit 1（均因无 `.git`）；`gh auth status` exit 1（token 无效）；`python --version`、`git --version`、`uv --version`、`docker --version`、`node --version` 见 `learning/stages/00.md`；`wsl --status` 访问拒绝。终端输出未另存日志。
- **新获得的概念理解（仅实际被考核的）**：无，尚未收到用户独立回答。
- **面试题、独立回答与得分**：尚未进行 Gate；第一小节诊断题待用户回答，不计分。
- **误区和变式复测要求**：无已知错题；初测待进行。
- **阻塞 / 未执行 / API 预算与授权**：本地 Git 仓库不存在；GitHub token 无效；仓库名称和可见性待用户确认。官方源码未克隆，Docker daemon/WSL 未核实。未调用付费 API。
- **更新过的记录文件**：`AGENTS.md`、`learning/PROGRESS.md`、`learning/stage_status.json`、`learning/stages/00.md`、`learning/gates/00.md`、`learning/SESSION_LOG.md`。
- **下次唯一任务**：用户亲手完成 Stage 00 环境检查小脚本并回答两道诊断题，Codex 复核。
- **是否正在等待用户批准进入下一阶段**：否，Stage 00 尚未考核。

### 2026-10-29 18:21（Asia/Shanghai） | Session 2 | Stage 00
- **起始状态**：IN_PROGRESS；上轮环境盘点已记录，尚无 Git 仓库、官方源码或 Demo。
- **本轮唯一目标**：把“Codex 负责开发、用户负责理解与验收”的新长期规则同步到项目文件，并建立 Stage 00 Git/GitHub 工作流。
- **实际完成（OBSERVED）**：修订开发分工、重要功能讲解、用户代码/Trace 阅读考核和原评分门槛；同步 Stage 00–13 的计划与 Gate/阶段模板。用户确认仓库名 `harness2-agent-evaluation`、公开可见。初始化本地 Git、提交 `main` 初始脚手架、建立 `stage-00-setup`；创建公开 GitHub 仓库并 Push `main`。
- **代码变更（Codex 实现 / 用户独立设计、审查或验收）**：Codex 修改 `AGENTS.md`、`MASTER_PLAN.md`、`CODEX_START_PROMPT.md`、`START_HERE.md`、`EVALUATION_SYSTEM_SPEC.md`、`interview/QUESTION_SCOPE.md`、学习模板及当前 Stage 记录；用户提出并确认新分工及公开仓库选择。未编写 Harness² 核心代码。
- **实际命令、退出码、日志与证据路径**：`git init -b main` exit 0；`git add -A` exit 0；`git diff --cached --check` exit 0；敏感凭证模式搜索无匹配；`git commit -m "chore: bootstrap harness evaluation workspace"` exit 0，SHA `46ba3d2`；`git switch -c stage-00-setup` exit 0；`gh repo create lyxnbclass/harness2-agent-evaluation --public --source . --remote origin` exit 0；`git push -u origin main` exit 0；`git commit -m "docs: record developer-led stage workflow"` exit 0，SHA `36c6eae`；`git push -u origin stage-00-setup` exit 0；`gh auth status` 复查 exit 0。终端输出未另存日志。
- **新获得的概念理解（仅实际被考核的）**：无；本轮是规则和仓库工作，未评估用户知识掌握。
- **面试题、独立回答与得分**：未考；上轮提出的手写环境脚本任务已取消，不计分。
- **误区和变式复测要求**：无已知错题；仍待正式初测。
- **阻塞 / 未执行 / API 预算与授权**：官方源码未克隆、Demo 未运行、Docker daemon/WSL 未核实；未调用付费 API。Stage 00 PR 不满足创建条件，尚未创建。
- **更新过的记录文件**：`AGENTS.md`、`MASTER_PLAN.md`、`CODEX_START_PROMPT.md`、`START_HERE.md`、`EVALUATION_SYSTEM_SPEC.md`、`interview/QUESTION_SCOPE.md`、`learning/MASTERY_MATRIX.md`、`learning/stages/00–13.md`、`learning/gates/00–13.md`、`learning/PROGRESS.md`、`learning/stage_status.json`、`learning/SESSION_LOG.md`。
- **下次唯一任务**：Codex checkout 官方 Harness²，记录真实 SHA/remote/tree 并读取 README 确定 Demo 入口；讲解后由用户分析。
- **是否正在等待用户批准进入下一阶段**：否，Stage 00 尚未考核。

### 2026-10-30 09:33（Asia/Shanghai） | Session 3 | Stage 00
- **起始状态**：IN_PROGRESS；`stage-00-setup` 与远端同步，无 PR；无根目录 README、官方 checkout、Demo 或 Benchmark 结果。
- **本轮唯一目标**：把用户提供的英文 README 素材整理成可核实的 GitHub 项目介绍，并建立每阶段合并后的 README 维护规则。
- **实际完成（OBSERVED）**：新增根目录英文 `README.md`，明确当前只完成仓库/记录基础设施，架构和自研模块仍为计划；在 `AGENTS.md` 加入 PR 合并后同步 README 的长期规则，并在 `MASTER_PLAN.md`、`CODEX_START_PROMPT.md`、`START_HERE.md` 引用。README 在 Stage 00 分支提交 `7f5d5e1`，在默认 `main` 提交 `f7a0ae1` 发布；`main` 与 Stage 00 分支的文档内容已同步。未创建 Stage 00 PR，未改变 Gate 状态。
- **代码变更（Codex 实现 / 用户独立设计、审查或验收）**：Codex 编写/核验 README 与规则；用户提供英文素材和持续维护要求。无 Agent 核心代码变更，用户掌握程度未考。
- **实际命令、退出码、日志与证据路径**：`python scripts/resume.py` exit 0（Stage 00 IN_PROGRESS）；`python scripts/check_workspace.py` exit 0；本地 README 链接检查发现 10 个相对链接、缺失 0；`git diff --check` exit 0；`git commit -m "docs: establish verified project overview"` exit 0，SHA `7f5d5e1`，Stage 00 分支 Push 成功；首次 `git cherry-pick 7f5d5e1` 到 `main` exit 1（四个学习记录文件有内容冲突），`git cherry-pick --abort` exit 0 后以核实的文件内容重新发布；`git commit -m "docs: publish project README on main"` exit 0，SHA `f7a0ae1`，main Push 成功；`git commit -m "docs: align stage records on main"` exit 0，SHA `a78fe22`，Push 成功；`git merge main --no-ff` 到 Stage 00 分支 exit 0，Push 成功；`gh api repos/lyxnbclass/harness2-agent-evaluation/contents/README.md --jq '.path'` exit 0，返回 `README.md`。终端输出未另存日志。
- **新获得的概念理解（仅实际被考核的）**：无；本轮无用户独立技术回答。
- **面试题、独立回答与得分**：未考。
- **误区和变式复测要求**：无已知错题；仍待初测。
- **阻塞 / 未执行 / API 预算与授权**：官方源码未检出、Demo/Benchmark 未运行；Docker daemon/WSL 能力未复核；无付费 API 调用。README 不声称性能提升。
- **更新过的记录文件**：`README.md`、`AGENTS.md`、`MASTER_PLAN.md`、`CODEX_START_PROMPT.md`、`START_HERE.md`、`learning/PROGRESS.md`、`learning/stage_status.json`、`learning/stages/00.md`、`learning/gates/00.md`、`learning/SESSION_LOG.md`。
- **下次唯一任务**：Codex checkout 官方 Harness² 到 `upstream/harness2/`，记录 SHA/remote/tree 并读取 README 确定 Demo 入口；讲解后由用户分析。
- **是否正在等待用户批准进入下一阶段**：否，Stage 00 尚未考核。

### 2026-10-30 10:00（Asia/Shanghai） | Session 4 | Stage 00
- **起始状态**：IN_PROGRESS；`stage-00-setup` clean、无 PR；官方 checkout/Demo/Benchmark 尚无证据。
- **本轮唯一目标**：从用户给定的 Google Research 官方仓库检出可复现源码，核实 SHA、License、Demo 入口和源码声明的数据流。
- **实际完成（OBSERVED）**：官方仓库以 Git submodule 检出到 `upstream/harness2/`，remote 与 gitlink 均固定 `1cfe254e8d25b15f37048c3730134686abe60335`，checkout clean，Apache 2.0 `LICENSE` 保留。定位 `pyproject.toml:32` 的 `harness2-demo` → `harness2/cli/demo.py:main` → `harness2/core/schedule.py:run_domain` → `harness2/demo.py:DemoAdapter.execute` 的本地源码调用关系；`demo.json`、`answer.txt`、`trajectory.md` 只是源码声明的产物，尚未运行验证。
- **代码变更（Codex 实现 / 用户独立设计、审查或验收）**：Codex 只添加官方 submodule 指针并更新项目笔记/README，未修改官方源码，未编写自研 Agent 代码；用户提供官方仓库和站点 URL 并要求开始 Stage 00。用户理解尚待回答验证。
- **实际命令、退出码、日志与证据路径**：`git ls-remote https://github.com/google-research/harness2.git HEAD` exit 0，返回上述 SHA；`git submodule add https://github.com/google-research/harness2.git upstream/harness2` exit 0；`git -C upstream/harness2 rev-parse HEAD` exit 0，返回同 SHA；`git -C upstream/harness2 status --short --branch` 显示 clean `main...origin/main`；`git ls-files --stage upstream/harness2` 显示 mode `160000` 与相同 SHA；`git submodule update --init upstream/harness2` exit 0。`uv python list --only-installed` 显示 Windows Python 3.12.13 可用；`docker info` exit 0 显示 Linux daemon 29.8.0，`docker image ls` 显示本地 `python:3.12-slim-trixie`。`python scripts/resume.py` 与 `python scripts/check_workspace.py` 均 exit 0。`git commit -m "chore: pin official harness2 source"` exit 0，SHA `0b1902d`，`git push` exit 0。源码阅读证据见 `learning/SOURCE_INDEX.md` 和 `learning/stages/00.md`；未另存终端日志。
- **新获得的概念理解（仅实际被考核的）**：无，尚未收到用户对调用链的独立解释。
- **面试题、独立回答与得分**：尚未进行 Gate；本轮源码理解题待用户作答，不计分。
- **误区和变式复测要求**：无已知错题；初测待进行。
- **阻塞 / 未执行 / API 预算与授权**：未安装上游依赖、未运行官方 Demo/测试/Benchmark、未调用模型或收费 API。官方 `pyproject.toml` 要求 Python `<3.14`，本机默认 3.14.6 不符合；隔离 Docker Python 3.12 镜像可用于后续 Demo。
- **更新过的记录文件**：`.gitmodules`、`upstream/harness2` gitlink、`upstream/README.md`、`README.md`、`learning/SOURCE_INDEX.md`、`learning/OFFICIAL_EVAL_AUDIT.md`、`learning/stages/00.md`、`learning/PROGRESS.md`、`learning/stage_status.json`、`learning/gates/00.md`、`learning/SESSION_LOG.md`。
- **下次唯一任务**：Codex 在隔离 Docker Python 3.12 环境运行无模型凭证的官方 Demo，核对真实输出并让用户解释入口与产物关系。
- **是否正在等待用户批准进入下一阶段**：否，Stage 00 远未通过。

### 2026-10-30 11:12（Asia/Shanghai） | Session 5 | Stage 00
- **起始状态**：IN_PROGRESS；官方源码固定并完成初步定位，Demo 未运行；用户尚未接受充分讲解就被提出源码题。
- **本轮唯一目标**：纠正教学顺序，对 Stage 00 Demo 入口、参数、返回、真实调用和源代码构造数据进行详细讲解，不进行考核。
- **实际完成（OBSERVED）**：重新阅读 `harness2/cli/demo.py`、`harness2/demo.py`、`harness2/core/schedule.py` 的 `run_task`/`run_domain`/`_run_one_mode` 及 `harness2/core/recursion.py` 的 adapter 调用位置；记录教学例子与源码/运行证据边界。撤回前次 `--k 0` 题，不计分。
- **代码变更（Codex 实现 / 用户独立设计、审查或验收）**：没有代码实现或上游改动；Codex 更新学习记录。用户指出讲解深度不够，尚无技术作答。
- **实际命令、退出码、日志与证据路径**：`Get-Content` 读取上述本地源码，均 exit 0；`git status --short --branch` 显示工作树原本 clean；教学细节记录在 `learning/stages/00.md`。官方 Demo/测试仍未执行。
- **新获得的概念理解（仅实际被考核的）**：无，用户尚未独立回答。
- **面试题、独立回答与得分**：未考；上轮题撤回，不计分。
- **误区和变式复测要求**：无用户技术错误；需要先完成解释，再安排新题。
- **阻塞 / 未执行 / API 预算与授权**：Demo、Benchmark、付费模型均未运行；无成本。
- **更新过的记录文件**：`learning/stages/00.md`、`learning/gates/00.md`、`learning/PROGRESS.md`、`learning/stage_status.json`、`learning/SESSION_LOG.md`。
- **下次唯一任务**：Codex 在隔离 Docker Python 3.12 环境运行无模型凭证 Demo，核对实际输出后再继续代码/Trace 教学。
- **是否正在等待用户批准进入下一阶段**：否，Stage 00 未通过。

### 2026-10-30 | Session 6 | Stage 00

- **起始状态与唯一工程任务**：IN_PROGRESS；固定官方源码但无运行证据。按用户最新纠正，先建立六步深度教学协议并实际运行官方无模型 Demo，为“整体概念与 Demo 工作原理”教学提供真实输入/输出。
- **Codex 实际修改**：更新 `AGENTS.md`、`MASTER_PLAN.md`、`START_HERE.md`、`learning/MASTERY_MATRIX.md`，新增独立 `learning/KNOWLEDGE_MASTERY.md`；更新 README 与 Stage 00 证据/进度记录。未改官方源码，未编写自研 Agent 模块；用户提出教学协议和 Stage 00 教学目标，尚未给技术题独立作答。
- **真实命令与输出**：`python scripts/resume.py`、`python scripts/check_workspace.py` 退出 0（修改前）；`gh auth status` 退出 0，`gh pr list --head stage-00-setup` 返回 `[]`；`git submodule status` 为官方 SHA `1cfe254e…`。Docker `python:3.12-slim-trixie` 以 `--network none`、只读源挂载运行 `python -m harness2.cli.demo --output /out/raw_runs/stage00_demo_k1 --k 1 --mode both`，退出 0，两个账本 task `ok`。`demo.json`：2 done、0 failed、14 local executions、16 scripted editor calls；`ledger-1` base 105.25，parallel/sequential final 85.15。原始路径与完整命令见 `learning/stages/00.md`。
- **掌握与考核**：整体教学在本轮开始，用户尚无独立技术回答；掌握等级保持 U；正式 Gate 未考。先前过早提出的 `--k 0` 问题继续撤回，不计分。
- **限制/未完成**：Stage 00 故障注入、完整分节教学、用户 Trace 分析、正式 Gate、PR 尚未完成；模型 Benchmark、SWE-bench 与付费调用未运行。Demo 的 `ok` 不能推断模型成功率。
- **下次唯一任务**：在整体图基础上详细讲解 CLI 入口与 `argparse`，先解释 Python 基础并对应已取得的真实 Demo 产物，再做少量理解检查。
- **下一阶段批准**：无；Stage 00 保持 IN_PROGRESS。
- **GitHub 保存**：`7dbb245 docs: establish deep teaching protocol and record demo run` 已 Push 至 `origin/stage-00-setup`；`gh pr list --head stage-00-setup` 返回 `[]`，正式 PR 尚未创建。

### 2026-10-30 | Session 7 | Stage 00

- **用户纠正**：上一轮系统讲解虽然覆盖概念和真实结果，但代码实现、参数/返回值及 ASCII 链路图不充分；用户明确表示代码设计层面仍不理解。不能把该知识点标教学完成或掌握。
- **本轮唯一任务**：在同一 Stage 00 Demo 知识点补上真实源码关键片段、Python 基础解释、ASCII 调用/数据流图，以及 `ledger-1` 的逐步真实值；不推进新阶段。
- **证据与修改**：重新读取官方 SHA `1cfe254e…` 的 `harness2/cli/demo.py`、`harness2/demo.py`、`harness2/core/schedule.py`、`harness2/core/recursion.py` 对应行，并复核已存在的 `demo.json` 和两份 Trajectory；改 `AGENTS.md`、`MASTER_PLAN.md`、`learning/KNOWLEDGE_MASTERY.md`、`learning/PROGRESS.md`、本日志。未新运行 Demo/Benchmark、未改官方代码或自研模块。
- **掌握与考核**：用户提供教学反馈，没有技术题回答；等级仍 U，正式 Gate 未考、无分数。
- **下一唯一任务**：待用户反馈代码贯穿讲解后，单独深入 CLI/`argparse` 的参数解析、调用和异常。
- **批准与阻塞**：Stage 00 IN_PROGRESS；无进入 Stage 01 批准。真实 LLM Benchmark 仍未运行。

### 2026-10-30 | Session 8 | Stage 00

- **用户输入与当前任务**：用户询问 `Trajectory` 和 `CSV` 是什么；先补这两个基础概念，再继续代码链路，不把提问当成技术错误。
- **真实证据**：重新读取本地官方 Demo 的 `experiments/raw_runs/stage00_demo_k1/sources/ledger-1/ledger.csv`（`amount` 表头与三个金额）以及基线、修改后 `trajectory.md`（观察值 `105.25` 与 `85.15`）；官方相关读取/写入代码位于固定 SHA `1cfe254e…` 的 `harness2/demo.py:30–37,86–105`。未重新执行 Demo、未改官方源码。
- **记录与掌握**：更新 `learning/KNOWLEDGE_MASTERY.md`、`learning/PROGRESS.md`、本日志。用户尚未独立回答理解题，等级 U，正式 Gate 未考。
- **下一唯一任务**：确认 CSV 与 Trajectory 的数据流理解后，再继续 Stage 00 的 CLI/`argparse` 小节。
- **批准与阻塞**：Stage 00 IN_PROGRESS；无进入下一阶段批准；PR 未创建。

### 2026-10-30 | Session 9 | Stage 00

- **用户独立回答**：CSV 属于输入；到 `answer.txt` 看输出；Trajectory 记录执行过程。三点正确，基础子知识点暂记 L1；未测试 Python 读取/写入代码或完整 Trace，不升级整条 Demo 等级。
- **用户新问题 / 唯一任务**：解释脚本如何被复制、更换和执行，提供整条链路的 ASCII 文件树。Codex 负责官方源码定位与运行产物核对。
- **真实证据**：读取官方固定 SHA `1cfe254e…` 的 `core/context.py:build`、`core/recursion.py:_run_stage/_accept_tree/_roll`、`core/tree.py:read_tree/write_tree/validate` 和 `demo.py:DemoProposer.call/DemoAdapter.execute`。对照本地 `base/scripts/summarize.py`、`runs/demo-oc-agg1/ledger-1/context/inv1/harness/scripts/summarize.py`、`harnesses/inv1`、`harnesses/agg1`、基线/候选 `answer.txt`。未重新运行 Demo，未改官方源码。
- **记录修改与考核**：更新 `learning/KNOWLEDGE_MASTERY.md`、`learning/PROGRESS.md` 和本日志；正式 Stage 00 Gate 未考。未执行付费模型、Benchmark 或新实验。
- **下次唯一任务**：用户理解此脚本替换链路后，继续 Stage 00 的 CLI/`argparse` 小节。
- **批准状态**：Stage 00 IN_PROGRESS；Stage 01 未获批准，Stage 00 PR 未创建。

### 2026-10-30 | Session 10 | Stage 00

- **用户独立回答**：对“候选工作副本校验失败后是否直接执行”的回答是“记录错误并回退”，方向正确。Codex 补充源码细节：`_run_stage()` 最多再尝试一次修正，仍失败才返回 `fell_back=True` 与错误；不能把首次失败直接说成最终回退。
- **掌握记录**：脚本候选校验与回退的基础概念暂记 L1；尚无完整函数分支或 Trace 的独立解释，不升级 L2/L3。正式 Stage 00 Gate 未考。
- **本轮修改**：更新 `learning/KNOWLEDGE_MASTERY.md`、`learning/MASTERY_MATRIX.md`、`learning/PROGRESS.md`、本日志；未改官方代码、未重新运行 Demo/测试/Benchmark。
- **下一唯一任务**：Stage 00 CLI/`argparse` 的命令输入、参数转换/校验、调用与退出码教学，再用新输入做理解检查。
- **批准状态**：Stage 00 保持 IN_PROGRESS，无阶段 PR，无进入 Stage 01 批准。

### 2026-10-30 | Session 11 | Stage 00

- **当前唯一任务**：Stage 00 CLI/`argparse` 的参数解析、模式转换、调度调用与退出码教学；不推进阶段。
- **源码与真实证据**：重新核对官方 SHA `1cfe254e…` 的 `pyproject.toml:32`、`harness2/cli/demo.py:27–58`、`core/schedule.py:48–55,669–733`。有效 `--k 1 --mode both` Demo 之前退出 0，`demo.json` 为 2 done/0 failed。新运行 `--k 0 --mode both` 的 Docker Python 3.12 无网络只读源码演示，stderr `--k must be positive`，Demo 进程退出码 2；外层 PowerShell 打印该值后退出 0。
- **归属、掌握和考核**：Codex 负责命令与讲解，未改官方代码或调用模型；用户本轮只说“继续”，尚未回答此小节问题。CLI 知识点 U，Stage 00 Gate 未考。
- **更新记录**：`learning/KNOWLEDGE_MASTERY.md`、`learning/MASTERY_MATRIX.md`、`learning/stages/00.md`、`learning/PROGRESS.md`、本日志。下一唯一任务为用户分析新参数 Trace，再针对性补课。
- **批准与 GitHub**：Stage 00 IN_PROGRESS，无 PR，无 Stage 01 批准；有价值的教学/故障证据按分支规范提交。

### 2026-10-30 | Session 12 | Stage 00

- **用户指令与进度边界**：用户要求先讲解 CLI 参数 Trace 题，再“进入下一步”；按 Stage 00 内的下一教学小节 DemoAdapter 执行，不能视为批准 Stage 01。该题由 Codex 给答案，无独立回答或分数，CLI 掌握仍 U。
- **本轮唯一工程/教学任务**：DemoAdapter 的任务/脚本/产物接口；对照官方固定 SHA `1cfe254e…` 的 `demo.py:41–117`、`core/spec.py:200–249` 与 CLI/调度调用方。
- **真实运行**：两个隔离 Docker Python 3.12 直接调用演示均退出 0：`tasks()` 两题、`task_prompt` 签名求和；`execute('ledger-1',None,...)` 产 `105.25`、delivered True、计数 1；同一输入在新 Adapter 实例下使用 base 与已有 `harnesses/inv1` 候选脚本，产 `105.25`/`85.15`，计数 2。无网络、无模型、无官方源码修改。详细证据见 `learning/stages/00.md`，原始文件在被忽略的 `experiments/raw_runs/stage00_adapter_*`。
- **掌握/考核**：DemoAdapter 小节尚待用户独立回答，U；此前 CSV/Trajectory 与候选校验基础各 L1；Stage 00 Gate 未考。
- **记录与下一唯一任务**：更新 `learning/KNOWLEDGE_MASTERY.md`、`MASTERY_MATRIX.md`、`stages/00.md`、`PROGRESS.md`、本日志；待用户回答 DemoAdapter 的 `harness_dir`/产物 Trace，再继续 `run_domain()`。
- **GitHub/批准**：Stage 00 IN_PROGRESS，PR 未创建，无进入下一阶段批准。

### 2026-10-30 | Session 13 | Stage 00

- **用户独立回答**：`execute('ledger-1', None, 'trial-a')` 选择初始错误脚本、原 CSV，两点正确；第三点只说 `answer.txt`，漏 `run_id='trial-a'` 的产物目录。不是已通过的完整路径 Trace。
- **最小补课**：以官方固定 SHA `1cfe254e…` 的 `demo.py:76–105` 解释 `task_id` 选 CSV、`harness_dir` 选脚本、`run_id` 与 `self.root` 拼出 `run_dir`，再写 `run_dir/answer.txt`。举真实已执行 `direct-base` 的路径作对照；`trial-a` 路径只做源码推导，不冒充已生成文件。
- **记录与掌握**：更新 `learning/KNOWLEDGE_MASTERY.md`、`MASTERY_MATRIX.md`、`MISTAKES.md`、`PROGRESS.md`、本日志。DemoAdapter 子点暂 L1，路径新变式待答；正式 Gate 未考。未改官方源码或重跑模型/Benchmark。
- **下一唯一任务**：让用户独立分析 `execute('ledger-2', None, 'review-b')` 的脚本、CSV 与完整产物路径，再按回答决定是否进入 `run_domain()`。
- **GitHub/批准**：Stage 00 IN_PROGRESS，无 PR，无 Stage 01 批准。
