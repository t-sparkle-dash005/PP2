# db.py
import psycopg2
from config import DATABASE_URL

def get_connection():
    return psycopg2.connect(DATABASE_URL)

def init_db():
    """Create tables if they don't exist."""
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS players (
                        id SERIAL PRIMARY KEY,
                        username VARCHAR(50) UNIQUE NOT NULL
                    );
                """)
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS game_sessions (
                        id SERIAL PRIMARY KEY,
                        player_id INTEGER REFERENCES players(id),
                        score INTEGER NOT NULL,
                        level_reached INTEGER NOT NULL,
                        played_at TIMESTAMP DEFAULT NOW()
                    );
                """)
                
            conn.commit()
    except Exception as e:
        print(f"Database initialization error: {e}")
        
    

def get_or_create_player(username):
    """Returns the player_id for a given username."""
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id FROM players WHERE username = %s;", (username,))
                res = cur.fetchone()
                if res:
                    return res[0]
                
                cur.execute("INSERT INTO players (username) VALUES (%s) RETURNING id;", (username,))
                player_id = cur.fetchone()[0]
            conn.commit()
            return player_id
    except Exception as e:
        print(f"DB Error (get/create player): {e}")
        return None

def save_game(player_id, score, level):
    if not player_id: return
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO game_sessions (player_id, score, level_reached) 
                    VALUES (%s, %s, %s);
                """, (player_id, score, level))
            conn.commit()
    except Exception as e:
        print(f"DB Error (save game): {e}")

def get_personal_best(player_id):
    if not player_id: return 0
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT MAX(score) FROM game_sessions WHERE player_id = %s;", (player_id,))
                res = cur.fetchone()
                return res[0] if res and res[0] else 0
    except Exception as e:
        return 0

def get_leaderboard():
    """Returns top 10 scores: [(rank, username, score, level, date), ...]"""
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT p.username, g.score, g.level_reached, TO_CHAR(g.played_at, 'YYYY-MM-DD')
                    FROM game_sessions g
                    JOIN players p ON g.player_id = p.id
                    ORDER BY g.score DESC
                    LIMIT 10;
                """)
                rows = cur.fetchall()
                return [(i+1, r[0], r[1], r[2], r[3]) for i, r in enumerate(rows)]
    except Exception as e:
        print(f"DB Error (leaderboard): {e}")
        return []
