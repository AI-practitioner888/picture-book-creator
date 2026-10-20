# 尺寸比例词库

AI 生成画面时经常出现比例失调问题：房子像狗窝、船小得坐不下人、碗比头还大。
根本原因是 prompt 中只用"大""小"这类模糊词，AI 没有尺度参照系。

**核心原则：用具体参照物描述大小，不用模糊形容词。**

---

## 比例校验原则

### 为什么"大"和"小"没用

- AI 不知道你说的"大房子"是相对于什么来说大——相对于蚂蚁？相对于人？相对于山？
- 不同模型对尺寸的理解差异很大
- 画面构图（特写 vs 远景）会进一步放大比例感知的偏差

### 正确做法：锚定参照物

在每页 prompt 中加入一个**已知尺寸的参照物**，帮助 AI 建立尺度感。

最常用的参照物：
1. **人物身高**：儿童约 120cm，成人约 170cm
2. **门的高度**：普通房门约 2 米 = 一个成人身高
3. **床的长度**：单人床约 2 米

**比例校验公式**：
- 房屋高度 = 2-3 个成人高（4-6 米）
- 桌子高度 = 成人腰的高度（约 75cm）
- 椅子坐面高度 = 成人膝盖高度（约 45cm）
- 碗的直径 = 成人手掌宽度（约 12cm）

---

## 常用物体比例描述词库

### 房屋类

| 中文名称 | 英文描述词 | 正常尺寸参照 |
|---------|-----------|-------------|
| 茅草屋 | thatched cottage, small one-story house | 约3米高 = 1.5个成人高，只能住1-2人 |
| 瓦房 / 土坯房 | tile-roofed house, mud-brick house | 约4-5米高 = 2-3个成人高，有门有窗 |
| 砖房 / 四合院 | brick house, courtyard home | 约5-6米高 = 3个成人高，多间房屋 |
| 芦苇屋 / 草棚 | reed hut, straw shelter | 约2米高 = 1个成人高，低矮简陋 |
| 小木屋 | wooden cabin | 约3.5米高 = 2个成人高，森林小屋大小 |
| 塔楼 / 碉楼 | tower, watchtower | 约8-10米高 = 5个成人高，多层结构 |

**Prompt 示例**：

```
# ❌ 模糊
a small house

# ✅ 有比例
a small thatched cottage, about the height of 2 adults,
with a wooden door just tall enough for a person to enter,
one-story rural dwelling
```

---

### 车船类

| 中文名称 | 英文描述词 | 载客量 / 尺寸参照 |
|---------|-----------|-----------------|
| 小木船 | small wooden rowboat | 坐2-3人，长约3米 |
| 乌篷船 | black-awning wooden boat, wupeng boat | 坐4-6人，长约5米，有篷顶 |
| 渡船 / 摆渡船 | ferry boat | 载10-20人，长约8-10米 |
| 牛车 | ox cart, bullock cart | 坐2-4人，有两个大木轮 |
| 马车 | horse-drawn carriage | 坐2-4人，有篷或敞篷 |
| 独轮车 | wooden wheelbarrow | 推1人或货物，一个大轮子 |
| 轿子 / 花轿 | sedan chair, bridal sedan chair | 坐1人，4人抬 |

**Prompt 示例**：

```
# ❌ 模糊
a boat on the river

# ✅ 有比例
a small wooden rowboat, just big enough for 2 children sitting inside,
about 3 meters long, with oars, floating on the river
```

---

### 家具类

| 中文名称 | 英文描述词 | 正常比例参照 |
|---------|-----------|-------------|
| 桌子（方桌/八仙桌） | wooden square table, eight-immortal table | 高约75cm = 成人腰高，桌面边长约1米 |
| 圆桌 | round wooden table | 高约75cm，直径约1.2米 |
| 椅子 | wooden chair | 坐面高约45cm = 成人膝盖高，靠背到人肩 |
| 长条凳 | wooden bench | 高约45cm，长约1.2米，坐2-3人 |
| 床（单人） | single bed, wooden bed | 长约2米，宽约1米，高约50cm |
| 炕 | kang, heated brick bed | 长约2.5米，宽约1.8米，高约60cm |
| 柜子 / 木箱 | wooden chest, cabinet | 高约1米 = 成人腰到胸，宽约80cm |
| 书架 | bookshelf | 高约1.8米 = 接近成人身高 |

**Prompt 示例**：

