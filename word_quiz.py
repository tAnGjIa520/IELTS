#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
单词测试生成器
自动从test.md文件读取单词表格，生成随机测试题
支持英译中、中译英、混合模式
"""

import argparse
import random
import re
import os
import sys


def parse_markdown_table(file_path):
    """解析markdown文件中的表格数据"""
    words = []

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"错误: 找不到文件 {file_path}")
        return []
    except Exception as e:
        print(f"错误: 读取文件失败 - {e}")
        return []

    # 查找表格行
    lines = content.split('\n')
    in_table = False
    header_found = False

    for line in lines:
        line = line.strip()

        # 检测表格开始
        if '| 单词 | 解释 |' in line:
            header_found = True
            continue

        # 跳过表格分隔行
        if header_found and '|------|------|' in line:
            in_table = True
            continue

        # 解析表格数据行
        if in_table and line.startswith('|') and line.endswith('|'):
            # 移除首尾的 |，然后分割
            parts = line[1:-1].split('|')
            if len(parts) >= 2:
                word = parts[0].strip()
                explanation = parts[1].strip()

                # 跳过空行或无效行
                if word and explanation and word != '单词' and explanation != '解释':
                    words.append((word, explanation))

        # 如果遇到新的标题或非表格行，结束当前表格解析
        elif in_table and (line.startswith('#') or (line and not line.startswith('|'))):
            in_table = False
            header_found = False

    return words


def parse_range(range_str):
    """解析范围字符串，如 '1-99' 返回 (1, 99)，'50' 返回 (1, 50)"""
    if not range_str:
        return None, None

    try:
        if '-' in range_str:
            start, end = range_str.split('-', 1)
            return int(start.strip()), int(end.strip())
        else:
            # 如果只有一个数字，表示从第1题到第N题
            num = int(range_str.strip())
            return 1, num
    except ValueError:
        print(f"错误: 无效的范围格式 '{range_str}'，请使用 '1-99' 或 '50' 格式")
        return None, None


def generate_quiz(words, mode='en2zh', output_file='quiz.md', word_range=None):
    """生成测试题并输出到markdown文件"""
    if not words:
        print("错误: 没有找到有效的单词数据")
        return

    # 根据范围筛选单词
    if word_range:
        start, end = word_range
        if start is not None and end is not None:
            # 验证范围有效性
            if start < 1 or end > len(words) or start > end:
                print(f"错误: 范围 {start}-{end} 超出有效范围 1-{len(words)}")
                return

            # 选择指定范围的单词 (转换为0-based index)
            selected_words = words[start-1:end]
            print(f"选择范围: {start}-{end} (共{len(selected_words)}个单词)")
        else:
            return
    else:
        selected_words = words.copy()

    # 随机打乱单词顺序
    shuffled_words = selected_words.copy()
    random.shuffle(shuffled_words)

    # 确定模式名称
    mode_names = {
        'en2zh': '英译中',
        'zh2en': '中译英',
        'mixed': '混合'
    }
    mode_name = mode_names.get(mode, '未知模式')

    # 生成markdown内容
    content = []
    content.append(f"# 单词测试 - {mode_name}模式")
    content.append("")
    content.append(f"## 测试题目 (共{len(shuffled_words)}题)")
    content.append("")

    # 生成问题表格
    if mode == 'en2zh':
        content.append("| 题号 | 单词 | 解释 |")
        content.append("|------|------|------|")
        for i, (word, explanation) in enumerate(shuffled_words, 1):
            content.append(f"| {i} | {word} |  |")
    elif mode == 'zh2en':
        content.append("| 题号 | 单词 | 解释 |")
        content.append("|------|------|------|")
        for i, (word, explanation) in enumerate(shuffled_words, 1):
            content.append(f"| {i} |  | {explanation} |")
    else:  # mixed mode
        content.append("| 题号 | 单词 | 解释 |")
        content.append("|------|------|------|")
        for i, (word, explanation) in enumerate(shuffled_words, 1):
            # 随机决定是英译中还是中译英
            if random.choice([True, False]):
                # 英译中
                content.append(f"| {i} | {word} |  |")
            else:
                # 中译英
                content.append(f"| {i} |  | {explanation} |")

    content.append("")
    content.append("---")
    content.append("")
    content.append("## 答案")
    content.append("")

    # 生成答案表格
    if mode == 'en2zh':
        content.append("| 题号 | 单词 | 解释 |")
        content.append("|------|------|------|")
        for i, (word, explanation) in enumerate(shuffled_words, 1):
            content.append(f"| {i} | {word} | <span style=\"color:red\">{explanation}</span> |")
    elif mode == 'zh2en':
        content.append("| 题号 | 单词 | 解释 |")
        content.append("|------|------|------|")
        for i, (word, explanation) in enumerate(shuffled_words, 1):
            content.append(f"| {i} | <span style=\"color:red\">{word}</span> | {explanation} |")
    else:  # mixed mode
        content.append("| 题号 | 单词 | 解释 | 题型 |")
        content.append("|------|------|------|------|")

        # 重新生成，保持与问题部分一致的随机选择
        random.seed(42)  # 使用固定种子确保一致性
        for i, (word, explanation) in enumerate(shuffled_words, 1):
            if random.choice([True, False]):
                # 英译中
                content.append(f"| {i} | {word} | <span style=\"color:red\">{explanation}</span> | 英译中 |")
            else:
                # 中译英
                content.append(f"| {i} | <span style=\"color:red\">{word}</span> | {explanation} | 中译英 |")

    # 写入文件
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(content))
        print(f"测试题已生成: {output_file}")
        print(f"模式: {mode_name}")
        print(f"题目数量: {len(shuffled_words)}")
    except Exception as e:
        print(f"错误: 无法写入文件 {output_file} - {e}")


def main():
    parser = argparse.ArgumentParser(description='单词测试生成器')
    parser.add_argument('--mode', '-m',
                       choices=['en2zh', 'zh2en', 'mixed'],
                       required=True,
                       help='测试模式: en2zh(英译中), zh2en(中译英), mixed(混合)')
    parser.add_argument('--output', '-o',
                       default='quiz.md',
                       help='输出文件名 (默认: quiz.md)')
    parser.add_argument('--range', '-r',
                       help='题目范围，格式: 1-99 或 50 (默认: 全部题目)')

    args = parser.parse_args()

    # 获取脚本所在目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    test_file = os.path.join(script_dir, 'test.md')

    # 解析单词数据
    print(f"正在读取文件: {test_file}")
    words = parse_markdown_table(test_file)

    if not words:
        print("未找到有效的单词数据，请检查test.md文件格式")
        sys.exit(1)

    print(f"成功读取 {len(words)} 个单词")

    # 解析范围参数
    word_range = None
    if args.range:
        start, end = parse_range(args.range)
        if start is not None and end is not None:
            word_range = (start, end)
        else:
            sys.exit(1)

    # 生成测试题
    output_path = os.path.join(script_dir, args.output)
    generate_quiz(words, args.mode, output_path, word_range)


if __name__ == '__main__':
    main()