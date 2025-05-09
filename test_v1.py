import pandas as pd
import numpy as np
import glob
import os
import shutil
import webbrowser
import uuid

# ─── Data directories ───────────────────────────────────────────────────────
source_directory      = r'D:\OneDrive\Documents\Sports Interactive\Football Manager 2024'
destination_directory = r'D:\OneDrive\Yohhan\dz\FM23\upload'
new_directory         = r'D:\OneDrive\Yohhan\dz\FM23\new'

# ─── Performance thresholds by metric ────────────────────────────────────────
af_metrics = {
    "xG":                {"Elite": "≥ 0.60", "Good": "0.40 – 0.59", "Average": "0.25 – 0.39"},
    "Shot/90":           {"Elite": "≥ 4.0",  "Good": "3.0 – 3.9",    "Average": "2.0 – 2.9"},
    "ShT":               {"Elite": "≥ 60%", "Good": "50% – 59%",  "Average": "40% – 49%"},
    "NP-xG/90":          {"Elite": "≥ 0.60", "Good": "0.40 – 0.59", "Average": "0.25 – 0.39"},
    "Pressure Success %": {"Elite": "≥ 33%", "Good": "28% – 32%",  "Average": "22% – 27%"},
    "Poss Lost/90":      {"Elite": "≤ 10",  "Good": "11 – 14",     "Average": "15 – 18"}
}

w_metrics = {
    "Drb/90":            {"Elite": "≥ 5.0",  "Good": "3.0 – 4.9",   "Average": "1.5 – 2.9"},
    "xA/90":             {"Elite": "≥ 0.35", "Good": "0.20 – 0.34", "Average": "0.10 – 0.19"},
    "ShT":               {"Elite": "≥ 60%",  "Good": "50% – 59%",  "Average": "40% – 49%"},
    "Pr passes/90":      {"Elite": "≥ 5.0",  "Good": "3.0 – 4.9",   "Average": "1.5 – 2.9"},
    "Sprints/90":        {"Elite": "≥ 20",   "Good": "15 – 19",     "Average": "10 – 14"},
    "Key Passes/90":     {"Elite": "≥ 2.5",  "Good": "1.5 – 2.4",   "Average": "1.0 – 1.4"},
    "Poss Lost/90":      {"Elite": "≤ 10",   "Good": "11 – 14",     "Average": "15 – 18"}
}

cm_metrics = {
    "Pr passes/90":      {"Elite": "≥ 6.5",  "Good": "5.0 – 6.4",   "Average": "3.5 – 4.9"},
    "Pas %":             {"Elite": "≥ 90%",  "Good": "85% – 89%",  "Average": "80% – 84%"},
    "Tck/90":            {"Elite": "≥ 3.0",  "Good": "2.0 – 2.9",   "Average": "1.0 – 1.9"},
    "xA/90":             {"Elite": "≥ 0.30", "Good": "0.20 – 0.29", "Average": "0.10 – 0.19"},
    "Poss Won/90":       {"Elite": "≥ 7.0",  "Good": "5.0 – 6.9",   "Average": "3.0 – 4.9"},
    "Key Passes/90":     {"Elite": "≥ 2.5",  "Good": "1.5 – 2.4",   "Average": "1.0 – 1.4"},
    "Pressures/90":      {"Elite": "≥ 20",   "Good": "15 – 19",     "Average": "10 – 14"},
    "Poss Lost/90":      {"Elite": "≤ 10",   "Good": "11 – 14",     "Average": "15 – 18"}
}

hb_metrics = {
    "Tck/90":            {"Elite": "≥ 3.0",  "Good": "2.0 – 2.9",   "Average": "1.0 – 1.9"},
    "Int/90":            {"Elite": "≥ 2.5",  "Good": "1.5 – 2.4",   "Average": "0.5 – 1.4"},
    "Pas %":             {"Elite": "≥ 90%",  "Good": "85% – 89%",  "Average": "80% – 84%"},
    "Poss Won/90":       {"Elite": "≥ 8.0",  "Good": "6.0 – 7.9",   "Average": "4.0 – 5.9"},
    "Clr/90":            {"Elite": "≥ 2.0",  "Good": "1.0 – 1.9",   "Average": "0.5 – 0.9"},
    "Pressures/90":      {"Elite": "≥ 20",   "Good": "15 – 19",     "Average": "10 – 14"},
    "Poss Lost/90":      {"Elite": "≤ 8",    "Good": "9 – 12",      "Average": "13 – 16"}
}

