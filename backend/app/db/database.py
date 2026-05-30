import sqlite3
from datetime import datetime

conn = sqlite3.connect(
    "commute.db",
    check_same_thread=False
)

cursor = conn.cursor()

# users 테이블
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    login_id TEXT UNIQUE,
    created_at TEXT
)
""")

# points 테이블
cursor.execute("""
CREATE TABLE IF NOT EXISTS points (
    user_id INTEGER PRIMARY KEY,
    total_points INTEGER DEFAULT 0,
    FOREIGN KEY (user_id)
    REFERENCES users(id)
)
""")

# badges 테이블
cursor.execute("""
CREATE TABLE IF NOT EXISTS badges (
    user_id INTEGER PRIMARY KEY,
    easy_success_count INTEGER DEFAULT 0,
    hard_success_count INTEGER DEFAULT 0,
    rain_success_count INTEGER DEFAULT 0,
    early_morning_count INTEGER DEFAULT 0,
    long_distance_count INTEGER DEFAULT 0,
    FOREIGN KEY (user_id)
    REFERENCES users(id)
)
""")

# logs 테이블
cursor.execute("""
CREATE TABLE IF NOT EXISTS logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    checked_at TEXT,
    start_location TEXT,
    class_start_time TEXT,
    route_summary TEXT,
    total_minutes INTEGER,
    late_probability INTEGER,
    FOREIGN KEY (user_id)
    REFERENCES users(id)
)
""")

# 테스트용 사용자 생성
cursor.execute("""
INSERT OR IGNORE INTO users (
    login_id,
    created_at
)
VALUES (
    '수정',
    ?
)
""", (
    datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    ),
))

# 테스트용 포인트 생성
cursor.execute("""
INSERT OR IGNORE INTO points (
    user_id,
    total_points
)
VALUES (
    1,
    100
)
""")

# 테스트용 뱃지 생성
cursor.execute("""
INSERT OR IGNORE INTO badges (
    user_id,
    easy_success_count,
    hard_success_count,
    rain_success_count,
    early_morning_count,
    long_distance_count
)
VALUES (
    1,
    5,
    2,
    1,
    0,
    3
)
""")

conn.commit()

# users 조회
cursor.execute("""
SELECT * FROM users
""")

# points 조회
cursor.execute("""
SELECT * FROM points
""")

# badges 조회
cursor.execute("""
SELECT * FROM badges
""")

# logs 조회
cursor.execute("""
SELECT * FROM logs
""")

def get_user_id(login_id):

    cursor.execute("""
    SELECT id
    FROM users
    WHERE login_id = ?
    """, (login_id,))

    result = cursor.fetchone()

    return result

def create_user(login_id):

    cursor.execute("""
    INSERT OR IGNORE INTO users (
        login_id,
        created_at
    )
    VALUES (
        ?,
        ?
    )
    """, (
        login_id,
        datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    ))
    
    conn.commit()
    
def add_points(
    login_id,
    earned_points
):

    cursor.execute("""
    SELECT id
    FROM users
    WHERE login_id = ?
    """, (login_id,))

    user = cursor.fetchone()

    if not user:
        return

    user_id = user[0]

    cursor.execute("""
    INSERT OR IGNORE INTO points (
        user_id,
        total_points
    )
    VALUES (
        ?,
        0
    )
    """, (user_id,))

    cursor.execute("""
    UPDATE points
    SET total_points =
        total_points + ?
    WHERE user_id = ?
    """, (
        earned_points,
        user_id
    ))

    conn.commit()

def get_points(login_id):

    cursor.execute("""
    SELECT id
    FROM users
    WHERE login_id = ?
    """, (login_id,))

    user = cursor.fetchone()

    if not user:
        return 0

    user_id = user[0]

    cursor.execute("""
    SELECT total_points
    FROM points
    WHERE user_id = ?
    """, (user_id,))

    result = cursor.fetchone()

    if not result:
        return 0

    return result[0]

def update_badge_count(
    login_id,
    badge_type
):

    cursor.execute("""
    SELECT id
    FROM users
    WHERE login_id = ?
    """, (login_id,))

    user = cursor.fetchone()

    if not user:
        return

    user_id = user[0]

    cursor.execute("""
    INSERT OR IGNORE INTO badges (
        user_id
    )
    VALUES (?)
    """, (user_id,))

    cursor.execute(f"""
    UPDATE badges
    SET {badge_type} = {badge_type} + 1
    WHERE user_id = ?
    """, (user_id,))

    conn.commit()

def get_badges(login_id):

    cursor.execute("""
    SELECT id
    FROM users
    WHERE login_id = ?
    """, (login_id,))

    user = cursor.fetchone()

    if not user:
        return None

    user_id = user[0]

    cursor.execute("""
    SELECT
        easy_success_count,
        hard_success_count,
        rain_success_count,
        early_morning_count,
        long_distance_count
    FROM badges
    WHERE user_id = ?
    """, (user_id,))

    result = cursor.fetchone()

    if not result:
        return None

    return {
        "easy_success_count": result[0],
        "hard_success_count": result[1],
        "rain_success_count": result[2],
        "early_morning_count": result[3],
        "long_distance_count": result[4]
    }

def add_log(
    login_id,
    checked_at,
    start_location,
    class_start_time,
    route_summary,
    total_minutes,
    late_probability
):

    cursor.execute("""
    SELECT id
    FROM users
    WHERE login_id = ?
    """, (login_id,))

    user = cursor.fetchone()

    if not user:
        return

    user_id = user[0]

    cursor.execute("""
    INSERT INTO logs (
        user_id,
        checked_at,
        start_location,
        class_start_time,
        route_summary,
        total_minutes,
        late_probability
    )
    VALUES (
        ?, ?, ?, ?, ?, ?, ?
    )
    """, (
        user_id,
        checked_at,
        start_location,
        class_start_time,
        route_summary,
        total_minutes,
        late_probability
    ))

    conn.commit()

def get_logs(login_id):

    cursor.execute("""
    SELECT id
    FROM users
    WHERE login_id = ?
    """, (login_id,))

    user = cursor.fetchone()

    if not user:
        return []

    user_id = user[0]

    cursor.execute("""
    SELECT
        checked_at,
        start_location,
        class_start_time,
        route_summary,
        total_minutes,
        late_probability
    FROM logs
    WHERE user_id = ?
    ORDER BY id DESC
    """, (user_id,))

    results = cursor.fetchall()

    logs = []

    for row in results:
        logs.append({
            "checkedAt": row[0],
            "startLocation": row[1],
            "classStartTime": row[2],
            "routeSummary": row[3],
            "totalMinutes": row[4],
            "lateProbability": row[5]
        })

    return logs