from __init__ import CONN,CURSOR

class Band():
    all={}
    def __init__(self,name,hometown):
        self.name=name
        self.hometown=hometown
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self,name):
        if isinstance(name,str) and len(name):
            self._name=name
        else:
            raise ValueError("Name must be a non_empty string")
    
    @property
    def hometown(self):
        return self._hometown
    
    @hometown.setter
    def hometown(self,hometown):
        if isinstance(hometown,str) and len(hometown):
            self._hometown=hometown
        else:
            raise ValueError("hometown must be a non_empty string")
    
    @classmethod
    def create_table(cls):
        sql="""
            CREATE TABLE IF NOT EXISTS bands (
                id INTEGER PRIMARY KEY,
                name TEXT,
                hometown TEXT
            )
        """
        CURSOR.execute(sql)
        CONN.commit()
        
    @classmethod
    def drop_table(cls):
        sql="""
            DROP TABLE IF EXISTS bands;
        """
        CURSOR.execute(sql)
        CONN.commit()
    
    def save(self):
        sql="""
            INSERT INTO bands (name,hometown)
            VALUES(?,?)
        """
        CURSOR.execute(sql,(self.name,self.hometown))
        CONN.commit()
        self.id=CURSOR.lastrowid
        type(self).all[self.id]=self
    
    @classmethod
    def create(cls,name,hometown):
        band=cls(name,hometown)
        band.save()
        return band
    
    def update(self):
        sql="""
            UPDATE bands 
            SET name=? ,hometown=?
            WHERE id=?
        """
        CURSOR.execute(sql,(self.name,self.hometown,self.id))
        CONN.commit()
    
    
    @classmethod
    def instance_from_db(cls,row):
        band=cls.all.get(row[0])
        
        if band :
            band.name=row[1]
            band.hometown=row[2]
        else:
            band=cls(row[1],row[2])
            band.id=row[0]
            cls.all[band.id]=band
        return band
    @classmethod
    def get_all(cls):
        sql="""
            SELECT * FROM bands
        """
        rows=CURSOR.execute(sql).fetchall()
        
        return[cls.instance_from_db(row) for row in rows]
    
    @classmethod
    def find_by_id(cls,id):
        sql="""
            SELECT * FROM bands 
            WHERE id=?
        """
        row=CURSOR.execute(sql,(id,)).fetchone()
        return cls.instance_from_db(row) if row else None
    
    @classmethod
    def find_by_name(cls,name):
        sql="""
            SELECT * FROM bands 
            WHERE name = ?
        """
        row=CURSOR.execute(sql,(name,)).fetchone()
        return cls.instance_from_db(row) if row else None
    
    def delete(self):
        sql="""
            DELETE FROM bands
            WHERE id=?
        """
        CURSOR.execute(sql,(self.id,))
        CONN.commit()
        
        del Band.all[self.id]
        self.id=None
    
    def concerts(self):
        from concert import Concert
        sql="""
            SELECT * FROM concerts WHERE band =?
        """
        rows=CURSOR.execute(sql,(self.name,)).fetchall()
        return [Concert.instance_from_db(row) for row in rows]
    
    def venues(self):
        from concert import Concert
        sql="""
            SELECT * FROM concerts WHERE band=?
        """
        rows=CURSOR.execute(sql,(self.name,)).fetchall()
        return [Concert.instance_from_db(row).venue for row in rows]
    
    def play_in_venue(self,venue, date):
        from venue import Venue
        from concert import Concert
        
        sql_value="""
            SELECT * FROM venues WHERE title=?
        """
        row=CURSOR.execute(sql_value,(venue,)).fetchone()
        
        if row:
            venue_instance=Venue.instance_from_db(row)
        else:
            venue_instance=Venue.create(venue,f"{venue} city")
        
        sql="""
            INSERT INTO concerts(date,band,venue)
            VALUES(?,?,?)
        """
        
        CURSOR.execute(sql,(date,self.name,venue_instance.title))
        CONN.commit()
        concert=Concert(date,self,venue_instance)
        concert.id=CURSOR.lastrowid
        return concert
    
    def all_introductions(self):
        concerts=self.concerts()
        intros=[]
        for concert in concerts:
            intro=f"Hello {concert.venue.city}!!!!! We are {self.name} and we're from {self.hometown}"
            intros.append(intro)
        return intros
    
    @classmethod
    def most_performances(cls):
        sql = """
            SELECT band, COUNT(*) as performance_count
            FROM concerts
            GROUP BY band
            ORDER BY performance_count DESC
            LIMIT 1
        """
        row = CURSOR.execute(sql).fetchone()
        if row:
            return cls.find_by_name(row[0])
        return None
        
        
