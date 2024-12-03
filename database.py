import sqlite3

# Função para criar o banco de dados e a tabela de pontuação
def create_db():
    conn = sqlite3.connect('game_data.db')  # Conecta ou cria o banco de dados
    cursor = conn.cursor()
    
    # Criação da tabela leaderboard caso ela não exista
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS leaderboard (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_name TEXT NOT NULL,
            score INTEGER NOT NULL,
            total_time REAL NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()

# Função para adicionar o jogador ao banco de dados
def add_to_leaderboard(player_name, score, total_time):
    conn = sqlite3.connect('game_data.db')  # Conecta ao banco de dados
    cursor = conn.cursor()
    
    # Insere os dados do jogador na tabela
    cursor.execute('''
        INSERT INTO leaderboard (player_name, score, total_time)
        VALUES (?, ?, ?)
    ''', (player_name, score, total_time))
    
    conn.commit()
    conn.close()

# Função para obter o ranking de jogadores
def get_leaderboard():
    conn = sqlite3.connect('game_data.db')
    cursor = conn.cursor()

    # Corrigido para a tabela correta
    cursor.execute('SELECT player_name, score, total_time FROM leaderboard ORDER BY score DESC LIMIT 10')
    leaderboard = cursor.fetchall()

    conn.close()
    return leaderboard

    return leaderboard
