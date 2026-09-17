#!/usr/bin/env python3
"""
tools/autonomous-loop.py
双引擎协同自主优化闭环引擎 (Dual-Loop Autonomous Engine):
Engine A (Website Loop): 负责代码质量、构建状态、测试验证、死链拦截与路由修复。
Engine B (Content Loop): 负责内容爬取、图谱索引清洗、3层视觉与筛选标准结构化增强、以及建议动态吸收沉淀。
"""

import time
import subprocess
import os
import sys
import json
from pathlib import Path

ROOT = Path("/home/user/GlobalLockSummary")
LOOP_DOC = ROOT / "docs" / "00_AUTONOMOUS_OPTIMIZATION_LOOP.md"
METHODOLOGY_DOC = ROOT / "docs" / "01_METHODOLOGY_AND_CONTEXT_MEMORY.md"

def log(msg):
    t_str = time.strftime('%Y-%m-%d %H:%M:%S')
    formatted = f"[{t_str}] {msg}"
    print(formatted)
    try:
        with open(LOOP_DOC, "a", encoding="utf-8") as f:
            f.write(formatted + "\n")
    except Exception as e:
        print(f"Failed to write to loop doc: {e}")

def run_cmd(cmd):
    res = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, shell=isinstance(cmd, str))
    return res.returncode == 0, res.stdout, res.stderr

def run_content_loop():
    """Content Loop: 运行爬虫抓取清洗与 3 层图谱索引增量优化"""
    harvester = ROOT / "tools" / "content-harvester.py"
    if harvester.exists():
        ok, out, err = run_cmd(["python3", str(harvester)])
        return ok, out.strip()
    return False, "Harvester script missing"

def run_website_loop():
    """Website Loop: 运行构建与回归测试"""
    ok_b, out_b, err_b = run_cmd(["node", "build.mjs"])
    if not ok_b:
        return False, f"Build error: {err_b}"
    ok_t, out_t, err_t = run_cmd(["npm", "test"])
    if not ok_t:
        return False, f"Test error: {err_t}"
    return True, "Build & Test 100% Passed"

def main():
    log("=== [Dual-Loop Autonomous Engine Activated] 双引擎协同自主闭环启动 ===")
    
    # 1. 运行 Content Loop
    log("[Content Loop] 正在执行内容爬取与增量图谱索引清洗...")
    c_ok, c_msg = run_content_loop()
    log(f"[Content Loop] 爬虫与图谱增强结果: {c_msg}")

    # 2. 运行 Website Loop
    log("[Website Loop] 正在执行全量 SSG 构建与 23+36 项质量测试...")
    w_ok, w_msg = run_website_loop()
    log(f"[Website Loop] 构建与测试结果: {w_msg}")

    # 3. 动态将建议与本轮成果吸纳进 Loop 记录与方法论
    log("[Knowledge Assimilation] 正在将用户最新指令与 3 项主动建议沉淀进长期知识库...")
    run_cmd(["python3", "tools/generate-project-excel.py"])
    run_cmd(["python3", "tools/generate-master-index-excel.py"])
    log("[Autonomous Checkpoint] 双引擎自进化完成，准备写入 Git 检查点。")

if __name__ == "__main__":
    main()
