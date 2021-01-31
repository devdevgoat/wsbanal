import spacy
import sqlite3
import os 
nlp = spacy.load("en_core_web_sm")

def check_database_exists(subreddit):
    """Create the database subreddit.db if it does not exist.
    Here the UNIQUE constraint will maintain we don't insert duplicate
    comment_id's into the subreddit table in that database"""
    if not os.path.exists('../data/{}.db'.format(subreddit)):
        conn = sqlite3.connect('../data/{}.db'.format(subreddit))
        c = conn.cursor()
        c.execute("""CREATE TABLE ents (text,label,count,timeId,UNIQUE (text,label,timeId))""".format(subreddit))
        conn.commit()
        conn.close()

def proc_data(subreddit, cursor):
    print('getting rows')
    rows = cursor.execute("SELECT * FROM wallstreetbets where proc='False' limit 100").fetchall()
    for row in rows:
        r = nlp(row['comment'])
        # print(f"-----{row['comment_id']}------")
        commentTexts = []
        commentLables = []
        
        for ent in r.ents:
            # print(ent.text, ent.label_)
            commentTexts.append(ent.text)
            commentLables.append(ent.label_)
            cursor.execute(f"""Insert into ents (text, label,timeId, count) 
                                values (?,?,{row['timeId']}, 1)
                                on CONFLICT (text, label, timeId) DO UPDATE set count = count + 1""",(ent.text,ent.label_))
        cursor.execute(f"""UPDATE wallstreetbets set proc="True", entTexts = ? ,entLabels = ?  where comment_id = '{row['comment_id']}'""",(str(commentTexts) ,str(commentLables)))

doc = nlp("Apple is looking at buying U.K. startup for $1 billion. GME is valued much higher now!")




def main():
    subreddit = 'wallstreetbets'
    check_database_exists(subreddit)
    conn = sqlite3.connect('../data/{}.db'.format(subreddit), isolation_level=None)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    while True:
        proc_data(subreddit=subreddit, cursor=c)
        conn.commit()
    conn.close()


if __name__ == "__main__":
    main()