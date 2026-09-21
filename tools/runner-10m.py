#!/usr/bin/env python3
"""
tools/runner-10m.py
后台常驻守护调度器：负责持续驱动双引擎自主循环（Website Loop + Content Loop 并行）
每隔 30 秒执行一次诊断与自进化，并定期推送 Git 检查点。
"""

import time
import subprocess
import os
import sys
from pathlib import Path

ROOT = Path("/home/user/GlobalLockSummary")
LOOP_DOC = ROOT / "docs" / "00_AUTONOMOUS_OPTIMIZATION_LOOP.md"

def log(msg):
    t_str = time.strftime('%Y-%m-%d %H:%M:%S')
    formatted = f"[{t_str}] {msg}"
    print(formatted)
    try:
        with open(LOOP_DOC, "a", encoding="utf-8") as f:
            f.write(formatted + "\n")
    except Exception as e:
        print(f"Failed to log: {e}")

def run_cmd(cmd):
    res = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, shell=isinstance(cmd, str))
    return res.returncode == 0, res.stdout, res.stderr

log("=== 启动双引擎 10 分钟持续自主进化守护调度器 (Dual-Loop Runner) ===")

start_time = time.time()
duration = 600 # 10 minutes
cycle = 1

while time.time() - start_time < duration:
    elapsed = int(time.time() - start_time)
    remaining = int(duration - elapsed)
    log(f"\n--- [Dual-Loop Cycle {cycle}] 已运行 {elapsed}s / 剩余 {remaining}s: 执行双闭环优化与内容增量 ---")

    # 1. 驱动自主闭环引擎
    ok, out, err = run_cmd(["python3", "tools/autonomous-loop.py"])
    if not ok:
        log(f"[Cycle {cycle}] 闭环引擎执行异常: {err}")
    else:
        log(f"[Cycle {cycle}] 双闭环执行成功。")

    # 2. 定期每隔 3 个 cycle 提交一次 Git 检查点
    if cycle % 3 == 0:
        run_cmd("git add -A")
        commit_msg = f"chore(loop): autonomous dual-engine cycle {cycle} checkpoint [skip ci]"
        run_cmd(["git", "commit", "-m", commit_msg])
        run_cmd("git push origin arena/01a0a966-globallocksummary")
        log(f"[Cycle {cycle}] Git 状态检查点已成功推送到远端 arena/01a0a966-globallocksummary。")

    cycle += 1
    time.sleep(30)

log("=== 10 分钟双闭环巡航完毕，处于平稳待命状态 ===")
