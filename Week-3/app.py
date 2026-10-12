import csv
import sys
import os
import matplotlib.pyplot as plt

def generate_error_html():
    """Generates the error page when inputs are invalid or data is missing."""
    html_content = """<!DOCTYPE html>
<html>
<head>
    <title>Something Went Wrong</title>
</head>
<body>
    <h1>Wrong Inputs</h1>
    <p>Something went wrong</p>
</body>
</html>"""
    with open("output.html", "w", encoding="utf-8") as f:
        f.write(html_content)

def main():
    # Expects: python app.py -s <student_id> OR python app.py -c <course_id>
    if len(sys.argv) != 3:
        generate_error_html()
        return

    flag = sys.argv[1]
    target_id = sys.argv[2]

    if flag not in ('-s', '-c'):
        generate_error_html()
        return

    if not os.path.exists("data.csv"):
        generate_error_html()
        return

    rows = []
    try:
        with open("data.csv", mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            if reader.fieldnames is None:
                generate_error_html()
                return
            # Normalize header column names by stripping whitespace
            reader.fieldnames = [fn.strip() for fn in reader.fieldnames]
            for row in reader:
                cleaned_row = {k.strip(): v.strip() for k, v in row.items()}
                rows.append(cleaned_row)
    except Exception:
        generate_error_html()
        return

    if not rows:
        generate_error_html()
        return

    # Identify exact column key names dynamically
    sample_row = rows[0]
    s_key = next((k for k in sample_row.keys() if 'student' in k.lower()), 'Student ID')
    c_key = next((k for k in sample_row.keys() if 'course' in k.lower()), 'Course ID')
    m_key = next((k for k in sample_row.keys() if 'mark' in k.lower()), 'Marks')

    if flag == '-s':
        student_rows = [r for r in rows if r.get(s_key) == target_id]
        if not student_rows:
            generate_error_html()
            return

        total_marks = 0
        table_rows_html = ""
        for r in student_rows:
            s_id = r.get(s_key, '')
            c_id = r.get(c_key, '')
            try:
                marks = float(r.get(m_key, 0))
                if marks.is_integer():
                    marks = int(marks)
                total_marks += marks
            except ValueError:
                marks = r.get(m_key, 0)

            table_rows_html += f"<tr><td>{s_id}</td><td>{c_id}</td><td>{marks}</td></tr>\n"

        if isinstance(total_marks, float) and total_marks.is_integer():
            total_marks = int(total_marks)

        html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>Student Data</title>
</head>
<body>
    <h1>Student Details</h1>
    <table border="1">
        <tr>
            <th>Student id</th>
            <th>Course id</th>
            <th>Marks</th>
        </tr>
        {table_rows_html}
        <tr>
            <td colspan="2">Total Marks</td>
            <td>{total_marks}</td>
        </tr>
    </table>
</body>
</html>"""
        with open("output.html", "w", encoding="utf-8") as f:
            f.write(html_content)

    elif flag == '-c':
        course_rows = [r for r in rows if r.get(c_key) == target_id]
        if not course_rows:
            generate_error_html()
            return

        marks_list = []
        for r in course_rows:
            try:
                marks_list.append(float(r.get(m_key, 0)))
            except ValueError:
                pass

        if not marks_list:
            generate_error_html()
            return

        max_marks = max(marks_list)
        avg_marks = sum(marks_list) / len(marks_list)
        
        avg_formatted = round(avg_marks, 1)
        if avg_formatted.is_integer():
            avg_formatted = int(avg_formatted)

        if isinstance(max_marks, float) and max_marks.is_integer():
            max_marks = int(max_marks)

        # Generate histogram plot
        plt.figure()
        plt.hist(marks_list, bins='auto')
        plt.xlabel('Marks')
        plt.ylabel('Frequency')
        plt.savefig('histogram.png')
        plt.close()

        html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>Course Data</title>
</head>
<body>
    <h1>Course Details</h1>
    <table border="1">
        <tr>
            <th>Average Marks</th>
            <th>Maximum Marks</th>
        </tr>
        <tr>
            <td>{avg_formatted}</td>
            <td>{max_marks}</td>
        </tr>
    </table>
    <br>
    <img src="histogram.png" alt="Histogram">
</body>
</html>"""
        with open("output.html", "w", encoding="utf-8") as f:
            f.write(html_content)

if __name__ == '__main__':
    main()