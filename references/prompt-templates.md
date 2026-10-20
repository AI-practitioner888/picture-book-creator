# 绘本生图 Prompt 模板库（v2 · 风格一致性强化版）

本文档为不同风格的儿童绘本提供可复用的 ImageGen prompt 模板。
使用方式：根据绘本风格选择合适的模板，将 `[替换变量]` 替换为实际内容。

**v2 核心变更：引入「冻结风格块」机制。** 纯文本 prompt 每张图都会重新采样，
色温、笔触、纸纹必然漂移——这是"角色一样但每页像不同人画的"的根因。
对策：把风格描述压缩成一段**全篇一字不改**的英文块（STYLE-BLOCK），
每页 prompt 都以它开头；再配合负向词库和图生图锚定，把风格锁死。

---

## 三段式 Prompt 组装公式（所有风格通用）

每一页的生图 prompt 按以下顺序组装，**方括号外的一切都是冻结的**：

```
[STYLE-BLOCK]        ← 冻结风格块：全篇一字不改（见各风格模板）
[场景描述]            ← 每页变化：场景 + 角色动作 + 情绪 + 光线
[CHARACTER-BLOCK]    ← 冻结角色块：定妆照确认后一字不改（见下）
[QUALITY-SUFFIX]     ← 固定质量后缀
```

- **STYLE-BLOCK**：媒介 + 笔触 + 色温 + 纸纹 + 渲染质感。这段是风格一致性的命门。
- **CHARACTER-BLOCK**：主角的完整外貌描述。第一张定妆照跑出满意效果后，
  把当时的 prompt 中的角色部分**原文冻结**，之后每页一字不改地追加。
  冻结后如需微调，只允许改一次并全书统一，不允许逐页各自微调。
- **负向词**：每页附带该风格的 NEGATIVE-BLOCK（见各风格），压制作风漂移。

---

## 模板 A：低幼水彩暖萌风（2-5岁）

适用主题：睡前故事、习惯养成、温馨日常。
角色示例：小兔子、小熊、小猫。

### STYLE-BLOCK（冻结风格块）

```
Soft watercolor children's book illustration, warm pastel palette with cream white base,
gentle wet-on-wet washes, soft bleeding edges, visible paper texture, loose brushstrokes,
muted low-contrast lighting, 2.5D flat perspective, rounded soft shapes,
hand-painted storybook aesthetic, dreamy cozy atmosphere
```

### CHARACTER-BLOCK 结构

```
same [角色名] character, [年龄] year old, [外貌描述], [颜色] fur,
large round innocent eyes, [标志性配饰]
```

### 场景 prompt 骨架

```
[STYLE-BLOCK], [场景描述], [角色名] [动作描述], [氛围词], storybook feel, cute innocent
```

### NEGATIVE-BLOCK（负向词，每页附带）

```
no 3D render, no photorealistic, no thick oil painting texture, no harsh saturated neon colors,
no dark horror mood, no sharp geometric vector look, no glossy digital shading
```

### 封面专用 prompt

```
[STYLE-BLOCK], children's book cover illustration,
[核心画面元素，如：a cute little bunny sitting on a moon],
large empty clear space at the top third of the image,
clean negative space reserved for book title,
soft gradient background in the empty area, no text in image,
dreamy starry atmosphere, storybook cover feel, high quality
```

> 封面与内页使用**同一个 STYLE-BLOCK**，这是封面-内页不断裂的关键。

### hex 色板（写进 prompt 时优先用色名+hex 双保险）

| 角色 | 色值 | 英文色名 |
|------|------|----------|
| 主色·暖粉 | `#F7C8D0` | soft warm pink |
| 底色·奶油白 | `#FBF3E4` | cream white |
| 辅色·淡蓝 | `#BBD7E8` | powder blue |
| 点缀·薄荷绿 | `#C9E4D5` | mint green |
| 点缀·柔黄 | `#F5DE9B` | soft butter yellow |

### 氛围词库

- 温馨安静：warm and quiet, cozy, serene
- 好奇探索：curious, gentle wonder, dreamy
- 快乐开心：cheerful, joyful, sweet
- 困倦入睡：sleepy, dreamy, calm, peaceful

---

## 模板 B：写实水彩怀旧风（6-12岁）

适用主题：文学名著改编、成长故事、历史背景绘本。
年代特征：中国北方乡村 1960s-1980s，土坯房，芦苇荡，粗布衣。

### STYLE-BLOCK（冻结风格块）

```
Realistic watercolor illustration, nostalgic warm palette dominated by amber gold and earth brown,
visible cold-press paper grain, loose expressive brushstrokes with controlled color bleeds,
soft diffused golden-hour lighting, low saturation, cinematic composition,
literary storybook aesthetic, painterly texture, muted earth tones
```

### CHARACTER-BLOCK 结构

