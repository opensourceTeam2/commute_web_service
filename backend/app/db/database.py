import sqlite3
import os
import hashlib
import hmac
from datetime import datetime


conn = sqlite3.connect(
    "commute.db",
    check_same_thread=False
)

cursor = conn.cursor()


# =========================
# 학기 계산
# =========================
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


# =========================
# users 테이블
# =========================
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    login_id TEXT UNIQUE,
    password_hash TEXT,
    nickname TEXT,
    created_at TEXT,
    semester TEXT
)
""")


# 기존 DB를 쓰고 있던 경우를 위한 컬럼 추가
for column_sql in [
    "ALTER TABLE users ADD COLUMN password_hash TEXT",
    "ALTER TABLE users ADD COLUMN nickname TEXT",
    "ALTER TABLE users ADD COLUMN semester TEXT"
]:
    try:
        cursor.execute(column_sql)
    except sqlite3.OperationalError:
        pass


# =========================
# points 테이블
# =========================
cursor.execute("""
CREATE TABLE IF NOT EXISTS points (
    user_id INTEGER PRIMARY KEY,
    total_points INTEGER DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES users(id)
)
""")


# =========================
# badges 테이블
# =========================
cursor.execute("""
CREATE TABLE IF NOT EXISTS badges (
    user_id INTEGER PRIMARY KEY,
    easy_success_count INTEGER DEFAULT 0,
    hard_success_count INTEGER DEFAULT 0,
    rain_success_count INTEGER DEFAULT 0,
    early_morning_count INTEGER DEFAULT 0,
    long_distance_count INTEGER DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES users(id)
)
""")


# =========================
# logs 테이블
# =========================
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
    FOREIGN KEY (user_id) REFERENCES users(id)
)
""")


# =========================
# themes 테이블
# =========================
cursor.execute("""
CREATE TABLE IF NOT EXISTS themes (
    user_id INTEGER PRIMARY KEY,
    selected_theme TEXT DEFAULT 'default',
    pink_theme INTEGER DEFAULT 0,
    blue_theme INTEGER DEFAULT 0,
    purple_theme INTEGER DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES users(id)
)
""")

conn.commit()


# =========================
# 비밀번호 처리
# =========================
def hash_password(password):
    salt = os.urandom(16).hex()

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        bytes.fromhex(salt),
        100000
    ).hex()

    return f"{salt}${password_hash}"


def verify_password(password, saved_hash):
    if not saved_hash:
        return False

    if "$" not in saved_hash:
        return False

    salt, original_hash = saved_hash.split("$", 1)

    check_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        bytes.fromhex(salt),
        100000
    ).hex()

    return hmac.compare_digest(original_hash, check_hash)


