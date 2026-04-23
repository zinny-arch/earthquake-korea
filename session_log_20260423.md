# 작업 세션 로그 — 2026-04-23

## 1. 다운로드 폴더 정리
- 위치: `C:\Users\zinny\Downloads` → `C:\Users\zinny\OneDrive\Desktop`
- 42개 파일을 7개 폴더로 분류

| 폴더 | 파일 수 | 내용 |
|------|--------|------|
| 설치파일 | 10개 | .exe, .msi |
| 학술논문 | 14개 | IS/MIS 영문 논문 PDF |
| 데이터 | 10개 | .xls, .csv |
| 강의자료 | 5개 | 강의계획서 + Summary 문서 |
| 압축파일 | 3개 | .zip 등 |
| 문서 | 1개 | 보도자료 초안 |
| 기타 | 2개 | winmd, 윈도우 정품키 |

---

## 2. Python 설치
- python.org에서 Python 3.12.9 인스톨러 직접 다운로드 후 설치
- 실제 설치된 버전: Python 3.13.13
- 경로: `C:\Users\zinny\AppData\Local\Programs\Python\Python313\python.exe`
- 설치 패키지: pandas, openpyxl, matplotlib, numpy, requests, xlrd

---

## 3. 지진 데이터 분석 프로젝트 생성

### 프로젝트 위치
- 로컬: `C:\Users\zinny\earthquake-korea\`
- GitHub: https://github.com/zinny-arch/earthquake-korea

### 구조
```
earthquake-korea/
├── data/raw/
│   └── 국내지진목록_2026-01-01_2026-03-08.xls
├── output/
│   ├── 지진데이터_2021-2026.xlsx
│   └── charts/
│       ├── 01_지역별_발생횟수.png
│       ├── 02_연도별_추세.png
│       ├── 03_규모등급_비율.png
│       ├── 04_월별_히트맵.png
│       └── 05_지역별_규모_분포.png
├── scripts/
│   ├── fetch_data.py       ← 데이터 수집
│   ├── process_excel.py    ← Excel 생성
│   └── visualize.py        ← 시각화
├── main.py
├── requirements.txt
└── .gitignore
```

### 실행 방법
```bash
cd C:\Users\zinny\earthquake-korea
python main.py
```

### 생성 결과물
- **Excel**: 지진 목록 / 지역별 통계 / 연도별 통계 3개 시트
- **차트 5종**: 지역별 막대, 연도별 추세, 규모 등급 도넛, 월별 히트맵, 박스플롯

### 참고
- 기존 XLS 파일(2026-01-01~03-08)이 xlrd 엔진 미지정으로 로드 실패
- 현재는 5년치 샘플 데이터(463건)로 대체됨
- 기상청 사이트에서 2021~2025년 데이터 추가 다운로드 후 `data/raw/`에 넣으면 자동 반영

---

## 4. Git 커밋 이력
| 커밋 | 내용 |
|------|------|
| 2bcdbaa | 프로젝트 초기 구성 |
| ecc10fd | visualize.py 색상 변수 순서 버그 수정 |
| 88426ba | 시각화 차트 5종 추가 |
