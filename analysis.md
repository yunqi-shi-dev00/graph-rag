# 问题数量减少分析

## 关键发现

在代码中找到了问题所在，在 `parallel_classified_question_generation` 函数中：

```python
# 问题分类定义（保持原有逻辑）
QUESTION_TYPES = {
    "factual": {
        "ratio": 1/6,
        "description": "事实型问题：获取指标、数值、性能参数等",
        "examples": [...]
    },
    "comparative": {
        "ratio": 1/6,
        "description": "比较型问题：比较不同材料、结构或方案等",
        "examples": [...]
    },
    "reasoning": {
        "ratio": 5/6,  # 注意这里
        "description": "推理型问题：机制原理解释，探究某种行为或结果的原因",
        "examples": [...]
    },
    "open": {
        "ratio": 3/6,
        "description": "开放型问题：优化建议，针对问题提出改进方法",
        "examples": [...]
    }
}
```

然后在生成问题时：

```python
# 创建所有问题类型的生成任务
question_tasks = []
for question_type, type_info in QUESTION_TYPES.items():
    num_questions = max(1, int(6 * type_info["ratio"]))  # 这里是关键！
    task = generate_questions_by_type_parallel(
        generator, 
        data_item["md_content"], 
        question_type,
        type_info,
        num_questions,  # 限制了每种类型的问题数量
        config
    )
```

## 问题原因

1. **比例计算问题**：
   - factual: 1/6 * 6 = 1个问题
   - comparative: 1/6 * 6 = 1个问题  
   - reasoning: 5/6 * 6 = 5个问题
   - open: 3/6 * 6 = 3个问题
   - **总计每个文本块只生成 1+1+5+3 = 10个问题**

2. **比例之和超过1**：
   - 1/6 + 1/6 + 5/6 + 3/6 = 10/6 = 1.67
   - 比例设置有误，总和应该等于1

3. **实际生成数量限制**：
   在 `generate_questions_by_type_parallel` 函数中：
   ```python
   # 优先选择长度适中的问题
   selected_questions = []
   for question in all_questions:
       if not isinstance(question, str):
           continue
           
       if 10 < len(question) < 200:
           selected_questions.append(question)
           if len(selected_questions) >= num_questions:  # 这里限制了数量
               break
   ```

## 计算验证

- 968个问题数据项
- 如果每个只保留约10个问题
- 968 / 10 ≈ 97个文本块
- 实际得到113个问题，说明有些文本块生成的问题更少

## 解决方案

1. 修正比例设置，使总和等于1
2. 增加每种类型的问题生成数量
3. 移除或调整 `num_questions` 限制