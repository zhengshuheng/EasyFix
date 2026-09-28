"""
PDF生成服务 - 使用fpdf2生成练习集PDF（支持中文）
"""
import os
import uuid
from datetime import datetime
from typing import List, Dict, Any
from fpdf import FPDF
from fpdf.enums import XPos, YPos
from app.config import get_settings
from app.utils.html import decode_html
from app.services.scoring import (
    compute_question_scores, normalize_score_mode, SCORE_MODE_DEFAULT,
)

settings = get_settings()


def _resolve_font_path():
    """中文字体路径：环境变量 EASYFIX_FONT 优先，其次常见 Linux/Windows 候选。

    - 服务器部署：可在 backend/.env 设 EASYFIX_FONT=... 指向部署目录内的字体
      （推荐随项目上传 simhei.ttf 到 backend/fonts/simhei.ttf，输出与本地一致）；
      install.sh 也会安装 fonts-noto-cjk 作为兜底。
    - 本地开发：保持原 Windows 路径 C:/Windows/Fonts/simhei.ttf。
    """
    env = os.environ.get("EASYFIX_FONT")
    if env and os.path.exists(env):
        return env
    candidates = [
        "C:/Windows/Fonts/simhei.ttf",
        "C:\\Windows\\Fonts\\simhei.ttf",
        # Linux 常见中文字体（Noto / 文泉驿 / Droid 回退）
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
        "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
        "/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf",
    ]
    for p in candidates:
        if os.path.exists(p):
            return p
    # 全都不存在时回退原默认路径（本地开发必存在；服务器上会由 EASYFIX_FONT 覆盖）
    return "C:/Windows/Fonts/simhei.ttf"


FONT_PATH = _resolve_font_path()


def generate_practice_set_pdf(
    practice_set_name: str,
    questions: List[Dict[str, Any]],
    output_dir: str = None,
    show_score: bool = True,
    score_mode: str = SCORE_MODE_DEFAULT,
    created_at=None,
    subject_name: str = None,
    grade_label: str = None,
    show_ai_author: bool = False,
) -> str:
    """
    生成练习集PDF

    Args:
        practice_set_name: 练习集名称（卷面标题）
        questions: 题目列表，每题包含 question_text, answer, difficulty 等
        output_dir: 输出目录，默认为 uploads/practice_sets
        show_score: 卷面是否显示分值（练习卷可不出分值）
        score_mode: hundred=百分制（满分100）/ default=按题型默认分值
        created_at: 出卷时间（datetime），打印在卷头
        subject_name: 学科名（卷头信息行）
        grade_label: 年级标签（卷头信息行，如「三年级」）
        show_ai_author: 卷头「出题人」是否署名「AI 出题助手」（默认留空白手填）

    Returns:
        生成的PDF文件相对路径
    """
    if output_dir is None:
        # PDF输出到 uploads/images/practice_sets，与静态文件服务一致
        upload_dir_abs = os.path.abspath(settings.UPLOAD_DIR)
        output_dir = os.path.join(upload_dir_abs, "practice_sets")

    # 确保目录存在
    os.makedirs(output_dir, exist_ok=True)
    print(f"[PDF DEBUG] output_dir: {output_dir}")
    print(f"[PDF DEBUG] dir exists: {os.path.exists(output_dir)}")
    print(f"[PDF DEBUG] is dir: {os.path.isdir(output_dir)}")

    # 生成文件名
    filename = f"{uuid.uuid4().hex[:8]}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
    output_path = os.path.join(output_dir, filename)
    print(f"[PDF DEBUG] output_path: {output_path}")

    # 创建PDF
    pdf = PracticeSetPDF(practice_set_name, questions, show_score=show_score,
                         score_mode=score_mode, created_at=created_at,
                         subject_name=subject_name, grade_label=grade_label,
                         show_ai_author=show_ai_author)
    pdf.generate(output_path)

    # 验证文件是否生成
    if os.path.exists(output_path):
        print(f"[PDF DEBUG] PDF生成成功: {output_path}, 大小: {os.path.getsize(output_path)}")
    else:
        print(f"[PDF DEBUG] PDF生成失败，文件不存在: {output_path}")

    # 返回相对路径（始终使用正斜杠以兼容URL）
    return f"practice_sets/{filename}"


