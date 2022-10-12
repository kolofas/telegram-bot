conn = das.connect('db.sqlite')
cur = conn.cursor()
cur.execute('SELECT role_id FROM chats WHERE chat_id=?', (chat_id,))
role_id = cur.fetchone()

cur.execute('SELECT text FROM checklist_points WHERE role_id=?', (role_id,))
checklist = cur.fetchone()
print(checklist, 'checklist!!!!')