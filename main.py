from flask import Flask, render_template, request, redirect, url_for, jsonify
from game import Game
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app)

winners = [
    {
        "winner": "John",
        "date": "2024-10-06",
    },
    {
        "winner": "Jane",
        "date": "2024-10-06",
    }
]

game = Game()

@app.before_request
def add_enumerate_to_jinja():
    app.jinja_env.globals.update(enumerate=enumerate)


@app.route('/')
def home():
    global game, winners
    game.new_game()
    return render_template('index.html', game=game.to_dict(), winners=winners)


@app.route('/column-click', methods=['POST'])
def column_click():
    global game
    data = request.get_json()
    col_index = data['col']
    game.column_click(col_index)
    socketio.emit('update_game_state', {
        'game': game.to_dict(),
        'winners': winners
    })  
    return jsonify(success=True) 


@app.route('/go-to-move', methods=['POST'])
def go_to_move():
    global game
    data = request.get_json()
    move_index = data['move']
    game.go_to_move(move_index)
    socketio.emit('update_game_state', {
        'game': game.to_dict(),
        'winners': winners
    })  
    return jsonify(success=True) 


@app.route('/new-game', methods=['POST'])
def new_game():
    global game, winners
    game.new_game()
    socketio.emit('update_game_state', {
        'game': game.to_dict(),
        'winners': winners
    })      
    return jsonify(success=True) 


@app.route('/submit-winner', methods=['POST'])
def submit_winner():
    data = request.get_json()

    winner_name = data.get('winner')

    from datetime import datetime
    winner_date = datetime.now().strftime("%Y-%m-%d")

    new_winner = {
        "winner": winner_name,
        "date": winner_date,
    }

    winners.append(new_winner) 
    return jsonify(success=True) 

if __name__ == '__main__':
    socketio.run(app, debug=True)
