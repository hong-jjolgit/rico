from flask import Flask, render_template, request
import math  # math 모듈 추가

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    total_length = 0
    total_weight = 0
    purchase_quantity = 0
    total_cutting_cost = 0
    width = height = thickness = 0
    type_of_pipe = ""
    sizes = ["" for _ in range(10)]
    quantities = ["" for _ in range(10)]

    if request.method == 'POST':
        type_of_pipe = request.form.get('type', '')
        width = int(float(request.form.get('width', 0) or 0))
        height = int(float(request.form.get('height', 0) or 0))
        thickness = float(request.form.get('thickness', 0) or 0)

        for i in range(1, 11):
            size = request.form.get(f'size{i}', '')
            quantity = request.form.get(f'quantity{i}', '')
            if size and quantity:
                size = int(float(size) if size else 0)
                quantity = int(quantity) if quantity else 0
                sizes[i-1] = size
                quantities[i-1] = quantity
                if size > 0 and quantity > 0:
                    length = size * quantity
                    total_length += length
                    weight = -(3.287 * thickness - (width + height)) * thickness * 0.0157 * length / 1000
                    total_weight += weight
                    if size < 1000:
                        total_cutting_cost += quantity

        # 총 길이를 미터로 변환하여 소수점 반올림 후 정수로 변환
        purchase_quantity = math.ceil(total_length / 1000)

    total_weight = round(total_weight, 2)
    formatted_length = "{:,}".format(total_length)  # 쉼표로 천 단위 구분
    return render_template('index.html', total_length=formatted_length, total_weight=total_weight,
                           purchase_quantity=purchase_quantity, total_cutting_cost=total_cutting_cost,
                           type_of_pipe=type_of_pipe, width=width, height=height, thickness=thickness,
                           sizes=sizes, quantities=quantities)

if __name__ == '__main__':
    app.run(debug=True)