```
# ❌ 模糊
a table and chairs in the room

# ✅ 有比例
a square wooden table of normal height (about waist-high),
with 4 wooden chairs around it, chair seats at knee level,
properly proportioned furniture
```

---

### 日常物品类

| 中文名称 | 英文描述词 | 正常比例参照 |
|---------|-----------|-------------|
| 碗 | ceramic bowl, rice bowl | 直径约12cm = 成人手掌宽 |
| 杯子 / 茶碗 | teacup, cup | 直径约8cm，高约10cm = 拳头大小 |
| 灯笼（圆） | round paper lantern | 直径约30cm = 两个拳头大 |
| 灯笼（长） | long red lantern | 高约50cm，直径约20cm |
| 书包 / 布包 | cloth bag, school bag | 约30x40cm = 一个书包大小 |
| 篮子 | bamboo basket | 直径约30cm，高约20cm |
| 雨伞 | oil-paper umbrella | 直径约1米 = 成人一臂长 |
| 扇子 | folding fan, palm-leaf fan | 展开约30cm宽 = 脸的大小 |
| 书本 | book, storybook | 约15x20cm = 巴掌大到A4大小 |
| 油灯 | oil lamp | 高约20cm = 小臂长度 |

---

### 食物类（绘本常见）

| 中文名称 | 英文描述词 | 正常比例参照 |
|---------|-----------|-------------|
| 包子 / 馒头 | steamed bun, mantou | 直径约8cm = 拳头大小 |
| 月饼 | mooncake | 直径约10cm，厚约3cm |
| 粽子 | zongzi, rice dumpling | 约拳头大小（10cm左右） |
| 饺子 | dumpling, jiaozi | 约5cm长 = 半个手掌 |
| 糖葫芦 | tanghulu, candied hawthorn | 一串约20cm长 = 小臂一半 |

---

### 动植物类

| 中文名称 | 英文描述词 | 正常比例参照 |
|---------|-----------|-------------|
| 猫 / 小猫 | cat, kitten | 肩高约25cm，身长约50cm = 小臂长 |
| 狗（小型） | small dog, puppy | 肩高约30cm = 小腿高 |
| 兔子 | rabbit, bunny | 身长约40cm（含耳约50cm） |
| 鸡 / 母鸡 | hen, chicken | 高约40cm = 膝盖高 |
| 鸭子 | duck | 高约30cm |
| 牛 / 水牛 | cow, water buffalo | 肩高约1.5米 = 成人胸口高 |
| 马 | horse | 肩高约1.5米 = 成人胸口高 |
| 大树 | big tree, large tree | 高约5-10米 = 3-5个成人高 |
| 小树 / 树苗 | sapling, young tree | 高约1-2米 = 一个成人高或更矮 |
| 花 | flower | 高度约10-30cm = 手的大小 |

---

## 比例错误自检清单

生成图片后，快速对照以下问题检查，5秒即可发现比例问题：

### 房屋场景
- [ ] 门的高度 ≈ 1个成人高（约2米）？
- [ ] 房子的高度 ≈ 2-3个成人高？
- [ ] 窗户的大小 ≈ 半个人高？
- [ ] 台阶高度 ≈ 人小腿的一半（约20cm）？

### 室内场景
- [ ] 桌子高度 ≈ 成人腰高（约75cm）？
- [ ] 椅子坐面 ≈ 成人膝盖高（约45cm）？
- [ ] 床的长度 ≈ 1个成人身高（约2米）？
- [ ] 碗/杯子的大小 ≈ 手的大小？

### 户外场景
- [ ] 船的大小能坐下人物吗？（小木船=2-3人）
- [ ] 树的高度 ≈ 几个成人高？
- [ ] 路/桥的宽度 ≈ 能走几个人？
- [ ] 车辆/交通工具和人的比例是否合理？

### 万能校验法
**找画面中已知尺寸的物体**（人、门、床最可靠），用它当"尺子"去量其他物体。
如果量出来明显不对，那就是比例错了，需要改 prompt 重画。

---

## 快速修复 Prompt 模板

当发现比例不对时，在原 prompt 末尾追加以下语句：

```
correct proportions, realistic scale,
[a child of about 120cm tall] is in the scene for size reference,
objects are properly sized relative to the person,
no oversized or undersized objects
```

**关键：参照物必须出现在画面里**，AI 才能用它建立尺度感。
如果画面中没有人，就用门或床作为参照。
