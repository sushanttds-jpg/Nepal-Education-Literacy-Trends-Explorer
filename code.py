import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as ply
import matplotlib.gridspec as gridspec
from matplotlib.ticker import MultipleLocator


os.makedirs("outputs", exist_ok=True)


C = {
    "male":    "#2563EB",
    "female":  "#DB2777",
    "primary": "#16A34A",
    "second":  "#CA8A04",
    "parity":  "#7C3AED",
    "nepal":   "#DC2626",
    "india":   "#F97316",
    "bangla":  "#10B981",
    "sri":     "#6366F1",
    "bg":      "#0F172A",
    "card":    "#1E293B",
    "text":    "#F1F5F9",
    "muted":   "#94A3B8",
    "grid":    "#334155",
}


DATA_PATH = "data/nepal_education_wb.csv"

if os.path.exists(DATA_PATH):
    raw = pd.read_csv(DATA_PATH, skiprows=4)
    # World Bank format: rows = indicators, columns = years
    def get_series(indicator_code):
        row = raw[raw["Indicator Code"] == indicator_code]
        if row.empty:
            return None
        years = [str(y) for y in range(1980, 2024)]
        vals  = row[years].values.flatten().astype(float)
        return pd.Series(vals, index=range(1980, 2024))

    lit_male   = get_series("SE.ADT.LITR.MA.ZS")
    lit_female = get_series("SE.ADT.LITR.FE.ZS")
    enr_prim   = get_series("SE.PRM.ENRR")
    enr_sec    = get_series("SE.SEC.ENRR")
    parity     = get_series("SE.ENR.PRSC.FM.ZS")
else:
  
    years = np.arange(1980, 2024)

    lit_male   = pd.Series(
        np.interp(years, [1980,1985,1990,1995,2000,2005,2010,2015,2018,2021,2023],
                         [29,  35,  40,  50,  60,  68,  75,  80,  83,  87,  89]),
        index=years)

    lit_female = pd.Series(
        np.interp(years, [1980,1985,1990,1995,2000,2005,2010,2015,2018,2021,2023],
                         [8,   11,  14,  21,  34,  45,  57,  65,  69,  75,  78]),
        index=years)

    enr_prim   = pd.Series(
        np.interp(years, [1980,1990,2000,2005,2010,2015,2020,2023],
                         [62,  71,  82,  88,  93,  96,  95,  94]),
        index=years)

    enr_sec    = pd.Series(
        np.interp(years, [1980,1990,2000,2005,2010,2015,2020,2023],
                         [20,  28,  38,  47,  58,  70,  78,  82]),
        index=years)

    parity     = pd.Series(
        np.interp(years, [1980,1990,2000,2005,2010,2015,2020,2023],
                         [0.38,0.48,0.66,0.78,0.88,0.95,1.01,1.03]),
        index=years)

# ── South Asia comparison (literacy rate, 2023 estimates) ─────────────────────
sa_countries  = ["Nepal", "India", "Bangladesh", "Sri Lanka", "Pakistan", "Bhutan"]
sa_lit_male   = [89,      84,      80,           97,          74,         80     ]
sa_lit_female = [78,      74,      75,           95,          52,         68     ]

# ══════════════════════════════════════════════════════════════════════════════
# FIGURE 1 — Literacy Rate Trends
# ══════════════════════════════════════════════════════════════════════════════
def plot_literacy():
    fig, ax = ply.subplots(figsize=(11, 6), facecolor=C["bg"])
    ax.set_facecolor(C["card"])

    ax.plot(lit_male.index,   lit_male.values,   color=C["male"],
            lw=2.5, label="Male literacy")
    ax.plot(lit_female.index, lit_female.values, color=C["female"],
            lw=2.5, label="Female literacy")

    ax.fill_between(lit_male.index, lit_female.values, lit_male.values,
                    alpha=0.12, color=C["male"])


    gap = lit_male.iloc[-1] - lit_female.iloc[-1]
    ax.annotate(f"Gap: {gap:.0f} pp",
                xy=(2023, (lit_male.iloc[-1]+lit_female.iloc[-1])/2),
                fontsize=10, color=C["muted"],
                ha="right", va="center")

    ax.set_title("Nepal Adult Literacy Rate (1980–2023)", color=C["text"],
                 fontsize=15, fontweight="bold", pad=14)
    ax.set_xlabel("Year",            color=C["muted"], fontsize=11)
    ax.set_ylabel("Literacy Rate (%)", color=C["muted"], fontsize=11)
    ax.tick_params(colors=C["muted"])
    ax.yaxis.set_minor_locator(MultipleLocator(5))
    ax.grid(color=C["grid"], lw=0.5, alpha=0.6)
    ax.set_xlim(1980, 2023)
    ax.set_ylim(0, 100)
    ax.legend(facecolor=C["card"], labelcolor=C["text"], fontsize=10)
    for sp in ax.spines.values():
        sp.set_color(C["grid"])

    fig.tight_layout()
    fig.savefig("outputs/literacy_trends.png", dpi=150, bbox_inches="tight")
    ply.close(fig)
    print("✔  saved outputs/literacy_trends.png")

