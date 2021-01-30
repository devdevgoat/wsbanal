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
        c.execute("""CREATE TABLE {}
                         (user, time, comment, comment_id, post_title, post_id, url, UNIQUE(comment_id))""".format(
            subreddit))
        conn.commit()
        conn.close()

def proc_data(subreddit, cursor):
    print('getting rows')
    rows = cursor.execute("SELECT * FROM wallstreetbets").fetchall()
    for row in rows:
        r = nlp(row['comment'])
        print(f'-----{}------'.)
        for ent in r.ents:
            print(ent.text, ent.start_char, ent.end_char, ent.label_)

doc = nlp("Apple is looking at buying U.K. startup for $1 billion. GME is valued much higher now!")




def main():
    subreddit = 'wallstreetbets'
    check_database_exists(subreddit)
    conn = sqlite3.connect('../data/{}.db'.format(subreddit))
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    proc_data(subreddit=subreddit, cursor=c)
    conn.commit()
    conn.close()


if __name__ == "__main__":
    main()