
import sqlite3
from pathlib import Path

db_path = Path(r"D:\Aware\Backend\instance\user.db")
conn = sqlite3.connect(db_path)

try:
    columns = {
        row[1]
        for row in conn.execute("PRAGMA table_info(transcript)")
    }

    print("Before:", sorted(columns))

    required = {
        "raw_text": "TEXT",
        "semantic_text": "TEXT",
        "start": "REAL",
        "end": "REAL",
    }

    for name, data_type in required.items():
        if name not in columns:
            conn.execute(
                f'ALTER TABLE transcript ADD COLUMN "{name}" {data_type}'
            )

    # Preserve existing transcript data
    conn.execute("""
        UPDATE transcript
        SET raw_text = COALESCE(raw_text, text, '')
        WHERE raw_text IS NULL
    """)

    conn.execute("""
        UPDATE transcript
        SET semantic_text = COALESCE(semantic_text, text, '')
        WHERE semantic_text IS NULL
    """)

    conn.execute("""
        UPDATE transcript
        SET start = COALESCE(start, start_time)
        WHERE start IS NULL
    """)

    conn.execute("""
        UPDATE transcript
        SET "end" = COALESCE("end", end_time)
        WHERE "end" IS NULL
    """)

    conn.commit()

    columns = {
        row[1]
        for row in conn.execute("PRAGMA table_info(transcript)")
    }

    print("After:", sorted(columns))
    print("Migration completed successfully.")

except Exception:
    conn.rollback()
    raise

finally:
    conn.close()
