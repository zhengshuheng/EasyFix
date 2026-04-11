"""学习分析服务 - 数据聚合"""
from sqlalchemy.orm import Session
from sqlalchemy import func, Integer
from app.models import Question, Subject, Word, WordReviewLog, PracticeSet, PracticeSetQuestion, KnowledgePoint
from app.models.tag import Tag
from typing import List, Dict, Any
from datetime import datetime, timedelta
from collections import Counter

class LearningAnalysisService:
    def __init__(self, db: Session):
        self.db = db

    def get_full_stats(self) -> Dict[str, Any]:
        """获取完整学习统计数据"""
        return {
            "question_stats": self._get_question_stats(),
            "word_stats": self._get_word_stats(),
            "practice_stats": self._get_practice_stats(),
            "knowledge_graph": self._get_knowledge_graph(),
        }

    def _get_question_stats(self) -> Dict[str, Any]:
        """获取错题统计，使用数据库聚合避免加载所有记录"""
        try:
            # 使用数据库聚合计算总数
            total = self.db.query(func.count(Question.id)).filter(Question.deleted == False).scalar() or 0

            # 难度分布 - 使用数据库分组聚合
            difficulty_results = (
                self.db.query(
                    Question.difficulty,
                    func.count(Question.id)
                )
                .filter(Question.deleted == False, Question.difficulty.isnot(None))
                .group_by(Question.difficulty)
                .all()
            )
            by_difficulty = {d.difficulty: d[1] for d in difficulty_results}

            # 错误类型分布 - 使用数据库分组聚合
            # 注意：错误类型存储为逗号分隔的字符串，需要在应用层拆分
            error_type_results = (
                self.db.query(Question.error_type)
                .filter(Question.deleted == False, Question.error_type.isnot(None))
                .all()
            )
            error_types = Counter()
            for row in error_type_results:
                if row.error_type:
                    for et in row.error_type.split(','):
                        et = et.strip()
                        if et:
                            error_types[et] += 1

            # 知识点错误排行 - 使用数据库分组聚合
            kp_results = (
                self.db.query(
                    Question.knowledge_point,
                    func.count(Question.id)
                )
                .filter(Question.deleted == False, Question.knowledge_point.isnot(None))
                .group_by(Question.knowledge_point)
                .order_by(func.count(Question.id).desc())
                .limit(10)
                .all()
            )
            top_kp = [{"point": kp[0], "count": kp[1]} for kp in kp_results]

            # 复习效果 - 使用数据库聚合
            not_reviewed = (
                self.db.query(func.count(Question.id))
                .filter(Question.deleted == False, (Question.review_count == 0) | (Question.review_count.is_(None)))
                .scalar() or 0
            )
            reviewed_once = (
                self.db.query(func.count(Question.id))
                .filter(Question.deleted == False, Question.review_count == 1)
                .scalar() or 0
            )
            reviewed_multiple = (
                self.db.query(func.count(Question.id))
                .filter(Question.deleted == False, Question.review_count > 1)
                .scalar() or 0
            )

            # 正确率趋势
            accuracy_trend = self._get_question_accuracy_trend()

            return {
                "total": total,
                "by_difficulty": by_difficulty,
                "by_error_type": dict(error_types),
                "top_error_knowledge_points": top_kp,
                "review_effectiveness": {
                    "not_reviewed": not_reviewed,
                    "reviewed_once": reviewed_once,
                    "reviewed_multiple": reviewed_multiple,
                },
                "accuracy_trend": accuracy_trend,
            }
        except Exception as e:
            # 错误处理：返回空数据而不是崩溃
            return {
                "total": 0,
                "by_difficulty": {},
                "by_error_type": {},
                "top_error_knowledge_points": [],
                "review_effectiveness": {
                    "not_reviewed": 0,
                    "reviewed_once": 0,
                    "reviewed_multiple": 0,
                },
                "accuracy_trend": [],
            }

    def _get_question_accuracy_trend(self) -> List[Dict]:
        """获取错题正确率趋势"""
        try:
            logs = (
                self.db.query(
                    func.date(PracticeSet.created_at).label('date'),
                    func.sum(func.cast(PracticeSetQuestion.is_correct, Integer)).label('correct'),
                    func.count(PracticeSetQuestion.id).label('total')
                )
                .join(PracticeSet, PracticeSet.id == PracticeSetQuestion.practice_set_id)
                .filter(
                    PracticeSet.deleted == False,
                    PracticeSet.source_type == 'question',
                    PracticeSet.reviewed == True,
                    PracticeSetQuestion.is_correct.isnot(None)
                )
                .group_by(func.date(PracticeSet.created_at))
                .order_by(func.date(PracticeSet.created_at))
                .all()
            )

            cumulative_correct = 0
            cumulative_total = 0
            trend = []
            for log in logs:
                cumulative_correct += log.correct or 0
                cumulative_total += log.total or 0
                accuracy = round(cumulative_correct / cumulative_total * 100, 1) if cumulative_total > 0 else 0
                trend.append({
                    "date": log.date.strftime('%Y-%m-%d') if hasattr(log.date, 'strftime') else str(log.date),
                    "accuracy": accuracy
                })
            return trend
        except Exception:
            return []

    def _get_word_stats(self) -> Dict[str, Any]:
        """获取单词统计，使用数据库聚合避免加载所有记录"""
        try:
            # 使用数据库聚合计算总数
            total = self.db.query(func.count(Word.id)).filter(Word.deleted == False).scalar() or 0

            # 掌握分布 - 使用数据库聚合
            unmastered = (
                self.db.query(func.count(Word.id))
                .filter(Word.deleted == False, (Word.review_count == 0) | (Word.review_count.is_(None)))
                .scalar() or 0
            )
            learning = (
                self.db.query(func.count(Word.id))
                .filter(Word.deleted == False, Word.review_count > 0, Word.review_count <= 3)
                .scalar() or 0
            )
            mastered = (
                self.db.query(func.count(Word.id))
                .filter(Word.deleted == False, Word.review_count > 3)
                .scalar() or 0
            )

            # 低准确率单词 - 使用数据库查询过滤
            low_acc_query = (
                self.db.query(Word.english, Word.correct_count, Word.review_count)
                .filter(
                    Word.deleted == False,
                    Word.review_count > 0,
                    Word.correct_count.isnot(None)
                )
                .all()
            )
            low_acc = []
            for w in low_acc_query:
                acc = w.correct_count / w.review_count * 100
                if acc < 70:
                    low_acc.append({"word": w.english, "accuracy": round(acc, 1)})

            # 记忆曲线状态 - 使用数据库聚合
            now = datetime.now()
            due_review = (
                self.db.query(func.count(Word.id))
                .filter(Word.deleted == False, Word.next_review_at.isnot(None), Word.next_review_at <= now)
                .scalar() or 0
            )
            on_track = total - due_review

            # 复习频率趋势
            frequency = self._get_word_frequency_trend()

            return {
                "total": total,
                "mastery_distribution": {
                    "unmastered": unmastered,
                    "learning": learning,
                    "mastered": mastered,
                },
                "low_accuracy_words": low_acc[:20],
                "memory_curve_status": {
                    "due_review": due_review,
                    "on_track": on_track,
                },
                "frequency_trend": frequency,
            }
        except Exception as e:
            # 错误处理：返回空数据而不是崩溃
            return {
                "total": 0,
                "mastery_distribution": {
                    "unmastered": 0,
                    "learning": 0,
                    "mastered": 0,
                },
                "low_accuracy_words": [],
                "memory_curve_status": {
                    "due_review": 0,
                    "on_track": 0,
                },
                "frequency_trend": [],
            }

    def _get_word_frequency_trend(self) -> List[Dict]:
        """获取单词复习频率趋势"""
        try:
            logs = (
                self.db.query(
                    func.date(WordReviewLog.reviewed_at).label('date'),
                    func.count(WordReviewLog.id).label('count')
                )
                .filter(WordReviewLog.deleted == False)
                .group_by(func.date(WordReviewLog.reviewed_at))
                .order_by(func.date(WordReviewLog.reviewed_at))
                .all()
            )
            return [
                {"date": log.date.strftime('%Y-%m-%d') if hasattr(log.date, 'strftime') else str(log.date), "count": log.count}
                for log in logs
            ]
        except Exception:
            return []

    def _get_practice_stats(self) -> Dict[str, Any]:
        """获取练习统计，使用数据库聚合避免加载所有记录"""
        try:
            # 使用数据库聚合计算总数
            total_practices = (
                self.db.query(func.count(PracticeSet.id))
                .filter(PracticeSet.deleted == False)
                .scalar() or 0
            )

            # 频率热力图（按星期）- 使用数据库分组聚合
            weekday_results = (
                self.db.query(
                    func.date_trunc('dow', PracticeSet.created_at).label('dow'),
                    func.count(PracticeSet.id)
                )
                .filter(PracticeSet.deleted == False)
                .group_by(func.date_trunc('dow', PracticeSet.created_at))
                .all()
            )
            # 注意：不同数据库的date_trunc语法可能不同，这里简化处理
            weekday_counts = {}
            for r in weekday_results:
                if r.dow:
                    weekday_counts[str(r.dow)] = r[1]

            # 正确率趋势
            accuracy_trend = self._get_practice_accuracy_trend()

            return {
                "total_practices": total_practices,
                "frequency_heatmap": weekday_counts,
                "accuracy_trend": accuracy_trend,
            }
        except Exception as e:
            # 错误处理：返回空数据而不是崩溃
            return {
                "total_practices": 0,
                "frequency_heatmap": {},
                "accuracy_trend": [],
            }

    def _get_practice_accuracy_trend(self) -> List[Dict]:
        """获取练习正确率趋势"""
        try:
            from app.models import WordReview
            sessions = (
                self.db.query(WordReview)
                .order_by(WordReview.reviewed_at)
                .all()
            )

            cumulative_correct = 0
            cumulative_total = 0
            trend = []
            for s in sessions:
                cumulative_correct += s.correct_count or 0
                cumulative_total += s.total_count or 0
                accuracy = round(cumulative_correct / cumulative_total * 100, 1) if cumulative_total > 0 else 0
                trend.append({
                    "date": s.reviewed_at.strftime('%Y-%m-%d') if hasattr(s.reviewed_at, 'strftime') else str(s.reviewed_at),
                    "accuracy": accuracy
                })
            return trend
        except Exception:
            return []

    def _get_knowledge_graph(self) -> Dict[str, Any]:
        """获取知识点关联图，使用数据库聚合避免加载所有记录"""
        try:
            nodes = []
            edges = []

            # 获取知识点及其错误次数（使用数据库分组聚合）
            kp_error_results = (
                self.db.query(
                    KnowledgePoint.id,
                    KnowledgePoint.name,
                    KnowledgePoint.subject_id,
                    func.count(Question.id).label('error_count')
                )
                .outerjoin(Question, (KnowledgePoint.name == Question.knowledge_point) & (Question.deleted == False))
                .filter(KnowledgePoint.deleted == False)
                .group_by(KnowledgePoint.id, KnowledgePoint.name, KnowledgePoint.subject_id)
                .all()
            )

            # 构建节点
            for kp in kp_error_results:
                nodes.append({
                    "id": str(kp.id),
                    "name": kp.name,
                    "error_count": kp.error_count or 0,
                    "category": kp.subject_id or 0
                })

            return {"nodes": nodes, "edges": edges}
        except Exception as e:
            # 错误处理：返回空数据而不是崩溃
            return {"nodes": [], "edges": []}