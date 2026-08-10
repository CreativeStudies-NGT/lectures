import openpyxl
from openpyxl.styles import PatternFill, Font, Alignment, Border, Side
from pathlib import Path

REPORT_DIR = Path('lec8_report_kumano')
OUT_FILE = Path('lec8_eval_kumano.xlsx')

KEY_MAP = {
    '大きな問題関心': 'interest',
    '所属プログラムあるいは専攻におけるフォーカス': 'focus',
    '研究テーマ': 'theme',
    '研究目的・背景': 'purpose',
    '研究の問い': 'question',
    '学術的重要性・独自性': 'originality',
    '研究方法・アプローチ': 'method',
    '必要な資質・能力': 'skills',
    '修士論文・プロジェクトの限界と学際性の必要性': 'interdiscipl',
}
REVISED_KEY = '修士論文・プロジェクトの限界と学際性の必要性\n追記版（第8回後に記入）\n→最終レポート'


def extract_fields(xlsx_path):
    try:
        wb = openpyxl.load_workbook(xlsx_path, data_only=True)
    except Exception:
        return None

    ws = wb['授業資料学際的学修デザイン'] if '授業資料学際的学修デザイン' in wb.sheetnames else wb.active

    data = {v: '' for v in KEY_MAP.values()}
    data['revised'] = ''
    data['course_count'] = 0

    rows = list(ws.iter_rows(values_only=True))
    in_course = False

    for row in rows:
        if not row or not row[0]:
            continue
        key = str(row[0]).strip()
        val = str(row[2]).strip() if len(row) > 2 and row[2] else ''

        if key in KEY_MAP:
            data[KEY_MAP[key]] = val
        elif key == REVISED_KEY:
            data['revised'] = val
        elif key == '履修計画（M1～2）':
            in_course = True
        elif in_course and key not in ('科目名', '課題研究（8単位）',
                                       '学際的基盤科目群（6単位以上）',
                                       '学位共通科目群（8単位以上）',
                                       'プログラム専門科目群（6単位以上）'):
            if val and val not in ('…', '概要', '種別'):
                data['course_count'] += 1

    return data


def _len(s):
    return len(s) if s and s != 'None' else 0


def score_clarity(d):
    # 観点1: 専門外の読者にも伝わる明瞭さ (15点) S/A/B
    # S: 目的・問い・方法すべて詳細(100文字以上)かつ独自性も充実
    # A: 目的・問い・方法が詳細(50文字以上)
    # B: 主要項目が記入されているが一部が薄い
    detailed  = sum(1 for f in [d['purpose'], d['question'], d['method']] if _len(f) >= 100)
    adequate  = sum(1 for f in [d['purpose'], d['question'], d['method']] if _len(f) >= 50)
    present   = sum(1 for f in [d['theme'], d['purpose'], d['question'], d['method']] if _len(f) >= 20)
    if detailed >= 3 and _len(d['originality']) >= 50:
        return 15, 'S'
    elif adequate >= 3 and _len(d['theme']) >= 10:
        return 14, 'A'
    else:
        return 8, 'B'


def score_consistency(d):
    # 観点2: 研究計画・履修計画としての一貫性 (15点) S/A/B
    # S: 7項目すべてが充実（50文字以上）
    # A: 7項目のうち5つ以上が充実（30文字以上）
    # B: 5項目以上が記入（10文字以上）
    plan_fields = [d['interest'], d['focus'], d['theme'], d['purpose'],
                   d['question'], d['method'], d['skills']]
    very_rich = sum(1 for f in plan_fields if _len(f) >= 50)
    rich      = sum(1 for f in plan_fields if _len(f) >= 30)
    filled    = sum(1 for f in plan_fields if _len(f) >= 10)
    if very_rich >= 7:
        return 15, 'S'
    elif rich >= 5:
        return 14, 'A'
    else:
        return 12, 'B'


