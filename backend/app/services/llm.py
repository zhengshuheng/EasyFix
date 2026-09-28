import os
import json
import time
from typing import Optional, List
import anthropic
from app.config import get_settings
from app.services.ai_gateway import AIGatewayClient, get_gateway_config, resolve_gateway_config
from app.services.question_prompts import (
    get_subject_stage_prompt,
    get_math_relevant,
    validate_math_choice,
    normalize_math_numbers,
    math_expr_value,
    extract_math_signatures,
    math_signatures_conflict,
)

settings = get_settings()


def load_llm_config() -> dict:
    """从config/llm.json加载配置"""
    config_file = "config/llm.json"
    if os.path.exists(config_file):
        with open(config_file) as f:
            return json.load(f)
    return {}


class LLMService:
    _instance: Optional["LLMService"] = None
    _client: Optional[anthropic.Anthropic] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self._config = load_llm_config()
        self._init_client()

    def _init_client(self):
        """客户端构建已下沉到 AI 网关（AIGatewayClient，凭证由 ops 配置）。

        保留空方法仅为兼容既有调用点（各公开方法开头都会重载配置并调它）；
        实际协议适配/上游调用统一在网关内，未来消耗/价格计算只需改网关。
        """
        pass

    def _get_config(self, key: str, default: str = "") -> str:
        """获取配置（订阅制）：
        - model      → config/llm.json 用户选择的模型名，未选则网关默认模型
        - api_key/base_url/provider → AI 网关（ops 后台配置，用户无需 Key）
        """
        if key == "model":
            chosen = (self._config.get("model") or "").strip()
            if chosen:
                return chosen
            return get_gateway_config().get("default_model") or default
        if key == "api_key":
            return get_gateway_config().get("api_key") or getattr(settings, key, default)
        if key == "base_url":
            return get_gateway_config().get("base_url") or default
        if key == "provider":
            return get_gateway_config().get("provider") or default
        return self._config.get(key, getattr(settings, key, default))

    def generate_similar_question(
        self,
        question: str,
        answer: str,
        subject: str = "",
        knowledge_point: str = "",
    ) -> dict:
        """
        生成相似题目

        Args:
            question: 原题目
            answer: 原答案
            subject: 学科
            knowledge_point: 知识点

        Returns:
            dict: {
                "similar_question": str,
                "similar_answer": str,
                "explanation": str,
            }
        """
        # 重新加载配置
        self._config = load_llm_config()
        self._init_client()

        api_key = self._get_config("api_key", settings.ANTHROPIC_API_KEY)
        if not api_key:
            return {
                "error": "LLM API Key not configured. Please set it in Settings.",
                "similar_question": "",
                "similar_answer": "",
                "explanation": "",
            }

        model = self._get_config("model", "claude-sonnet-4-20250514")
        prompt = self._build_prompt(question, answer, subject, knowledge_point)

        try:
            # 使用重试机制调用API
            response = self._retry_on_rate_limit(
                self._call_messages_create,
                model=model,
                max_tokens=1000,
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                timeout=60,
                # 禁用思考块，避免MiniMax返回纯思考内容
                thinking={
                    "type": "disabled",
                },
            )

            # 获取文本内容（跳过ThinkingBlock，只取TextBlock）
            content = ""
            for block in response.content:
                if hasattr(block, 'type') and block.type == 'text' and hasattr(block, 'text'):
                    content = block.text
                    break

            if not content:
                return {
                    "error": "LLM返回内容为空或仅包含思考过程",
                    "similar_question": "",
                    "similar_answer": "",
                    "explanation": "",
                }

            return self._parse_response(content)
        except anthropic.RateLimitError as e:
            return {
                "error": f"API速率限制，请稍后再试: {str(e)}",
                "similar_question": "",
                "similar_answer": "",
                "explanation": "",
            }
        except Exception as e:
            return {
                "error": str(e),
                "similar_question": "",
                "similar_answer": "",
                "explanation": f"LLM调用失败: {str(e)}",
            }

    def _build_prompt(
        self,
        question: str,
        answer: str,
        subject: str,
        knowledge_point: str,
    ) -> str:
        subject_info = f"学科：{subject}" if subject else "学科：未知"
        knowledge_info = f"知识点：{knowledge_point}" if knowledge_point else ""

        prompt = f"""请根据以下题目生成一道相似的练习题，要求：
1. 题型相似、难度相近
2. 考察的知识点相同
3. 但具体数值或情境不同

{subject_info}
{knowledge_info}

原题目：
{question}

原答案：
{answer}

请以以下JSON格式返回结果：
{{
    "similar_question": "生成的相似题目",
    "similar_answer": "相似题目的答案",
    "explanation": "简要解析"
}}
"""
        return prompt

    def _parse_response(self, content: str) -> dict:
        """解析LLM返回的内容"""
        import json
        import re

        # 尝试从markdown代码块中提取JSON
        json_match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", content, re.DOTALL)
        if json_match:
            content = json_match.group(1)

        # 尝试直接解析JSON
        try:
            data = json.loads(content)
            # 兼容不同的字段名
            return {
                "similar_question": data.get("similar_question") or data.get("question") or data.get("similar_text") or "",
                "similar_answer": data.get("similar_answer") or data.get("answer") or "",
                "explanation": data.get("explanation") or data.get("解析") or "",
            }
        except json.JSONDecodeError:
            # 尝试提取JSON对象
            start = content.find("{")
            end = content.rfind("}") + 1
            if start != -1 and end != 0:
                try:
                    data = json.loads(content[start:end])
                    return {
                        "similar_question": data.get("similar_question") or data.get("question") or data.get("similar_text") or "",
                        "similar_answer": data.get("similar_answer") or data.get("answer") or "",
                        "explanation": data.get("explanation") or data.get("解析") or "",
                    }
                except json.JSONDecodeError:
                    pass

        return {
            "similar_question": content,
            "similar_answer": "",
            "explanation": "解析失败",
        }

    def generate_learning_report(
        self,
        subject_name: Optional[str],
        grade: Optional[int],
        time_range_days: Optional[int],
        data_summary: dict,
    ) -> dict:
        """
        生成学习状态分析报告

        Args:
            subject_name: 学科名称
            grade: 年级
            time_range_days: 时间范围天数
            data_summary: 数据摘要，包含错题和单词的统计数据

        Returns:
            dict: 多维度分析报告内容
        """
        # 重新加载配置
        self._config = load_llm_config()
        self._init_client()

        api_key = self._get_config("api_key", settings.ANTHROPIC_API_KEY)
        if not api_key:
            raise Exception("LLM API Key not configured. Please set it in Settings.")

        model = self._get_config("model", "claude-sonnet-4-20250514")
        prompt = self._build_learning_report_prompt(
            subject_name, grade, time_range_days, data_summary
        )

        try:
            # 使用重试机制调用API
            response = self._retry_on_rate_limit(
                self._call_messages_create,
                model=model,
                max_tokens=4000,  # 报告较长，需要更多token
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                timeout=120,  # 报告生成可能需要更长时间
                thinking={
                    "type": "disabled",
                },
            )

            # 获取文本内容
            content = ""
            for block in response.content:
                if hasattr(block, 'type') and block.type == 'text' and hasattr(block, 'text'):
                    content = block.text
                    break

            if not content:
                raise Exception("LLM返回内容为空")

            return self._parse_learning_report_response(content)
        except anthropic.RateLimitError as e:
            raise Exception(f"API速率限制，请稍后再试: {str(e)}")
        except Exception as e:
            raise Exception(f"LLM调用失败: {str(e)}")

    def _build_learning_report_prompt(
        self,
        subject_name: Optional[str],
        grade: Optional[int],
        time_range_days: Optional[int],
        data_summary: dict,
    ) -> str:
        """构建学习报告生成的Prompt"""
        import json

        scope_info = []
        if subject_name:
            scope_info.append(f"学科：{subject_name}")
        if grade:
            scope_info.append(f"年级：{self._get_grade_name(grade)}")
        if time_range_days:
            scope_info.append(f"时间范围：最近{time_range_days}天")
        if not scope_info:
            scope_info.append("范围：全学科、全年级、所有时间")

        scope_text = "，".join(scope_info)

        prompt = f"""你是一位专业的学习分析师。请根据以下学习数据，生成一份详细的多维度学习状态分析报告。

## 分析范围
{scope_text}

## 数据摘要
{json.dumps(data_summary, ensure_ascii=False, indent=2)}

## 报告要求

请生成一份结构化的多维度学习分析报告，包含以下维度：

### 1. 整体概况
- 学习数据总量（错题数量、单词数量）
- 整体正确率/准确率

### 2. 错题分析
- **难度分布**：各难度级别（1-5）的错题数量和占比
- **错误类型分析**：计算错误、概念错误、审题错误、其他错误的分布
- **知识点分布**：高频出错知识点TOP10
- **复习效果**：错题的复习次数分布，未复习/复习1次/复习多次的比例

### 3. 单词分析（如有数据）
- 总体掌握率
- 低准确率单词（正确率低于70%的单词）
- 复习间隔建议

### 4. 学习建议
- 针对薄弱知识点推荐练习方向
- 记忆类科目的复习策略建议
- 下一阶段学习重点

### 5. 总结
- 简明扼要的核心发现（3-5条）
- 优先改进项（最多3条）

## 输出格式

请以JSON格式返回报告内容：
{{
    "overview": {{
        "total_questions": number,
        "total_words": number,
        "overall_accuracy": number
    }},
    "question_analysis": {{
        "difficulty_distribution": {{"1": count, "2": count, ...}},
        "error_type_distribution": {{"计算": count, "概念": count, ...}},
        "top_error_knowledge_points": [{{"point": "知识点名", "count": number}}],
        "review_effectiveness": {{"not_reviewed": count, "reviewed_1": count, "reviewed_multiple": count}}
    }},
    "word_analysis": {{
        "mastery_rate": number,
        "low_accuracy_words": [{{"word": "单词", "accuracy": number}}],
        "recommended_review_interval": "建议"
    }},
    "suggestions": [
        {{"type": "练习", "content": "建议内容"}}
    ],
    "summary": {{
        "key_findings": ["发现1", "发现2", ...],
        "priority_improvements": ["优先项1", "优先项2", ...]
    }}
}}

请确保返回的是合法的JSON格式，不要包含markdown代码块标记。"""
        return prompt

    def _get_grade_name(self, grade: int) -> str:
        """转换年级数字为名称"""
        grade_map = {
            1: "一年级", 2: "二年级", 3: "三年级", 4: "四年级",
            5: "五年级", 6: "六年级", 7: "初一", 8: "初二",
            9: "初三", 10: "高一", 11: "高二", 12: "高三"
        }
        return grade_map.get(grade, f"{grade}年级")

    def _parse_learning_report_response(self, content: str) -> dict:
        """解析LLM返回的报告内容"""
        import json
        import re

        # 尝试提取JSON
        json_match = re.search(r'\{.*\}', content, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group(0))
            except json.JSONDecodeError:
                pass

        # 如果解析失败，返回一个错误结构
        raise Exception("无法解析LLM返回的报告内容，请重试")

    def _retry_on_rate_limit(self, func, *args, max_retries=3, **kwargs):
        """
        重试装饰器，处理API速率限制错误

        Args:
            func: 要重试的函数
            max_retries: 最大重试次数
        """
        for attempt in range(max_retries):
            try:
                return func(*args, **kwargs)
            except anthropic.RateLimitError as e:
                if attempt == max_retries - 1:  # 最后一次重试
                    raise e
                # 指数退避：等待 2^attempt * 2 秒
                wait_time = (2 ** attempt) * 2
                print(f"API速率限制，等待 {wait_time} 秒后重试 (尝试 {attempt + 1}/{max_retries})")
                time.sleep(wait_time)
            except Exception as e:
                import openai
                if isinstance(e, openai.RateLimitError):
                    if attempt == max_retries - 1:
                        raise e
                    wait_time = (2 ** attempt) * 2
                    print(f"API速率限制，等待 {wait_time} 秒后重试 (尝试 {attempt + 1}/{max_retries})")
                    time.sleep(wait_time)
                    continue
                raise

    def _call_messages_create(self, **kwargs):
        """统一经 AI 网关转发上游（凭证由 ops 配置，用户无需 Key）。

        按用户选择的厂商（llm.json vendor）解析网关配置；未选厂商时走默认厂商/旧配置。
        兼容旧签名（model/max_tokens/messages/system/extra_body/thinking/timeout）；
        RateLimitError 由网关原样冒泡，本方法及 _retry_on_rate_limit 行为不变。

        注意：AI 网关 AIGatewayClient.chat() 只透传 extra_body 中的参数（thinking 不是顶层
        参数，顶层传会 TypeError: unexpected keyword argument 'thinking'）——这里把旧调用方
        传的顶层 thinking 自动合并进 extra_body（与 k12_import.py 的写法对齐）。
        """
        thinking = kwargs.pop("thinking", None)
        if thinking is not None:
            extra = dict(kwargs.get("extra_body") or {})
            extra["thinking"] = thinking
            kwargs["extra_body"] = extra
        vendor = (self._config.get("vendor") or "").strip()
        return AIGatewayClient(resolve_gateway_config(vendor or None)).chat(**kwargs)

    def generate_reading_passage(self, grade: int, topic: str, difficulty: int) -> dict:
        """
        生成英语阅读理解短文

        Returns:
            dict: {"title": str, "content": str, "word_count": int}
        """
        self._config = load_llm_config()
        self._init_client()

        api_key = self._get_config("api_key", settings.ANTHROPIC_API_KEY)
        if not api_key:
            return {"error": "LLM API Key not configured. Please set it in Settings."}

        model = self._get_config("model", "claude-sonnet-4-20250514")

        # 根据难度确定词数范围
        word_ranges = {
            1: "80-120词", 2: "120-180词", 3: "180-250词",
            4: "250-320词", 5: "320-400词",
        }
        difficulty_labels = {
            1: "简单", 2: "较简单", 3: "中等", 4: "较难", 5: "困难",
        }

        prompt = f"""你是一位专业的英语教师。请根据以下要求生成一篇英语阅读理解短文。

## 要求
- 年级：{self._get_grade_name(grade)}
- 话题：{topic}
- 难度：{difficulty_labels.get(difficulty, '中等')}
- 词数：{word_ranges.get(difficulty, '180-250词')}

## 输出格式
请以以下JSON格式返回：
{{
    "title": "短文标题（中文或英文均可）",
    "content": "英语短文内容",
    "word_count": 实际词数
}}

注意：
- 短文内容应为2-4段，难度与指定等级匹配
- 避免使用过于生僻的词汇
- 内容健康积极，适合对应年级学生阅读
"""
        try:
            # 使用重试机制调用API
            response = self._retry_on_rate_limit(
                self._call_messages_create,
                model=model,
                max_tokens=2000,
                messages=[{"role": "user", "content": prompt}],
                timeout=60,
                thinking={"type": "disabled"},
            )

            content = ""
            for block in response.content:
                if hasattr(block, 'type') and block.type == 'text' and hasattr(block, 'text'):
                    content = block.text
                    break

            if not content:
                return {"error": "LLM返回内容为空"}

            return self._parse_generate_response(content)
        except anthropic.RateLimitError as e:
            return {"error": f"API速率限制，请稍后再试: {str(e)}"}
        except Exception as e:
            return {"error": str(e)}

    def generate_reading_questions(self, passage_content: str) -> dict:
        """
        为短文生成4道阅读理解选择题

        Returns:
            dict: {"questions": [...]}
        """
        self._config = load_llm_config()
        self._init_client()

        api_key = self._get_config("api_key", settings.ANTHROPIC_API_KEY)
        if not api_key:
            return {"error": "LLM API Key not configured"}

        model = self._get_config("model", "claude-sonnet-4-20250514")

        prompt = f"""你是一位专业的英语教师。请为以下英语短文生成4道阅读理解选择题。

## 短文
{passage_content}

## 要求
- 题型：4选1选择题
- 每题必须包含A/B/C/D四个选项
- 问题应涵盖：主旨大意、细节理解、推理判断、词义猜测等类型
- 正确答案分布合理（不全部选同一选项）

## 输出格式
请以以下JSON格式返回：
{{
    "questions": [
        {{
            "question_number": 1,
            "question_text": "What is the main idea of the passage?",
            "option_a": "The school has many buildings.",
            "option_b": "The students enjoy playing sports.",
            "option_c": "The writer describes his school life.",
            "option_d": "The Book Club is very popular.",
            "correct_answer": "C",
            "explanation": "解析说明"
        }}
    ]
}}

重要规则：
1. option_a/option_b/option_c/option_d 的值必须是纯英文选项内容，绝对不要加 "A." "B." "C." "D." 等字母前缀！
2. 选项必须以大写字母开头，是完整的英文句子或短语
3. 题目和选项都要用英文
4. 解析用中文简要说明
"""
        try:
            # 使用重试机制调用API
            response = self._retry_on_rate_limit(
                self._call_messages_create,
                model=model,
                max_tokens=2000,
                messages=[{"role": "user", "content": prompt}],
                timeout=60,
                thinking={"type": "disabled"},
            )

            content = ""
            for block in response.content:
                if hasattr(block, 'type') and block.type == 'text' and hasattr(block, 'text'):
                    content = block.text
                    break

            if not content:
                return {"error": "LLM返回内容为空"}

            return self._parse_reading_questions_response(content)
        except anthropic.RateLimitError as e:
            return {"error": f"API速率限制，请稍后再试: {str(e)}"}
        except Exception as e:
            return {"error": str(e)}

    def _parse_generate_response(self, content: str) -> dict:
        """解析短文生成响应"""
        import json, re
        json_match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", content, re.DOTALL)
        if json_match:
            content = json_match.group(1)

        try:
            data = json.loads(content)
            return {
                "title": data.get("title", ""),
                "content": data.get("content", ""),
                "word_count": data.get("word_count", 0),
            }
        except json.JSONDecodeError:
            start = content.find("{")
            end = content.rfind("}") + 1
            if start != -1 and end != 0:
                try:
                    data = json.loads(content[start:end])
                    return {
                        "title": data.get("title", ""),
                        "content": data.get("content", ""),
                        "word_count": data.get("word_count", 0),
                    }
                except json.JSONDecodeError:
                    pass
            return {"error": "解析失败"}

    def _parse_reading_questions_response(self, content: str) -> dict:
        """解析选择题生成响应"""
        import json, re

        def strip_option_prefix(text: str) -> str:
            """去除选项前缀A. B. C. D. 等各种格式，保留完整内容"""
            if not text:
                return ''
            text = text.strip()
            # 匹配前缀：A. / A、 / A． / (A) / A) 等，后面可能有空格
            # 注意：只匹配明确的选项前缀，避免误删内容首字母
            match = re.match(r'^[A-Da-d]\s*[.、．]\s*', text)
            if match:
                return text[match.end():]
            match = re.match(r'^\([A-Da-d]\)\s*', text)
            if match:
                return text[match.end():]
            match = re.match(r'^[A-Da-d]\)\s*', text)
            if match:
                return text[match.end():]
            return text

        # 添加调试信息
        print(f"[DEBUG] 原始响应内容: {content[:500]}...")

        json_match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", content, re.DOTALL)
        if json_match:
            content = json_match.group(1)
            print(f"[DEBUG] 提取的JSON内容: {content[:500]}...")

        try:
            data = json.loads(content)
            questions = data.get("questions", [])
            if not questions and "question" in data:
                questions = [data["question"]]
            # 去除选项前缀
            for q in questions:
                if "option_a" in q:
                    q["option_a"] = strip_option_prefix(q["option_a"])
                if "option_b" in q:
                    q["option_b"] = strip_option_prefix(q["option_b"])
                if "option_c" in q:
                    q["option_c"] = strip_option_prefix(q["option_c"])
                if "option_d" in q:
                    q["option_d"] = strip_option_prefix(q["option_d"])
            print(f"[DEBUG] 解析成功，共 {len(questions)} 道题")
            return {"questions": questions}
        except json.JSONDecodeError as e:
            print(f"[DEBUG] JSON解析失败: {e}")
            start = content.find("{")
            end = content.rfind("}") + 1
            if start != -1 and end != 0:
                try:
                    data = json.loads(content[start:end])
                    questions = data.get("questions", [])
                    # 去除选项前缀
                    for q in questions:
                        if "option_a" in q:
                            q["option_a"] = strip_option_prefix(q["option_a"])
                        if "option_b" in q:
                            q["option_b"] = strip_option_prefix(q["option_b"])
                        if "option_c" in q:
                            q["option_c"] = strip_option_prefix(q["option_c"])
                        if "option_d" in q:
                            q["option_d"] = strip_option_prefix(q["option_d"])
                    print(f"[DEBUG] 备用解析成功，共 {len(questions)} 道题")
                    return {"questions": questions}
                except json.JSONDecodeError as e:
                    print(f"[DEBUG] 备用JSON解析也失败: {e}")
                    pass
            return {"error": "解析失败"}

    def analyze_learning_data(self, prompt: str) -> str:
        """分析学习数据"""
        try:
            # 使用重试机制调用API
            response = self._retry_on_rate_limit(
                self._call_messages_create,
                model=self._get_config("model", "claude-sonnet-4-20250514"),
                max_tokens=4000,
                messages=[{"role": "user", "content": prompt}]
            )
            # 获取文本内容（跳过ThinkingBlock，只取TextBlock）
            content = ""
            for block in response.content:
                if hasattr(block, 'type') and block.type == 'text' and hasattr(block, 'text'):
                    content = block.text
                    break
            return content or ""
        except anthropic.RateLimitError as e:
            raise Exception(f"API速率限制，请稍后再试: {str(e)}")
        except Exception as e:
            raise Exception(f"LLM调用失败: {str(e)}")

    def grade_answers(
        self,
        questions: List[dict],
        subject: str = "",
    ) -> dict:
        """
        大模型一键批改

        Args:
            questions: [{"question_id": int, "question": str, "answer": str, "student_answer": str}]
            subject: 学科名

        Returns:
            dict: {"results": [{"question_id": int, "is_correct": bool, "comment": str}]}
        """
        # 重新加载配置
        self._config = load_llm_config()
        self._init_client()

        api_key = self._get_config("api_key", settings.ANTHROPIC_API_KEY)
        if not api_key:
            return {"error": "LLM API Key not configured. Please set it in Settings.", "results": []}

        if not questions:
            return {"error": "没有可批改的题目", "results": []}

        model = self._get_config("model", "claude-sonnet-4-20250514")
        prompt = self._build_grading_prompt(questions, subject)

        try:
            response = self._retry_on_rate_limit(
                self._call_messages_create,
                model=model,
                max_tokens=2000,
                messages=[{"role": "user", "content": prompt}],
                timeout=60,
                # 禁用思考块，避免MiniMax返回纯思考内容
                thinking={"type": "disabled"},
            )

            # 获取文本内容（跳过ThinkingBlock，只取TextBlock）
            content = ""
            for block in response.content:
                if hasattr(block, 'type') and block.type == 'text' and hasattr(block, 'text'):
                    content = block.text
                    break

            if not content:
                return {"error": "LLM返回内容为空或仅包含思考过程", "results": []}

            return self._parse_grading_response(content, questions)
        except anthropic.RateLimitError as e:
            return {"error": f"API速率限制，请稍后再试: {str(e)}", "results": []}
        except Exception as e:
            return {"error": f"LLM调用失败: {str(e)}", "results": []}

    def _build_grading_prompt(self, questions: List[dict], subject: str) -> str:
        lines = []
        for i, q in enumerate(questions, start=1):
            lines.append(
                f"{i}. 题目：{q.get('question', '')}\n"
                f"   标准答案：{q.get('answer', '')}\n"
                f"   学生作答：{q.get('student_answer', '')}"
            )
        subject_info = f"学科：{subject}" if subject else "全科"
        return f"""你是一位耐心的{subject_info}老师，请逐题批改以下练习（共{len(questions)}题）。
批改规则：
- 数值/含义等价即算对（如 0.21 与 21/100 等价，书写形式不同但含义相同算对）
- 学生作答为空算错
- 学生作答与标准答案含义不同但有道理时，按实际对错判断，不要过于苛刻

对每道题给出判断和简要评语（答对：简述"回答正确，xxx"；答错：说明错因并给出正确答案）。

请严格按以下JSON数组格式返回，只返回数组本身，不要包含多余文字：
[
  {{"question_id": 1, "is_correct": true, "comment": "回答正确"}},
  {{"question_id": 2, "is_correct": false, "comment": "错因：xxx，正确答案是 xxx"}}
]

题目：
{chr(10).join(lines)}
"""

    def _parse_grading_response(self, content: str, questions: List[dict]) -> dict:
        """解析批改结果"""
        import json
        import re

        text = content.strip()
        # 去掉 ```json ``` 代码块
        json_match = re.search(r"```(?:json)?\s*(\[.*?\])\s*```", text, re.DOTALL)
        if json_match:
            text = json_match.group(1)
        else:
            start = text.find("[")
            end = text.rfind("]")
            if start != -1 and end != -1:
                text = text[start : end + 1]
        try:
            data = json.loads(text)
            valid_ids = {q.get("question_id") for q in questions}
            results = []
            for pos, item in enumerate(data, start=1):
                qid = item.get("question_id")
                # 模型经常返回 1..N 的位置序号（提示词里就是按序号列的），
                # 这里统一映射回真实题号，否则前端/落库都匹配不上。
                if qid not in valid_ids:
                    if isinstance(qid, int) and 1 <= qid <= len(questions):
                        qid = questions[qid - 1].get("question_id")
                    elif pos <= len(questions):
                        qid = questions[pos - 1].get("question_id")
                is_correct = bool(item.get("is_correct"))
                comment = item.get("comment", "")
                results.append(
                    {"question_id": qid, "is_correct": is_correct, "comment": comment}
                )
            return {"results": results}
        except Exception:
            return {"error": "批改结果解析失败，请重试", "results": []}

    def generate_questions_by_knowledge(
        self,
        knowledge_points: List[str],
        subject: str,
        grade: int = None,
        count: int = 5,
        difficulty: int = None,
        question_types: List[str] = None,
        question_categories: List[str] = None,
        avoid_stems: List[str] = None,
    ) -> dict:
        """
        AI 结合知识点出题（依据义务教育课程标准 2022 版设计）

        Args:
            knowledge_points: 知识点列表（如 ["分数加减法", "乘法分配律"]）
            subject: 学科名
            grade: 年级（1-6）
            count: 题目总数
            difficulty: 难度（1-5）
            question_types: 题型列表（choice/fill/judge/calc/application/operation/reading/writing/sentence），空=混合
            question_categories: 类型列表（basic/scene/comprehensive/thinking），空=混合

        Returns:
            dict: {"questions": [{"question", "answer", "explanation", "knowledge_point", "question_type", "question_category"}]}
        """
        # 重新加载配置
        self._config = load_llm_config()
        self._init_client()

        api_key = self._get_config("api_key", settings.ANTHROPIC_API_KEY)
        if not api_key:
            return {"error": "LLM API Key not configured. Please set it in Settings.", "questions": []}

        if not knowledge_points:
            return {"error": "缺少知识点", "questions": []}

        result = self._generate_raw(
            knowledge_points, subject, grade, count, difficulty,
            question_types=question_types or [],
            question_categories=question_categories or [],
            avoid_stems=avoid_stems,
        )
        if result.get("error"):
            return result
        # 质量过滤：剔除重复/数学选择题无唯一答案，数量不足自动补生成
        questions = self._dedupe_questions(result["questions"], subject)
        if len(questions) < count:
            questions = self._quality_topup(
                questions,
                knowledge_points=knowledge_points,
                subject=subject,
                grade=grade,
                count=count,
                difficulty=difficulty,
                question_types=question_types or [],
                question_categories=question_categories or [],
                avoid_stems=avoid_stems,
            )
        # 语义级复核：选择题必须恰好 1 个正确、干扰项与题干相容、题干不内嵌选项
        # （数值校验拦不住的盲区：如"说法正确的是"出现两项都对、选项与题干矛盾）
        questions = self._verify_choice_questions(questions, subject, grade)
        # 严格截断到请求数量（LLM 多给时只取前 count 道）
        return {"questions": questions[:count]}

    def _generate_raw(
        self,
        knowledge_points: List[str],
        subject: str,
        grade: int,
        count: int,
        difficulty: int,
        question_types: List[str],
        question_categories: List[str],
        avoid_stems: List[str] = None,
    ) -> dict:
        """调用一次 LLM 并解析题目（不做质量过滤；供主流程与质量补题共用，避免递归）"""
        model = self._get_config("model", "claude-sonnet-4-20250514")
        prompt = self._build_question_gen_prompt(
            knowledge_points, subject, grade, count, difficulty,
            question_types=question_types or [],
            question_categories=question_categories or [],
            avoid_stems=avoid_stems,
        )

        # 推理模型偶发返回空/思考文本，自动重试最多 3 次（轮换关闭思考的参数写法）
        # 注意：AI 网关（OpenAI 兼容协议）只透传 extra_body 中的参数，thinking 必须以 extra_body 传递
        thinking_variants = [
            {"extra_body": {"thinking": {"type": "disabled"}}},
            {"extra_body": {"enable_thinking": False}},
            {},
        ]
        last_error = None
        for attempt in range(3):
            try:
                call_kwargs = {
                    "model": model,
                    "max_tokens": 4000,
                    "messages": [{"role": "user", "content": prompt}],
                    "timeout": 120,
                }
                call_kwargs.update(thinking_variants[attempt % len(thinking_variants)])

                response = self._retry_on_rate_limit(
                    self._call_messages_create,
                    **call_kwargs,
                )

                content = ""
                for block in response.content:
                    if hasattr(block, 'type') and block.type == 'text' and hasattr(block, 'text'):
                        content = block.text
                        break

                if not content:
                    last_error = "LLM返回内容为空"
                    continue

                parsed = self._parse_question_gen_response(content, subject)
                if parsed.get("questions"):
                    return parsed
                last_error = parsed.get("error", "解析失败")
            except anthropic.RateLimitError as e:
                return {"error": f"API速率限制，请稍后再试: {str(e)}", "questions": []}
            except Exception as e:
                last_error = str(e)
                continue

        return {"error": f"AI出题多次重试仍失败：{last_error}", "questions": []}

    # 题型定义（按学科）：value -> 中文名 + 出题要点
    QUESTION_TYPE_SPECS = {
        "choice": "选择题（4个选项，其中1个正确，其余为易错干扰项，考查概念辨析）",
        "fill": "填空题（直接填写结果，考查基础概念与简单计算）",
        "judge": "判断题（对/错并简要说明理由，考查概念正误辨析）",
        "calc": "计算题（直接写得数/竖式计算/脱式计算/简便运算，考查运算能力）",
        "application": "应用题（解决实际问题，需列式解答，考查数量关系与问题解决）",
        "operation": "操作实践题（画图、测量、统计等动手操作，考查几何直观与实践能力）",
        "reading": "阅读理解题（短文阅读后作答，考查阅读理解与分析能力）",
        "writing": "写话/习作题（看图写话、小练笔等，考查书面表达与交流）",
        "sentence": "连词成句/句型转换题（组织语言，考查句法结构与表达能力）",
    }
    # 类型定义（对齐课标"四基四能"与核心素养）
    QUESTION_CATEGORY_SPECS = {
        "basic": "基础巩固：直接考查该知识点的概念、公式、法则（对应课标'四基'中的基础知识和基本技能）",
        "scene": "情境应用：把知识点放到生活真实情境中解决实际问题，题目要有现实背景（对应课标'四能'与'强化情景设计'要求）",
        "comprehensive": "综合提升：跨知识点/多步骤综合运用，需要两步以上思考（对应课标'综合与实践'领域）",
        "thinking": "思维拓展：开放题、规律探究、一题多解、变式推理，培养创新意识和推理意识（对应课标核心素养导向）",
    }
    # 题型默认配额权重（参考真实学校试卷：计算/口算占最大头，其次填空，再次应用，选择少量）
    # 一年级期末卷100分示例：口算20+竖式12（计算32%）、填空32%、应用23%、选择6%、操作7%
    DEFAULT_TYPE_WEIGHTS = {
        "calc": 0.32,
        "fill": 0.28,
        "application": 0.18,
        "choice": 0.12,
        "operation": 0.10,
    }
    # 各学科默认题型池（未指定题型时按此池分配配额）
    DEFAULT_TYPE_POOL = {
        "数学": ["calc", "fill", "choice", "application", "operation"],
        "语文": ["fill", "choice", "judge", "reading", "writing"],
        "英语": ["fill", "choice", "judge", "sentence", "reading"],
    }

    def _build_type_quota(self, count: int, question_types: List[str], subject: str) -> str:
        """
        根据题型池/权重生成"题型配额"指令文本（参考学校试卷结构）。
        返回类似：选择题2道、填空题2道、计算题4道、应用题2道
        """
        if question_types:
            pool = [t for t in question_types if t in self.QUESTION_TYPE_SPECS]
            if not pool:
                pool = ["choice", "fill", "application"]
        else:
            pool = self.DEFAULT_TYPE_POOL.get(subject, self.DEFAULT_TYPE_POOL["数学"])

        # 计算每类题数：按权重分配，余数补给出题性价比高/学校占比较大的题型
        weights = {t: self.DEFAULT_TYPE_WEIGHTS.get(t, 0.1) for t in pool}
        total_w = sum(weights.values())
        counts = {t: max(0, int(count * w / total_w)) for t, w in weights.items()}
        remaining = count - sum(counts.values())
        # 学校卷填空/计算是主体，优先补这两种；其次应用
        priority = [t for t in ("fill", "calc", "application", "choice", "operation") if t in counts]
        i = 0
        while remaining > 0:
            counts[priority[i % len(priority)]] += 1
            remaining -= 1
            i += 1

        names = {"choice": "选择题", "fill": "填空题", "judge": "判断题", "calc": "计算题",
                 "application": "应用题", "operation": "操作实践题", "reading": "阅读理解题",
                 "writing": "写话/习作题", "sentence": "连词成句题"}
        parts = [f"{names[t]} {counts[t]} 道" for t in pool if counts.get(t, 0) > 0]
        return "、".join(parts)

    def _build_question_gen_prompt(
        self,
        knowledge_points: List[str],
        subject: str,
        grade: int,
        count: int,
        difficulty: int,
        question_types: List[str] = None,
        question_categories: List[str] = None,
        avoid_stems: List[str] = None,
    ) -> str:
        grade_info = f"小学{grade}年级" if grade else "小学"
        diff_desc = {
            1: "非常基础，直接套用公式/法则即可",
            2: "基础，略有变化",
            3: "中等，需要两步思考",
            4: "偏难，需要综合运用",
            5: "困难，需要灵活综合运用",
        }
        diff_info = f"难度：{diff_desc.get(difficulty, '中等')}（满分5，当前{difficulty}）" if difficulty else "难度：中等偏基础，适合日常练习"

        kp_text = "、".join(knowledge_points)
        per = max(1, count // len(knowledge_points))

        # 题型约束（显式配额，参考学校试卷结构，解决"混合模式不出选择题"问题）
        quota_text = self._build_type_quota(count, question_types or [], subject)
        if question_types:
            type_names = "、".join(self.QUESTION_TYPE_SPECS[t] for t in question_types if t in self.QUESTION_TYPE_SPECS)
            type_info = f"题型要求：本套题只使用以下题型，按配额出题，不得使用其他题型：\n- {type_names}\n- 题型配额（共 {count} 题，必须严格按此数量）：{quota_text}"
        else:
            type_info = f"题型要求：按学校试卷常见结构混合出题，题型配额（共 {count} 题，必须严格按此数量）：{quota_text}"

        # 类型约束
        if question_categories:
            cat_names = "、".join(self.QUESTION_CATEGORY_SPECS[c] for c in question_categories if c in self.QUESTION_CATEGORY_SPECS)
            cat_info = f"类型要求：本套题请覆盖以下考查类型（均衡分配）：\n- {cat_names}"
        else:
            cat_info = "类型要求：按'基础巩固→情境应用→综合提升→思维拓展'梯度递进编排，多数为基础巩固与情境应用，少量综合提升与思维拓展"

        # 学科×学段专属出题规则（按 科目×学段 单独维护，见 question_prompts.py；
        # 运营后台可覆盖：prompt_rules_service.load_prompt_rule_map → DB 优先，未保存用内置默认）
        from app.services.prompt_rules_service import load_prompt_rule_map, DEFAULT_GENERAL_RULES
        _rules_map = load_prompt_rule_map()
        general_rules = (_rules_map.get("general") or "").strip() or DEFAULT_GENERAL_RULES
        subject_guide = get_subject_stage_prompt(subject, grade, overrides=_rules_map)

        # 近期已展示过的题干 → 严禁重复出相同/高度相似题（举一反三核心：每次生成新变式）
        avoid_text = ""
        if avoid_stems:
            _shown = [s[:60] for s in avoid_stems][:20]
            avoid_text = (
                "\n- 【严禁重复】以下题目近期已给该孩子做过，**严禁**出现相同题干或只改数字/人名的相似题，必须换成不同情境、物品或问法：\n"
                + "\n".join("  - " + s for s in _shown)
            )

        return f"""你是一位经验丰富的{grade_info}{subject}老师，请依据《义务教育课程标准（2022年版）》围绕以下知识点出一套练习题：
知识点：{kp_text}

出题要求：
- 共 {count} 道题，围绕知识点出题，每个知识点至少 {per} 道
- {diff_info}
- {type_info}
- {cat_info}
- 题干要表述清晰完整，适合{grade_info}学生作答，题目要有区分度
- {general_rules}
- 【年级内容必须严格匹配】题目的词汇量、数字大小、运算难度、情境复杂度必须符合{grade_info}学生的真实水平：{grade_info}学生没学过的知识点、超纲词汇、过大的数字（如三年级以前不要出现四位数以上加减乘除）、过长的题目描述一律禁止。宁可出得简单，也不要出超纲题
{avoid_text}
{subject_guide}
- 每道题必须给出：题目、选项、正确答案、简要解析、所属知识点、题型（choice/fill/judge/calc/application/operation/reading/writing/sentence）、类型（basic/scene/comprehensive/thinking）、难度（difficulty 1-5）
- 【选择题硬性要求】choice 题必须真的给 4 个选项：题干只写问题本身（如"下面说法正确的是（　）"），四个选项放进 options 数组，不带"A."/"A、"/"A）"等字母前缀，且只有 1 个正确答案；answer 只填正确选项的字母（如 "B"）
- 【非选择题】options 一律返回空数组 []
- 【题型必须与内容一致】严禁为了凑配额把填空题/问答题贴上 choice 标签：没有 4 个选项的题不许标 choice；题干留括号横线的标 fill；纯算式标 calc；可判断对错的陈述句标 judge；解决实际问题的标 application。凑不齐某题型时宁可少出，也不要错标
- 【配图场景 visual】数学小学阶段（1-3年级）的情景题（如"袋子里装饼干/盘子里放水果/每盒几支笔"）尽量带 visual 字段，让前端能画出示意图。visual 是结构化 JSON 对象，取值：
  - 两数加减（低年级重点，如"有9本书又新买7本/原来有8个拿走3个"）：{{"type":"count-split","left_emoji":"📚","left_count":9,"right_emoji":"📚","right_count":7,"operator":"+","unknown":"sum","label":"书","max_count":16}}（left_count/right_count 必须**精确等于题干两个数字**，left/right 可用不同物品 emoji；加法求一共 unknown="sum"，减法求剩余 unknown="remainder"；max_count=总数或被减数）
  - 物品成组摆放：{{"type":"group","emoji":"🍪","groups":3,"per_group":5,"label":"饼干"}}（emoji 用题中物品对应符号：苹果🍎 饼干🍪 糖🍬 花🌸 鸟🐦 书📚 笔✏️ 球⚽ 汽车🚗 星星⭐ 香蕉🍌 桃子🍑 鸡蛋🥚 树🌳 鱼🐟；groups=组数，per_group=每组个数，乘积不超过24，且 groups/per_group 必须精确等于题干数字）
  - 数一数/一共多少个（题干只有一个数量）：{{"type":"count","emoji":"🍎","count":8,"label":"苹果"}}（count 必须精确等于题干数量）
  - 认识几何图形：{{"type":"shape","shape":"三角形"}}（shape 取：三角形/正方形/长方形/圆/正方体/长方体/圆柱/球/五角星/梯形/平行四边形）
  - 不适合配图的题（纯计算、判断题、选项是文字说法的选择题）visual 返回 null
  - 【重要】1-2年级数学题 visual 的**数量必须与题干数字精确一致**（count-split 两堆=题干两个数、count=题干数量、group 组数×每组=题干结构）；凡题干含两个数量且是"一共/还剩"关系的，一律用 count-split 把两堆都画出来，不能只画一堆。**3年级起尽量少配图**（仅几何图形 shape 或必须图示的关键题），4年级以上一律 visual 返回 null，避免图例削弱学生读题建模能力考察。带单位（元/厘米/米/千克等）的测量计算题一律不配图

请严格按以下JSON数组格式返回，只返回数组本身，不要包含多余文字：
[
  {{"question": "题目内容", "options": ["选项一", "选项二", "选项三", "选项四"], "answer": "正确答案", "explanation": "简要解析", "knowledge_point": "所属知识点", "question_type": "choice", "question_category": "basic", "difficulty": 2, "visual": null}},
  {{"question": "填空/计算/应用题内容", "options": [], "answer": "正确答案", "explanation": "简要解析", "knowledge_point": "所属知识点", "question_type": "fill", "question_category": "basic", "difficulty": 3, "visual": {{"type":"count","emoji":"🍎","count":8,"label":"苹果"}}}}
]
"""

    def _parse_question_gen_response(self, content: str, subject: str = "") -> dict:
        """解析AI出题结果（容忍思考文本/截断等杂讯，尽力提取JSON数组）"""
        import json
        import re

        text = content.strip()
        # 1) 优先提取 ```json ... ``` 代码块
        json_match = re.search(r"```(?:json)?\s*(\[.*?\])\s*```", text, re.DOTALL)
        if json_match:
            text = json_match.group(1)
        else:
            # 2) 从文本中截取从第一个 [ 到最后一个 ] 的部分
            start = text.find("[")
            end = text.rfind("]")
            if start != -1 and end != -1 and end > start:
                text = text[start : end + 1]

        data = None
        try:
            data = json.loads(text)
        except Exception:
            # 3) 逐个提取 { ... } 对象（容忍对象之间的杂讯/截断）
            objects = re.findall(r"\{[^{}]*\}", text, re.DOTALL)
            if objects:
                data = []
                for obj in objects:
                    try:
                        data.append(json.loads(obj))
                    except Exception:
                        continue

        questions = []
        if isinstance(data, list):
            for item in data:
                if not isinstance(item, dict):
                    continue
                q = {
                    "question": str(item.get("question", "")).strip(),
                    "options": item.get("options"),
                    "answer": str(item.get("answer", "")).strip(),
                    "explanation": str(item.get("explanation", "")).strip(),
                    "knowledge_point": str(item.get("knowledge_point", "")).strip(),
                    "question_type": str(item.get("question_type", "")).strip(),
                    "question_category": str(item.get("question_category", "")).strip(),
                }
                # 题型/选项校验：choice 必须带 ≥2 个选项（否则按内容重判题型）
                self._finalize_question(q, subject)
                if q["question_category"] not in self.QUESTION_CATEGORY_SPECS:
                    q["question_category"] = "basic"
                if q["question"] and q["answer"]:
                    questions.append(q)
        elif isinstance(data, dict):
            # 单个对象也接受
            q = {
                "question": str(data.get("question", "")).strip(),
                "options": data.get("options"),
                "answer": str(data.get("answer", "")).strip(),
                "explanation": str(data.get("explanation", "")).strip(),
                "knowledge_point": str(data.get("knowledge_point", "")).strip(),
                "question_type": str(data.get("question_type", "")).strip(),
                "question_category": str(data.get("question_category", "")).strip(),
            }
            self._finalize_question(q, subject)
            if q["question_category"] not in self.QUESTION_CATEGORY_SPECS:
                q["question_category"] = "basic"
            if q["question"] and q["answer"]:
                questions.append(q)

        if not questions:
            return {"error": "AI生成的题目为空或格式不正确", "questions": []}
        return {"questions": questions}

    def _dedupe_questions(self, questions: List[dict], subject: str = "") -> List[dict]:
        """生成后质量过滤：
        1) 数学选择题硬校验：4 个选项且恰好 1 个等于正确答案（剔除无正确答案/多正确答案）；
        2) 全卷去重：题干完全相同或高度相似；数学额外按算式数字组合去重
           （8+5 与 5+8 视为同一算式），应用题与填空/计算题数字组合不得重复；
        3) 保持题型顺序。
        """
        import difflib
        import re as _re

        math = get_math_relevant(subject)
        kept: List[dict] = []
        seen_stems: List[str] = []          # 归一化题干（去数字/标点/空白）
        seen_math_nums: List[tuple] = []     # 数学题去重签名（算式对集合 + 数字元组）
        dropped = 0

        def _norm_stem(s: str) -> str:
            t = _re.sub(r"\d+", "", s or "")
            return _re.sub(r"\s+|[，。？！、,.?!；;：:（）()\"'“”]", "", t)

        for q in questions:
            stem = (q.get("question") or "").strip()
            if not stem:
                dropped += 1
                continue
            # 数学选择题唯一性校验
            if math and (q.get("question_type") == "choice" or (q.get("options") or [])):
                if (q.get("options") or []) and not validate_math_choice(q):
                    dropped += 1
                    continue
            # 题干重复（含高度相似）
            ns = _norm_stem(stem)
            if ns and any(difflib.SequenceMatcher(None, ns, s).ratio() >= 0.9 for s in seen_stems):
                dropped += 1
                continue
            # 数学算式/数字组合去重（填空/计算/应用题都参与；算式对 + 数字组合任一命中即判重）
            if math:
                sig = extract_math_signatures(stem)
                if any(math_signatures_conflict(sig, s0) for s0 in seen_math_nums):
                    dropped += 1
                    continue
                seen_math_nums.append(sig)
            kept.append(q)
            seen_stems.append(ns)
        if dropped:
            print(f"[llm] 出题质量过滤：剔除 {dropped} 道（重复/无唯一答案）")
        return kept

    def _verify_choice_questions(self, questions: List[dict], subject: str = "", grade: int = None) -> List[dict]:
        """语义级选择题复核 —— 补齐数值校验的盲区：

        数值校验（validate_math_choice）只在选项可解析出数值时查重/查唯一，
        "说法正确的是"等语义类选择题四个选项都不可解析 → 双正确、矛盾干扰项会溜过。
        策略：让 LLM 逐项独立判断每个选项本身是否正确（judgments），程序化统计：
        - 正确项恰好 1 个 → 通过
        - 正确项 ≥2 或 =0 → 要求 LLM 改写选项；程序化核对"多正确但选项原样没改" → 第二轮强制改写
        只改选项与答案（题干/知识点/题型不动）；任何失败/解析异常都保留原题，绝不因校验丢题。
        """
        choices = [
            (i, q) for i, q in enumerate(questions)
            if (q.get("question_type") == "choice" or (q.get("options") or []))
        ]
        if not choices:
            return questions

        import re as _re
        grade_label = f"{grade}年级" if grade else "（年级未知）"
        total_changed = 0

        def _build_lines(items_to_check):
            """构建复核题目列表（第二轮只列待强制改写的题）"""
            out = []
            for i, (_, q) in enumerate(items_to_check):
                stem = (q.get("question") or "").replace("\\n", "\n").strip()
                opts = self._normalize_options(q.get("options"))
                out.append(
                    f"第{i + 1}题（知识点：{q.get('knowledge_point') or '未知'}）：\n"
                    f"题干：{stem}\n"
                    "选项：\n"
                    + "\n".join(f"{'ABCD'[k]}. {o}" for k, o in enumerate(opts[:4]))
                    + f"\n原答案：{q.get('answer') or ''}"
                )
            return out

        def _build_prompt(items_to_check, force_rewrite: bool) -> str:
            head = (
                "你是小学数学命题质检员。下面每题是选择题：「题干：」之后那一行是题干原文，"
                "「选项：」之后 A/B/C/D 是四个待判断的说法。"
                "请逐项独立判断每个选项【作为一句说法本身】是否正确，不要脑补题干、不要把某个选项的内容当成题干。\n"
            )
            if force_rewrite:
                head += (
                    "注意：上一轮复核已确认下列题存在多个正确选项（或正确项为 0、或选项与题干矛盾），"
                    "但你上一轮没有真正改写选项。【本轮必须改写选项内容】——把多余的正确答案/矛盾干扰项"
                    "替换成一句明确错误或合理干扰的话，使每题恰好 1 个正确选项，并同步给出新答案字母。\n"
                )
            head += (
                "规则：\n"
                "1. judgments 逐项标注该说法本身是否正确（true=正确）；\n"
                "2. 正确项恰好 1 个 → changed=false，options 原样返回；\n"
                "3. 正确项 ≥2 个 → 必须把多余的正确说法改写为明确错误的话（如把「1~10中最大的数是10，最小的数是1」"
                "改成「1~10中最大的数是9，最小的数是0」），只保留 1 个正确，changed=true；\n"
                "4. 正确项 0 个 → 把其中一个选项改写为正确说法，changed=true；\n"
                "5. 比较类题干（最多/最少/一样）不得出现「一样多」「无法确定」等与比较直接冲突的干扰项，"
                "要改写为具体数量，changed=true；\n"
                "6. 选项重复/同义/同值 → 改写其一，changed=true；\n"
                "7. 题干里内嵌了 A. B. C. D. 选项列表 → 从题干移除（选项只放 options 数组），changed=true；\n"
                "8. 判断无需修改时，reason 必须写出其余 3 个选项各自错误的具体原因。\n"
                f"科目：{subject or '数学'}，年级：{grade_label}。\n"
                "题目列表：\n"
                + "\n\n".join(_build_lines(items_to_check))
                + "\n\n请逐题检查，严格按以下 JSON 数组返回【所有题】的复核结果：\n"
                '[{"index": 0, "stem": "题干原文（逐字复制）", "judgments": [true, false, false, false], "options": ["选项A","选项B","选项C","选项D"], "answer": "B", "changed": false, "reason": "..."}]'
                "\n- index 从 0 开始编号（第 1 题 index=0……）；stem 必须逐字复制该题题干原文；"
                "judgments 是 4 个布尔；options 是修正后的 4 个选项（按 A B C D 顺序，绝不能少于 4 个）；"
                "answer 是修正后正确选项的字母（A/B/C/D）；changed=true 表示修改过（给出 reason）。"
                "\n只输出 JSON，不要输出任何其他文字。"
            )
            return head

        def _call_llm(prompt_text) -> List[dict]:
            model = self._get_config("model", "claude-sonnet-4-20250514")
            call_kwargs = {
                "model": model,
                "max_tokens": 4000,
                "messages": [{"role": "user", "content": prompt_text}],
                "timeout": 120,
                "extra_body": {"thinking": {"type": "disabled"}},
            }
            response = self._retry_on_rate_limit(self._call_messages_create, **call_kwargs)
            content = ""
            for block in response.content:
                if hasattr(block, 'type') and block.type == 'text' and hasattr(block, 'text'):
                    content = block.text
                    break
            return self._parse_choice_verify_response(content)

        pending = []
        for round_no in range(2):
            force = round_no == 1
            to_check = pending if force else choices
            if not to_check:
                break
            try:
                items = _call_llm(_build_prompt(to_check, force))
            except Exception as e:
                print(f"[llm] 选择题语义复核失败，保留原题: {e}")
                break
            if not items:
                print("[llm] 选择题语义复核：无法解析复核结果，保留原题")
                break

            round_pending = []
            for item in items:
                target = self._pick_choice_target(item, to_check)
                if target is None:
                    # 兜底：按 index 定位（0-based）
                    try:
                        idx = int(item.get("index"))
                        if 0 <= idx < len(to_check):
                            target = to_check[idx]
                    except (TypeError, ValueError):
                        pass
                if target is None:
                    continue
                q = questions[target[0]]
                prev_opts = self._normalize_options(q.get("options"))
                opts = self._normalize_options(item.get("options"))
                if len(opts) == 4:
                    q["options"] = opts
                ans = str(item.get("answer") or "").strip()
                m = _re.fullmatch(r"([A-Da-d])", ans)
                if m:
                    q["answer"] = m.group(1).upper()
                elif ans:
                    # 答案不是字母时按内容匹配选项
                    for k, o in enumerate(opts):
                        if ans == str(o).strip():
                            q["answer"] = "ABCD"[k]
                            break
                # 题干内嵌选项剥离（模型把选项写回题干时）
                cleaned, inline = self._extract_options_from_text(q.get("question") or "")
                if inline:
                    q["question"] = cleaned
                if item.get("changed"):
                    total_changed += 1
                # 程序化防线：judgments 显示正确项≠1 且选项原样没改 → 留到第二轮强制改写
                judgments = item.get("judgments")
                true_cnt = None
                if isinstance(judgments, list) and len(judgments) >= 2:
                    true_cnt = sum(1 for j in judgments if bool(j))
                new_opts = self._normalize_options(q.get("options"))
                if true_cnt is not None and true_cnt != 1 and new_opts == prev_opts:
                    if not force:
                        round_pending.append(target)
            if round_pending and not force:
                pending = round_pending
            else:
                pending = []
        if total_changed:
            print(f"[llm] 选择题语义复核：修正 {total_changed} 道（唯一正确/干扰项相容性）")
        return questions

    def _parse_choice_verify_response(self, content: str) -> List[dict]:
        """解析选择题复核 JSON（容忍代码块/杂讯/截断）"""
        import json
        import re
        text = (content or "").strip()
        m = re.search(r"```(?:json)?\s*(\[.*?\])\s*```", text, re.DOTALL)
        if m:
            text = m.group(1)
        else:
            start = text.find("[")
            end = text.rfind("]")
            if start != -1 and end != -1 and end > start:
                text = text[start:end + 1]
        try:
            data = json.loads(text)
        except Exception:
            objects = re.findall(r"\{[^{}]*\}", text, re.DOTALL)
            data = []
            for obj in objects:
                try:
                    data.append(json.loads(obj))
                except Exception:
                    continue
        if not isinstance(data, list):
            return []
        items = []
        for it in data:
            if isinstance(it, dict) and "index" in it:
                items.append(it)
        return items

    def _pick_choice_target(self, item: dict, choices) -> Optional[tuple]:
        """定位复核结果对应的选择题（免疫模型 index 0/1-based 错位）：
        优先按题干原文相似度（stem 字段），其次按修正后选项与原选项的重叠数。"""
        import difflib
        stem = str(item.get("stem") or "").strip()
        if stem:
            def sim(c):
                return difflib.SequenceMatcher(None, stem, (c[1].get("question") or "")).ratio()
            best = max(choices, key=sim)
            if sim(best) >= 0.7:
                return best
        opts = self._normalize_options(item.get("options"))
        if opts:
            def ov(c):
                cur = self._normalize_options(c[1].get("options"))
                return len(set(opts) & set(cur))
            best = max(choices, key=ov)
            if ov(best) >= 2:
                return best
        return None


    def _quality_topup(
        self,
        questions: List[dict],
        knowledge_points: List[str],
        subject: str,
        grade: int,
        count: int,
        difficulty: int,
        question_types: List[str],
        question_categories: List[str],
        avoid_stems: List[str] = None,
    ) -> List[dict]:
        """质量过滤后数量不足 count 时，补生成缺失数量并再次过滤（最多补 3 轮，每轮多要一点）"""
        math = get_math_relevant(subject)
        missing = count - len(questions)
        for _round in range(3):
            if missing <= 0:
                break
            try:
                result = self._generate_raw(
                    knowledge_points=knowledge_points,
                    subject=subject,
                    grade=grade,
                    count=max(missing + 2, int(missing * 1.5)),
                    difficulty=difficulty,
                    question_types=question_types,
                    question_categories=question_categories,
                    avoid_stems=avoid_stems,
                )
            except Exception as e:
                print(f"[llm] 质量补题失败: {e}")
                break
            extras = result.get("questions", []) if isinstance(result, dict) else []
            extras = self._dedupe_questions(extras, subject)
            # 与已收题目再去重（题干相似 + 数学算式/数字组合）
            import difflib, re as _re

            def _norm(s: str) -> str:
                t = _re.sub(r"\d+", "", s or "")
                return _re.sub(r"\s+|[，。？！、,.?!；;：:（）()\"'“”]", "", t)

            existing_norms = [_norm(q.get("question") or "") for q in questions]
            existing_sigs = [extract_math_signatures(q.get("question") or "") for q in questions]
            for q in extras:
                ns = _norm(q.get("question") or "")
                if ns and any(difflib.SequenceMatcher(None, ns, s).ratio() >= 0.9 for s in existing_norms):
                    continue
                if math:
                    sig = extract_math_signatures(q.get("question") or "")
                    if any(math_signatures_conflict(sig, s0) for s0 in existing_sigs):
                        continue
                    existing_sigs.append(sig)
                questions.append(q)
                existing_norms.append(ns)
            missing = count - len(questions)
            if len(questions) >= count:
                break
        # 严格截断到请求数量（补题多收时只取前 count 道）
        return questions[:count]

    def _normalize_options(self, raw) -> List[str]:
        """规整选项：支持数组/单个字符串，剥离 "A."/"（A）" 等前缀"""
        import re
        if not raw:
            return []
        if isinstance(raw, str):
            _, extracted = self._extract_options_from_text(raw)
            if extracted:
                return extracted
            raw = [s for s in re.split(r"[\n;；]+", raw) if s.strip()]
        if not isinstance(raw, list):
            return []
        out = []
        for o in raw:
            s = str(o if o is not None else "").strip()
            s = re.sub(r"^[（(]?\s*[A-Da-d]\s*[)）.、．:：]\s*", "", s).strip()
            if s:
                out.append(s)
        return out

    def _extract_options_from_text(self, text: str):
        """从题干里切出内嵌选项（形如 "A. xx B. xx C. xx D. xx"），返回 (去选项的题干, 选项列表)"""
        import re
        t = text or ""
        # 取"从 A 开始、字母连续递增"的标签序列，避免把"点A、点B"当成选项
        marks = list(re.finditer(r"([A-Da-d])\s*[.、．)）]\s*", t))
        seq = []
        expected = "A"
        for m in marks:
            if m.group(1).upper() == expected:
                seq.append(m)
                expected = chr(ord(expected) + 1)
                if expected > "D":
                    break
        if len(seq) < 2:
            return t, []
        opts = []
        for i, m in enumerate(seq):
            end = seq[i + 1].start() if i + 1 < len(seq) else len(t)
            opts.append(t[m.end():end].strip(" 　"))
        stem = t[: seq[0].start()].strip()
        if len(stem) < 4 or any(not o for o in opts):
            return t, []
        return stem, opts

    def _finalize_question(self, q: dict, subject: str = "") -> None:
        """校验并纠正题型与选项：确保 choice 一定带 ≥2 个选项，其余题型不带选项"""
        import re
        text = (q.get("question") or "").strip()
        answer = (q.get("answer") or "").strip()
        opts = self._normalize_options(q.get("options"))
        # 模型没按 options 字段返回时，尝试从题干里切出内嵌选项
        if len(opts) < 2:
            cleaned, extracted = self._extract_options_from_text(text)
            if len(extracted) >= 2:
                opts, text = extracted, cleaned
        declared = (q.get("question_type") or "").strip()
        if len(opts) >= 2:
            # 有 4 个选项就是选择题（不论模型标成什么）
            qtype = "choice"
        elif declared in self.QUESTION_TYPE_SPECS and declared != "choice":
            qtype = declared
        else:
            # 声明为 choice 却没有选项 → 不是选择题，按内容重判
            qtype = self._infer_question_type(text, answer, subject, allow_choice=False)
        if qtype == "choice" and opts:
            letters = "ABCD"
            m = re.match(r"^\s*([A-Da-d])[.、．)）]\s*", answer)
            if m:
                answer = m.group(1).upper()
            else:
                for i, o in enumerate(opts[:4]):
                    if answer and answer.strip() == o.strip():
                        answer = letters[i]
                        break
            if not re.fullmatch(r"[A-D]", answer):
                # 兜底：题干末尾形如 "（ B ）" 的答案
                m2 = re.search(r"[（(]\s*([A-Da-d])\s*[)）]", text)
                if m2:
                    answer = m2.group(1).upper()
        q["question"] = text
        q["answer"] = answer
        q["question_type"] = qtype
        q["options"] = opts[:4] if qtype == "choice" else []

    def _infer_question_type(self, question: str, answer: str, subject: str = "", allow_choice: bool = True) -> str:
        """按题目内容特征推断题型（模型省略 question_type 时的兜底）"""
        import re
        q = question or ""
        a = answer or ""
        # 1) 选择题：选项标签从 A 起连续出现（≥3 个；或 ≥2 个且题干有"下列/正确的是"等选择句式）
        if allow_choice:
            letters = [m.group(1).upper() for m in re.finditer(r"([A-Da-d])\s*[.、．)）]\s*", q)]
            seq = 0
            for L in ("A", "B", "C", "D"):
                if L in letters:
                    seq += 1
                else:
                    break
            strong = any(k in q for k in ("下列", "正确的是", "错误的是", "哪个", "哪一个", "（ ）", "（）", "( )"))
            if seq >= 3 or (seq >= 2 and strong):
                return "choice"
        # 2) 判断题：答案是对/错/√/×
        if any(k in a for k in ["√", "×", "对", "错", "正确", "错误"]):
            return "judge"
        # 3) 填空题：括号/横线
        if any(k in q for k in ["（ ）", "（  ）", "( )", "（  ）", "____", "____", "○", "填一填"]):
            return "fill"
        # 4) 计算题：纯算式（数字+运算符）
        cleaned = re.sub(r"[\s=＝（）()]", "", q)
        if cleaned and re.fullmatch(r"[\d\+\-\×\÷\*/\.]+", cleaned):
            return "calc"
        # 5) 学科特征
        if subject == "语文":
            if "阅读" in q or len(q) > 100:
                return "reading"
            if "写" in q and ("话" in q or "作" in q):
                return "writing"
        if subject == "英语":
            if "连词成句" in q or "排序" in q:
                return "sentence"
        # 6) 默认：应用题（解决实际问题）
        return "application"


# 全局单例
llm_service = LLMService()


def extract_inline_options(text: str):
    """从题干里切出内嵌选项（旧数据兜底，供接口层复用）"""
    return llm_service._extract_options_from_text(text)


def infer_question_type(question: str, answer: str = "", subject: str = "", allow_choice: bool = True) -> str:
    """推断题型（旧数据纠偏，供接口层复用）"""
    return llm_service._infer_question_type(question, answer, subject, allow_choice)
