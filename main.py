import json
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from pathlib import Path


def get_data():
    with open("data/data.json", "r") as f:
        data = json.load(f)
        return data["lecs_data"]


translate_map = {
    "Econometrics": "אקונומטריקה",
    "Macro": "מאקרו",
    "Micro": "מיקרו",
    "Discrete Math": "מתמטיקה בדידה",
    "Linear Algebra": "אלגברה לינארית",
    "lec": "הרצאה",
    "rec": "תרגול",
    "citot": "כיתות",
    "bergels": "ברגלס",
    "handasa": "הנדסה"
}

def reverse (w):
    return w[::-1]

def translate(w):
    if not isinstance(w, str):
        return w
    parts = w.split("-")
    translated = []
    for p in parts:
        value = translate_map.get(p, p)
        # Only reverse if it’s Hebrew text (not numbers or mixed)
        if value.isdigit():
            translated.append(value)
        else:
            translated.append(reverse(value))
    return " ".join(translated)


def get_day(n):
    days = ["", "א", "ב", "ג", "ד", "ה"]
    return days[n]


def get_color(d):
    return "#9bbcff" if d["lesson_type"] == "lec" else "#ffd699"


def main():
    data = get_data()
    stime = min(d["start"] for d in data)
    ftime = max(d["start"] + d["duration"] for d in data) + 1
    diff = ftime - stime

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlim(0.5, 6)
    ax.set_ylim(stime - 1, ftime)

    # Draw each class
    for d in data:
        x = d["day"]
        y = d["start"]
        h = d["duration"]
        color = get_color(d)

        rect = Rectangle((x , y), width=1, height=h, color=color,  ec="black")
        ax.add_patch(rect)

        ax.text(
            x + 0.5,
            y + h / 2,
            f"{translate(d['name'])}\n{translate(d['location'])}",
            ha="center",
            va="center",
            fontsize=8,
            wrap=True,
        )

    # Draw hour labels (left side)
    for hour in range(stime, ftime + 1):
        if not hour%2 == 0 or hour == 20:
            continue
        ax.text(
            0.55 , hour + 0.2, f"{hour}:00",
            va = "top", ha = "right"
        )
    for d in range(1,6):
        ax.text(
            d, stime - 0.8, get_day(d), va = "top", ha = "right"
        )
    # Style
    ax.set_xticks(range(1, 6))
    # ax.set_xticklabels([get_day(i) for i in range(1, 6)])
    ax.set_yticks(range(stime, ftime + 1))
    ax.invert_yaxis()
    ax.invert_xaxis()
    ax.set_yticklabels([])
    ax.grid(True, which = "major", axis = "both", linewidth = 0.5, alpha = 0.6)
    plt.tight_layout()
    out_dir = Path("out")
    out_dir.mkdir(parents = True, exist_ok = True)
    plt.savefig("out/sceduale.png", dpi = 300)
    plt.show()




if __name__ == "__main__":
    main()
