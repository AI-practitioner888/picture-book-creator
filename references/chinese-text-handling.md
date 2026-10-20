# 中文文字处理指南

AI 生成中文文字经常出现写错、变形、缺笔画等问题，这是绘本创作的高频坑。
本文档解释背后原理，并提供三种可落地的解决方案。

---

## 为什么 AI 画不准中文

### 根本原因

1. **训练数据量不足**：AI 模型训练集中，带中文文字的图片占比远低于英文，模型对中文字形的"记忆"不够准确。
2. **文字是高维信息**：中文汉字笔画多、结构复杂（上下/左右/包围结构），AI 在像素级别生成时容易出现笔画错位、粘连、缺失。
3. **生图模型的底层逻辑**：扩散模型是从噪声中"想象"画面，它理解的是"文字的视觉感觉"而非"文字的语义正确性"。

### 典型错误表现

- 笔画多的字缺胳膊少腿（如"瓣""囊""藏"）
- 左右结构的字左右写反（如"邻""部"）
- 整行字看起来"像中文"但一个也认不出来
- 同一页中，有的字对有的字错，毫无规律

**结论：不要指望 AI 生成可读的中文文字，这是一个系统性的、目前无法根治的问题。**
策略不是"让它写对"，而是"绕开它"。

---

## 三种解决方案

### 方案 A：HTML 文字层叠加（⭐ 推荐）

**适用场景**：绘本正文、对话气泡、标牌、书信等所有需要读者辨认的文字。

**原理**：AI 只生成画面，文字通过 HTML/CSS 叠加在图片上。文字是真实的 HTML 文本，100% 准确。

**实现方式**：

绘本模板已内置文字浮层功能（见 `assets/picture-book-template.html`），通过 `data-layout` 属性切换样式。
制作时只需将文字内容填入 `pages` 数组的 `text` 字段，模板自动渲染。

**进阶：对话气泡样式 CSS 模板**

如果需要在画面特定位置（如角色头顶）加对话气泡，可用以下 CSS 在 HTML 中自定义：

```css
/* 对话气泡通用样式 */
.speech-bubble {
  position: absolute;
  background: rgba(255, 255, 255, 0.95);
  color: #333;
  padding: 12px 18px;
  border-radius: 18px;
  font-size: 16px;
  line-height: 1.5;
  max-width: 60%;
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

/* 气泡尾巴 —— 朝下（角色在下方说话） */
.speech-bubble.bottom-tail::after {
  content: '';
  position: absolute;
  bottom: -10px;
  left: 30px;
  border-width: 10px 10px 0;
  border-style: solid;
  border-color: rgba(255,255,255,0.95) transparent transparent;
}

/* 气泡尾巴 —— 朝上 */
.speech-bubble.top-tail::after {
  content: '';
  position: absolute;
  top: -10px;
  right: 30px;
  border-width: 0 10px 10px;
  border-style: solid;
  border-color: transparent transparent rgba(255,255,255,0.95);
}

/* 定位示例 —— 左上角气泡 */
.bubble-top-left {
  top: 8%;
  left: 5%;
}

/* 定位示例 —— 右下角气泡 */
.bubble-bottom-right {
  bottom: 15%;
  right: 5%;
}
```

**使用建议**：
- 正文 narration 用底部浮层（模板默认样式）
- 角色对话用气泡样式，气泡位置根据角色站位调整
- 标牌/书信类可加半透明背景卡片，文字叠加在卡片上

---

### 方案 B：画面留白 + 后期排版

**适用场景**：封面书名、章节标题、扉页文字等需要设计感的大字号文字。

**原理**：生图时在 prompt 中指定留白区域，生成后用设计工具（PS/Figma/PPT）手动排版。

**Prompt 写法**：

```
... [画面内容], large empty clear space at the top third of the image,
clean negative space reserved for title, no text in image,
soft gradient background in the empty area, storybook cover style
```

**留白位置关键词**：

