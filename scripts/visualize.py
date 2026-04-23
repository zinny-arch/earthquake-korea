"""
지진 데이터 시각화 스크립트
지역별/연도별/규모별 통계를 차트로 출력합니다.
"""
import os
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib.patches as mpatches
import numpy as np

matplotlib.use("Agg")

DATA_FILE   = os.path.join(os.path.dirname(__file__), "..", "data", "raw", "earthquake_5years.csv")
OUTPUT_DIR  = os.path.join(os.path.dirname(__file__), "..", "output", "charts")

# ── 한글 폰트 설정 ────────────────────────────────────────────────────────────
def setup_korean_font():
    candidates = ["Malgun Gothic", "NanumGothic", "AppleGothic", "Gulim"]
    for name in candidates:
        if any(name.lower() in f.name.lower() for f in fm.fontManager.ttflist):
            plt.rcParams["font.family"] = name
            plt.rcParams["axes.unicode_minus"] = False
            return name
    # fallback: 시스템에서 첫 번째 한글 폰트 검색
    for f in fm.fontManager.ttflist:
        if any(kw in f.name for kw in ["Gothic", "Nanum", "Gungsuh", "Batang"]):
            plt.rcParams["font.family"] = f.name
            plt.rcParams["axes.unicode_minus"] = False
            return f.name
    print("  경고: 한글 폰트를 찾지 못했습니다. 폰트를 직접 지정하세요.")
    return None


PALETTE = ["#1F4E79", "#2E75B6", "#4BACC6", "#70AD47", "#ED7D31",
           "#FF0000", "#7030A0", "#C00000", "#FFC000", "#375623",
           "#843C0C", "#833C00"]


def load_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_FILE, encoding="utf-8-sig")
    df["규모"] = pd.to_numeric(df["규모"], errors="coerce")
    df["발생시각"] = pd.to_datetime(df["발생시각"], errors="coerce")
    df["연도"] = df["발생시각"].dt.year
    df["월"] = df["발생시각"].dt.month
    df["규모등급"] = pd.cut(
        df["규모"],
        bins=[0, 2.0, 3.0, 4.0, 10],
        labels=["미소지진 (<2.0)", "소규모 (2.0~3.0)", "중규모 (3.0~4.0)", "강진 (≥4.0)"]
    )
    return df


def fig1_region_bar(df: pd.DataFrame):
    """지역별 발생 횟수 가로 막대 차트"""
    region_counts = df["위치"].value_counts().head(12)

    fig, ax = plt.subplots(figsize=(11, 6))
    bars = ax.barh(region_counts.index[::-1], region_counts.values[::-1],
                   color=PALETTE[:len(region_counts)], edgecolor="white", linewidth=0.5)

    for bar, val in zip(bars, region_counts.values[::-1]):
        ax.text(val + 0.5, bar.get_y() + bar.get_height() / 2,
                f"{val}건", va="center", fontsize=9, color="#333333")

    ax.set_title("지역별 지진 발생 횟수 (2021~2026)", fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel("발생 횟수 (건)", fontsize=10)
    ax.spines[["top", "right"]].set_visible(False)
    ax.set_facecolor("#F9FBFD")
    fig.patch.set_facecolor("#FFFFFF")
    ax.grid(axis="x", linestyle="--", alpha=0.4)
    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, "01_지역별_발생횟수.png")
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  저장: {path}")


def fig2_yearly_trend(df: pd.DataFrame):
    """연도별 발생 추세 꺾은선 + 막대 복합 차트"""
    yearly = df.groupby("연도").agg(
        발생횟수=("규모", "count"),
        평균규모=("규모", "mean")
    ).reset_index()

    fig, ax1 = plt.subplots(figsize=(10, 5))
    ax2 = ax1.twinx()

    bars = ax1.bar(yearly["연도"], yearly["발생횟수"], color="#2E75B6",
                   alpha=0.7, label="발생 횟수", width=0.5)
    line, = ax2.plot(yearly["연도"], yearly["평균규모"], color="#ED7D31",
                     marker="o", linewidth=2, markersize=6, label="평균 규모")

    ax1.set_title("연도별 지진 발생 추세 (2021~2026)", fontsize=14, fontweight="bold", pad=15)
    ax1.set_xlabel("연도", fontsize=10)
    ax1.set_ylabel("발생 횟수 (건)", color="#2E75B6", fontsize=10)
    ax2.set_ylabel("평균 규모 (M)", color="#ED7D31", fontsize=10)
    ax1.tick_params(axis="y", labelcolor="#2E75B6")
    ax2.tick_params(axis="y", labelcolor="#ED7D31")
    ax1.spines[["top"]].set_visible(False)
    ax2.spines[["top"]].set_visible(False)
    ax1.set_facecolor("#F9FBFD")
    fig.patch.set_facecolor("#FFFFFF")

    handles = [bars, line]
    labels = ["발생 횟수", "평균 규모"]
    ax1.legend(handles, labels, loc="upper left", fontsize=9)

    for bar, val in zip(bars, yearly["발생횟수"]):
        ax1.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5,
                 str(val), ha="center", va="bottom", fontsize=9)

    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, "02_연도별_추세.png")
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  저장: {path}")