# =========================
# 사용자 기본 데이터 생성
# =========================
def init_user_data(user_id):
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
    INSERT OR IGNORE INTO badges (
        user_id,
        easy_success_count,
        hard_success_count,
        rain_success_count,
        early_morning_count,
        long_distance_count
    )
    VALUES (
        ?,
        0,
        0,
        0,
        0,
        0
    )
    """, (user_id,))

    cursor.execute("""
    INSERT OR IGNORE INTO themes (
        user_id,
        selected_theme,
        pink_theme,
        blue_theme,
        purple_theme
    )
    VALUES (
        ?,
        'default',
        0,
        0,
        0
    )
    """, (user_id,))


# =========================
# 회원가입
# =========================
def register_user(login_id, password, nickname):
    login_id = login_id.strip()
    nickname = nickname.strip() if nickname else login_id

    cursor.execute("""
    SELECT id, password_hash
    FROM users
    WHERE login_id = ?
    """, (login_id,))

    existing_user = cursor.fetchone()

    password_hash = hash_password(password)
    current_semester = get_current_semester()

    # 기존에 포인트 기능으로만 생성된 사용자가 있고 비밀번호가 없다면 회원가입으로 전환
    if existing_user:
        user_id = existing_user[0]
        saved_password_hash = existing_user[1]

        if saved_password_hash:
            raise ValueError("이미 존재하는 아이디입니다.")

        cursor.execute("""
        UPDATE users
        SET password_hash = ?,
            nickname = ?,
            semester = ?
        WHERE id = ?
        """, (
            password_hash,
            nickname,
            current_semester,
            user_id
        ))

        init_user_data(user_id)
        conn.commit()

        return {
            "loginId": login_id,
            "nickname": nickname,
            "semester": current_semester
        }

    cursor.execute("""
    INSERT INTO users (
        login_id,
        password_hash,
        nickname,
        created_at,
        semester
    )
    VALUES (
        ?,
        ?,
        ?,
        ?,
        ?
    )
    """, (
        login_id,
        password_hash,
        nickname,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        current_semester
    ))

    user_id = cursor.lastrowid

    init_user_data(user_id)
    conn.commit()

    return {
        "loginId": login_id,
        "nickname": nickname,
        "semester": current_semester
    }


# =========================
# 로그인
# =========================
def login_user(login_id, password):
    login_id = login_id.strip()

    cursor.execute("""
    SELECT id, login_id, password_hash, nickname, semester
    FROM users
    WHERE login_id = ?
    """, (login_id,))

    user = cursor.fetchone()

    if not user:
        return None

    user_id = user[0]
    saved_login_id = user[1]
    saved_password_hash = user[2]
    nickname = user[3]

    if not verify_password(password, saved_password_hash):
        return None

    init_user_data(user_id)
    check_semester(saved_login_id)
    conn.commit()

    return {
        "loginId": saved_login_id,
        "nickname": nickname if nickname else saved_login_id,
        "semester": get_current_semester()
    }


# =========================
# 회원 정보 조회
# =========================
def get_user_profile(login_id):
    cursor.execute("""
    SELECT id, login_id, nickname, created_at, semester
    FROM users
    WHERE login_id = ?
    """, (login_id,))

    user = cursor.fetchone()

    if not user:
        return None

    return {
        "id": user[0],
        "loginId": user[1],
        "nickname": user[2] if user[2] else user[1],
        "createdAt": user[3],
        "semester": user[4]
    }


# =========================
# 기존 포인트/테마 기능용 사용자 생성
# =========================
def get_user_id(login_id):
    if not login_id:
        return None

    check_semester(login_id)

    cursor.execute("""
    SELECT id
    FROM users
    WHERE login_id = ?
    """, (login_id,))

    result = cursor.fetchone()

    return result


def create_user(login_id):
    if not login_id:
        return

    current_semester = get_current_semester()

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
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        current_semester
    ))

    cursor.execute("""
    SELECT id
    FROM users
    WHERE login_id = ?
    """, (login_id,))

    user = cursor.fetchone()

    if user:
        init_user_data(user[0])

    conn.commit()


# =========================
# 포인트
# =========================
def add_points(login_id, earned_points):
    cursor.execute("""
    SELECT id
    FROM users
    WHERE login_id = ?
    """, (login_id,))

    user = cursor.fetchone()

    if not user:
        return

    user_id = user[0]
    init_user_data(user_id)

    cursor.execute("""
    UPDATE points
    SET total_points = total_points + ?
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
    init_user_data(user_id)

    cursor.execute("""
    SELECT total_points
    FROM points
    WHERE user_id = ?
    """, (user_id,))

    result = cursor.fetchone()

    if not result:
        return 0

    return result[0]


# =========================
# 뱃지
# =========================
def update_badge_count(login_id, badge_type):
    valid_badge_types = [
        "easy_success_count",
        "hard_success_count",
        "rain_success_count",
        "early_morning_count",
        "long_distance_count"
    ]

    if badge_type not in valid_badge_types:
        return

    cursor.execute("""
    SELECT id
    FROM users
    WHERE login_id = ?
    """, (login_id,))

    user = cursor.fetchone()

    if not user:
        return

    user_id = user[0]
    init_user_data(user_id)

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
    init_user_data(user_id)

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


# =========================
# 로그
# =========================
def add_log(
    login_id,
    checked_at,
    start_location,
    class_start_time,
    route_summary,
    total_minutes,
    late_probability
):
    if not login_id:
        return

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
        ?,
        ?,
        ?,
        ?,
        ?,
        ?,
        ?
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


# =========================
# 테마
# =========================
def buy_theme(login_id, theme_name):
    valid_themes = ["pink", "blue", "purple"]

    if theme_name not in valid_themes:
        return {
            "success": False,
            "message": "존재하지 않는 테마입니다."
        }

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
    init_user_data(user_id)

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


def get_themes(login_id):
    cursor.execute("""
    SELECT id
    FROM users
    WHERE login_id = ?
    """, (login_id,))

    user = cursor.fetchone()

    if not user:
        return None

    user_id = user[0]
    init_user_data(user_id)

    cursor.execute("""
    SELECT
        selected_theme,
        pink_theme,
        blue_theme,
        purple_theme
    FROM themes
    WHERE user_id = ?
    """, (user_id,))

    theme = cursor.fetchone()

    if not theme:
        return None

    return {
        "selected_theme": theme[0],
        "pink_theme": theme[1],
        "blue_theme": theme[2],
        "purple_theme": theme[3]
    }


def apply_theme(login_id, theme_name):
    valid_themes = ["default", "pink", "blue", "purple"]

    if theme_name not in valid_themes:
        return {
            "success": False,
            "message": "존재하지 않는 테마입니다."
        }

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
    init_user_data(user_id)

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
    """, (
        theme_name,
        user_id
    ))

    conn.commit()

    return {
        "success": True,
        "message": "테마 적용 완료"
    }


# =========================
# 학기 변경 시 초기화
# =========================
def check_semester(login_id):
    current_semester = get_current_semester()

    cursor.execute("""
    SELECT id, semester
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
    check_semester(login_id)