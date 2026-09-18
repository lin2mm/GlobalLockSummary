with open('docs/10_SMART_LOCK_RETROFIT_METHODOLOGY.md', 'r', encoding='utf-8') as f:
    methodology = f.read()

compliance_chapter = """
---

## 六、 海外多国家合规与数据安全合规清单（Global Compliance & Data Governance）

当智能锁产品及配套建站系统出海时，除机械与五金适配外，必须满足目标国家的主权级法律与合规准入：

### 1. 欧洲市场（EU / EEA）
* **CE-RED (无线电设备指令 2014/53/EU)**：Matter over Thread、BLE 5.3 与 Wi-Fi 射频合规，EN 300 328 认证；
* **GDPR (通用数据保护条例)**：
  - 用户上传门锁照片识别时，服务端严禁持久化保存带有门牌号、地理 GPS EXIF 信息的原图；
  - 必须提供“一键删除门锁诊断记录”及“数据可携权导出”接口；
* **EN 15684 (机电锁芯标准)**：电子锁芯物理抗拔、抗扭（≥15 N·m）与电子防破译评级。

### 2. 北美市场（US / Canada）
* **FCC Part 15C / ISED**：民用 ISM 频段无意发射与辐射抑制；
* **ANSI/BHMA A156.36 / A156.25 (加装与电子锁)**：Grade 1 / 2 机械冲撞寿命（25万次）与电机拉力测试；
* **CCPA / CPRA (加州隐私法案)**：免责声明中必须显式标明“Do Not Sell or Share My Personal Information”，B2B 留资与访客行为追踪需明示 Cookie Banner。

### 3. 中东海湾地区（GCC / SASO）
* **SASO IECEE 认证与 Saber 平台注册**：沙特强制要求整机符合 IEC 62368-1 安规并取得能效与耐高温认证；
* **高温太阳辐射耐受 (IEC 60068-2-5)**：塑料外壳与硅胶必须具备 UL 94 V-0 阻燃与耐紫外线黄变（UV 1000h）。

### 4. 专利与自由运作（FTO）法律闭环
* **规避声明签署**：新品量产开模前，结构工程与 IP 团队必须对照《Nuki-Like 专利规避清单》逐项签署不侵权确认函（Non-Infringement Opinion），重点规避：
  - 锁芯三顶丝径向挤压（改用弹性夹头收紧）；
  - 双侧翻折翼形卡爪（改用 45° 旋转卡口或磁吸螺栓锁紧）；
  - 电动脱开轴向齿轮离合（改用单向超越离合器或超低反驱无刷电机）。
"""

if "海外多国家合规与数据安全合规清单" not in methodology:
    methodology = methodology + "\n" + compliance_chapter
    with open('docs/10_SMART_LOCK_RETROFIT_METHODOLOGY.md', 'w', encoding='utf-8') as f:
        f.write(methodology)
    print("Added compliance chapter to docs/10_SMART_LOCK_RETROFIT_METHODOLOGY.md")

