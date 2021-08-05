print('Start #################################################################');
conn = new Mongo();
db = conn.getDB("m_db")

db.createUser(
        {
            user: "admin1",
            pwd: "admin1",
            roles: [
                {
                    role: "readWrite",
                    db: "m_db"
                }
            ]
        }
);
print('END #################################################################');
