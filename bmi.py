from flask import Flask, request, render_template_string

app = Flask(__name__)

html = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>Tính chỉ số BMI</title>

    <style>
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #74ebd5, #ACB6E5);
            padding: 40px;
        }

        .container {
            background: white;
            width: 420px;
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
            font-size: 14px;
            margin-top: 5px;
        }

        .result {
            margin-top: 20px;
            padding: 15px;
            border-radius: 8px;
            text-align: center;
        }

        .green {
            background: #d4edda;
            color: #155724;
        }

        .yellow {
            background: #fff3cd;
            color: #856404;
        }

        .red {
            background: #f8d7da;
            color: #721c24;
        }
    </style>
</head>

<body>
    <div class="container">
        <h2>Tính chỉ số BMI</h2>

        <form method="POST">
            <label>Chiều cao (cm)</label>
            <input type="text" name="cao"
                   value="{{ cao }}"
                   placeholder="Ví dụ: 170 hoặc 170,5">

            {% if error_cao %}
                <div class="error">{{ error_cao }}</div>
            {% endif %}

            <label>Cân nặng (kg)</label>
            <input type="text" name="nang"
                   value="{{ nang }}"
                   placeholder="Ví dụ: 65 hoặc 65,5">

            {% if error_nang %}
                <div class="error">{{ error_nang }}</div>
            {% endif %}

            <button type="submit">Tính BMI</button>
        </form>

        {% if bmi is not none %}
            <div class="result {{ mau }}">
                <h3>BMI: {{ bmi }}</h3>
                <h3>{{ phan_loai }}</h3>
                <p>Cân nặng nên có: {{ can_nang_min }}
                   - {{ can_nang_max }} kg</p>
            </div>
        {% endif %}
    </div>
</body>
</html>
"""


def kiem_tra(value, min_value, max_value):
    if not value.strip():
        return None, "Vui lòng nhập một số."

    try:
        x = float(value.replace(",", "."))
    except ValueError:
        return None, "Vui lòng nhập một số."

    if x < min_value or x > max_value:
        return None, f"Giá trị phải từ {min_value} đến {max_value}."

    return x, ""


@app.route("/", methods=["GET", "POST"])
def index():
    cao = ""
    nang = ""

    error_cao = ""
    error_nang = ""

    bmi = None
    phan_loai = ""
    mau = ""

    can_nang_min = 0
    can_nang_max = 0

    if request.method == "POST":
        cao = request.form.get("cao", "").strip()
        nang = request.form.get("nang", "").strip()

        h, error_cao = kiem_tra(cao, 50, 250)
        w, error_nang = kiem_tra(nang, 10, 300)

        if not error_cao and not error_nang:
            h = h / 100

            bmi = round(w / (h * h), 1)

            # Tinh can nang nen co theo BMI 18.5 - 22.9
            can_nang_min = round(18.5 * h * h, 1)
            can_nang_max = round(22.9 * h * h, 1)

            # Phan loai BMI theo chuan chau A
            if bmi < 18.5:
                phan_loai = "Thiếu cân"
                mau = "yellow"

            elif bmi < 23:
                phan_loai = "Bình thường"
                mau = "green"

            elif bmi < 25:
                phan_loai = "Thừa cân"
                mau = "yellow"

            else:
                phan_loai = "Béo phì"
                mau = "red"

    return render_template_string(
        html,
        cao=cao,
        nang=nang,
        error_cao=error_cao,
        error_nang=error_nang,
        bmi=bmi,
        phan_loai=phan_loai,
        mau=mau,
        can_nang_min=can_nang_min,
        can_nang_max=can_nang_max
    )


if __name__ == "__main__":
    app.run(debug=True, port=5002)