def fig3_magnitude_pie(df: pd.DataFrame):
    """규모 등급별 비율 도넛 차트"""
    grade_counts = df["규모등급"].value_counts()
    MAG_LOW  = "#C6EFCE"
    MAG_MID  = "#FFEB9C"
    MAG_HIGH = "#FFC7CE"
    colors = [MAG_LOW, MAG_MID, MAG_HIGH, "#C00000"]

    fig, ax = plt.subplots(figsize=(8, 7))
    wedges, texts, autotexts = ax.pie(
        grade_counts.values,
        labels=None,
        autopct="%1.1f%%",
        startangle=90,
        colors=colors[:len(grade_counts)],
        pctdistance=0.78,
        wedgeprops={"width": 0.55, "edgecolor": "white", "linewidth": 2},
    )
    for at in autotexts:
        at.set_fontsize(9)
        at.set_fontweight("bold")

    ax.legend(wedges, grade_counts.index, title="규모 등급", loc="lower center",
              bbox_to_anchor=(0.5, -0.1), ncol=2, fontsize=9)
    ax.set_title("규모 등급별 발생 비율 (2021~2026)", fontsize=14, fontweight="bold", pad=15)
    fig.patch.set_facecolor("#FFFFFF")

    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, "03_규모등급_비율.png")
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  저장: {path}")


def fig4_monthly_heatmap(df: pd.DataFrame):
    """연도 × 월 히트맵"""
    pivot = df.pivot_table(index="연도", columns="월", values="규모",
                           aggfunc="count", fill_value=0)
    pivot.columns = ["1월","2월","3월","4월","5월","6월",
                     "7월","8월","9월","10월","11월","12월"][:len(pivot.columns)]

    fig, ax = plt.subplots(figsize=(12, 5))
    im = ax.imshow(pivot.values, cmap="Blues", aspect="auto")

    ax.set_xticks(range(len(pivot.columns)))
    ax.set_xticklabels(pivot.columns, fontsize=9)
    ax.set_yticks(range(len(pivot.index)))
    ax.set_yticklabels(pivot.index, fontsize=9)

    for i in range(len(pivot.index)):
        for j in range(len(pivot.columns)):
            val = pivot.values[i, j]
            color = "white" if val > pivot.values.max() * 0.6 else "#333333"
            ax.text(j, i, str(int(val)), ha="center", va="center",
                    fontsize=8, color=color)

    plt.colorbar(im, ax=ax, label="발생 횟수")
    ax.set_title("연도 × 월별 지진 발생 현황 히트맵", fontsize=14, fontweight="bold", pad=15)
    fig.patch.set_facecolor("#FFFFFF")
    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, "04_월별_히트맵.png")
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  저장: {path}")


def fig5_region_magnitude_box(df: pd.DataFrame):
    """지역별 규모 분포 박스플롯"""
    top_regions = df["위치"].value_counts().head(8).index.tolist()
    df_top = df[df["위치"].isin(top_regions)]

    groups = [df_top[df_top["위치"] == r]["규모"].dropna().values for r in top_regions]

    fig, ax = plt.subplots(figsize=(11, 5))
    bp = ax.boxplot(groups, patch_artist=True, notch=False,
                    medianprops={"color": "#C00000", "linewidth": 2})
    for patch, color in zip(bp["boxes"], PALETTE):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)

    ax.set_xticks(range(1, len(top_regions) + 1))
    ax.set_xticklabels(top_regions, fontsize=9, rotation=20, ha="right")
    ax.set_ylabel("규모 (M)", fontsize=10)
    ax.set_title("주요 지역별 지진 규모 분포", fontsize=14, fontweight="bold", pad=15)
    ax.spines[["top", "right"]].set_visible(False)
    ax.set_facecolor("#F9FBFD")
    fig.patch.set_facecolor("#FFFFFF")
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, "05_지역별_규모_분포.png")
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  저장: {path}")


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    font = setup_korean_font()
    print(f"사용 폰트: {font}")

    print(f"데이터 로드: {DATA_FILE}")
    df = load_data()
    print(f"  → {len(df)}건\n")

    print("차트 생성 중...")
    fig1_region_bar(df)
    fig2_yearly_trend(df)
    fig3_magnitude_pie(df)
    fig4_monthly_heatmap(df)
    fig5_region_magnitude_box(df)
    print(f"\n모든 차트 저장 완료: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
