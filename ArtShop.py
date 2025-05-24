from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # замените на свой секретный ключ

# Данные о картинах с расширенной информацией
paintings = [
    {
        'id': 1,
        'title': 'Буря на Чёрном море',
        'artist': 'Бадредтинова Диана',
        'price': 7500,
        'image': 'images/Буря на Чёрном море.jpeg',
        'description': '',
        'history': ''
    },
    {
        'id': 2,
        'title': 'Вечернее Небо',
        'artist': 'Бадредтинова Диана',
        'price': 15000,
        'image': 'images/Вечернее Небо.jpg',
        'description': '',
        'history': ''
    },
    {
        'id': 3,
        'title': 'Сакура',
        'artist': 'Бадредтинова Диана',
        'price': 20000,
        'image': 'images/Сакура.jpg',
        'description': '',
        'history': ''
    },
    {
        'id': 4,
        'title': 'Декабрь',
        'artist': 'Бадредтинова Диана',
        'price': 10000,
        'image': 'images/Декабрь.jpg',
    }   

]

# Инициализация корзины
@app.before_request
def before_request():
    if 'cart' not in session:
        session['cart'] = []

# Главная страница - каталог
@app.route('/')
def index():
    return render_template('index.html', paintings=paintings)

# Страница детали картины
@app.route('/painting/<int:painting_id>')
def painting_detail(painting_id):
    painting = next((p for p in paintings if p['id'] == painting_id), None)
    if not painting:
        return "Картина не найдена", 404
    return render_template('detail.html', painting=painting)

# Добавление в корзину
@app.route('/add_to_cart/<int:painting_id>')
def add_to_cart(painting_id):
    session['cart'].append(painting_id)
    session.modified = True
    return redirect(request.referrer or url_for('index'))

# Корзина
@app.route('/cart')
def cart():
    cart_items = [p for p in paintings if p['id'] in session['cart']]
    total_price = sum(p['price'] for p in cart_items)
    return render_template('cart.html', cart_items=cart_items, total_price=total_price)

# Оформление заказа
@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        # Тут можно добавить обработку данных клиента или интеграцию платежных систем
        session['cart'] = []  # очистка корзины после заказа
        return render_template('thank_you.html')
    else:
        cart_items = [p for p in paintings if p['id'] in session['cart']]
        total_price = sum(p['price'] for p in cart_items)
        return render_template('checkout.html', cart_items=cart_items, total_price=total_price)

if __name__ == '__main__':
    app.run(debug=True)