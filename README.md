# 单词测试生成器 (Word Quiz Generator)

一个Python脚本，用于从Markdown表格文件中读取单词数据，自动生成随机化的单词测试题。

## 功能特性

- 🔀 **随机打乱**: 每次生成的测试题顺序都不相同
- 🎯 **多种模式**: 支持英译中、中译英、混合模式
- 📊 **表格格式**: 清晰的表格式输出，便于打印和使用
- 🎨 **彩色答案**: 答案用红色标注，醒目易识别
- 📏 **范围选择**: 可指定题目范围，如1-50题
- 📄 **Markdown输出**: 输出为标准Markdown格式文件

## 安装要求

- Python 3.6+
- 同目录下需要有 `test.md` 文件（包含单词表格）

## 使用方法

### 基本语法

```bash
python word_quiz.py --mode <模式> [选项]
```

### 必需参数

- `--mode`, `-m`: 测试模式
  - `en2zh`: 英译中（看英文单词，填写中文解释）
  - `zh2en`: 中译英（看中文解释，填写英文单词）
  - `mixed`: 混合模式（随机混合两种模式）

### 可选参数

- `--output`, `-o`: 输出文件名（默认: `quiz.md`）
- `--range`, `-r`: 题目范围（格式: `1-99` 表示第1到99题，`50` 表示第1到50题，默认: 全部题目）

## 使用示例

### 1. 英译中模式（全部单词）
```bash
python word_quiz.py --mode en2zh
```

### 2. 中译英模式（指定输出文件）
```bash
python word_quiz.py --mode zh2en --output chinese_to_english.md
```

### 3. 混合模式（指定范围）
```bash
python word_quiz.py --mode mixed --range 1-50
```

### 4. 测试前20个单词
```bash
python word_quiz.py --mode en2zh --range 20
```

### 5. 测试前100个单词
```bash
python word_quiz.py --mode zh2en --range 100 --output first_100.md
```

### 6. 测试第10到第30题
```bash
python word_quiz.py --mode mixed --range 10-30
```

## 输入文件格式

脚本需要读取同目录下的 `test.md` 文件，文件应包含如下格式的表格：

```markdown
# 章节标题

| 单词 | 解释 |
|------|------|
| atmosphere | n. 大气层, 大气圈; 气氛 |
| hydrosphere | n. 水圈; 大气中的水气; |
| lithosphere | n. 岩石圈 |
```

## 输出格式示例

### 问题部分
```markdown
# 单词测试 - 英译中模式

## 测试题目 (共10题)

| 题号 | 单词 | 解释 |
|------|------|------|
| 1 | atmosphere |  |
| 2 | hydrosphere |  |
| 3 | lithosphere |  |
```

### 答案部分
```markdown
## 答案

| 题号 | 单词 | 解释 |
|------|------|------|
| 1 | atmosphere | <span style="color:red">n. 大气层, 大气圈; 气氛</span> |
| 2 | hydrosphere | <span style="color:red">n. 水圈; 大气中的水气;</span> |
| 3 | lithosphere | <span style="color:red">n. 岩石圈</span> |
```

## 文件结构

```
项目目录/
├── word_quiz.py    # 主程序
├── test.md         # 单词数据文件
├── README.md       # 说明文档
└── quiz.md         # 生成的测试题（默认输出）
```

## 注意事项

1. **文件编码**: 确保 `test.md` 文件使用 UTF-8 编码
2. **表格格式**: 表格必须包含 `| 单词 | 解释 |` 表头
3. **范围限制**: 指定的范围不能超出实际单词数量
4. **输出覆盖**: 如果输出文件已存在，会被覆盖

## 错误处理

- 如果 `test.md` 文件不存在，程序会报错并退出
- 如果指定的范围无效，程序会显示错误信息
- 如果表格格式不正确，程序会跳过无效行

## 版本信息

- 版本: 1.1.0
- 支持Python版本: 3.6+
- 最后更新: 2024年

## 开发者说明

### 功能扩展
如需添加新功能，可以修改以下部分：
- `parse_markdown_table()`: 解析不同格式的输入文件
- `generate_quiz()`: 修改输出格式或添加新的测试模式
- `main()`: 添加新的命令行参数

### 自定义
- 修改 `mode_names` 字典可以更改模式显示名称
- 调整 HTML 样式可以改变答案的显示效果
- 修改随机种子可以控制题目的随机化程度

## 许可证

此项目仅用于学习和个人使用。

---

💡 **提示**: 建议将生成的测试题打印出来，或在支持Markdown渲染的编辑器中查看以获得最佳体验。