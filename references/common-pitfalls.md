# 绘本创作常见问题与解决方案

基于真实项目经验总结的避坑指南。遇到以下问题时，按对应方案处理。

---

## 问题 1：ImageGen 并行生图文件互相覆盖

**现象**：多页同时调用 ImageGen，生成的文件时间戳相同，后生成的覆盖先生成的。

**解决方案**：
- 多页生图采用串行策略：每次只调用一个 ImageGen，等待结果后再调用下一个
- 或为不同批次使用不同的 output_dir（如 `outputs/batch1/`、`outputs/batch2/`）
- 串行是最可靠的方案，虽然稍慢但不会丢图

**检测方法**：
```bash
ls -lt outputs/  # 检查文件修改时间，同秒即存在覆盖
```

---

## 问题 2：相邻页面画面雷同

**现象**：比如 P5 和 P6 都是户外大场景，两张图看起来像同一张。

**根本原因**：prompt 中构图、光线、场景类型没有明确区分。

**解决方案（三选一或多选组合）**：

| 策略 | 操作 | 示例 |
|------|------|------|
| 构图区分 | 一页用 close-up，另一页用 wide scene | P5: "extreme close-up" → P6: "wide crowd scene" |
| 时间区分 | 一页黄昏，另一页白天 | P5: "winter noon sunlight" → P6: "twilight winter evening" |
| 场景区分 | 一页室内，另一页室外 | P5: "inside muddy house, dim" → P6: "open threshing ground" |
| 氛围区分 | 一页激烈，另一页宁静 | P13: "howling gale, dramatic" → P14: "gentle breeze, peaceful" |

**检查清单**：每写完一组相邻页的 prompt，确认至少两个维度不重复。

---

## 问题 3：角色形象不稳定

**现象**：同一角色的外貌、穿着、体型在不同页面中变化明显。

**解决方案**：
1. 每页 prompt 末尾固定追加完全相同的角色描述块（一字不改）
2. 第一个页面跑出满意形象后，作为"定妆照"保存
3. 后续页面如平台支持，使用图生图模式以定妆照为参考
4. Midjourney 用户可使用 `--cref [定妆照URL]` 参数

**角色描述块示例**：
```
same white bunny character, long soft ears, round black eyes, fluffy white fur, cute innocent expression
```

---

## 问题 4：画面与文字内容不匹配

**现象**：图生成了但和故事描述的场景/距离/空间关系不对。

**典型案例**："隔河相望" → 两个人都在河里离得很近。

**解决方案**：在 prompt 中显式写明空间关系关键词。
- 不够："a river between them" → 太模糊
- 正确："a wide river clearly dividing the frame into left and right banks, the two children are far apart on opposite sides of the river, significant distance between them"

**空间关系关键词库**：
- 远距离：far apart, distant, on the horizon, tiny figure, vast distance
- 近距离：close-up, extreme close-up, intimate, foreground
- 隔开/分隔：clearly dividing, separated by, on opposite sides
- 在一侧/对岸：on the left/right bank, across the river

---

## 问题 5：文字密度不匹配年龄段

| 年龄 | 每页字数 | 语言特征 | 句子结构 |
|:---:|:---:|---|---|
| 2-3岁 | 15-40字 | 叠词、拟声词为主 | 短句，重复句式 |
| 3-5岁 | 30-80字 | 简单因果，有节奏 | 短句+中度句，可朗读 |
| 5-7岁 | 50-120字 | 有情节推进 | 完整句子，可加入对话 |
| 8-12岁 | 80-200字 | 文学性，情感层次 | 长句+描写，散文气质 |

---

## 问题 6：HTML 绘本图片路径不对

**现象**：HTML 引用本地图片 `p01.png` 但浏览器找不到。

**解决方案**：
- 所有图片和 HTML 放在**同一个目录**下
- HTML 中使用相对路径：`src="p01.png"` 而非绝对路径
- 图片命名统一用 `p01.png` ~ `pN.png` 格式

---

## 问题 7：AI 年代穿帮

**现象**：1960年代乡村故事生成了现代建筑、塑料物品、现代服装。