l_metrics = {
    "Pr passes/90":      {"Elite": "≥ 6.5",  "Good": "5.0 – 6.4",   "Average": "3.5 – 4.9"},
    "Tck/90":            {"Elite": "≥ 2.5",  "Good": "1.5 – 2.4",   "Average": "0.5 – 1.4"},
    "Int/90":            {"Elite": "≥ 2.5",  "Good": "1.5 – 2.4",   "Average": "0.5 – 1.4"},
    "Pas %":             {"Elite": "≥ 90%",  "Good": "85% – 89%",  "Average": "80% – 84%"},
    "Clr/90":            {"Elite": "≥ 4.0",  "Good": "2.5 – 3.9",   "Average": "1.0 – 2.4"},
    "Pressures/90":      {"Elite": "≥ 15",   "Good": "10 – 14",     "Average": "5 – 9"},
    "Poss Lost/90":      {"Elite": "≤ 8",    "Good": "9 – 12",      "Average": "13 – 16"}
}

ifb_metrics = {
    "Pr passes/90":      {"Elite": "≥ 6.5",  "Good": "5.0 – 6.4",   "Average": "3.5 – 4.9"},
    "Tck/90":            {"Elite": "≥ 2.5",  "Good": "1.5 – 2.4",   "Average": "0.5 – 1.4"},
    "Int/90":            {"Elite": "≥ 2.5",  "Good": "1.5 – 2.4",   "Average": "0.5 – 1.4"},
    "Pas %":             {"Elite": "≥ 90%",  "Good": "85% – 89%",  "Average": "80% – 84%"},
    "Poss Won/90":       {"Elite": "≥ 8.0",  "Good": "6.0 – 7.9",   "Average": "4.0 – 5.9"},
    "Pressures/90":      {"Elite": "≥ 20",   "Good": "15 – 19",     "Average": "10 – 14"},
    "Poss Lost/90":      {"Elite": "≤ 8",    "Good": "9 – 12",      "Average": "13 – 16"}
}

sk_metrics = {
    "Saves/90":          {"Elite": "≥ 4.0",  "Good": "3.0 – 3.9",   "Average": "2.0 – 2.9"},
    "xSv %":             {"Elite": "≥ 75%",  "Good": "70% – 74%",  "Average": "65% – 69%"},
    "xGP/90":            {"Elite": "≥ 0.20", "Good": "0.10 – 0.19", "Average": "0.00 – 0.09"},
    "Pas %":             {"Elite": "≥ 88%",  "Good": "85% – 87%",  "Average": "80% – 84%"},
    "Clr/90":            {"Elite": "≥ 1.5",  "Good": "1.0 – 1.4",   "Average": "0.5 – 0.9"}
}

# ─── Combine thresholds into one dict ──────────────────────────────────────
ideal_performance_metrics = {}
for d in (af_metrics, w_metrics, cm_metrics, hb_metrics, l_metrics, ifb_metrics, sk_metrics):
    ideal_performance_metrics.update(d)

# ─── Helper functions ───────────────────────────────────────────────────────
def evaluate_metric_quality(value, thresholds):
    if pd.isna(value):
        return None
    for quality, thr_str in thresholds.items():
        thr = thr_str.replace('–','-').strip()
        if thr.startswith('≥') and value >= float(thr.lstrip('≥').strip()):
            return quality
        if thr.startswith('≤') and value <= float(thr.lstrip('≤').strip()):
            return quality
        if '-' in thr:
            low, high = [float(x) for x in thr.split('-',1)]
            if low <= value <= high:
                return quality
    return None

# ─── Map roles to their performance metrics ─────────────────────────────────
role_performance_metrics = {
    "AF":  ["xG","Shot/90","ShT","NP-xG/90","Pressure Success %","Poss Lost/90"],
    "W":   ["Drb/90","xA/90","ShT","Pr passes/90","Sprints/90","Key Passes/90","Poss Lost/90"],
    "CM":  ["Pr passes/90","Pas %","Tck/90","xA/90","Poss Won/90","Key Passes/90","Pressures/90","Poss Lost/90"],
    "HB":  ["Tck/90","Int/90","Pas %","Poss Won/90","Clr/90","Pressures/90","Poss Lost/90"],
    "L":   ["Pr passes/90","Tck/90","Int/90","Pas %","Clr/90","Pressures/90","Poss Lost/90"],
    "IFB": ["Pr passes/90","Tck/90","Int/90","Pas %","Poss Won/90","Pressures/90","Poss Lost/90"],
    "SK":  ["Saves/90","xSv %","xGP/90","Pas %","Clr/90"]
}

