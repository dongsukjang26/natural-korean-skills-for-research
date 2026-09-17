#!/usr/bin/env python3
"""ko-lint.py — natural-korean-skills-for-research 스킬의 기계적 검사기.

표준 라이브러리만 씁니다. 파일이나 stdin을 받아 번역투, AI 문체, 용어 표기를
검사하고, 어긴 자리를 행 번호와 함께 보고합니다.

  python3 ko-lint.py 초안.md
  cat 초안.md | python3 ko-lint.py --json
  python3 ko-lint.py --selftest

심각도
  S1  한 번만 나와도 고칩니다. 이 건수가 --baseline을 넘으면 종료 코드 1.
  S2  빈도로 판단합니다. 한 문단 안에서 임계값을 넘으면 보고합니다.
  S3  참고용입니다. 종료 코드에 영향을 주지 않습니다.

검사하지 못하는 것: 뜻이 통하는지, 사실이 맞는지, 고친 글이 원문과 같은
주장을 하는지. 문체 표면만 봅니다.
"""

import argparse
import json
import re
import sys
from statistics import mean, pstdev

JONG_RIEUL = 8  # 종성 ㄹ의 인덱스


# ---------------------------------------------------------------- 전처리

FENCE = re.compile(r"^\s*(```|~~~)")
INLINE_CODE = re.compile(r"`[^`\n]*`")
URL = re.compile(r"https?://\S+")


def mask_code(text):
    """코드와 URL을 같은 길이의 공백으로 덮습니다. 행 번호가 보존됩니다."""
    out, in_fence = [], False
    for line in text.split("\n"):
        if FENCE.match(line):
            in_fence = not in_fence
            out.append(" " * len(line))
            continue
        if in_fence:
            out.append(" " * len(line))
            continue
        line = INLINE_CODE.sub(lambda m: " " * len(m.group(0)), line)
        line = URL.sub(lambda m: " " * len(m.group(0)), line)
        out.append(line)
    return "\n".join(out)


def line_of(text, pos):
    return text.count("\n", 0, pos) + 1


def paragraphs(text):
    """(시작 오프셋, 문단 텍스트) 목록."""
    result, pos = [], 0
    for chunk in re.split(r"\n\s*\n", text):
        result.append((pos, chunk))
        pos += len(chunk) + 2
    return [(p, c) for p, c in result if c.strip()]


SENT_SPLIT = re.compile(r"(?<=[.!?…])\s+|\n+")


def sentences(text):
    raw = SENT_SPLIT.split(text)
    return [s.strip() for s in raw if len(s.strip()) > 1]


# ---------------------------------------------------------------- 규칙

# (id, 심각도, 정규식, 메시지, 제안)
ALWAYS = [
    ("double-passive",
     "S1",
     r"(되어|보여|나뉘어|쓰여|불려|잊혀|짜여|모여|닫혀|열려)(지|져|졌|짐|집)",
     "이중 피동입니다. 한국어 규범에서 비문으로 봅니다.",
     "피동을 한 번만 쓰거나 능동으로 바꾸세요. 되어진다 → 된다 / (행위자)가 한다"),
    ("e-isseoseo",
     "S1",
     r"에\s*있어서",
     "'~에 있어서'는 일본어 において의 차용입니다.",
     "'~에서', '~의 경우'로 바꾸거나 통째로 빼세요."),
    ("gajigo-issda",
     "S1",
     r"(을|를)\s*(가지고|갖고)\s*있",
     "영어 have의 직역입니다.",
     "형용사로 바꾸세요. 기능을 가지고 있다 → 기능이 다양하다"),
    ("ai-ending",
     "S1",
     r"(결론적으로|시사하는\s*바|주목할\s*만하|지금이야말로|본질적으로|핵심적으로)",
     "AI 결말 관용구입니다. 영어 결론 정형 표현의 직역입니다.",
     "통째로 지우고 본문으로 끝내세요."),
    ("abstract-subject",
     "S1",
     r"(을|를)\s*가져(온다|올|왔|옵니다|왔습니다)",
     "추상 주어 + 만능 동사입니다. 영어 X brings Y 구조입니다.",
     "구체적인 주어로 바꾸세요. 변화는 향상을 가져온다 → 이렇게 바꾸면 빨라진다"),
]