**解决方案**：Prompt 中锁定以下关键词：
- 建筑：mud-brick house, adobe, thatched roof, red brick 1960s building
- 服装：patched cotton clothes, traditional Chinese rural clothing, no modern fabrics
- 道具：oil lamp (not electric), wooden table, earthen floor
- 环境：dirt path, well, haystack, no paved roads, no cars
- 显式排除：no modern elements, no cars, no plastic, no electronics

---

## 问题 8：镜子 / 倒影里角色不一致

**现象**：画面中有镜子、水面等反射场景，但倒影里的角色和本尊对不上——
发型不同、表情相反、甚至性别都变了。

**根本原因**：AI 生成反射时是"重新画了一个角色"，而不是"复制本尊翻转"，
所以左右可能是反的，细节也对不上。

**解决方案**：

### Prompt 写法（核心关键词）

```
... [场景描述], there is a mirror/water surface reflecting the character,
IDENTICAL reflection, perfect mirror image,
the reflection is exactly the same as the character,
same face same clothes same expression in the reflection,
no differences between character and reflection
```

### 关键必加词

| 关键词 | 作用 |
|--------|------|
| `IDENTICAL reflection` | 强调反射完全一致（全大写更容易被AI注意到） |
| `perfect mirror image` | 明确是镜像而非另画一个 |
| `exactly the same` | 强化一致性要求 |

### 如果 AI 还是画不对

- **简化场景**：尽量减少反射场景，或者反射只照到背景不照到人
- **后期处理**：把本尊的图翻转后P到镜子/水面位置（PS/Figma几秒钟搞定）
- **换角度**：让角色背对镜子，读者看不到反射的脸

---

## 问题 9：AI 画错中文文字

**现象**：画面中的中文文字写错、变形、缺笔画，看起来"像中文但一个也认不出来"。

**根本原因**：AI 模型对中文字形的训练不足，扩散模型是从噪声中"想象"文字，
理解的是"文字的视觉感觉"而非"文字的语义正确性"。

**解决方案**：不要指望 AI 写对字，策略是"绕开它"。根据场景选择方案：

| 场景 | 推荐方案 | 说明 |
|------|---------|------|
| 绘本正文 / 对话 | HTML 文字浮层 | 文字是真实HTML文本，100%准确 |
| 封面书名 / 章节标题 | 画面留白 + 后期排版 | 生图时留空，后期用设计工具加字 |
| 背景招牌 / 远镜头文字 | Prompt 模糊化处理 | 只暗示"有字"的感觉，不要求可辨认 |

**详细操作指南见**：`references/chinese-text-handling.md`

**一句话原则：需要读者辨认的文字，一律不要让 AI 直接生成。**

---

## 问题 10：关键物体比例失调

**现象**：房子像狗窝、船小得坐不下人、碗比头还大、桌子只有膝盖高。

**根本原因**：Prompt 中只用"大""小"这类模糊形容词，AI 没有尺度参照系。

**解决方案**：

### 1. 用参照物锚定比例

在每页 prompt 中加入一个已知尺寸的参照物，帮助 AI 建立尺度感：

```
a child of about 120cm tall is in the scene for size reference,
objects are properly proportioned relative to the child
```

### 2. 具体描述代替模糊形容词

```
# ❌ 不要这样
a small house
a big table

# ✅ 要这样
a house about 3 meters tall (height of 2 adults)
a table at waist height, about 75cm tall
```

### 3. 生图后快速校验

用画面中的人物当"尺子"：
- 门 ≈ 1个成人高（约2米）？
- 房子 ≈ 2-3个成人高？
- 桌子 ≈ 成人腰高？
- 船能坐下人物吗？

**完整比例词库和自检清单见**：`references/size-proportion-lexicon.md`

---

## 问题 11：跨页风格漂移（v2 新增，最高发问题）

**现象**：角色是同一个人，但每一页像不同人画的——P3 色温偏冷、P7 突然出现厚涂笔触、
P10 纸纹消失、P12 对比度变高。单张看都不错，翻起页来"一本书五个画风"。