def adjust_player_scores(df, performance_thresholds, role_metrics, quality_factors=None):
    if quality_factors is None:
        quality_factors = {'Elite':1.5,'Good':1.0,'Average':0.8}
    for role, metrics in role_metrics.items():
        def compute_adj(row):
            total_f = 0.0
            for m in metrics:
                val = row.get(m, np.nan)
                band = evaluate_metric_quality(val, performance_thresholds.get(m, {}))
                total_f += quality_factors.get(band, 1.0)
            avg_f = total_f / len(metrics)
            return round(row[role] * avg_f, 1)
        df[f"{role}_adj"] = df.apply(compute_adj, axis=1)
    return df

# ─── File operations & data prep ─────────────────────────────────────────────
os.makedirs(destination_directory, exist_ok=True)
os.makedirs(new_directory, exist_ok=True)

def move_files(src, dest):
    html_files = glob.glob(os.path.join(src, '*.html'))
    for file in html_files:
        dest_file = os.path.join(dest, os.path.basename(file))
        if os.path.exists(dest_file):
            os.remove(dest_file)
        shutil.move(file, dest_file)
    print(f"Moved {len(html_files)} files.")

def handle_range(value):
    if isinstance(value, str) and '-' in value:
        parts = value.split('-')
        if len(parts)==2 and parts[0].isdigit() and parts[1].isdigit():
            low,high = map(int, parts)
            return (low+high)/2
    try:
        return float(value)
    except:
        return None

def load_latest_file(directory):
    latest = max(glob.glob(os.path.join(directory,'*')), key=os.path.getctime)
    print(f"Latest file loaded: {latest}")
    return pd.read_html(latest, header=0, keep_default_na=False)[0]

def preprocess_columns(df, cols):
    for c in cols:
        df[c] = df[c].apply(handle_range)

def calculate_player_scores(df):
    roles_weights = {
        "AF": {
    "Acc": 100, "Pac": 100, "Ant": 90, "Cmp": 50, "Dec": 90,
    "Dri": 90, "Fin": 100, "Fir": 90, "OtB": 100, "Tec": 90,
    "Pas": 50, "Str": 50, "Agg": 90, "Sta": 90, "Wor": 90,
    "Vis": 50, "Cmd": 0, "Ref": 0, "1v1": 0, "TRO": 0,
    "Kic": 0, "Thr": 0, "Cor": 0, "Mar": 0, "Tck": 0
  },
        "W": {
    "Acc": 100, "Pac": 100, "Ant": 90, "Cmp": 50, "Dec": 90,
    "Dri": 100, "Fin": 50, "Fir": 90, "OtB": 90, "Tec": 90,
    "Pas": 90, "Str": 50, "Agg": 50, "Sta": 100, "Wor": 90,
    "Vis": 90, "Cmd": 0, "Ref": 0, "1v1": 0, "TRO": 0,
    "Kic": 0, "Thr": 0, "Cor": 50, "Mar": 20, "Tck": 20
  },
        "CM": {
    "Acc": 90, "Pac": 90, "Ant": 90, "Cmp": 100, "Dec": 100,
    "Dri": 50, "Fin": 20, "Fir": 90, "OtB": 90, "Tec": 90,
    "Pas": 100, "Str": 50, "Agg": 50, "Sta": 90, "Wor": 90,
    "Vis": 90, "Cmd": 0, "Ref": 0, "1v1": 0, "TRO": 0,
    "Kic": 0, "Thr": 0, "Cor": 20, "Mar": 20, "Tck": 90
  },
        "HB": {
    "Acc": 50, "Pac": 50, "Ant": 90, "Cmp": 90, "Dec": 100,
    "Dri": 20, "Fin": 0, "Fir": 90, "OtB": 50, "Tec": 50,
    "Pas": 90, "Str": 90, "Agg": 50, "Sta": 90, "Wor": 100,
    "Vis": 50, "Cmd": 0, "Ref": 0, "1v1": 0, "TRO": 0,
    "Kic": 0, "Thr": 0, "Cor": 0, "Mar": 90, "Tck": 100
  },
        "L": {
    "Acc": 90, "Pac": 90, "Ant": 100, "Cmp": 100, "Dec": 100,
    "Dri": 90, "Fin": 0, "Fir": 90, "OtB": 90, "Tec": 90,
    "Pas": 100, "Str": 90, "Agg": 50, "Sta": 90, "Wor": 90,
    "Vis": 90, "Cmd": 0, "Ref": 0, "1v1": 0, "TRO": 0,
    "Kic": 0, "Thr": 0, "Cor": 0, "Mar": 90, "Tck": 90
  },
        "IFB": {
    "Acc": 90, "Pac": 90, "Ant": 90, "Cmp": 90, "Dec": 90,
    "Dri": 90, "Fin": 0, "Fir": 90, "OtB": 90, "Tec": 90,
    "Pas": 90, "Str": 70, "Agg": 50, "Sta": 100, "Wor": 100,
    "Vis": 70, "Cmd": 0, "Ref": 0, "1v1": 0, "TRO": 0,
    "Kic": 0, "Thr": 0, "Cor": 20, "Mar": 50, "Tck": 90
  },
        "SK": {
    "Acc": 90, "Pac": 50, "Ant": 90, "Cmp": 90, "Dec": 90,
    "Dri": 50, "Fin": 0, "Fir": 90, "OtB": 0, "Tec": 50,
    "Pas": 90, "Str": 70, "Agg": 20, "Sta": 50, "Wor": 50,
    "Vis": 70, "Cmd": 90, "Ref": 100, "1v1": 100, "TRO": 90,
    "Kic": 50, "Thr": 90, "Cor": 0, "Mar": 0, "Tck": 0
}
    }
    for role, weights in roles_weights.items():
        total_w = sum(weights.values())
        def comp(row):
            t=0
            for a,w in weights.items():
                v = row.get(a,0); t += (0 if pd.isna(v) else v)*w
            return round(((t/total_w)*20)-121,1) if total_w else None
        df[role]=df.apply(comp,axis=1)
    return df

