from flask import Flask, request, render_template_string

app = Flask(__name__)

html = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>Tính điểm học phần</title>
    <style>
        body {
            font-family: Arial;
            background: linear-gradient(135deg, #74ebd5, #ACB6E5);
            padding: 40px;
        }

        .container {
            background: white;
            width: 400px;
            margin: auto;
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 5px 20px #888;
        }

        h2 {
            text-align: center;
            color: #287a64;
        }

        label {
            display: block;
            margin-top: 15px;
            font-weight: bold;
        }

        input {
            width: 100%;
            padding: 10px;
            margin-top: 5px;
            box-sizing: border-box;
            border: 1px solid #ccc;
            border-radius: 5px;
        }

        button {
            width: 100%;
            margin-top: 20px;
            padding: 12px;
            background: #287a64;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }

        button:hover {
            background: #195844;
        }

        .error {
            color: red;
            margin-top: 5px;
            font-size: 14px;
        }

        .result {
            margin-top: 20px;
            padding: 15px;
            background: #e1f8e5;
            border-radius: 8px;
            text-align: center;
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>Tính điểm học phần</h2>

        <form method="POST">
            <label>Điểm chuyên cần (10%)</label>
            <input type="text" name="cc" value="{{ cc }}">
            {% if error_cc %}
                <div class="error">{{ error_cc }}</div>
            {% endif %}

            <label>Điểm giữa kỳ (30%)</label>
            <input type="text" name="gk" value="{{ gk }}">
            {% if error_gk %}
                <div class="error">{{ error_gk }}</div>
            {% endif %}

            <label>Điểm cuối kỳ (60%)</label>
            <input type="text" name="ck" value="{{ ck }}">
            {% if error_ck %}
                <div class="error">{{ error_ck }}</div>
            {% endif %}

            <button type="submit">Tính điểm</button>
        </form>

        {% if result is not none %}
            <div class="result">
                <h3>Điểm học phần: {{ result }}</h3>
                <h3>Điểm chữ: {{ grade }}</h3>
            </div>
        {% endif %}
    </div>
</body>
</html>
"""


def kiem_tra(value):
    if not value.strip():
        return None, "Vui lòng nhập điểm."

    try:
        diem = float(value.replace(",", "."))
    except ValueError:
        return None, "Vui lòng nhập số hợp lệ."

    if diem < 0 or diem > 10:
        return None, "Điểm phải từ 0 đến 10."

    return diem, ""


def xep_loai(diem):
    if diem >= 8.5:
        return "A"
    elif diem >= 7.0:
        return "B"
    elif diem >= 5.5:
        return "C"
    elif diem >= 4.0:
        return "D"
    else:
        return "F"


@app.route("/", methods=["GET", "POST"])
def index():
    cc = ""
    gk = ""
    ck = ""

    error_cc = ""
    error_gk = ""
    error_ck = ""

    result = None
    grade = ""

    if request.method == "POST":
        cc = request.form.get("cc", "").strip()
        gk = request.form.get("gk", "").strip()
        ck = request.form.get("ck", "").strip()

        dcc, error_cc = kiem_tra(cc)
        dgk, error_gk = kiem_tra(gk)
        dck, error_ck = kiem_tra(ck)

        if not error_cc and not error_gk and not error_ck:
            result = round(
                dcc * 0.1 + dgk * 0.3 + dck * 0.6, 1
            )

            grade = xep_loai(result)

            if dck < 1:
                grade = "F"

    return render_template_string(
        html,
        cc=cc,
        gk=gk,
        ck=ck,
        error_cc=error_cc,
        error_gk=error_gk,
        error_ck=error_ck,
        result=result,
        grade=grade
    )


if __name__ == "__main__":
    app.run(debug=True, port=5001)
