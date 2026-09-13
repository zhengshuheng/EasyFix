"""
导入六年级上学期词表到数据库
数据来源：教材图片解析
"""
import json
import sys
import os

# 添加 backend 到 path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal, engine, Base
from app.models import Word, Tag
from app.models.word import word_tag


def ensure_tables():
    """确保表已创建"""
    Base.metadata.create_all(bind=engine)


def get_or_create_unit_tag(db, unit: int) -> Tag:
    """获取或创建单元标签"""
    tag_name = f"六上Unit{unit}"
    tag = db.query(Tag).filter(Tag.name == tag_name, Tag.deleted == False).first()
    if not tag:
        # 单元标签用不同颜色区分
        colors = {
            1: "#409EFF",
            2: "#67C23A",
            3: "#E6A23C",
            4: "#F56C6C",
            5: "#909399",
            6: "#00c1de",
        }
        tag = Tag(name=tag_name, color=colors.get(unit, "#409EFF"), deleted=False)
        db.add(tag)
        db.commit()
        db.refresh(tag)
        print(f"创建标签: {tag_name} (id={tag.id})")
    return tag


def import_words():
    """导入单词"""
    json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "grade6_sem1_words.json")
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    grade = data["grade"]
    semester = data["semester"]
    units = data["units"]

    db = SessionLocal()
    created = 0
    skipped = 0
    tagged = 0
    errors = []

    try:
        for unit_data in units:
            unit = unit_data["unit"]
            tag = get_or_create_unit_tag(db, unit)
            print(f"\n=== Unit {unit} ({len(unit_data['words'])} words) ===")

            for w in unit_data["words"]:
                english = (w.get("english") or "").strip()
                chinese = (w.get("chinese") or "").strip()
                phonetic = (w.get("phonetic") or "").strip() or None

                if not english or not chinese:
                    skipped += 1
                    continue

                # 查重：同英文且未软删除
                existing = (
                    db.query(Word)
                    .filter(Word.english == english, Word.deleted == False)
                    .first()
                )
                if existing:
                    # 补全年级/学期/音标
                    changed = False
                    if existing.grade is None:
                        existing.grade = grade
                        changed = True
                    if existing.semester is None:
                        existing.semester = semester
                        changed = True
                    if not existing.phonetic and phonetic:
                        existing.phonetic = phonetic
                        changed = True
                    if not existing.chinese and chinese:
                        existing.chinese = chinese
                        changed = True
                    if changed:
                        db.commit()
                    # 绑定单元标签
                    if tag not in existing.tags:
                        existing.tags.append(tag)
                        db.commit()
                        tagged += 1
                    skipped += 1
                    print(f"  skip (exists): {english}")
                    continue

                word = Word(
                    english=english,
                    chinese=chinese,
                    phonetic=phonetic,
                    grade=grade,
                    semester=semester,
                    review_count=0,
                    correct_count=0,
                    ease_factor=250,
                    interval=1,
                    learning_phase="新学",
                    deleted=False,
                )
                db.add(word)
                db.commit()
                db.refresh(word)
                word.tags.append(tag)
                db.commit()
                created += 1
                tagged += 1
                print(f"  + {english} | {chinese[:40]}")

        print("\n========== 导入完成 ==========")
        print(f"新建: {created}")
        print(f"已存在跳过: {skipped}")
        print(f"标签绑定次数: {tagged}")
        print(f"错误: {len(errors)}")
    except Exception as e:
        db.rollback()
        print(f"导入失败: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    ensure_tables()
    import_words()
