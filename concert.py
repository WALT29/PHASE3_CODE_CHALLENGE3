from __init__ import CONN,CURSOR

class Concert():
    all={}
    def __init__(self,date,band,venue):
        self.date=date
        self.band=band
        self.venue=venue
    
    @property
    def date(self):
        return self._date
    
    @date.setter
    def date(self,date):
        if isinstance(date,str) and len(date):
            self._date=date
        else:
            raise ValueError("Date is a non empty string")
    
    @property
    def band(self):
        return self._band
    
    @band.setter
    def band(self,band):
        from band import Band
        if isinstance(band,Band):
            self._band=band
        else:
            raise ValueError("Band must be an instance of class Band")
    
    @property
    def venue(self):
        return self._venue
    
    @venue.setter
    def venue(self,venue):
        from venue import Venue
        if isinstance(venue,Venue):
            self._venue=venue
        else:
            raise ValueError("Venue must be an instance of class Venue")
    
    @classmethod
    def create_table(cls):
        sql="""
            CREATE TABLE IF NOT EXISTS concerts(
                id INTEGER PRIMARY KEY,
                date TEXT,
                band TEXT,
                venue TEXT
            )
        """
        CURSOR.execute(sql)
        CONN.commit()
    
    @classmethod
    def drop_table(cls):
        sql="""
            DROP TABLE IF EXISTS concerts
        """
        CURSOR.execute(sql)
        CONN.commit()
    
    def save(self):
        sql="""
            INSERT INTO concerts(date,band,venue)
            VALUES(?,?,?)
        """
        CURSOR.execute(sql,(self.date,self.band.name,self.venue.city))
        CONN.commit()
        self.id=CURSOR.lastrowid
        Concert.all[self.id]=self
        
    def create(cls,date,band,venue):
        concert=cls(date,band,venue)
        concert.save()
        return concert
    
    def update(self):
        sql="""
            UPDATE concerts 
            SET date=?,band=?,venue=?
            WHERE id=?
        """
        CURSOR.execute(sql,(self.date,self.band.name,self.venue.title,self.id))
        CONN.commit()
    
    
    def delete(self):
        sql="""
            DELETE FROM concerts WHERE id=?
        """
        CURSOR.execute(sql,(self.id,))
        CONN.commit()
        del Concert.all[self.id]
        self.id=None
    
    @classmethod
    def instance_from_db(cls,row):
        concert=cls.all.get(row[0])
        if concert:
            concert.date=row[1]
            concert.band=row[2]
            concert.venue=row[3]
        else:
            concert=cls(row[1],row[2],row[3])
            concert.id=row[0]
            cls.all[concert.id]=concert
        return concert
    
    @classmethod
    def get_all(cls):
        sql="""
            SELECT * FROM concerts
        """
        rows=CURSOR.execute(sql).fetchall()
        return[cls.instance_from_db(row) for row in rows]
    
    @classmethod
    def find_by_id(cls,id):
        sql="""
            SELECT * FROM concerts
            WHERE id=?
        """
        row=CURSOR.execute(sql,(id,)).fetchone()
        return cls.instance_from_db(row) if row else None
    
    
    def band(self):
        return self.band
    
    
    def venue(self):
        return self.venue
    
    def hometown_show(self):
        sql="""
            SELECT concerts.band ,concerts.venue
            FROM concerts
            INNER JOIN bands
            ON concerts.venue =bands.hometown
            WHERE concert.band=?
        """
        row=CURSOR.execute(sql,(self.band.name)).fetchone()
        return True if row else False
    
    def introduction(self):
        return f"Hello {self.venue.city}!!!!! We are {self.band.name} and we're from {self.band.hometown}"
    
    
    