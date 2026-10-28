from flask import Flask, request, render_template_string
app = Flask(__name__)

html = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>Máy tính cơ bản</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #74ebd5, #ACB6E5);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            margin: 0;
        }

        .container {
            background: white;
            width: 400px;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 8px 25px #0003;
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

        input, select {
            width: 100%;
            padding: 10px;
            margin-top: 6px;
            box-sizing: border-box;
            border: 1px solid #ccc;
            border-radius: 6px;
            font-size: 16px;
        }

        button {
            width: 100%;
            padding: 12px;
            margin-top: 20px;
            background: #287a64;
            color: white;
            border: none;
            border-radius: 6px;
            font-size: 16px;
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
            background: #e4f8e9;
            color: #176b37;
            border-radius: 8px;
            text-align: center;
            overflow-wrap: anywhere;
        }
    </style>
</head>
<body>
<div class="container">
    <h2>Máy tính cơ bản</h2>

    <form method="POST">
        <label>Số thứ nhất (a)</label>
        <input type="text" name="a"
               value="{{ a }}" placeholder="Ví dụ: 2,5">
        {% if error_a %}
            <div class="error">{{ error_a }}</div>
        {% endif %}

        <label>Phép toán</label>
        <select name="op">
            {% for value, label in ops %}
                <option value="{{ value }}"
                    {% if op == value %}selected{% endif %}>
                    {{ label }}
                </option>
            {% endfor %}
        </select>
        {% if error_op %}
            <div class="error">{{ error_op }}</div>
        {% endif %}

        <label>Số thứ hai (b)</label>
        <input type="text" name="b"
               value="{{ b }}" placeholder="Ví dụ: 3">
        {% if error_b %}
            <div class="error">{{ error_b }}</div>
        {% endif %}

        <button type="submit">Tính kết quả</button>
    </form>

    {% if result is not none %}
        <div class="result">
            <strong>{{ expression }}</strong>
        </div>
    {% endif %}
</div>
</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def index():
    a = ""
    b = ""
    op = "+"
    error_a = ""
    error_b = ""
    error_op = ""
    result = None
    expression = ""

    ops = [
        ("+", "Cộng (+)"),
        ("-", "Trừ (-)"),
        ("*", "Nhân (*)"),
        ("/", "Chia (/)")
    ]

    if request.method == "POST":
        a = request.form.get("a", "").strip()
        b = request.form.get("b", "").strip()
        op = request.form.get("op", "+")

        # Kiểm tra số thứ nhất
        try:
            if not a:
                raise ValueError
            x = float(a.replace(",", "."))
        except ValueError:
            error_a = "Vui lòng nhập một số."

        # Kiểm tra số thứ hai
        try:
            if not b:
                raise ValueError
            y = float(b.replace(",", "."))
        except ValueError:
            error_b = "Vui lòng nhập một số."

        # Kiểm tra phép toán
        if op not in ["+", "-", "*", "/"]:
            error_op = "Phép toán không hợp lệ."

        # Thực hiện phép tính khi dữ liệu hợp lệ
        if not error_a and not error_b and not error_op:
            if op == "+":
                result = x + y
            elif op == "-":
                result = x - y
            elif op == "*":
                result = x * y
            elif op == "/":
                if y == 0:
                    error_b = "Không thể chia cho 0."
                else:
                    result = x / y

        # Tạo biểu thức kết quả
        if result is not None:
            expression = f"{a} {op} {b} = {result:g}"

    return render_template_string(
        html,
        a=a,
        b=b,
        op=op,
        ops=ops,
        error_a=error_a,
        error_b=error_b,
        error_op=error_op,
        result=result,
        expression=expression
    )


if __name__ == "__main__":
    app.run(debug=True)