**根本原因**：纯文本 prompt 每张图都是独立采样，风格词写得再细也会漂移。
AI 生图对"媒介/笔触/纸纹"这类抽象风格词的遵循度远低于对"角色/物体"的遵循度。
只锁角色不锁风格，必然漂移。

**解决方案（按优先级，组合使用）**：

### 1. 冻结风格块（必做）

把风格描述压缩成一段 STYLE-BLOCK，全书一字不改，放在每页 prompt 最前面。
模板见 `references/prompt-templates.md` 各风格「STYLE-BLOCK」。
禁忌：逐页改写法、换同义词、调语序——任何改动都会引入新的采样分布。

### 2. 负向词压制（必做）

每页附带该风格的 NEGATIVE-BLOCK，把最常见的漂移形态写进排除项：
3D 渲染感、照片级真实、厚涂油画、高饱和霓虹、矢量干净感等。
负向词对"防止风格跑偏"比正向词更有效。

### 3. 图生图锚定（最强手段）

第一张图（定妆照）满意后，后续每张以它为参考图生成。
参考图传递的是"画过的事实"，比任何文字描述都硬。
详见 `references/prompt-templates.md` 通用技巧第 5 条「风格锚定工作流」。

### 4. 中段校准（防累积漂移）

每 4-5 页把最新图与第一张并排比对（缩略图即可），
色温/笔触/纸纹/对比度任一维度肉眼可见地漂移，立即用第一张重新图生图覆盖，
不要带着漂移继续画后面的页——漂移只会累积不会自愈。

### 5. 检测方法

```
把所有页缩略图拖进同一文件夹，用系统预览的缩略图视图（或拼图工具）整体扫一眼：
健康的书 = 远看像一个人画的，近看每页内容不同
漂移的书 = 远看就五彩斑斓，每页气质各异
```

**一句话原则：风格靠"冻结 + 锚定"，不靠"写得细"。**

## 问题 12：文字卡遮挡画面主体（v2.1 新增，v2.1.1/v2.1.2 两轮实战迭代，HTML 组装阶段高发）

**现象**：插图本身张张满意，但 HTML 翻起来好几页"主角被压住"——
侧边卡片垂直居中压在角色身上，或底部浮层盖住了角色的关键动作。
单看生图完全没问题，问题全部出在组装阶段。

**根本原因**：layout 是逐页手填的，但填的时候没有对照该页插图的主体方位，
习惯性全部填同一种（八成是默认值）。侧边卡片 42% 宽度 + 垂直居中，
恰好覆盖画面中段——而绘本构图的主角十次有九次在中段。

**解决方案（layout 选择规则，按优先级）**：

### 1. 首选 bottom 横版底部带——默认就它，别再折腾

文字沿画面下缘的"地平线"（床面/窗台/草地/地板）横铺，白字坐在渐变暗带上，
文字像是长在画面里——这是绘本文字的母语。**实战三轮反馈的最终结论**：
全书统一 bottom 被认可；任何"挂字"方案（白卡片 → 四角浮字）都被判"不自然"。

bottom 渐变的上缘是透明渐隐区（约从文字块顶开始），角色的脸和关键动作
在画面中上部时完全不受影响；主体中下部被渐变压暗不是缺陷——暗下去
反而融入夜色/氛围。只有当主体完全居中、且底部本身就是关键叙事区时，
才换 layout（见第 3 条）。

### 2. 先看主体，再定例外

组装 HTML 前把全部页面缩略图并排看一遍，只做一个判断：
**有没有哪一页，主体完全居中且 bottom 会压掉关键叙事？**
- 没有 → 全书 bottom，一个字都别改
- 有 → 那一页用四角浮字，其余仍 bottom

### 3. 四角浮字是备选，不是首选

`side-tr / side-tl / side-br / side-bl` 四角浮字变体（宽 40%）仅用于
第 2 条判定的例外页。样式为**无框浮字**：极淡奶雾渐变底
（rgba(255,253,248,0.52→0.32)）+ 深暖灰字（#3f3a36）+ 白色 text-shadow 晕边，
让纸纹从字底透出来。

