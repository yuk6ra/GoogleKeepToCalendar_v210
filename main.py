import GoogleKeep
import GoogleCalendar

def main(search_label, default_title_name, calendar_id):

    # オブジェクトの生成
    reader = GoogleKeep.Reader()
    writer = GoogleCalendar.Writer()

    # Google Keepを読み込む
    reader.google_keep_searcher(search_label=search_label)
    df = reader.google_keep_reader(default_title_name=default_title_name)

    # Google Calendarに書き込む
    writer.google_calendar_writer(df=df, calendar_id=calendar_id)


if __name__ == "__main__":

    """
        定義:
            search_label: Googleカレンダーに書き込みたいGoogleKeepのラベル
            default_title_name: タイトルがなかった場合のデフォルとのタイトル
            calendar_id: 書き込みたいGoogleカレンダーのID
    """

    # メモ
    main(search_label='メモ',
         default_title_name='メモ',
         calendar_id='')

    # 日記
    main(search_label='日記',
         default_title_name='日記',
         calendar_id='')
