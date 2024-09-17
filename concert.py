from __init__ import CONN,CURSOR

class Concert():
    all={}
    def __init__(self,date,bandd,venuee):
        self.date=date
        self.bandd=bandd
        self.venuee=venuee
    
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
    def bandd(self):
        return self._bandd
    
    @bandd.setter
    def bandd(self,band):
        from band import Band
        if isinstance(band,Band):
            self._bandd=band
        else:
            raise ValueError("Band must be an instance of class Band")
    
    @property
    def venuee(self):
        return self._venuee
    
    @venuee.setter
    def venuee(self,venue):
        from venue import Venue
        if isinstance(venue,Venue):
            self._venuee=venue
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
        CURSOR.execute(sql,(self.date,self.bandd.name,self.venuee.title))
        CONN.commit()
        self.id=CURSOR.lastrowid
        Concert.all[self.id]=self
    @classmethod   
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
        CURSOR.execute(sql,(self.date,self.bandd.name,self.venuee.title,self.id))
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
        from band import Band
        from venue import Venue
        
        band=Band.find_by_name(row[2])
        
        sql="""SELECT * FROM venues WHERE title=?"""
        venue_row=CURSOR.execute(sql,(row[3],)).fetchone()
        
        if venue_row:
            venue=Venue.instance_from_db(venue_row)
        else:
            venue=None
        
        concert=cls.all.get(row[0])
        if concert:
            concert.date=row[1]
            concert.band=band
            concert.venue=venue
        else:
            concert=cls(row[1],band,venue)
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
        return self.bandd
    
    
    def venue(self):
        return self.venuee
    
    def hometown_show(self):
        sql="""
            SELECT concerts.band ,concerts.venue
            FROM concerts
            INNER JOIN bands
            ON concerts.venue =bands.hometown
            WHERE concerts.band=?
        """
        row=CURSOR.execute(sql,(self.bandd.name,)).fetchone()
        return True if row else False
    
    def introduction(self):
        return f"Hello {self.venuee.city}!!!!! We are {self.bandd.name} and we're from {self.bandd.hometown}"
    
    
    