def score_interdiscipl(d):
    # 観点3: 学際的思考・専門性の限界・改善 (20点) S/A/B
    # S: 初版が充実(150文字以上) + 追記版が実質的に新しい内容(150文字以上)
    # A: 初版が充実(100文字以上) + 追記版に改善あり(80文字以上)
    # B: どちらか一方が充実、または両方あるが薄い
    init_len = _len(d['interdiscipl'])
    rev_len  = _len(d['revised'])
    similarity = len(set(d['interdiscipl'][:50]) & set(d['revised'][:50])) / max(len(set(d['interdiscipl'][:50])), 1) \
        if d['interdiscipl'] and d['revised'] else 0
    genuinely_revised = rev_len >= 80 and similarity < 0.9

    if init_len >= 300 and rev_len >= 150 and genuinely_revised:
        return 20, 'S'
    elif init_len >= 100 and genuinely_revised:
        return 18, 'A'
    else:
        return 16, 'B'


def get_student_info(fname):
    parts = fname.stem.split('_')
    sid = parts[1] if len(parts) > 1 else ''
    name = parts[2] if len(parts) > 2 else ''
    return sid, name


def main():
    files = sorted(REPORT_DIR.glob('*.xlsx'))
    pdf_files = sorted(REPORT_DIR.glob('*.pdf'))

    wb_out = openpyxl.Workbook()
    ws = wb_out.active
    ws.title = '評価案'

    # ヘッダー
    headers = [
        '番号', '在籍番号', '氏名',
        '①明瞭さ(15)', '①判定',
        '②一貫性(15)', '②判定',
        '③学際性(20)', '③判定',
        '合計(50)',
        '研究テーマ', '研究の問い', '研究方法',
        '限界と学際性（初版）', '限界と学際性（追記版）',
        '備考'
    ]
    ws.append(headers)

    header_fill = PatternFill('solid', fgColor='1F4E79')
    header_font = Font(color='FFFFFF', bold=True)
    for cell in ws[1]:
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal='center', wrap_text=True)

    # 色設定
    fill_s = PatternFill('solid', fgColor='9DC3E6')
    fill_a = PatternFill('solid', fgColor='C6EFCE')
    fill_b = PatternFill('solid', fgColor='FFEB9C')
    fill_c = PatternFill('solid', fgColor='FFC7CE')

    def judgement_fill(label):
        if label == 'S':
            return fill_s
        elif label == 'A':
            return fill_a
        elif label == 'C':
            return fill_c
        else:
            return fill_b

    for i, f in enumerate(files, 1):
        sid, name = get_student_info(f)
        data = extract_fields(f)
        if data is None:
            ws.append([i, sid, name, '-', '-', '-', '-', '-', '-', '-', '読み込みエラー'])
            continue

        s1, j1 = score_clarity(data)
        s2, j2 = score_consistency(data)
        s3, j3 = score_interdiscipl(data)
        total = s1 + s2 + s3

        row = [
            i, sid, name,
            s1, j1,
            s2, j2,
            s3, j3,
            total,
            data['theme'][:40] if data['theme'] else '',
            data['question'][:40] if data['question'] else '',
            data['method'][:30] if data['method'] else '',
            data['interdiscipl'][:60] if data['interdiscipl'] else '',
            data['revised'][:60] if data['revised'] else '',
            ''
        ]
        ws.append(row)

        r = ws.max_row
        for col, jval in [(5, j1), (7, j2), (9, j3)]:
            ws.cell(r, col).fill = judgement_fill(jval)

    # PDFファイルは別途メモ
    if pdf_files:
        ws.append([])
        ws.append(['※ PDFファイル（要手動評価）'])
        for f in pdf_files:
            sid, name = get_student_info(f)
            ws.append(['', sid, name, '', '', '', '', '', '', '', 'PDF形式・手動確認要'])

    # 列幅調整
    col_widths = [5, 13, 10, 10, 7, 10, 7, 10, 7, 10, 35, 35, 25, 50, 50, 20]
    for i, w in enumerate(col_widths, 1):
        ws.column_dimensions[openpyxl.utils.get_column_letter(i)].width = w

    ws.freeze_panes = 'A2'
    ws.auto_filter.ref = f'A1:{openpyxl.utils.get_column_letter(len(headers))}1'

    wb_out.save(OUT_FILE)
    print(f'保存: {OUT_FILE}  ({len(files)}名)')


if __name__ == '__main__':
    main()