# (id, 심각도, 정규식, 문단당 임계값, 메시지, 제안)
DENSITY = [
    ("e-daehae", "S2", r"에\s*대(해서?|한)\b", 2,
     "'~에 대해/대한'이 잦습니다. 영어 about의 직역입니다.",
     "목적격 조사로 환원하세요. X에 대해 분석 → X를 분석"),
    ("reul-tonghae", "S2", r"(을|를)\s*통(해서?|하여)", 2,
     "'~를 통해'가 잦습니다. 영어 through의 직역입니다.",
     "'~로', '~해서', '~함으로써'로 분산하세요."),
    ("eul-wihae", "S2", r"(을|를)\s*위(해서?|하여|한)", 2,
     "'~을 위해'가 잦습니다. 영어 in order to의 직역입니다.",
     "'~려고', '~고자'로 분산하거나 조사로 직결하세요."),
    ("e-uihae", "S2", r"에\s*의(해서?|한)\b", 2,
     "'~에 의해'가 잦습니다. 영어 수동태의 직역입니다.",
     "행위자를 주어로 올려 능동으로 쓰세요. 단, 학술 정형 표현은 그대로 둡니다."),
    ("e-giban", "S2", r"(에\s*기반(해서?|하여|한)|(을|를)\s*바탕으로)", 2,
     "'~에 기반하여/바탕으로'가 잦습니다. 영어 based on의 직역입니다.",
     "'~로', '~을 보고', '~을 토대로'로 분산하세요."),
    ("gwanryeon", "S2", r"(와|과)\s*관련(해서?|하여|된|한)", 2,
     "'~와 관련하여'가 잦습니다. 격식 잉여입니다.",
     "명사구로 직결하세요. 교육과 관련된 정책 → 교육 정책"),
    ("geot-ida", "S2", r"(것이(다|었|겠)|것입니다|것이라고)", 2,
     "'~것이다'가 잦습니다. 영어 will의 직역입니다.",
     "단언 현재형으로 바꾸세요. 증가할 것이다 → 증가한다"),
    ("jeok-N", "S2", r"[가-힣]적\s+[가-힣]", 3,
     "'~적 N' 추상 체인이 잦습니다.",
     "풀어 쓰세요. 구조적 한계 → 구조의 한계"),
    ("hype", "S2", r"(혁신적|획기적|압도적|전례\s*없|강력한|놀라운|엄청난|치명적|파격적)", 2,
     "강조 어휘가 잦습니다.",
     "한 단락에 하나까지 두고 나머지는 구체적 사실로 바꾸세요."),
    ("ai-vocab", "S2", r"(핵심적|효과적|지속\s*가능한|필수적|다양한)", 2,
     "AI가 자주 쓰는 상투적 서술어입니다.",
     "구체적인 말로 바꾸세요. 다양한 → 여러 / 세 가지"),
    ("deul-plural", "S3", r"[가-힣]들(이|을|은|의|과|도|에게|에서)?\s", 3,
     "복수 '-들'이 잦습니다. 한국어는 복수를 잘 표시하지 않습니다.",
     "'-들'을 빼세요. 모델들을 → 모델을"),
    ("demonstrative", "S3", r"(이러한|그러한|이와\s*같은|해당|이를\s*통해)", 3,
     "지시어가 잦습니다.",
     "명사를 다시 쓰거나 빼세요. 해당 오류 → 이 오류 / (생략)"),
    ("pronoun", "S3", r"(그것|이것|그들|우리는)", 3,
     "대명사가 잦습니다. 한국어는 문맥으로 아는 주어를 생략합니다.",
     "자명한 주어와 대명사를 빼세요."),
    ("conj-comma", "S3", r"(하고|하며|되고|이며|으며|지만|면서),", 2,
     "연결어미 뒤 쉼표가 잦습니다. 영어식 쉼표 배치입니다.",
     "쉼표를 빼거나 문장을 나누세요."),
]

# 음차한 1층 용어 → 영문
TRANSLIT = {
    "어텐션": "attention",
    "셀프 어텐션": "self-attention",
    "임베딩": "embedding",
    "파인튜닝": "fine-tuning",
    "파인 튜닝": "fine-tuning",
    "프리트레이닝": "pretraining",
    "트랜스포머": "transformer",
    "베이스라인": "baseline",
    "토크나이저": "tokenizer",
    "그래디언트": "gradient",
    "옵티마이저": "optimizer",
    "오버피팅": "overfitting",
    "드롭아웃": "dropout",
    "러닝레이트": "learning rate",
    "러닝 레이트": "learning rate",
    "배치사이즈": "batch size",
    "배치 사이즈": "batch size",
    "어블레이션": "ablation",
    "할루시네이션": "hallucination",
    "인퍼런스": "inference",
    "사고의 연쇄": "chain-of-thought",
}