class PracticeSetPDF(FPDF):
    """练习集 PDF 生成器 —— 学校试卷样式（卷头 + 大题 + 答题留白）

    设计原则：这是一张给孩子做的卷子，不是系统报表——
    卷头 = 标题 + 满分/题数 + 姓名班级得分栏（双线分隔）；
    大题用「一、二、三」编号，写法与学校卷一致；
    每题只有 题号 + 题干 + 选项；主观题（计算/应用/操作/写作）下方留出足够的答题空间。
    """

    # 题型单题分值（内置默认，参考学校试卷：计算/填空占大头，主观题分高）
    TYPE_SCORES = {
        "choice": 3, "fill": 3, "judge": 2, "calc": 4, "application": 6,
        "operation": 5, "reading": 4, "writing": 10, "sentence": 2,
    }
    TYPE_NAMES = {
        "choice": "选择题", "fill": "填空题", "judge": "判断题", "calc": "计算题",
        "application": "应用题", "operation": "操作实践题", "reading": "阅读理解题",
        "writing": "写话/习作题", "sentence": "连词成句题",
    }
    TYPE_ORDER = {"choice": 1, "fill": 2, "judge": 3, "calc": 4, "application": 5,
                  "operation": 6, "reading": 7, "writing": 8, "sentence": 9}

    # 答题留白高度（mm）：一行算式约 8mm，应用题至少留 5 行书写空间
    WRITING_SPACE = {
        "choice": 2, "judge": 2, "fill": 10, "calc": 26,
        "application": 42, "operation": 34, "reading": 14,
        "writing": 70, "sentence": 16,
    }

    BLACK = (0, 0, 0)
    GRAY_TEXT_COLOR = (120, 120, 120)

    def __init__(self, title: str, questions: List[Dict[str, Any]],
                 show_score: bool = True, score_mode: str = SCORE_MODE_DEFAULT,
                 created_at=None, subject_name: str = None, grade_label: str = None,
                 show_ai_author: bool = False):
        super().__init__()
        self.title = title
        self.questions = questions
        self.show_score = bool(show_score)
        self.score_mode = normalize_score_mode(score_mode)
        self.subject_name = subject_name or ''
        self.grade_label = grade_label or ''
        self.show_ai_author = bool(show_ai_author)
        # 每题分值：百分制按题型权重把 100 分分到各题；default 用题型内置分值
        self.question_scores = compute_question_scores(questions, self.score_mode)
        if created_at is not None:
            self.created_at_text = created_at.strftime('%Y年%m月%d日 %H:%M')
        else:
            self.created_at_text = datetime.now().strftime('%Y年%m月%d日 %H:%M')
        self.set_margins(15, 12, 15)
        self.set_auto_page_break(auto=True, margin=18)
        # 注册中文字体（使用下划线后缀_B表示粗体）
        self.add_font('chinese', '', FONT_PATH)
        self.add_font('chinese_b', '', FONT_PATH)
        self.alias_nb_pages()
        self.set_title(title)

    # ==================== 卷头 / 页脚 ====================

    def total_score(self) -> int:
        """卷面总分（按配置的计分方式）"""
        return sum(self.question_scores)

    def header(self):
        """首页画完整卷头，后续页只留标题 + 细线"""
        if self.page_no() == 1:
            self.set_font('chinese_b', size=17)
            self.set_text_color(*self.BLACK)
            self.multi_cell(0, 10, self.title, align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            self.set_font('chinese', size=11)
            meta = f'共 {len(self.questions)} 题'
            if self.show_score:
                meta = f'满分 {self.total_score()} 分　{meta}'
            self.cell(0, 7, meta, align='C',
                      new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            # 卷面信息行：学科 / 年级 / 出题人（默认留空白，出题界面可让 AI 署名）
            info_items = []
            if self.subject_name:
                info_items.append(f'学科：{self.subject_name}')
            if self.grade_label:
                info_items.append(f'年级：{self.grade_label}')
            author = 'AI 出题助手' if self.show_ai_author else '__________'
            info_items.append(f'出题人：{author}')
            self.cell(0, 7, '　　'.join(info_items), align='C',
                      new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            self.ln(1)
            name_line = '姓名：____________　　班级：__________'
            if self.show_score:
                name_line += '　　得分：__________'
            self.cell(0, 8, name_line, align='C',
                      new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            # 出卷时间（家长备查，小字右对齐）
            self.set_font('chinese', size=9)
            self.set_text_color(*self.GRAY_TEXT_COLOR)
            self.cell(0, 6, f'出卷时间：{self.created_at_text}', align='R',
                      new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            self.set_text_color(*self.BLACK)
            self.set_font('chinese', size=11)
            self.ln(1)
            y = self.get_y()
            self.set_draw_color(*self.BLACK)
            self.set_line_width(0.6)
            self.line(self.l_margin, y, self.w - self.r_margin, y)
            self.set_line_width(0.2)
            self.line(self.l_margin, y + 1.3, self.w - self.r_margin, y + 1.3)
            self.ln(7)
        else:
            self.set_font('chinese', size=9)
            self.set_text_color(*self.GRAY_TEXT_COLOR)
            self.cell(0, 6, self.title, align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            self.set_text_color(*self.BLACK)
            y = self.get_y()
            self.set_draw_color(*self.GRAY_TEXT_COLOR)
            self.set_line_width(0.2)
            self.line(self.l_margin, y, self.w - self.r_margin, y)
            self.ln(5)

    def footer(self):
        """页脚：第 X 页 / 共 Y 页"""
        self.set_y(-14)
        self.set_font('chinese', size=9)
        self.set_text_color(*self.GRAY_TEXT_COLOR)
        self.cell(0, 8, '第 {p} 页 / 共 {{nb}} 页'.format(p=self.page_no()), align='C')
        self.set_text_color(*self.BLACK)

    # ==================== 大题 ====================

    def add_section_header(self, section_index: int, type_key: str, count: int,
                           score_per: int = None, section_total: int = None):
        """大题标题：一、填空题（共3题，每题3分，共9分）

        不显示分数时只写「共N题」；同一大题内每题分值不一致（百分制除不尽）时，
        每题的分值改在题号后单独标注，这里只写大题总分。
        """
        cn_num = "一二三四五六七八九十"
        prefix = f"{cn_num[section_index - 1]}、" if section_index <= len(cn_num) else f"{section_index}、"
        if not self.show_score:
            tail = f"（共{count}题）"
        elif score_per:
            tail = f"（共{count}题，每题{score_per}分，共{count * score_per}分）"
        else:
            tail = f"（共{count}题，共{section_total or 0}分）"
        title = f"{prefix}{self.TYPE_NAMES.get(type_key, '题目')}{tail}"
        if self.get_y() > self.h - self.b_margin - 40:
            self.add_page()
        self.ln(3)
        self.set_font('chinese_b', size=12)
        self.set_text_color(*self.BLACK)
        self.cell(0, 8, title, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='L')
        self.ln(1)

    # ==================== 题目 ====================

    @staticmethod
    def _strip_option_prefix(text: str) -> str:
        """去掉选项里已有的 A. / (A) / A) 前缀，避免打成「A. A. xxx」"""
        if not text:
            return ''
        text = str(text).strip()
        import re
        for pattern in (r'^[A-Da-d]\s*[.、．]\s*', r'^\([A-Da-d]\)\s*', r'^[A-Da-d]\)\s*'):
            match = re.match(pattern, text)
            if match:
                return text[match.end():]
        return text

    def add_question(self, index: int, question_text: str, question_type: str = '',
                     score: int = None, options: List[str] = None):
        """一道题：题号 + 题干 + 选项 + 答题留白

        score 不为空时在题号后标出该题分值（同一大题内分值不一致时才会传）。
        """
        write_mm = self.WRITING_SPACE.get(question_type, 4)
        text = decode_html(question_text) if question_text else '暂无题目内容'
        # AI 出题常把选项用字面 \n 拼进题干 → 转成真换行，避免打成字面 "\n"
        text = str(text).replace('\\n', '\n')
        # 题干内嵌了 A. B. C. D. 选项、且独立 options 已给出 → 剥离题干内嵌段，避免重复打印
        if options and any(o and str(o).strip() for o in options):
            from app.services.llm import extract_inline_options
            cleaned, inline_opts = extract_inline_options(text)
            if inline_opts:
                text = cleaned
        num_w = 8
        score_str = f'({score}分)' if (score and self.show_score) else ''
        score_w = 13 if score_str else 0
        text_w = self.w - self.r_margin - self.l_margin - num_w - score_w
        # 预判高度：题干行数（中文约 4.2mm/字）+ 选项行 + 留白，放不下就换页
        chars_per_line = max(10, int(text_w / 4.2))
        text_lines = 1
        for seg in str(text).split('\n'):
            text_lines += max(0, (len(seg) - 1) // chars_per_line)
        option_rows = 0
        opts = []
        if options:
            opts = [self._strip_option_prefix(o) for o in options if o and str(o).strip()]
            if opts:
                short = max(len(o) for o in opts) <= 12 and len(opts) <= 4
                option_rows = (len(opts) + 1) // 2 if short else len(opts)
        need = text_lines * 7.5 + option_rows * 7 + write_mm + 4
        remaining = self.h - self.b_margin - self.get_y()
        if need > remaining:
            text_need = text_lines * 7.5 + option_rows * 7
            if text_need + 12 <= remaining:
                # 题干放得下、只是留白不够 → 就地压缩留白，避免整题翻页、上一页留出大片空白
                write_mm = max(10, remaining - text_need - 2)
            else:
                self.add_page()

        # 题号（+分值）+ 题干（题号悬挂缩进，像学校卷）
        self.set_font('chinese_b', size=12)
        self.set_text_color(*self.BLACK)
        self.cell(num_w, 7.5, f'{index}.', new_x=XPos.RIGHT, new_y=YPos.TOP)
        if score_str:
            self.set_font('chinese', size=9)
            self.set_text_color(*self.GRAY_TEXT_COLOR)
            self.cell(score_w, 7.5, score_str, new_x=XPos.RIGHT, new_y=YPos.TOP)
            self.set_text_color(*self.BLACK)
        self.set_font('chinese', size=12)
        self.multi_cell(text_w, 7.5, str(text), align='L', new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        # 选项：短选项两列排，长选项一行一个
        if opts:
            letters = 'ABCD'
            self.set_font('chinese', size=11)
            short = max(len(o) for o in opts) <= 12 and len(opts) <= 4
            if short:
                col_w = text_w / 2
                for i in range(0, len(opts), 2):
                    self.set_x(self.l_margin + num_w)
                    for j in range(2):
                        if i + j < len(opts):
                            self.cell(col_w, 7, f'{letters[i + j]}. {opts[i + j]}',
                                      new_x=XPos.RIGHT, new_y=YPos.TOP)
                    self.ln(7)
            else:
                for i, opt in enumerate(opts):
                    self.set_x(self.l_margin + num_w)
                    self.multi_cell(text_w, 7, f'{letters[i]}. {opt}', align='L',
                                    new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        # 答题留白：纯空白，给孩子书写（应用题留足竖式/列式空间）
        if write_mm > 0:
            self.ln(write_mm)

    # ==================== 阅读理解 ====================

    def add_reading_passage(self, title: str, content: str):
        """添加阅读短文（单独一页）"""
        self.add_page()
        self.set_font('chinese_b', size=14)
        self.set_text_color(*self.BLACK)
        self.cell(0, 10, title, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
        self.ln(3)
        self.set_font('chinese', size=11)
        for para in (content or '').split('\n'):
            para = para.strip()
            if para:
                self.multi_cell(0, 6, para, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
                self.ln(1)
        self.ln(6)

    def add_reading_question(self, index: int, question_text: str, option_a: str = None,
                             option_b: str = None, option_c: str = None, option_d: str = None):
        """阅读理解题（与普通选择题同一套排版）"""
        self.add_question(index, question_text, 'reading',
                          options=[option_a, option_b, option_c, option_d])

    # ==================== 主流程 ====================

    def generate(self, output_path: str):
        """生成 PDF"""
        has_reading = any(q.get('is_reading_question') for q in self.questions)

        if has_reading:
            first = self.questions[0]
            self.add_reading_passage(first.get('_passage_title', '阅读短文'),
                                     first.get('_passage_content', ''))
            for idx, q in enumerate(self.questions, 1):
                self.add_question(idx, q.get('question_text', ''), 'reading',
                                  options=[q.get('option_a'), q.get('option_b'),
                                           q.get('option_c'), q.get('option_d')])
        else:
            # 普通练习集：按题型分大题（选择→填空→判断→计算→应用→操作→阅读→写作）
            self.add_page()
            groups = {}
            for i, q in enumerate(self.questions):
                groups.setdefault(q.get('question_type') or '', []).append((i, q))
            ordered_groups = sorted(
                groups.items(),
                key=lambda kv: self.TYPE_ORDER.get(kv[0], 99) if kv[0] else 99,
            )

            global_idx = 1
            for section_idx, (type_key, pairs) in enumerate(ordered_groups, 1):
                sec_scores = [self.question_scores[i] for i, _ in pairs]
                uniform = len(set(sec_scores)) == 1
                if type_key:
                    self.add_section_header(
                        section_idx, type_key, len(pairs),
                        score_per=sec_scores[0] if uniform else None,
                        section_total=sum(sec_scores),
                    )
                elif self.get_y() > self.h - self.b_margin - 40:
                    self.add_page()
                for (_, q), sec_score in zip(pairs, sec_scores):
                    self.add_question(
                        global_idx,
                        q.get('question_text', ''),
                        type_key,
                        score=None if uniform else sec_score,
                        options=[q.get('option_a'), q.get('option_b'),
                                 q.get('option_c'), q.get('option_d')]
                        if (q.get('option_a') or q.get('option_b')) else None,
                    )
                    global_idx += 1

        # 输出到文件
        self.output(output_path)


# ==================== 单词默写PDF ====================

def generate_word_print_pdf(
    title: str,
    words: List[Dict[str, Any]],
    output_dir: str = None
) -> str:
    """
    生成单词默写PDF

    Args:
        title: 标题
        words: 单词列表，每项包含 chinese, english, length
        output_dir: 输出目录

    Returns:
        生成的PDF文件相对路径
    """
    if output_dir is None:
        upload_dir_abs = os.path.abspath(settings.UPLOAD_DIR)
        output_dir = os.path.join(upload_dir_abs, "practice_sets")

    os.makedirs(output_dir, exist_ok=True)

    filename = f"word_{uuid.uuid4().hex[:8]}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
    output_path = os.path.join(output_dir, filename)

    pdf = WordPrintPDF(title, words)
    pdf.generate(output_path)

    return f"practice_sets/{filename}"


class WordPrintPDF(FPDF):
    """单词默写PDF生成器"""

    def __init__(self, title: str, words: List[Dict[str, Any]]):
        super().__init__()
        self.title = title
        self.words = words
        self.set_auto_page_break(auto=True, margin=15)
        self.add_font('chinese', '', FONT_PATH)
        self.add_font('chinese_b', '', FONT_PATH)

    def header(self):
        """页眉"""
        self.set_font('chinese_b', size=18)
        self.cell(0, 12, self.title, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
        self.set_font('chinese', size=10)
        date_str = datetime.now().strftime('%Y年%m月%d日')
        self.cell(0, 8, date_str, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
        self.ln(3)
        self.set_draw_color(64, 158, 255)
        self.set_line_width(0.5)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(8)

    def footer(self):
        """页脚"""
        self.set_y(-15)
        self.set_font('chinese', size=9)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'第 {self.page_no()} 页', align='C')

    def add_word_item(self, index: int, chinese: str, word_length: int):
        """添加一个单词条目"""
        # 序号
        self.set_font('chinese_b', size=12)
        self.set_fill_color(64, 158, 255)
        self.set_text_color(255, 255, 255)
        self.cell(12, 10, f'{index}.', new_x=XPos.RIGHT, new_y=YPos.TOP, align='C', fill=True)

        # 中文
        self.set_text_color(51, 51, 51)
        self.set_font('chinese', size=14)
        self.cell(80, 10, chinese, new_x=XPos.RIGHT, new_y=YPos.TOP, align='L')

        # 长度提示
        self.set_font('chinese', size=10)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'({word_length}个字母)', new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='R')

        # 答题线
        self.set_draw_color(189, 195, 199)
        self.set_line_width(0.3)
        self.line(10, self.get_y() + 2, 200, self.get_y() + 2)
        self.ln(10)

    def generate(self, output_path: str):
        """生成PDF文件"""
        self.add_page()

        for idx, w in enumerate(self.words, 1):
            if self.get_y() > 250:
                self.add_page()

            chinese = w.get('chinese', '')
            word_length = w.get('length', len(w.get('english', '')))
            self.add_word_item(idx, chinese, word_length)

        # 输出到文件
        self.output(output_path)
