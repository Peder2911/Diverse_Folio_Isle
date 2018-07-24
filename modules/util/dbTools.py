import sqlite3 as sq

import yaml
import itertools

#####################################

def listToQuery(list):
    list = [x.replace('\'','') for x in list]
    list = ['\''+x+'\'' for x in list]
    query = ','.join(list)
    query = '('+query+')'
    return(query)

#####################################

def checkExists(currId,cursor):
    cursor.execute('SELECT id FROM sentences WHERE id=\'%s\''%(currId))
    entry = cursor.fetchone()

    return(entry is not None)

#####################################

def addToDB(db,table,values,overwrite):
    conn = sq.connect(db)
    c = conn.cursor()

    values = [val.replace('\'','') for val in values]
    values = ["'"+val+"'" for val in values]
    values = ','.join(values)
    values = '('+values+')'


    if exists and overwrite:
        c.execute('DELETE FROM sentences WHERE ')

    command = 'INSERT INTO {tab} VALUES {val}'.format(tab=table,val=values)
    c.execute(command)

    conn.commit()
    conn.close()


def bulkAdd(entries,db,table,overwrite=True):
    # Make it return a status...

    currId = entries[0]['id']

    con = sq.connect(db)
    c = con.cursor()

    if overwrite and checkExists(currId,c):
        c.execute('DELETE FROM sentences WHERE id=\'%s\''%(currId))

    columns = listToQuery([*entries[0].keys()])
    values = [listToQuery([*entry.values()]) for entry in entries]
    values = ', '.join(values)

    c.execute('''INSERT INTO {tab} {col} VALUES {val}
              '''.format(tab=table,col=columns,val=values))

    con.commit()
    con.close()
    return(1)

#####################################

def dbFacts(dbFile):
    con = sq.connect(dbFile)
    c = con.cursor()

    c.execute('SELECT body FROM sentences')
    entries = c.fetchall()
    nrow = len(entries)
    sentences = [b[0].split('\n') for b in entries]
    sentences = list(itertools.chain.from_iterable(sentences))
    nsent = len(sentences)

    c.execute('SELECT id FROM sentences')
    ids = c.fetchall()
    uniqueIds = set(ids)
    uniqueIds_n = len(uniqueIds)

    print('#'*10)
    print('\n')
    print('Number of entries : %i'%(nrow))
    print('Number of sentences : %i'%(nsent))
    print('Number of unique queries : %i'%(uniqueIds_n))
    for query in uniqueIds:
        print('--|%s'%(query))
    print('\n')
    print('#'*10)

#####################################

def bulkGet(db,table,column,filter = None):
    con = sq.connect(db)
    c = con.cursor()

    q = 'SELECT {col} FROM {tab}'.format(col=column,tab=table)

    if filter is not None:
        q += ' WHERE id=\'{fil}\''.format(fil=filter)
    else:
        pass

    c.execute(q)
    res = c.fetchall()
    con.close()

    if column != '*':
        res = [tup[0] for tup in res]
    else:
        pass

    return(res)