```
[角色描述], [年龄约X岁], [面部特征], [肤色], [穿着描述]
```

### 场景 prompt 骨架

```
[STYLE-BLOCK], [地点/年代], [场景描述], [角色] [动作/表情], [光线描述], [情绪氛围], storybook feel
```

### NEGATIVE-BLOCK

```
no modern elements, no neon colors, no 3D render, no digital glossy look, no high saturation,
no cartoon exaggeration, no clean vector shapes, no harsh studio lighting
```

### 封面专用 prompt

```
[STYLE-BLOCK], book cover illustration,
[核心画面元素，如：a young boy standing by a river at sunset],
1960s Chinese countryside setting,
large empty clear space at the top third of the image,
clean negative space reserved for book title,
soft golden sunset glow in the empty area, no text in image,
nostalgic atmosphere, cinematic composition, storybook cover feel, high quality
```

> 写实风格封面建议用大场景 + 人物剪影/远影，留白区融入天空/晚霞。

### hex 色板

| 角色 | 色值 | 英文色名 |
|------|------|----------|
| 主色·暖金黄 | `#D9A441` | amber gold |
| 主色·土棕 | `#8B6B4A` | earth brown |
| 辅色·深蓝 | `#3E5C76` | deep indigo blue |
| 点缀·暗红 | `#A4503C` | muted brick red |
| 点缀·灰绿 | `#8A9B7E` | sage grey green |

### 技巧要点

1. 显式写明年代 + 地点，防止 AI 生成现代元素
2. STYLE-BLOCK 中的 `nostalgic warm palette` 保证全篇色调统一（暖黄/金棕/深蓝）
3. 穿着/建筑描述具体化（"patched cotton clothes" "mud-brick house"）

---

## 模板 C：水墨淡彩国风（全年龄）

适用主题：中国传统文化、古诗词绘本、神话故事。

### STYLE-BLOCK（冻结风格块）

```
Traditional Chinese ink wash painting illustration, sumi-e aesthetic,
monochrome ink black with restrained ochre and cinnabar accents,
generous negative space, xuan rice paper texture, visible brush strokes with varying ink density,
soft watercolor washes, minimalist composition, poetic atmosphere, elegant simplicity,
oriental aesthetic, flat layered depth
```

### 场景 prompt 骨架

```
[STYLE-BLOCK], [场景], [角色], [动作], [季节/光线], traditional Chinese aesthetic
```

### NEGATIVE-BLOCK

```
no western oil painting texture, no 3D render, no thick impasto, no saturated colors,
no cartoon style, no modern clothing, no gradient mesh digital look, no cluttered composition
```

### 封面专用 prompt

```
[STYLE-BLOCK], book cover illustration,
[核心画面元素，如：a little scholar gazing at the moon],
elegant simplicity, poetic atmosphere,
large empty space at the top for vertical title calligraphy,
clean negative space with soft ink wash gradient,
no text in image, reserved for title placement,
minimalist composition, high quality
```

> 国风封面适合竖排书名，留白在上方或左侧均可。竖排左留白将 `at the top` 改为 `on the left side, vertical empty space`。

### hex 色板

| 角色 | 色值 | 英文色名 |
|------|------|----------|
| 主色·墨黑 | `#2B2B2B` | ink black |
| 留白·宣纸 | `#F5F0E6` | xuan paper white |
| 辅色·淡赭 | `#C9A876` | light ochre |
| 点缀·花青 | `#4A6B7C` | flower blue |
| 点缀·朱砂 | `#B04A3A` | cinnabar red |

---

## 模板 D：扁平卡通风（3-6岁）

适用主题：趣味科普、数字认知、生活习惯。

### STYLE-BLOCK（冻结风格块）

```
Flat vector illustration style, simple geometric shapes, bold bright color blocks,
clean uniform line weight, minimal details, no gradients, no texture,
children's book art, friendly and playful, cheerful high-key palette,
graphic design aesthetic, solid color fills
```

### 场景 prompt 骨架

```
[STYLE-BLOCK], [场景], [角色], [动作], children's book art, friendly and playful
```

### NEGATIVE-BLOCK

```
no watercolor texture, no brushstrokes, no 3D render, no realistic shading,
no gradients, no paper texture, no photographic elements, no muted colors
```

### 封面专用 prompt

```
[STYLE-BLOCK], children's book cover,
[核心画面元素，如：a happy cartoon dinosaur in a playful pose],
large empty clear space at the top third,
solid color background area reserved for book title,
no text in image, friendly and playful,
children's book cover design, high quality
```

> 扁平卡通封面的留白区建议用纯色或简单渐变，书名更醒目。

### hex 色板

