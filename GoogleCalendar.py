from __future__ import print_function
import pickle
import os.path
import datetime
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']

class Writer(object):
    def __init__(self):
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        self.service = build('calendar', 'v3', credentials=creds)



    def google_calendar_writer(self, df, calendar_id):
        for index, row in df.iterrows():

            self.year = int(row['year'])
            self.month = int(row['month'])
            self.day = int(row['day'])
            self.title = str(row['title'])
            self.content = str(row['content'])

            # timeMin, timeMaxの設定
            # ここの設定は諸注意が必要
            dt = f'{self.year}-{self.month}-{self.day}'
            td = datetime.timedelta(days=1)
            timemax = datetime.datetime.strptime(dt, "%Y-%m-%d")
            timemin = timemax - td

            # カレンダーに書かれている情報を取得する
            event_result = self.service.events().list(
                calendarId=calendar_id,
                q=self.content,
                timeMin="{}-{}-{}T00:00:00Z".format(timemin.year, timemin.month, timemin.day),
                timeMax="{}-{}-{}T00:00:00Z".format(timemax.year, timemax.month, timemax.day),
                singleEvents=True,
                orderBy="startTime",
            ).execute()


            event = event_result.get("items", [])

            new_event = {
                'summary': self.title,
                'location': "",
                "kind": "calendar#event",
                'description': self.content,
                'start': {
                    'date': "{}-{}-{}".format(self.year, self.month, self.day),
                    'timeZone': 'Japan',
                },
                'end': {
                    'date': '{}-{}-{}'.format(self.year, self.month, self.day),
                    'timeZone': 'Japan',
                },
            }


            # if the note have already been writen, bool value is "True".
            # もしカレンダーを調べた結果、そこに何も予定が書きこまれていなければ
            if bool(event) is False:

                # #もしも近辺に同じような書き込みがある場合は、それを削除して、新しくつくる
                #
                # #通常通り更新する
                # content_similarity = round(difflib.SequenceMatcher(None, old_content, self.content).ratio(), 3)
                # title_similarity = round(difflib.SequenceMatcher(None, old_title, self.title).ratio(), 3)
                # sim_number = 0.9

                self.service.events().insert(calendarId=calendar_id, body=new_event).execute()
                print("Calendar Insertion Complete. :", self.year, self.month, self.day, self.title, self.content[0:10])

                # self.service.events().update(calendarId=calendar_id, body=new_event).execute()
                # print("Google Calendar :Done :",self.year, self.month, self.day , self.title, self.content[0:10])

            else:# すでにカレンダーに予定が書き込まれていた場合は

                d = event[0] #調べているやつ
                old_title, old_content = d.get('summary'), d.get('description') # d.get()によって、keyが存在しないときはNoneを返すようになる

                #もしもタイトルとコンテンツが同じだったら、書き込みを行わない。
                if old_title == self.title and old_content == self.content:
                    print("Calendar Already Exists :", self.year, self.month, self.day, self.title,self.content[0:10])
                # elif (old_title == self.title and similarity >= half_similarity) | (old_title != self.title and ):


                #そのほかのタイトルもコンテンツも違うものは
                else:
                    # 更新する
                    s = d.get('id')
                    self.service.events().update(calendarId=calendar_id, body=new_event, eventId=s).execute()
                    print("Calendar Updated :", self.year, self.month, self.day, self.title,self.content[0:10])


# writer = Writer()
# writer.google_calendar_writer(calendar_id=calendar_id)

