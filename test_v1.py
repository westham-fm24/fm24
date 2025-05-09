import pandas as pd
import numpy as np
import glob
import os
import shutil
import webbrowser
import uuid


source_directory = r'D:\OneDrive\Documents\Sports Interactive\Football Manager 2024'
#source_directory = r'D:\temp'
destination_directory = r'D:\OneDrive\Yohhan\dz\FM23\upload'
new_directory = r'D:\OneDrive\Yohhan\dz\FM23\new'


os.makedirs(destination_directory, exist_ok=True)
os.makedirs(new_directory, exist_ok=True)

def move_files(src, dest):
    """ Move HTML files from source to destination directory """
    html_files = glob.glob(os.path.join(src, '*.html'))
    for file in html_files:
    #    shutil.move(file, dest)
        dest_file = os.path.join(dest, os.path.basename(file))
        if os.path.exists(dest_file):
            os.remove(dest_file)
        shutil.move(file, dest_file)
    print(f"Moved {len(html_files)} files.")
    
def handle_range(value):
    """ Convert range values to their average or return the value for non-ranges """
    if isinstance(value, str):
        if '-' in value:
            parts = value.split('-')
            if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
                low, high = map(int, parts)
                return (low + high) / 2
    try:
        return float(value)
    except (ValueError, TypeError):
        return None  # Return None for non-numeric values or invalid inputs
    
def load_latest_file(directory):
    """ Load the latest HTML file from a directory """
    list_of_files = glob.glob(os.path.join(directory, '*'))
    latest_file = max(list_of_files, key=os.path.getctime)
    print(f"Latest file loaded: {latest_file}")
    return pd.read_html(latest_file, header=0, encoding="utf-8", keep_default_na=False)[0]

def preprocess_columns(data, columns):
    """ Preprocess specified columns in the DataFrame """
    for column in columns:
        data[column] = data[column].apply(handle_range)

def calculate_player_scores(data):
    """
    For each role in roles_weights, compute Tactical True CA as:
        (weighted_average_of_attributes * 20) - 121
    and store it in a new column named after the role.
    """
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

    # For each role, compute the Tactical True CA
    for role, weights in roles_weights.items():
        sum_of_weights = sum(weights.values())

        def compute_tactical_ca(row):
            """
            1) Sum up (attribute_value * attribute_weight)
            2) Divide by the total of all weights to get a weighted average
            3) Multiply by 20 and subtract 121 => (weighted_avg * 20) - 121
            """
            total = 0.0
            for attr, weight in weights.items():
                # Safely fetch the attribute from the row; use 0 if not found or if NaN
                val = row.get(attr, 0)  # or row[attr] if guaranteed in columns
                if pd.isna(val):
                    val = 0
                total += val * weight

            if sum_of_weights == 0:
                return None  # avoid dividing by zero
            weighted_avg = total / sum_of_weights
            return round((weighted_avg * 20) - 121, 1)

        # Create a new column in 'data' for this role
        data[role] = data.apply(compute_tactical_ca, axis=1)

    # Assign top 3 roles based on Tactical CA
    return data

