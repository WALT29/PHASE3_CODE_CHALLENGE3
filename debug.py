from band import Band
from venue import Venue
from concert import Concert



def program():
    Band.drop_table()
    Venue.drop_table()
    Concert.drop_table()

    Band.create_table()
    Venue.create_table()
    Concert.create_table()
    
    london_cowboys=Band("Chelsea","london")
    london_cowboys.save()
    manchester_reds=Band.create("Man Utd","manchester")
    
    uhuru_gardens=Venue.create("UHURU GARDENS","Nairobi")
    kasarani=Venue.create("KASARANI STADIUM","KASARANI")
    
    sato_concert=Concert("23-12-2023",london_cowboys,kasarani)
    sato_concert.save()
    
    sunday_concert=Concert.create("24-12-2023",manchester_reds,uhuru_gardens)
    
    # print(sunday_concert.band())
    # print(sunday_concert.venue())
    # print(kasarani.concerts())
    # print(kasarani.bands())
    
    print(london_cowboys.concerts())
    # print(london_cowboys.venues())
    
    
    print(sunday_concert.hometown_show())
    print(sato_concert.introduction())
    london_cowboys.play_in_venue("KIBAKI STADIUM","23-06-2024")
    # print(london_cowboys.concerts())
    print(london_cowboys.concerts())
    print(london_cowboys.venues())
    print(london_cowboys.all_introductions())
    
    print(Band.most_performances())
program()