def plot_enrollment():
    fig, ax = ply.subplots(figsize=(11, 6), facecolor=C["bg"])
    ax.set_facecolor(C["card"])

    ax.plot(enr_prim.index, enr_prim.values, color=C["primary"],
            lw=2.5, label="Primary (net %)")
    ax.plot(enr_sec.index,  enr_sec.values,  color=C["second"],
            lw=2.5, linestyle="--", label="Secondary (net %)")

    ax.axhline(100, color=C["muted"], lw=0.8, linestyle=":")
    ax.annotate("100% benchmark", xy=(1982, 101), color=C["muted"], fontsize=9)

    ax.set_title("Nepal School Enrollment Rates (1980–2023)", color=C["text"],
                 fontsize=15, fontweight="bold", pad=14)
    ax.set_xlabel("Year",                color=C["muted"], fontsize=11)
    ax.set_ylabel("Net Enrollment Rate (%)", color=C["muted"], fontsize=11)
    ax.tick_params(colors=C["muted"])
    ax.grid(color=C["grid"], lw=0.5, alpha=0.6)
    ax.set_xlim(1980, 2023)
    ax.set_ylim(0, 110)
    ax.legend(facecolor=C["card"], labelcolor=C["text"], fontsize=10)
    for sp in ax.spines.values():
        sp.set_color(C["grid"])

    fig.tight_layout()
    fig.savefig("outputs/enrollment_trends.png", dpi=150, bbox_inches="tight")
    ply.close(fig)
    print("✔  saved outputs/enrollment_trends.png")

def plot_parity():
    fig, ax = ply.subplots(figsize=(11, 6), facecolor=C["bg"])
    ax.set_facecolor(C["card"])

    ax.plot(parity.index, parity.values, color=C["parity"], lw=2.5)
    ax.fill_between(parity.index, parity.values, 1.0,
                    where=(parity.values < 1.0), alpha=0.2,
                    color=C["female"], label="Girls behind")
    ax.fill_between(parity.index, parity.values, 1.0,
                    where=(parity.values >= 1.0), alpha=0.2,
                    color=C["primary"], label="Girls ahead")

    ax.axhline(1.0, color=C["text"], lw=1.2, linestyle="--",
               label="Parity (GPI = 1.0)")

    ax.set_title("Gender Parity Index — Nepal School Enrollment (1980–2023)",
                 color=C["text"], fontsize=15, fontweight="bold", pad=14)
    ax.set_xlabel("Year", color=C["muted"], fontsize=11)
    ax.set_ylabel("GPI  (female/male enrollment)", color=C["muted"], fontsize=11)
    ax.tick_params(colors=C["muted"])
    ax.grid(color=C["grid"], lw=0.5, alpha=0.6)
    ax.set_xlim(1980, 2023)
    ax.set_ylim(0.2, 1.2)
    ax.legend(facecolor=C["card"], labelcolor=C["text"], fontsize=10)
    for sp in ax.spines.values():
        sp.set_color(C["grid"])

    fig.tight_layout()
    fig.savefig("outputs/gender_parity.png", dpi=150, bbox_inches="tight")
    ply.close(fig)
    print("✔  saved outputs/gender_parity.png")


def plot_south_asia():
    fig, ax = ply.subplots(figsize=(12, 6), facecolor=C["bg"])
    ax.set_facecolor(C["card"])

    x      = np.arange(len(sa_countries))
    width  = 0.35
    bars_m = ax.bar(x - width/2, sa_lit_male,   width, label="Male",
                    color=C["male"], alpha=0.85)
    bars_f = ax.bar(x + width/2, sa_lit_female, width, label="Female",
                    color=C["female"], alpha=0.85)

    # highlight Nepal
    bars_m[0].set_edgecolor("white"); bars_m[0].set_linewidth(1.8)
    bars_f[0].set_edgecolor("white"); bars_f[0].set_linewidth(1.8)

    for bar in list(bars_m) + list(bars_f):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.8,
                f"{bar.get_height():.0f}", ha="center", va="bottom",
                color=C["text"], fontsize=9)

    ax.set_title("South Asia — Adult Literacy Rate by Gender (~2023)",
                 color=C["text"], fontsize=15, fontweight="bold", pad=14)
    ax.set_ylabel("Literacy Rate (%)", color=C["muted"], fontsize=11)
    ax.set_xticks(x)
    ax.set_xticklabels(sa_countries, color=C["text"], fontsize=11)
    ax.tick_params(axis="y", colors=C["muted"])
    ax.set_ylim(0, 110)
    ax.grid(axis="y", color=C["grid"], lw=0.5, alpha=0.6)
    ax.legend(facecolor=C["card"], labelcolor=C["text"], fontsize=10)
    for sp in ax.spines.values():
        sp.set_color(C["grid"])

    fig.tight_layout()
    fig.savefig("outputs/south_asia_comparison.png", dpi=150, bbox_inches="tight")
    ply.close(fig)
    print("✔  saved outputs/south_asia_comparison.png")