# ─── HTML generation ─────────────────────────────────────────────────────────
def generate_html(df):
    html_table = df.to_html(table_id='table', index=False, classes='display')
    # … your existing HTML template …
    return f"""<!DOCTYPE html>…"""

def save_and_open_html(html, dir):
    fname = str(uuid.uuid4())+'.html'
    path = os.path.join(dir, fname)
    with open(path,'w',encoding='utf-8') as f: f.write(html)
    webbrowser.open_new_tab(path)


def delete_files(dir):
    for f in glob.glob(os.path.join(dir,'*.html')): os.remove(f)

# ─── Main pipeline ───────────────────────────────────────────────────────────
def main():
    move_files(source_directory, destination_directory)
    squad = load_latest_file(destination_directory)

    cols_to_prep = [
    'Acc', 'Wor', 'Vis', 'Thr', 'Tec', 'Tea', 'Tck', 'Str', 'Sta', 'TRO', 'Ref',
    'Pun', 'Pos', 'Pen', 'Pas', 'Pac', '1v1', 'OtB', 'Nat', 'Mar', 'L Th', 'Lon',
    'Ldr', 'Kic', 'Jum', 'Hea', 'Han', 'Fre', 'Fla', 'Fir', 'Fin', 'Ecc', 'Dri',
    'Det', 'Dec', 'Cro', 'Cor', 'Cnt', 'Cmp', 'Com', 'Cmd', 'Bra', 'Bal', 'Ant',
    'Agi', 'Agg', 'Aer',

    # Added performance metrics
    'xG', 'Shot/90', 'ShT', 'NP-xG/90',
    'Pressure Success %', 'Poss Lost/90',
    'Drb/90', 'xA/90', 'Pr passes/90',
    'Sprints/90', 'Key Passes/90',
    'Pas %', 'Tck/90', 'Poss Won/90',
    'Pressures/90', 'Int/90', 'Clr/90',
    'Saves/90', 'xSv %', 'xGP/90'
    ]
    preprocess_columns(squad, cols_to_prep)

    squad = calculate_player_scores(squad)
    squad = adjust_player_scores(squad, ideal_performance_metrics, role_performance_metrics)

    cols = [ 'Transfer Value','Position','Name','Age', … 'AF','AF_adj','Height','Club','Salary' ]
    html = generate_html(squad[cols])
    save_and_open_html(html, new_directory)
    delete_files(destination_directory)

if __name__ == '__main__':
    main()
