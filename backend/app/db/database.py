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
    semester TEXT
)
""")

try:
    cursor.execute("""
    ALTER TABLE users
    ADD COLUMN semester TEXT
    """)
except:
    pass

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

# themes 테이블
cursor.execute("""
CREATE TABLE IF NOT EXISTS themes (
    user_id INTEGER PRIMARY KEY,
    selected_theme TEXT DEFAULT 'default',
    pink_theme INTEGER DEFAULT 0,
    blue_theme INTEGER DEFAULT 0,
    purple_theme INTEGER DEFAULT 0,
    FOREIGN KEY (user_id)
    REFERENCES users(id)
)
""")

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

    check_semester(
        login_id
    )

    cursor.execute("""
    SELECT id
    FROM users
    WHERE login_id = ?
    """, (login_id,))

    result = cursor.fetchone()

    return result

def create_user(login_id):

    current_semester = (
        get_current_semester()
    )

    cursor.execute("""
    INSERT OR IGNORE INTO users (
        login_id,
        created_at,
        semester
    )
    VALUES (
        ?,
        ?,
        ?
    )
    """, (
        login_id,
        datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),
        current_semester
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

def buy_theme(
    login_id,
    theme_name
):

    cursor.execute("""
    SELECT id
    FROM users
    WHERE login_id = ?
    """, (login_id,))

    user = cursor.fetchone()

    if not user:
        return {
            "success": False,
            "message": "사용자를 찾을 수 없습니다."
        }

    user_id = user[0]

    cursor.execute("""
    SELECT total_points
    FROM points
    WHERE user_id = ?
    """, (user_id,))

    point_result = cursor.fetchone()

    if not point_result:
        return {
            "success": False,
            "message": "포인트 정보가 없습니다."
        }

    current_points = point_result[0]

    if current_points < 500:
        return {
            "success": False,
            "message": "포인트가 부족합니다."
        }

    cursor.execute(f"""
    SELECT {theme_name}_theme
    FROM themes
    WHERE user_id = ?
    """, (user_id,))

    owned = cursor.fetchone()

    if owned and owned[0] == 1:
        return {
            "success": False,
            "message": "이미 구매한 테마입니다."
        }

    cursor.execute("""
    UPDATE points
    SET total_points = total_points - 500
    WHERE user_id = ?
    """, (user_id,))

    cursor.execute(f"""
    UPDATE themes
    SET {theme_name}_theme = 1
    WHERE user_id = ?
    """, (user_id,))

    conn.commit()

    return {
        "success": True,
        "message": "구매 완료"
    }
    
cursor.execute("""
    SELECT *
    FROM themes
    """)
    
cursor.execute("""
    SELECT *
    FROM themes
    """)

def get_themes(login_id):

    local_cursor = conn.cursor()

    local_cursor.execute("""
    SELECT id
    FROM users
    WHERE login_id = ?
    """, (login_id,))

    user = local_cursor.fetchone()

    if not user:
        return None

    user_id = user[0]

    local_cursor.execute("""
    SELECT
        selected_theme,
        pink_theme,
        blue_theme,
        purple_theme
    FROM themes
    WHERE user_id = ?
    """, (user_id,))

    theme = local_cursor.fetchone()

    if not theme:
        return None

    return {
        "selected_theme": theme[0],
        "pink_theme": theme[1],
        "blue_theme": theme[2],
        "purple_theme": theme[3]
    }
    
def apply_theme(
    login_id,
    theme_name
):

    cursor.execute("""
    SELECT id
    FROM users
    WHERE login_id = ?
    """, (login_id,))

    user = cursor.fetchone()

    if not user:
        return {
            "success": False,
            "message": "사용자를 찾을 수 없습니다."
        }

    user_id = user[0]

    if theme_name != "default":

        cursor.execute(f"""
        SELECT {theme_name}_theme
        FROM themes
        WHERE user_id = ?
        """, (user_id,))

        owned = cursor.fetchone()

        if not owned or owned[0] == 0:
            return {
                "success": False,
                "message": "구매하지 않은 테마입니다."
            }

    cursor.execute("""
    UPDATE themes
    SET selected_theme = ?
    WHERE user_id = ?
    """, (theme_name, user_id))

    conn.commit()

    return {
        "success": True,
        "message": "테마 적용 완료"
    }

def get_current_semester():

    now = datetime.now()

    if 3 <= now.month <= 6:
        return f"{now.year}년 1학기"

    elif 7 <= now.month <= 8:
        return f"{now.year}년 여름학기"

    elif 9 <= now.month <= 12:
        return f"{now.year}년 2학기"

    else:
        return f"{now.year}년 겨울학기"

def check_semester(login_id):

    current_semester = (
        get_current_semester()
    )

    cursor.execute("""
    SELECT
        id,
        semester
    FROM users
    WHERE login_id = ?
    """, (login_id,))

    user = cursor.fetchone()

    if not user:
        return

    user_id = user[0]
    saved_semester = user[1]

    if saved_semester == current_semester:
        return

    cursor.execute("""
    UPDATE points
    SET total_points = 0
    WHERE user_id = ?
    """, (user_id,))

    cursor.execute("""
    UPDATE badges
    SET
        easy_success_count = 0,
        hard_success_count = 0,
        rain_success_count = 0,
        early_morning_count = 0,
        long_distance_count = 0
    WHERE user_id = ?
    """, (user_id,))

    cursor.execute("""
    DELETE FROM logs
    WHERE user_id = ?
    """, (user_id,))

    cursor.execute("""
    UPDATE users
    SET semester = ?
    WHERE id = ?
    """, (
        current_semester,
        user_id
    ))

    conn.commit()

def validate_semester(login_id):

    check_semester(
        login_id
    )