ENG_HADA = re.compile(r"[A-Za-z][A-Za-z\-]{1,}(하다|한다|했|합니다|하고|하면|해서|하는|한\s|함)")
# 연구 글은 학술 정형 표현과 불확실성 표현을 더 허용합니다.
THRESHOLD_OVERRIDE = {"e-uihae": 3, "geot-ida": 3}

MAX_EOJEOL = 30   # 문장 최대 어절
AVG_EOJEOL = 21   # 평균 어절 권장

# 한글 음차 + 영문 병기: 같은 용어를 두 번 이상 병기하면 읽기가 끊깁니다.
BYEONGGI = re.compile(r"([가-힣]{2,})\s*\(\s*([A-Za-z][A-Za-z \-]*)\s*\)")


def find_su_issda(text):
    """'~할 수 있다' — 앞 음절의 받침이 ㄹ일 때만 셉니다."""
    hits = []
    for m in re.finditer(r"수\s*있", text):
        j = m.start() - 1
        while j >= 0 and text[j].isspace():
            j -= 1
        if j < 0:
            continue
        ch = text[j]
        if "가" <= ch <= "힣" and (ord(ch) - 0xAC00) % 28 == JONG_RIEUL:
            hits.append(m.start())
    return hits


# ---------------------------------------------------------------- 검사

def check(text, path="<stdin>", disabled=()):
    masked = mask_code(text)
    findings = []

    def add(rule, sev, pos, msg, fix):
        if rule in disabled:
            return
        findings.append({
            "file": path, "line": line_of(masked, pos), "rule": rule,
            "severity": sev, "message": msg, "suggestion": fix,
        })

    for rule, sev, pat, msg, fix in ALWAYS:
        for m in re.finditer(pat, masked):
            add(rule, sev, m.start(), f"{msg} — '{m.group(0)}'", fix)

    for start, para in paragraphs(masked):
        for rule, sev, pat, thresh, msg, fix in DENSITY:
            thresh = THRESHOLD_OVERRIDE.get(rule, thresh)
            hits = list(re.finditer(pat, para))
            if len(hits) > thresh:
                add(rule, sev, start + hits[0].start(),
                    f"{msg} 이 문단에 {len(hits)}회.", fix)
        su = find_su_issda(para)
        if len(su) > 4:
            add("su-issda", "S2", start + su[0],
                f"'~할 수 있다'가 이 문단에 {len(su)}회. 영어 can의 직역입니다.",
                "진짜 불확실성을 나타내는 자리는 그대로 두고, 능력과 허가를 "
                "말하는 자리만 단언으로 바꾸세요.")
        for ko, en in TRANSLIT.items():
            for m in re.finditer(re.escape(ko), para):
                # 바로 뒤에 영문을 병기했으면 입문자용 정식 표기이므로 넘어갑니다.
                if re.match(r"\s*\(\s*[A-Za-z]", para[m.end():m.end() + 8]):
                    continue
                add("translit-term", "S2", start + m.start(),
                    f"1층 용어를 음차했습니다 — '{ko}'.",
                    f"영문으로 쓰세요: {en}")
        for m in ENG_HADA.finditer(para):
            add("eng-hada", "S3", start + m.start(),
                f"영어 어근에 '-하다'를 직결했습니다 — '{m.group(0)}'.",
                "조사를 넣으세요. fine-tuning했다 → fine-tuning을 했다")

    seen = {}
    for m in BYEONGGI.finditer(masked):
        key = m.group(2).strip().lower()
        seen.setdefault(key, []).append(m)
    for key, hits in seen.items():
        if len(hits) > 1:
            add("repeat-byeonggi", "S3", hits[1].start(),
                f"같은 용어를 {len(hits)}번 병기했습니다 — '{hits[1].group(0)}'.",
                "병기는 문서에서 처음 등장할 때 한 번만 하고, 그다음부터는 "
                "한 표기로 고정하세요.")

    max_w, avg_w = MAX_EOJEOL, AVG_EOJEOL
    sents = sentences(masked)
    if sents:
        lens = [len(s.split()) for s in sents]
        for s, n in zip(sents, lens):
            if n > max_w:
                pos = masked.find(s)
                add("long-sentence", "S2", pos if pos >= 0 else 0,
                    f"문장이 {n}어절입니다. 상한은 {max_w}어절입니다.",
                    "문장을 나누세요. 한국어는 관계절을 겹쳐 쌓지 못합니다.")
        if mean(lens) > avg_w:
            add("avg-length", "S3", 0,
                f"평균 문장 길이가 {mean(lens):.1f}어절입니다. 권장은 {avg_w}어절 이하입니다.",
                "설명을 두 문장으로 나누세요.")
        if len(lens) >= 5 and mean(lens) > 0 and pstdev(lens) / mean(lens) < 0.15:
            add("monotone", "S3", 0,
                "문장 길이가 거의 같습니다. AI가 쓴 글의 특징입니다.",
                "짧은 문장을 하나 끼워 리듬을 만드세요.")
        commas = masked.count(",") + masked.count("，")
        if commas / len(sents) > 1.0:
            add("comma-density", "S2", 0,
                f"문장당 쉼표가 {commas / len(sents):.1f}개입니다.",
                "연결어미 뒤 쉼표를 빼세요. 한국어는 쉼표 없이 이어집니다.")

    order = {"S1": 0, "S2": 1, "S3": 2}
    findings.sort(key=lambda f: (order[f["severity"]], f["line"]))
    return findings