def generate_html(dataframe):
    table_html = dataframe.to_html(table_id="table", index=False, classes="display")

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Soccer Player Analysis</title>
        <link rel="stylesheet" href="https://cdn.datatables.net/1.11.5/css/jquery.dataTables.min.css">
        <link rel="stylesheet" href="https://cdn.datatables.net/fixedheader/3.2.2/css/fixedHeader.dataTables.min.css">
        <link rel="stylesheet" href="https://cdn.datatables.net/fixedcolumns/4.0.2/css/fixedColumns.dataTables.min.css">
        <style>
            body {{ font-family: Arial, sans-serif; }}
            #controls {{
                display: flex;
                align-items: center;
                margin-bottom: 1em;
            }}
            #controls label {{ margin-right: 1.5em; font-size: 0.9em; }}
            table {{ width: 100%; }}
            th, td {{ text-align: left; padding: 8px; white-space: nowrap; }}
            tr:nth-child(even) {{ background-color: #f2f2f2; }}
            .DTFC_LeftBodyWrapper table,
            .DTFC_LeftHeadWrapper table {{ background-color: white; }}
            .hidden-col {{ display: none !important; }}
        </style>
    </head>
    <body>
        <div id="controls">
            <label><input type="checkbox" id="origToggle" checked> Original</label>
            <label><input type="checkbox" id="adjToggle" checked> Adjusted</label>
        </div>

        {table_html}

        <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
        <script src="https://cdn.datatables.net/1.11.5/js/jquery.dataTables.min.js"></script>
        <script src="https://cdn.datatables.net/fixedheader/3.2.2/js/dataTables.fixedHeader.min.js"></script>
        <script src="https://cdn.datatables.net/fixedcolumns/4.0.2/js/dataTables.fixedColumns.min.js"></script>

        <script>
        $(document).ready(function() {{
            // Identity columns you ALWAYS want to show
            const alwaysVisible = ['Name', 'Position', 'Age', 'Height', 'Club', 'TransferValue', 'Salary'];

            // Find column indexes for sorting
            var adjIndexes = [];
            $('#table thead th').each(function(i) {{
                if ($(this).text().trim().endsWith('_adj')) {{
                    adjIndexes.push(i);
                }}
            }});

            // Init DataTable with numeric sorting for _adj columns
            var table = $('#table').DataTable({{
                scrollX: true,
                scrollY: true,
                paging: true,
                searching: true,
                order: [[1, 'asc']],
                pageLength: 15,
                fixedHeader: true,
                fixedColumns: {{ leftColumns: 4 }},
                columnDefs: [
                    {{ 
                        targets: adjIndexes,
                        type: 'num',
                        render: $.fn.dataTable.render.number(
                        ',',
                        '.',
                        1
                        ) }}
                ]
            }});

            var fc = table.fixedColumns();

            // Tag each column
            table.columns().every(function(idx) {{
                var header = $(this.header()).text().trim();
                if (alwaysVisible.includes(header)) {{
                    $(this.header()).addClass('identity-col');
                    $(this.nodes()).addClass('identity-col');
                }} else if (header.endsWith('_adj')) {{
                    $(this.header()).addClass('adj-col');
                    $(this.nodes()).addClass('adj-col');
                }} else {{
                    $(this.header()).addClass('orig-col');
                    $(this.nodes()).addClass('orig-col');
                }}
            }});

            function toggleColumnGroup(groupClass, visible) {{
                const action = visible ? 'removeClass' : 'addClass';
                $('.' + groupClass)[action]('hidden-col');
                table.columns.adjust();
                fc.update();
            }}

            $('#origToggle').on('change', function() {{
                toggleColumnGroup('orig-col', this.checked);
            }});

            $('#adjToggle').on('change', function() {{
                toggleColumnGroup('adj-col', this.checked);
            }});

            $(window).on('resize', function() {{
                table.columns.adjust();
                fc.update();
            }});
        }});
        </script>
    </body>
    </html>
    """
    return html


def save_and_open_html(html_content, directory):
    """ Save HTML content to a file and open it in a web browser """
    filename = str(uuid.uuid4()) + ".html"
    full_path = os.path.join(directory, filename)
    with open(full_path, "w", encoding="utf-8") as file:
        file.write(html_content)
    webbrowser.open_new_tab(full_path)
    print(f"File saved to {full_path}")

def delete_files(directory):
    """ Delete all HTML files in a specified directory """
    html_files = glob.glob(os.path.join(directory, '*.html'))
    for file in html_files:
        os.remove(file)
        print(f"Deleted file: {file}")


def main():
    move_files(source_directory, destination_directory)
    squad_rawdata = load_latest_file(destination_directory)
    columns_to_preprocess = [
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

    
    squad_rawdata = calculate_player_scores(squad_rawdata)
    {
    "AF": ["xG", "Shot/90", "ShT", "NP-xG/90", "Pressure Success %", "Poss Lost/90"],
    "W": ["Drb/90", "xA/90", "ShT", "Pr passes/90", "Sprints/90", "Key Passes/90", "Poss Lost/90"],
    "CM": ["Pr passes/90", "Pas %", "Tck/90", "xA/90", "Poss Won/90", "Key Passes/90", "Pressures/90", "Poss Lost/90"],
    "HB": ["Tck/90", "Int/90", "Pas %", "Poss Won/90", "Clr/90", "Pressures/90", "Poss Lost/90"],
    "L": ["Pr passes/90", "Tck/90", "Int/90", "Pas %", "Clr/90", "Pressures/90", "Poss Lost/90"],
    "IFB": ["Pr passes/90", "Tck/90", "Int/90", "Pas %", "Poss Won/90", "Pressures/90", "Poss Lost/90"],
    "SK": ["Saves/90", "xSv %", "xGP/90", "Pas %", "Clr/90"]
    }

    html_content = generate_html(squad_rawdata[['Transfer Value', 'Position', 'Name', 'Age',
        'SK', 'IFB', 'L', 'HB', 'CM', 'W', 'AF',
        'Height', 'Club','Salary']])
    save_and_open_html(html_content, new_directory)
    delete_files(destination_directory)

    
if __name__ == "__main__":
    main()
