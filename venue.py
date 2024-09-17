from __init__ import CONN,CURSOR

class Venue():
    all={}
    def __init__(self,title,city):
        self.title=title
        self.city=city
        
    @property
    def  title(self):
        return self._title
    
    @title.setter
    def title(self,title):
        if isinstance(title,str) and len(title):
            self._title=title
        else:
            raise ValueError("Title must be a non_empty string")
    
    @property
    def city(self):
        return self._city
    
    @city.setter
    def city(self,city):
        if isinstance(city,str) and len(city):
            self._city=city
        else:
            raise ValueError("City must be a non_empty string")
    
    @classmethod
    def create_table(cls):
        sql="""
            CREATE TABLE IF NOT EXISTS venues(
                id INTEGER PRIMARY KEY,
                title TEXT,
                city TEXT
                )
            """
        CURSOR.execute(sql)
        CONN.commit()
        
    @classmethod
    def drop_table(cls):
        sql="""
            DROP TABLE IF EXISTS venues
        """
        CURSOR.execute(sql)
        CONN.commit()
    
    def save(self):
        sql="""
            INSERT INTO venues(title,city)
            VALUES(?,?)
        """
        CURSOR.execute(sql,(self.title,self.city))
        CONN.commit()
        self.id=CURSOR.lastrowid
        Venue.all[self.id]=self
    
    @classmethod
    def create(cls,title,city):
        venue=cls(title,city)
        venue.save()
        return venue;
    
    def update(self):
        sql="""
            UPDATE venues
            SET title=? ,city=?
            WHERE id=?
        """
        CURSOR.execute(sql,(self.title,self.city,self.id))
        CONN.commit()
    
    def delete(self):
        sql="""
            DELETE FROM venues
            WHERE id=?
        """
        CURSOR.execute(sql,(self.id,))
        CONN.commit()
    
    @classmethod
    def instance_from_db(cls,row):
        venue=cls.all.get(row[0])
        
        if venue:
            venue.title=row[1]
            venue.city=row[2]
        
        else:
            venue=cls(row[1],row[2])
            venue.id=row[0]
            cls.all[venue.id]=venue
        
        return venue
    
    @classmethod
    def get_all(cls):
        sql="""
            SELECT * FROM venues
        """
        rows=CURSOR.execute(sql).fetchall()
        return [cls.instamce_from_db(row) for row in rows]
    
    def concerts(self):
        from concert import Concert
        sql="""
            SELECT * FROM concerts WHERE venue=?
        """
        rows=CURSOR.execute(sql,(self.title,)).fetchall()
        return [Concert.instance_from_db(row) for row in rows]
        
    def bands(self):
        from concert import Concert
        sql="""
            SELECT * FROM concerts WHERE venue=?
        """
        rows=CURSOR.execute(sql,(self.title,)).fetchall()
        return[Concert.instance_from_db(row) for row in rows]
    
    def concert_on(self,date):
        from concert import Concert
        if not isinstance(date,str):
            raise ValueError("Date must be a non empty string ")
        
        sql="""
            SELECT * FROM concerts
            WHERE date=? and venue=?
        """
        row=CURSOR.execute(sql,(date,self.title)).fetchone()
        return Concert.instance_from_db(row) if row else None
    
    
    def most_frequent_band(self):
        sql = """
            SELECT band, COUNT(*) as performance_count
            FROM concerts
            WHERE venue = ?
            GROUP BY band
            ORDER BY performance_count DESC
            LIMIT 1
        """
        row=CURSOR.execute(sql,(self.title,)).fetchone()
        if row:
            from band import Band
            return Band.find_by_name(row[0])
        return None