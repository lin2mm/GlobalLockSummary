with open('build.mjs', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. 在 rewriteNav 中计算 patentCount
old_var_init = "  let pitfallsCount = 0;\n  let indexCount = 6;"
new_var_init = """  let pitfallsCount = 0;
  let indexCount = 8;
  let patentCount = 5; // 5 大核心规避专题路径"""

if old_var_init in code:
    code = code.replace(old_var_init, new_var_init)

# 2. 为 patent-avoidance.html 添加动态统计数字 label
old_patent_block = """    } else if (item.href.includes('patent-avoidance.html')) {
      subItems = [
        { label: isZh ? '1. 锁芯夹持与背板锁紧' : '1. Cylinder Clamping', href: isZh ? '/zh/patent-avoidance.html#nuki-clamping' : '/en/patent-avoidance.html#nuki-clamping' },
        { label: isZh ? '2. 钥匙抓取与浮动耦合' : '2. Key Gripper & Oldham', href: isZh ? '/zh/patent-avoidance.html#key-coupling' : '/en/patent-avoidance.html#key-coupling' },
        { label: isZh ? '3. 手动优先与脱开离合' : '3. Manual Clutch & BLDC', href: isZh ? '/zh/patent-avoidance.html#clutch-disconnect' : '/en/patent-avoidance.html#clutch-disconnect' },
        { label: isZh ? '4. 尾轴卡扣与翼形卡爪' : '4. Tailpiece Wing Latches', href: isZh ? '/zh/patent-avoidance.html#august-tailpiece' : '/en/patent-avoidance.html#august-tailpiece' },
        { label: isZh ? '5. 出海 FTO 自查清单' : '5. Global FTO Checklist', href: isZh ? '/zh/patent-avoidance.html#checklist' : '/en/patent-avoidance.html#checklist' }
      ];"""

new_patent_block = """    } else if (item.href.includes('patent-avoidance.html')) {
      // 后装专利规避 (全动态 5 大专题)
      label = `${rawLabel} (${patentCount})`;
      subItems = [
        { label: isZh ? '1. 锁芯夹持与背板锁紧' : '1. Cylinder Clamping', href: isZh ? '/zh/patent-avoidance.html#nuki-clamping' : '/en/patent-avoidance.html#nuki-clamping' },
        { label: isZh ? '2. 钥匙抓取与浮动耦合' : '2. Key Gripper & Oldham', href: isZh ? '/zh/patent-avoidance.html#key-coupling' : '/en/patent-avoidance.html#key-coupling' },
        { label: isZh ? '3. 手动优先与脱开离合' : '3. Manual Clutch & BLDC', href: isZh ? '/zh/patent-avoidance.html#clutch-disconnect' : '/en/patent-avoidance.html#clutch-disconnect' },
        { label: isZh ? '4. 尾轴卡扣与翼形卡爪' : '4. Tailpiece Wing Latches', href: isZh ? '/zh/patent-avoidance.html#august-tailpiece' : '/en/patent-avoidance.html#august-tailpiece' },
        { label: isZh ? '5. 出海 FTO 自查清单' : '5. Global FTO Checklist', href: isZh ? '/zh/patent-avoidance.html#checklist' : '/en/patent-avoidance.html#checklist' }
      ];"""

if old_patent_block in code:
    code = code.replace(old_patent_block, new_patent_block)
    print("Added dynamic counter to patent-avoidance in build.mjs!")

with open('build.mjs', 'w', encoding='utf-8') as f:
    f.write(code)

