# @Ondřej Divina & Jan Melichařík

from diary_record import DiaryRecord
from datetime import datetime

if __name__== "__main__":
    print("Welcome to our app")
    records = [
        DiaryRecord(datetime(2020, 2, 23), "Den ve škole", "Ráno jsem šel do školy. Po škole jsem šel domů.\n "
                                                         "Doma to byla sranda."),
        DiaryRecord(datetime(2020, 2, 22), "Pohodová neděle", "Ráno jsem nešel do školy.  Odpoledne byla procházka.\n "\
                                                         "Doma to byla sranda$÷+ěš  .")
    ]
