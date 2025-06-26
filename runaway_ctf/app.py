from flask import Flask, render_template, request, redirect, url_for, session, make_response, Response, jsonify
import base64
import json

app = Flask(__name__)
app.secret_key = 'secretkeyforthisctfchallenge'

# 判斷使用者是否已通過當前關卡
def check_level(level):
    if not session.get('current_level'):
        session['current_level'] = 0
    
    if session['current_level'] < level:
        return False
    return True

@app.route('/')
def index():
    # 重置遊戲進度
    session['current_level'] = 0
    # 清除所有相關Cookie
    resp = make_response(render_template('index.html'))
    resp.set_cookie('admin', '', expires=0)
    resp.set_cookie('secret_cookie', '', expires=0)
    resp.set_cookie('secret_recipe', '', expires=0)
    return resp

@app.route('/robots.txt')
def robots():
    if check_level(0):
        session['current_level'] = 1
        robots_content = """User-agent: *
Disallow: /cookie_store
Disallow: /flag

# 機器人筆記：記得禁止訪問這個路徑，裡面有囚犯的秘密餅乾店

# You caught the robot.
"""
        return Response(robots_content, mimetype='text/plain')
    return redirect(url_for('index'))

@app.route('/flag')
def flag():
    # 重定向到 YouTube 影片
    return redirect("https://www.youtube.com/watch?v=IsXsqMKHaQU&list=PLKsVAE4kQDrRnLk_1axMQ4YZTlbwx0E1h")

@app.route('/cookie_store')
def cookie_store():
    if not check_level(1):
        return redirect(url_for('robots' if session['current_level'] == 0 else 'index'))
    # 設置初始 secret_cookie 為 guest
    response = make_response(render_template('cookie_store.html'))
    if not request.cookies.get('secret_cookie'):
        response.set_cookie('secret_cookie', 'guest')
    return response

@app.route('/cookie_recipe/<cookie_id>', methods=['GET'])
def cookie_recipe(cookie_id):
    if not check_level(1):
        return redirect(url_for('robots' if session['current_level'] == 0 else 'index'))
    
    # 檢查 secret_cookie 的值
    secret_cookie = request.cookies.get('secret_cookie', 'guest')
    
    # 如果 secret_cookie 為 admin，顯示特殊密碼
    if secret_cookie == 'admin':
        # 設置獲得秘方的cookie
        response = jsonify({
            'success': True,
            'message': '特殊密碼：チョコミントよりもあ・な・た'
        })
        response.set_cookie('secret_recipe', 'obtained')
        return response
    
    # 只有特務餅有正確的秘方密碼
    if cookie_id == 'cookie6':
        # 設置獲得秘方的cookie
        response = jsonify({
            'success': True,
            'message': '您已成功獲得特務餅的秘方！秘方密碼是：prison_cookies_123'
        })
        response.set_cookie('secret_recipe', 'obtained')
        return response
    else:
        return jsonify({
            'success': False,
            'message': f'很抱歉，該餅乾的秘方目前不提供給囚犯。'
        })

@app.route('/check_password', methods=['POST'])
def check_password():
    if not check_level(1):
        return redirect(url_for('robots' if session['current_level'] == 0 else 'index'))
    
    password = request.form.get('password', '')
    secret_recipe = request.cookies.get('secret_recipe', '')
    
    # 檢查是否已獲得秘方並輸入正確的密碼
    if secret_recipe == 'obtained' and password == 'チョコミントよりもあ・な・た':
        session['current_level'] = 2  # 升級到第三關
        return jsonify({
            'success': True,
            'message': '密碼正確！進入下一關。'
        })
    else:
        return jsonify({
            'success': False,
            'message': '密碼錯誤或您尚未獲得廚房後門的秘方！'
        })

@app.route('/paths')
def paths():
    if not check_level(2):
        if session['current_level'] == 1:
            return redirect(url_for('cookie_store'))
        return redirect(url_for('index'))
    # 確保進入第三關
    session['current_level'] = 2
    response = make_response(render_template('paths.html'))
    # 清除第二關的cookie
    response.set_cookie('secret_cookie', '', expires=0)
    response.set_cookie('secret_recipe', '', expires=0)
    response.headers['Content-Type'] = 'text/html; charset=utf-8'
    return response

@app.route('/path/<int:path_id>')
@app.route('/paths/<int:path_id>')
def path_route(path_id):
    # 確認用戶至少通過了第二關
    if not check_level(2):
        if session['current_level'] == 1:
            return redirect(url_for('cookie_store'))
        return redirect(url_for('index'))
    
    paths = {
        1: "這條路通往餐廳",
        2: "這條路通往浴室",
        3: "這條路通往工廠",
        4: "這條路通往儲藏室",
        5: "這條路通往球場",
        6: "這條路通往出口，<a href='/door'>前往下一關</a>"
    }
    
    # 在路徑4或路徑6時都允許進入下一關
    if path_id == 4 or path_id == 6:
        session['current_level'] = 3
    
    response = make_response(f"""<!DOCTYPE html>
    <html lang="zh-Hant">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>路徑 {path_id}</title>
        <style>
            body {{ font-family: 'Arial', sans-serif; background-color: #1a1a1a; color: #33ff33; text-align: center; padding: 50px; }}
            h1 {{ text-shadow: 0 0 10px #33ff33; }}
            a {{ color: #33ff33; }}
        </style>
    </head>
    <body>
        <h1>{paths.get(path_id, '這條路不存在')}</h1>
        <p><a href="/paths">返回選擇</a></p>
    </body>
    </html>
    """)
    response.headers['Content-Type'] = 'text/html; charset=utf-8'
    return response

@app.route('/door')
def door():
    if not check_level(3):
        if session['current_level'] == 2:
            return redirect(url_for('paths'))
        elif session['current_level'] == 1:
            return redirect(url_for('cookie_store'))
        return redirect(url_for('index'))
    
    # 設置cookie中的admin為False
    resp = make_response(render_template('door.html'))
    if not request.cookies.get('admin'):
        resp.set_cookie('admin', 'False')
    return resp

@app.route('/door/login', methods=['POST'])
def door_login():
    if not check_level(3):
        if session['current_level'] == 2:
            return redirect(url_for('paths'))
        elif session['current_level'] == 1:
            return redirect(url_for('cookie_store'))
        return redirect(url_for('index'))
    
    username = request.form.get('username', '')
    password = request.form.get('password', '')
    
    correct_username = "Goooooooooood H@CKer"  # base64: R29vb29vb29vb29vZCBIQENLZXI=
    # 將ASCII碼轉換為字符
    correct_password = "".join([chr(int(code)) for code in "106 105 51 97 112 55 103 52 121 106 105 52 99 108 51 99 57 52 100 107 52".split()])
    
    if username == correct_username and password == correct_password:
        is_admin = request.cookies.get('admin', 'False')
        if is_admin == 'True':
            # 設定session為最終關卡，並確保只能回到index.html
            session.clear()
            session['current_level'] = 4  # 最終通關
            return render_template('success.html', flag="AIS3{Y0u_4r3_w5_m4573r}")
        else:
            return render_template('not_admin.html')
    
    return "帳號或密碼錯誤，請再試一次"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)
