# 上游源代码目录

官方源码在 `upstream/harness2/`，作为 Git submodule 固定到 Google Research 的 `google-research/harness2`。当前锁定 commit：`1cfe254e8d25b15f37048c3730134686abe60335`；来源 URL 由根目录 `.gitmodules` 记录。

新检出本项目时，运行 `git submodule update --init upstream/harness2` 获取父仓库记录的同一版本。官方代码保留其 `LICENSE`；项目自研代码放在根目录 `experiments/`，不要直接修改官方 checkout。源码已检出不等于 Demo 已运行或 Benchmark 已复现。