| 角色 | 色值 | 英文色名 |
|------|------|----------|
| 主色·明黄 | `#FFC93C` | bright yellow |
| 主色·湖蓝 | `#3ABBC9` | lake blue |
| 辅色·草绿 | `#7FC98F` | grass green |
| 辅色·橘红 | `#FF7A59` | coral orange |
| 点缀·紫罗兰 | `#9B7EDE` | violet |

---

## 通用质量提升技巧

### 1. 避免"同一画面两张图"
不同页码的 prompt 必须在以下至少一个维度上拉开差距：
- **构图距离**：P5用"close-up / extreme close-up" → P6用"wide scene / crowd scene"
- **时间/光线**：黄昏 vs 清晨、暖光 vs 冷光
- **场景类型**：室内 vs 室外、特写 vs 远景
- **天气/季节**：雪景 vs 夏日、大风 vs 微风

### 2. Parallel generation 时间戳冲突
ImageGen 并行调用时，同秒生成的文件会互相覆盖。
**解决方案**：多页生图时串行执行，或为每批使用不同的 output_dir。

### 3. Prompt 末尾统一加 quality tags
```
high quality, storybook illustration, professional children's book art
```

### 4. 角色一致性（冻结机制）
- 所有页面使用**完全冻结**的角色描述块（一字不改）
- 第一张定妆照满意后，把角色部分原文冻结，禁止逐页微调
- 如果 AI 偏离角色形象，用图生图模式以前一页为参考
- Midjourney 用户可使用 `--cref` 参数

### 5. 风格锚定工作流 ⭐（v2 核心，跨页风格一致的最强手段）

纯文本无法 100% 锁风格，必须借用"参考图"通道。按优先级执行：

1. **第一张 = 三重身份**：全书第一张图（通常是封面或 P1）同时充当
   定妆照（锁角色）+ 风格锚点（锁色温/笔触/纸纹）+ 比例基准（锁尺度）。
   这张图要单独打磨到满意，不急着推进。
2. **后续页图生图**：每张新图都以第一张为参考图生成（图生图 / image-to-image），
   参考强度中高档（保持辨识度但不照搬构图）。
   - 本环境 ImageGen 工具支持传入参考图时，每页都传
   - 参考图只借"风格与角色"，场景描述仍以当页文字为准
3. **seed 固定（如工具支持）**：若生图工具暴露随机种子参数，全书固定同一 seed；
   不支持时跳过，以图生图为主。
4. **封面与 P1 同锚**：封面必须也用第一张锚定，或封面满意后反哺为锚。
5. **中段校准**：每生成 4-5 页，把最新一张与第一张并排比对，
   色温/笔触/纸纹任一维度明显漂移时，用第一张重新图生图覆盖该页。

### 6. 比例锚定技巧 ⭐
在每页 prompt 中加入一个**已知尺寸的参照物**，帮助 AI 建立尺度感，
避免"房子像狗窝""船太小"等比例失调问题。

**最常用参照物（选一个加在 prompt 末尾）**：
```
a child of about 120cm tall is in the scene for size reference,
objects are properly proportioned relative to the child
```

如果画面中没有人，用门/床/桌子替代：
```
a standard door about 2 meters tall, properly proportioned room
```

**核心原则**：用具体参照物描述大小，不用"大""小"模糊词。
完整比例词库见 `references/size-proportion-lexicon.md`。

### 7. 反射一致性 ⭐
画面中有镜子、水面、玻璃等反射场景时，必须加以下关键词，
否则倒影里的角色可能和本尊不一致（发型变、表情反、甚至性别变）。

```
IDENTICAL reflection, perfect mirror image,
the reflection is exactly the same as the character,
same face same clothes same expression in the reflection
```

> **注意**：`IDENTICAL` 全大写更容易被 AI 注意到。如果反射仍然不对，
> 考虑简化场景（反射只照背景不照人）或后期处理。

---

## 风格色板参考（中文速查）

| 风格 | 主色调 | 辅助色 | 光影 |
|------|--------|--------|------|
| 低幼水彩 | 暖粉 #F7C8D0、奶油白 #FBF3E4、淡蓝 #BBD7E8 | 薄荷绿 #C9E4D5、柔黄 #F5DE9B | 柔和均匀光 |
| 写实怀旧 | 暖金黄 #D9A441、土棕 #8B6B4A、深蓝 #3E5C76 | 暗红 #A4503C、灰绿 #8A9B7E | 夕阳侧光/逆光 |
| 水墨国风 | 墨黑 #2B2B2B、宣纸白 #F5F0E6、淡赭 #C9A876 | 花青 #4A6B7C、朱砂 #B04A3A | 自然光，散点透视 |
| 扁平卡通 | 明黄 #FFC93C、湖蓝 #3ABBC9、草绿 #7FC98F | 橘红 #FF7A59、紫罗兰 #9B7EDE | 无阴影/扁平投影 |

> 具体 hex 与英文色名以各风格模板内的色板表为准；prompt 中色名与 hex 并用效果最佳。