**不要用不透明白底卡片**（白底 + 圆角 + 边框 + 投影）——位置再淡也像一块补丁
贴在水彩画上，文字和插图是"两张皮"。更不要为了"避让"把全书拆成七八种
layout——形态不统一，翻页像换了一本书。实战反馈排序：
**底部横带（自然） > 四角浮字（像挂字） > 白底卡片（像补丁）。**
判据：文字要像"画在纸上"，不能"贴在纸上"，更不能"挂在角上"。

### 4. `split` 不是万能的

`split`（上图下文）确实零遮挡，但图片只显示上部 62%，
主体偏下的页面（坐姿/睡姿/站在光池里）会被切掉角色下半身。
只有主体在画面上半部时才用 split。

### 5. 验证动作（必做）

HTML 组装完成后，用无头浏览器逐页截图过一遍：
渐变上缘有没有吃掉主角的脸/关键道具？文字和背景对比度够不够？
肉眼判据只有一条：**翻页时，眼睛先看到的是故事，不是文字。**

**一句话原则：layout 是构图的下半场——文字带沿着画面的地平线走，
和插图说同一种语言；避让是例外，统一才是默认。**

## 问题 13：组装阶段图片全黑（data URI 前缀缺失，v2.1.3 新增）

**现象**：HTML 组装完成，无头浏览器截图发现插画区域全部黑屏/空白，
但文字、翻页、页码都正常。控制台报 `net::ERR_INVALID_URL` 或 `ERR_FILE_NOT_FOUND`。

**根本原因**：模板的占位符 `coverImage: "__COVER_IMAGE__"` 和 pages JSON 里的
`image` 字段**都不含 data URI 前缀**。如果组装脚本只把纯 base64 字符串塞进去，
浏览器会把 `AAAA...` 当作相对 URL 去加载——必然失败。

**解决方案**：base64 编码函数必须返回完整 data URI：

```python
def b64(fp):
    return 'data:image/png;base64,' + base64.b64encode(open(fp, 'rb').read()).decode()
```

**快速诊断**：截图全黑时，先用 playwright dump `document.images`，
看 `naturalWidth` 是否为 0 且 `complete` 为 true——是则资源加载失败，
查 data URI 前缀；`naturalWidth > 0` 但仍黑屏才是渲染/时机问题。

## 问题 14：并行生图时间戳覆盖（v2.1.3 强化）

同一秒内发起多个 ImageGen 调用，输出文件名按时间戳生成——并行调用会
写到同一个文件，后写的覆盖先写的，**返回值里的 localPath 还是那个路径，
不报错**，丢图无从察觉。实测：3 个并行调用只落盘 1 张。

**解决方案**：多页生图一律串行，一次一张，生成→质检→下一张。
宁可慢，不可丢。

## 问题 15：批量去水印的三个工具链坑（v2.2.0 新增）

ImageGen 出图默认带小水印，用 `buddy-image-processing.py image-edit --operation erase`
云端服务去除（约 30-60s/张）。多页批量时踩过三个坑：

1. **结果字段名不是 `images`**：CLI 的 stdout 含多段 JSON（提交状态 + 最终结果），
   且最终结果里图片路径在 `result_files[].path`，不是 `images[].path`。
   解析必须逐个 `JSONDecoder().raw_decode()` 解码所有 JSON 对象再取含路径的那个，
   或直接正则抓 `"path": "..."`。
2. **token 中途过期**：`connect_cloud_service` 返回的 clientTempToken 有效期约 40-60 分钟，
   20 张批量跑 15 分钟以上就可能中途 `AUTHENTICATION_EXPIRED`——**每轮批处理都要
   重新取一次 token**，并在脚本里检测到连续鉴权失败立即中止（别把时间烧在重试上）。
3. **失败不覆盖原图**：erase 失败时不要动原图；成功时把结果 copyfile 覆盖、删临时文件。
   WorkBuddy 会话目录下会残留 `processed_image_*` 临时文件，跑完记得清理。

**一句话：批处理去水印 = 新 token + raw_decode 解析 result_files + 失败保留原图。**