# ---------------------------------------------------------------- 출력

def report(findings, as_json, baseline):
    hard = sum(1 for f in findings if f["severity"] == "S1")
    if as_json:
        print(json.dumps({"findings": findings, "hard": hard}, ensure_ascii=False, indent=2))
    else:
        for f in findings:
            print(f"{f['file']}:{f['line']} [{f['severity']}] {f['rule']}  {f['message']}")
            print(f"    → {f['suggestion']}")
        s2 = sum(1 for f in findings if f["severity"] == "S2")
        s3 = sum(1 for f in findings if f["severity"] == "S3")
        if findings:
            print(f"\nS1 {hard}건, S2 {s2}건, S3 {s3}건.")
        else:
            print("규칙 위반 없음.")
    return 1 if hard > baseline else 0


# ---------------------------------------------------------------- 자체 검사

BAD = """본 연구에 있어서 데이터는 신중하게 분석되어집니다. 이러한 결과는
연구팀에 의해 검증된 것이며, 어텐션 메커니즘에 기반하여 파인튜닝을
진행하였습니다. 결론적으로 이 기법은 효과적임을 시사하는 바가 큽니다.
"""

GOOD = """이 연구에서는 데이터를 신중하게 분석했다. 연구팀이 직접 검증했다.
attention 기반 모델로 fine-tuning을 하니 정확도가 baseline보다 높았다.
이 기법이 통한다는 신호로 볼 만하다.
"""

HEDGE = "이 설정은 학습을 발산시킬 수 있다.\n"


def selftest():
    ok = True

    got = {f["rule"] for f in check(BAD, "BAD")}
    want = {"double-passive", "e-isseoseo", "ai-ending", "translit-term"}
    missing = want - got
    if missing:
        print(f"FAIL: BAD 샘플에서 못 잡은 규칙 {sorted(missing)}")
        ok = False

    findings = check(GOOD, "GOOD")
    hard = [f for f in findings if f["severity"] == "S1"]
    if hard:
        print(f"FAIL: GOOD 샘플에서 S1 오검출 {[f['rule'] for f in hard]}")
        ok = False

    # 추측 표현 1회는 잡지 않습니다. 확신의 세기는 내용이지 문체가 아닙니다.
    if check(HEDGE, "HEDGE"):
        print("FAIL: 단발 추측 표현을 잡았습니다")
        ok = False

    # 코드 블록 안은 검사하지 않습니다.
    fenced = "```\n분석되어집니다\n```\n정상 문장이다.\n"
    if [f for f in check(fenced, "FENCE") if f["rule"] == "double-passive"]:
        print("FAIL: 코드 블록 안을 검사했습니다")
        ok = False

    print("selftest 통과" if ok else "selftest 실패")
    return 0 if ok else 1


def main():
    p = argparse.ArgumentParser(description="natural-korean-skills-for-research 기계적 검사기 (AI/CS 연구 글)")
    p.add_argument("files", nargs="*", help="검사할 파일. 없으면 stdin.")
    p.add_argument("--json", action="store_true")
    p.add_argument("--baseline", type=int, default=0, help="허용할 S1 건수")
    p.add_argument("--disable", default="", help="끌 규칙 id를 쉼표로 구분")
    p.add_argument("--selftest", action="store_true")
    a = p.parse_args()

    if a.selftest:
        return selftest()

    disabled = tuple(x.strip() for x in a.disable.split(",") if x.strip())
    findings = []
    if a.files:
        for path in a.files:
            with open(path, encoding="utf-8") as fh:
                findings += check(fh.read(), path, disabled)
    else:
        findings += check(sys.stdin.read(), "<stdin>", disabled)
    return report(findings, a.json, a.baseline)


if __name__ == "__main__":
    sys.exit(main())
