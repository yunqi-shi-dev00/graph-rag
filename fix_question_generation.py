# 修复方案：修改 parallel_classified_question_generation 函数中的问题数量限制

# 方案1：修正比例，使总和等于1，并增加基础数量
QUESTION_TYPES_FIXED = {
    "factual": {
        "ratio": 0.15,  # 15%
        "base_count": 3,  # 基础数量
        "description": "事实型问题：获取指标、数值、性能参数等",
    },
    "comparative": {
        "ratio": 0.15,  # 15%
        "base_count": 3,  # 基础数量
        "description": "比较型问题：比较不同材料、结构或方案等",
    },
    "reasoning": {
        "ratio": 0.40,  # 40%
        "base_count": 8,  # 基础数量
        "description": "推理型问题：机制原理解释，探究某种行为或结果的原因",
    },
    "open": {
        "ratio": 0.30,  # 30%
        "base_count": 6,  # 基础数量
        "description": "开放型问题：优化建议，针对问题提出改进方法",
    }
}

# 方案2：不限制问题数量，保留所有生成的问题
async def parallel_classified_question_generation_unlimited(generator, qa_input_data, config, max_concurrent_questions):
    """并行分类问题生成 - 不限制数量版本"""
    
    async def generate_questions_for_item(data_item):
        """为单个数据项生成所有类型的问题"""
        try:
            logger.info(f"为 {data_item['paper_name']} 并行生成分类问题...")
            
            item_questions = {
                "paper_name": data_item["paper_name"],
                "source_content": data_item["md_content"],
                "questions": {},
                "source_info": data_item.get("source_info", {})
            }
            
            # 创建所有问题类型的生成任务
            question_tasks = []
            for question_type, type_info in QUESTION_TYPES_FIXED.items():
                # 不限制数量，让模型自由生成
                task = generate_questions_by_type_no_limit(
                    generator, 
                    data_item["md_content"], 
                    question_type,
                    type_info,
                    config
                )
                question_tasks.append((question_type, task))
            
            # 并行等待所有问题类型生成完成
            results = await asyncio.gather(
                *[task for _, task in question_tasks],
                return_exceptions=True
            )
            
            # 收集结果 - 保留所有生成的问题
            for i, (question_type, _) in enumerate(question_tasks):
                if not isinstance(results[i], Exception):
                    item_questions["questions"][question_type] = results[i]  # 保留所有问题
                else:
                    logger.error(f"生成{question_type}问题失败: {results[i]}")
                    item_questions["questions"][question_type] = []
            
            logger.info(f"为 {data_item['paper_name']} 生成的问题总数: {sum(len(q) for q in item_questions['questions'].values())}")
            return item_questions
            
        except Exception as e:
            logger.error(f"为 {data_item['paper_name']} 生成分类问题失败: {e}")
            return None
    
    # ... 其余代码保持不变

# 方案3：增加每种类型的问题生成数量
def calculate_question_counts(total_target=30):
    """计算每种类型应该生成的问题数量"""
    counts = {}
    for question_type, type_info in QUESTION_TYPES_FIXED.items():
        # 使用基础数量或按比例计算，取较大值
        ratio_count = int(total_target * type_info["ratio"])
        base_count = type_info["base_count"]
        counts[question_type] = max(ratio_count, base_count)
    return counts

# 修复 generate_questions_by_type_parallel 函数
async def generate_questions_by_type_parallel_fixed(
    generator, 
    content: str, 
    question_type: str, 
    type_info: dict, 
    num_questions: int,  # 可以设置为None，表示不限制
    config: dict
):
    """并行生成特定类型的问题 - 修复版本"""
    try:
        # 调用原有的问题生成逻辑
        all_questions = await call_model_for_question_generation(
            generator=generator,
            content=content,
            question_type=question_type,
            type_info=type_info,
            config=config
        )
        
        if not isinstance(all_questions, list):
            logger.warning(f"生成的问题不是列表格式: {type(all_questions)}")
            all_questions = []
        
        actual_count = len(all_questions)
        logger.info(f"生成{question_type}类型问题: 实际生成{actual_count}个")
        
        if not all_questions:
            return []
        
        # 如果不限制数量，返回所有问题
        if num_questions is None:
            logger.info(f"不限制数量，返回所有{actual_count}个{question_type}类型问题")
            return all_questions
        
        # 如果生成的问题少于要求的数量，返回所有问题
        if actual_count <= num_questions:
            logger.info(f"生成数量({actual_count})少于或等于要求({num_questions})，返回所有问题")
            return all_questions
        
        # 只有在生成的问题多于要求时才进行筛选
        # 优先选择长度适中的问题
        selected_questions = []
        
        # 第一轮：选择长度适中的问题
        for question in all_questions:
            if not isinstance(question, str):
                continue
            # 放宽长度限制
            if 5 < len(question) < 500:  # 原来是 10 < len < 200
                selected_questions.append(question)
                if len(selected_questions) >= num_questions:
                    break
        
        # 如果未选够，补充其他问题
        if len(selected_questions) < num_questions:
            for question in all_questions:
                if isinstance(question, str) and question not in selected_questions:
                    selected_questions.append(question)
                    if len(selected_questions) >= num_questions:
                        break
        
        logger.info(f"从{actual_count}个问题中选择了{len(selected_questions)}个{question_type}类型问题")
        return selected_questions[:num_questions]
        
    except Exception as e:
        logger.error(f"生成{question_type}类型问题失败: {e}")
        import traceback
        logger.error(f"堆栈跟踪:\n{traceback.format_exc()}")
        return []

# 使用示例：在主流程中替换原有函数
"""
# 原代码：
question_data = await parallel_classified_question_generation(
    generator, qa_input_data, config, max_concurrent_questions
)

# 修改为：
# 方案A：使用修正的比例和增加的基础数量
question_data = await parallel_classified_question_generation_with_fixed_ratios(
    generator, qa_input_data, config, max_concurrent_questions, 
    target_questions_per_text=30  # 每个文本生成30个问题
)

# 或方案B：不限制数量
question_data = await parallel_classified_question_generation_unlimited(
    generator, qa_input_data, config, max_concurrent_questions
)
"""