| 留白位置 | Prompt 关键词 |
|---------|--------------|
| 上方 1/3 | `large empty space at top third, reserved for book title` |
| 下方 1/3 | `clear negative space at bottom third` |
| 居中圆形 | `circular empty area in the center, surrounded by [装饰元素]` |
| 左侧竖排 | `vertical empty space on left side` |

**后期排版工具推荐**：
- **简单快速**：PPT / 可画（Canva）/ 图怪兽
- **专业精细**：Figma / Photoshop
- **国风字体**：站酷快乐体、汉仪粗圆体、叶根友字体（注意商用授权）

---

### 方案 C：Prompt 中模糊化处理

**适用场景**：文字不是主体、只是环境氛围的一部分，不需要读者辨认。
例如：远处店铺的招牌、墙上的张贴画、书本上模糊的文字感。

**原理**：不要求 AI 写具体的字，而是用"有文字的感觉"这类描述，让它生成视觉上类似文字的图案。

**Prompt 写法**：

```
# ❌ 不要这样写（AI 会试图写出具体字，结果很糟）
a sign that says "平安药店"

# ✅ 这样写（AI 生成"像有字的招牌"的视觉效果）
a wooden shop sign with indistinct Chinese characters,
blurry text on the sign, lettering suggestion,
the text is not legible, just the feeling of writing
```

**模糊化关键词库**：
- `indistinct characters` 模糊的字
- `suggestion of writing` 书写的暗示
- `illegible text` 不可辨认的文字
- `soft blurred lettering` 柔和模糊的刻字
- `the feeling of calligraphy` 书法的感觉
- `decorative script patterns` 装饰性文字图案

---

## 绝对不要让 AI 生成的场景

以下场景**必须**使用方案 A 或 B，绝不能指望 AI 直接生成：

| 场景 | 错误做法 | 正确做法 |
|------|---------|---------|
| 绘本正文文字 | 让 AI 把文字画在图里 | HTML 文字浮层（方案A） |
| 封面书名 | 让 AI 写出书名 | 画面留白+后期排版（方案B） |
| 角色对话气泡 | 让 AI 画气泡里的字 | HTML 气泡叠加（方案A） |
| 商店招牌/路牌 | prompt 里写具体店名 | 模糊化处理（方案C），或HTML叠加 |
| 书信/纸条内容 | 让 AI 画信上的字 | HTML 半透明卡片叠加 |
| 课本/作业上的题 | 让 AI 画题目 | 后期P上去，或改画无字书本 |
| 章节标题页 | 让 AI 写字在图上 | 留白+后期排版（方案B） |

---

## 特殊场景处理技巧

### 沙地写字 / 泥地写字

孩子在沙地上写字是绘本常见画面。处理方式：

```
# Prompt 写法
child drawing lines in the sand with a stick,
abstract wavy lines and shapes in sand,
suggestion of writing but not actual characters,
the drawing is childlike and messy,
soft sunlight, beach scene
```

**要点**：强调"孩子画的""乱的""线条"，而不是"写了XX字"。
如果剧情需要明确是某个字（如孩子写自己的名字），则用 HTML 在沙地位置叠加文字，
调整文字透明度和混合模式（如 `mix-blend-mode: multiply`），让字看起来像刻在沙里。

### 黑板写字 / 白板写字

```
# Prompt 写法
a blackboard with chalk dust smudges,
faint chalk marks, suggestion of writing,
the text is not legible, classroom setting,
soft chalk dust texture
```

如果需要黑板上有明确内容，用 HTML 叠加粉笔字体效果：

```css
.chalk-text {
  font-family: "楷体", "KaiTi", serif;
  color: rgba(255, 255, 255, 0.85);
  text-shadow: 0 0 2px rgba(255,255,255,0.5);
  letter-spacing: 0.1em;
}
```

### 灯笼 / 春联 / 匾额

这些场景的文字往往是画面的视觉焦点。

**推荐方案**：画面生成无字版本 → HTML 叠加书法字体文字 → 调整文字的透视/旋转匹配画面角度。

如果是正面对称的灯笼/匾额，HTML 正中央叠加即可，不需要复杂变形。
如果有透视角度（如仰拍的匾额），可用 CSS `transform: perspective() rotateX()` 模拟透视。
