"""
대한민국 최근 5년 지진 데이터 분석 프로젝트
실행: python main.py
"""
import subprocess
import sys
import os

def run(script: str):
    print(f"\n{'='*50}")
    print(f" 실행 중: {script}")
    print('='*50)
    result = subprocess.run([sys.executable, script], capture_output=False)
    if result.returncode != 0:
        print(f"오류 발생: {script}")
        sys.exit(1)

if __name__ == "__main__":
    base = os.path.dirname(__file__)
    run(os.path.join(base, "scripts", "fetch_data.py"))
    run(os.path.join(base, "scripts", "process_excel.py"))
    run(os.path.join(base, "scripts", "visualize.py"))
    print("\n✔ 완료!")
    print(f"  Excel  → output/지진데이터_2021-2026.xlsx")
    print(f"  차트   → output/charts/")