def plot_dashboard():
    fig = ply.figure(figsize=(18, 12), facecolor=C["bg"])
    gs  = gridspec.GridSpec(2, 2, figure=fig, hspace=0.45, wspace=0.35)

    axes = [fig.add_subplot(gs[r, c]) for r in range(2) for c in range(2)]
    for ax in axes:
        ax.set_facecolor(C["card"])
        for sp in ax.spines.values():
            sp.set_color(C["grid"])
        ax.tick_params(colors=C["muted"])
        ax.grid(color=C["grid"], lw=0.4, alpha=0.5)

    axes[0].plot(lit_male.index,   lit_male.values,   color=C["male"],   lw=2)
    axes[0].plot(lit_female.index, lit_female.values, color=C["female"], lw=2)
    axes[0].fill_between(lit_male.index, lit_female.values, lit_male.values,
                         alpha=0.1, color=C["male"])
    axes[0].set_title("Literacy Rate",   color=C["text"], fontsize=13, fontweight="bold")
    axes[0].set_ylabel("% adults",       color=C["muted"])
    axes[0].set_ylim(0, 100)
    axes[0].set_xlim(1980, 2023)
    axes[0].legend(["Male","Female"], facecolor=C["card"], labelcolor=C["text"], fontsize=9)


    axes[1].plot(enr_prim.index, enr_prim.values, color=C["primary"], lw=2)
    axes[1].plot(enr_sec.index,  enr_sec.values,  color=C["second"],  lw=2, linestyle="--")
    axes[1].axhline(100, color=C["muted"], lw=0.8, linestyle=":")
    axes[1].set_title("School Enrollment",  color=C["text"], fontsize=13, fontweight="bold")
    axes[1].set_ylabel("Net enrollment %",  color=C["muted"])
    axes[1].set_ylim(0, 110)
    axes[1].set_xlim(1980, 2023)
    axes[1].legend(["Primary","Secondary"], facecolor=C["card"], labelcolor=C["text"], fontsize=9)
    axes[2].plot(parity.index, parity.values, color=C["parity"], lw=2)
    axes[2].fill_between(parity.index, parity.values, 1.0,
                         where=(parity.values < 1.0), alpha=0.2, color=C["female"])
    axes[2].fill_between(parity.index, parity.values, 1.0,
                         where=(parity.values >= 1.0), alpha=0.2, color=C["primary"])
    axes[2].axhline(1.0, color=C["text"], lw=1, linestyle="--")
    axes[2].set_title("Gender Parity Index", color=C["text"], fontsize=13, fontweight="bold")
    axes[2].set_ylabel("GPI",                color=C["muted"])
    axes[2].set_ylim(0.2, 1.2)
    axes[2].set_xlim(1980, 2023)


    x = np.arange(len(sa_countries))
    w = 0.35
    axes[3].bar(x - w/2, sa_lit_male,   w, color=C["male"],   alpha=0.85, label="Male")
    axes[3].bar(x + w/2, sa_lit_female, w, color=C["female"], alpha=0.85, label="Female")
    axes[3].set_title("South Asia Comparison (~2023)", color=C["text"],
                      fontsize=13, fontweight="bold")
    axes[3].set_ylabel("Literacy %",  color=C["muted"])
    axes[3].set_xticks(x)
    axes[3].set_xticklabels(sa_countries, color=C["text"], fontsize=9, rotation=15)
    axes[3].set_ylim(0, 110)
    axes[3].legend(facecolor=C["card"], labelcolor=C["text"], fontsize=9)

    fig.suptitle("Nepal Education & Literacy Dashboard (1980–2023)",
                 color=C["text"], fontsize=17, fontweight="bold", y=1.01)

    fig.savefig("outputs/dashboard.png", dpi=150, bbox_inches="tight",
                facecolor=C["bg"])
    ply.close(fig)
    print("saved outputs/dashboard.png")
if __name__ == "__main__":
    print("\nNepal Education Trends — generating charts...\n")
    plot_literacy()
    plot_enrollment()
    plot_parity()
    plot_south_asia()
    plot_dashboard()
    print("\nDone! All charts saved to outputs/")