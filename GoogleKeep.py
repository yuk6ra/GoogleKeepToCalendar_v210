import pandas as pd

import gkeepapi
import re

ACCOUNT_ID = 'xxxxxxxx@gmail.com'
PASSWORD = 'yyyy1234'

class Reader(object):
    def __init__(self):

        self.title = []
        self.content = []
        self.year = []
        self.month = []
        self.day = []

        # find Google Account ID and Password
        self.keep = gkeepapi.Keep()
        r = self.keep.login(ACCOUNT_ID, PASSWORD)
        print("LOGIN :", "#"*30,r,"#"*30)

        self.keep.sync()

    def google_keep_searcher(self, search_label):

        self.keep.sync()

        #　「2020年1月13日」などを読み込む
        self.date_type = re.compile(r"""(
            (^\d{4})
            (\D)
            (\d{1,2})
            (\D)
            (\d{1,2})
            (\S|\s|)+(\S|)
            )""",re.VERBOSE)

        #　「2020年1月13日　タイトル」の文字列タイトルを読み込む
        self.string_type = re.compile(r'\S+$')

        # find the keyword of query="Test"
        self.note = self.keep.find(query=self.date_type, labels=[self.keep.findLabel(search_label)])
        # indicate the found memos

        # list を返す
    def google_keep_reader(self, default_title_name):
        # dict change

        dict_notes = {}
        for note_data in self.note:
            title = note_data.title
            text = note_data.text
            note_id = note_data.id
            notes = {title: [text, note_id]}
            dict_notes.update(notes)

        # Separate date, content

        for date, contents in dict_notes.items():
            # Hit data to "hit_date"
            hit_date = self.date_type.search(date)

            if bool(hit_date) is False: # Title is not string value
                continue

            split = hit_date.groups()
            all_note_title = self.string_type.search(split[0])

            if all_note_title:
                title_name = all_note_title.group()
            else:
                title_name = hit_date.string

            if title_name == hit_date.string:

                # print("Title :", default_title_name)
                self.new_title_name = default_title_name
            else:
                # .strip()によって\u3000という空白を取り除いています
                # print("Title :", title_name.strip())
                self.new_title_name = title_name.strip()

            # Tuple unpacking
            year, month, day = int(split[1]), int(split[3]), int(split[5])

            if year < 3000 and month <= 12 and day <= 31:
                content = contents[0]
                note_id = contents[1]

                # print("Date　:{}-{}-{}\nContent :{}".format(year, month, day, content[0:10]))

                self.gnote = self.keep.get(note_id)

                self.title.append(self.new_title_name)
                self.content.append(content)
                self.year.append(year)
                self.month.append(month)
                self.day.append(day)

                # not Japan time zone
                # print(str(note_data.timestamps.created),"\n")
                # print("-"*80)
            else:
                continue

        notes = {
            "year": self.year,
            "month": self.month,
            "day": self.day,
            "title": self.title,
            "content": self.content,
        }

        df = pd.DataFrame(notes)
        self.keep.sync()
        return df

DEFAULT_TITLE_NAME = 'メモ'

# reader = Reader()
# reader.google_keep_searcher(search_label=SEARCH_LABEL)
# result = reader.google_keep_reader(default_title_name=DEFAULT_TITLE_NAME)
# print(result)

# writer = CsvWriter()
# writer.csv_writer(result)