import time

import requests
import json
import uuid

if __name__ == '__main__':
    account = input("请输入账号:")
    cookie = input("请输入cookie:")
    password = account[-6:]
    headers = {
        'Cookie': '4D7C38DF79A3336A21E6FC2805E1FEFE=' + cookie
    }
    url = 'https://se.mhtall.com/hbfsh/student/login.jsp?txtLoginName=' + account + '&txtPassword=' + password
    session = requests.session()
    session.get(url, headers=headers)
    request = session.get('https://se.mhtall.com/hbfsh/rs/student/score_info')
    jsonb = json.loads(request.text)
    for key in jsonb['data']:
        if key['scoreLesson'] != 100:
            learningCourseId = key['learningCourseId']
            strUid = str(uuid.uuid4())
            detailUrl = 'https://learning.mhtall.com/rest/course/detail?course_id=' + learningCourseId + '&course_uuid=' \
                        + strUid + '&course_code=&client_type=99'
            jsonfile = session.get(detailUrl, headers=headers)
            johnny = json.loads(jsonfile.text)
            for item in johnny['data']['courseLessonList']:
                if (item.get('finishLen') != item.get('timeLen')) and (item.get('lessonFormat') == 1):
                    videoPlayNum = item.get('timeLen') / 10
                    while videoPlayNum:
                        videoUrl = 'https://learning.mhtall.com/rest/user/course/lesson/onexit?course_id=' + learningCourseId + '&course_uuid=' + strUid + '&course_code=null&client_type=99&lesson_id=' + str(
                            item.get('lessonId')) + '&finish_len=9&video_position=10&video_duration=' + str(
                            item.get('timeLen'))
                        videoReturn = session.get(videoUrl, headers=headers)
                        time.sleep(10)
                        ss = json.loads(videoReturn.text)
                        if ss['code'] == '-1':
                            print(ss['message'])
                            break
                        else:
                            print(item.get('lessonName') + "--->还有" + str(
                                item.get('timeLen') - ss['data']) + "秒播放完毕-->" + time.strftime(
                                '%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
                            if ss['data'] == item.get('timeLen'):
                                break
