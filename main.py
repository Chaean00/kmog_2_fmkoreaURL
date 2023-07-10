import os
import sys
import chromedriver_autoinstaller
import requests
import urllib.request
import tkinter.messagebox as msgbox
import threading
import yt_dlp
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from bs4 import BeautifulSoup
from tkinter import *
from tkinter import filedialog
import re
from datetime import datetime


# 디렉토리 설정
def ask_directory():
    global dirName
    dirName = filedialog.askdirectory()
    print(dirName)


# 파일 이름 특수문자 제거
def clean_filename(filename):
    valid_chars = r"[^<>|:\\/\?*\"\/]"
    new_filename = "".join(re.findall(valid_chars, filename))

    new_filename = new_filename.replace("인스티즈", "")
    return new_filename


# 전체 구현 프로세스
def run():
    global dirName
    runBtn.config(state="disabled")
    today = datetime.now()
    formatted_today = today.strftime("%Y%m%d_%H%M%S")
    post = 0
    prefs = {
        "profile.managed_default_content_settings.stylesheets": 2,
    }

    os.environ['WDM_RUNTIME'] = os.path.dirname(sys.executable) + os.pathsep + os.environ['PATH']
    if hasattr(sys, '_MEIPASS'):
        os.environ['WDM_LOCAL'] = sys._MEIPASS
    else:
        os.environ['WDM_LOCAL'] = os.path.dirname(os.path.abspath(__file__))

    chromedriver_autoinstaller.install()
    options = Options()
    options.add_argument('--headless')
    options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(options=options)
    driver.set_window_size(1920, 1080)
    driver.implicitly_wait(10)

    urlLists = [urlEntry1.get(), urlEntry2.get(), urlEntry3.get(),
                urlEntry4.get(), urlEntry5.get(), urlEntry6.get(),
                urlEntry7.get(), urlEntry8.get(), urlEntry9.get(),
                urlEntry10.get(), urlEntry11.get(), urlEntry12.get(),
                urlEntry13.get(), urlEntry14.get(), urlEntry15.get(),
                urlEntry16.get(), urlEntry17.get(), urlEntry18.get(),
                urlEntry19.get(), urlEntry20.get()]

    print(urlLists)
    for urlList in urlLists:
        if not os.path.exists(formatted_today):
            if dirName:
                os.mkdir(dirName + '/' + formatted_today)
            else:
                os.mkdir(formatted_today)
        if urlList != '':
            r = requests.get(urlList)
            soup = BeautifulSoup(r.text, "html.parser")

            # div id="memo_content_1" 요소를 찾습니다.
            div_element = soup.find('div', {'id': 'memo_content_1'})
            title = soup.find('span', {'id': 'nowsubject'}).text
            fn, file_extension = os.path.splitext(title)
            safe_fn = clean_filename(fn)  # 폴더 구분자가 파일 이름에 포함된 경우, 대시(-)로 변경, 파일명

            # div 태그의 하위에 있는 모든 img,iframe 태그를 찾습니다.
            img_elements = div_element.find_all('img')
            vid_elements = div_element.find_all('iframe')

            # 이미지 다운로드
            for img_element in img_elements:
                post += 1
                src = img_element['src']
                _, ext = os.path.splitext(src)
                filename = str(post) + "_" + safe_fn + ext
                if dirName == None:
                    filepath = os.path.join(formatted_today, filename)
                else:
                    filepath = os.path.join(dirName, formatted_today, filename)

                try:
                    urllib.request.urlretrieve(src, filepath)
                except Exception as e:
                    print(f"Error downloading {src}: {e}")
                else:
                    pass

            # 영상 다운로드
            for vid_element in vid_elements:
                post += 1
                src = vid_element['src']
                if src.startswith("//"):
                    src = "https:" + src

                # Vimeo
                if re.search(r'player.vimeo.com/video', src):
                    video_id = re.search(r'(\d+)', src).group()
                    src = f'https://vimeo.com/{video_id}'

                # KakaoTV
                elif re.search(r'kakaotv.daum.net/embed', src):
                    video_id = re.search(r'rv[\w\W]+my', src).group()[:-3]
                    src = f'https://tv.kakao.com/channel/{video_id}'
                print(src)
                filename = str(post) + "_" + safe_fn + ".mp4"
                if dirName == None:
                    filepath = os.path.join(formatted_today, filename)
                else:
                    filepath = os.path.join(dirName, formatted_today, filename)
                try:
                    download_video(src, filepath)
                except Exception as e:
                    print(f"Error downloading {src}: {e}")



    runBtn.config(state="normal")
    msgbox.showinfo("Info", "작업이 완료되었습니다.")

def download_video(url, filepath):
    ydl_opts = {
        'format': 'best',
        'outtmpl': filepath,
        'verbos': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


# 값 비어있으면 에러메세지 + 스레드 실행
def validate_and_run():
    urlText = urlEntry1.get()

    if not urlText:
        msgbox.showerror("Error", "URL을 입력하세요.")
        return

    # 검색어와 파일 개수가 모두 입력되면 run 함수 실행
    t = threading.Thread(target=run, daemon=True)
    t.start()


if __name__ == "__main__":
    dirName = None
    shift_pressed = False
    count = 1

    fonts = ('맑은고딕', 13, 'bold')
    window = Tk()
    window.title("Tottoria_URL")
    window.geometry("1088x612")
    window.resizable(height=False, width=False)

    searchLabel = Label(window, text="URL", font=fonts)  # URL 라벨
    searchLabel.place(x=500, y=10)

    urlLabel1 = Label(window, text="1.", font=fonts)
    urlLabel1.place(x=20, y=80)
    urlEntry1 = Entry(width=55)
    urlEntry1.place(x=50, y=80)

    urlLabel2 = Label(window, text="2.", font=fonts)
    urlLabel2.place(x=20, y=110)
    urlEntry2 = Entry(width=55)
    urlEntry2.place(x=50, y=110)

    urlLabel3 = Label(window, text="3.", font=fonts)
    urlLabel3.place(x=20, y=140)
    urlEntry3 = Entry(width=55)
    urlEntry3.place(x=50, y=140)

    urlLabel4 = Label(window, text="4.", font=fonts)
    urlLabel4.place(x=20, y=170)
    urlEntry4 = Entry(width=55)
    urlEntry4.place(x=50, y=170)

    urlLabel5 = Label(window, text="5.", font=fonts)
    urlLabel5.place(x=20, y=200)
    urlEntry5 = Entry(width=55)
    urlEntry5.place(x=50, y=200)

    urlLabel6 = Label(window, text="6.", font=fonts)
    urlLabel6.place(x=20, y=230)
    urlEntry6 = Entry(width=55)
    urlEntry6.place(x=50, y=230)

    urlLabel7 = Label(window, text="7.", font=fonts)
    urlLabel7.place(x=20, y=260)
    urlEntry7 = Entry(width=55)
    urlEntry7.place(x=50, y=260)

    urlLabel8 = Label(window, text="8.", font=fonts)
    urlLabel8.place(x=20, y=290)
    urlEntry8 = Entry(width=55)
    urlEntry8.place(x=50, y=290)

    urlLabel9 = Label(window, text="9.", font=fonts)
    urlLabel9.place(x=20, y=320)
    urlEntry9 = Entry(width=55)
    urlEntry9.place(x=50, y=320)

    urlLabel10 = Label(window, text="10.", font=fonts)
    urlLabel10.place(x=20, y=350)
    urlEntry10 = Entry(width=55)
    urlEntry10.place(x=50, y=350)

    urlLabel11 = Label(window, text="11.", font=fonts)
    urlLabel11.place(x=550, y=80)
    urlEntry11 = Entry(width=55)
    urlEntry11.place(x=580, y=80)

    urlLabel12 = Label(window, text="12.", font=fonts)
    urlLabel12.place(x=550, y=110)
    urlEntry12 = Entry(width=55)
    urlEntry12.place(x=580, y=110)

    urlLabel13 = Label(window, text="13.", font=fonts)
    urlLabel13.place(x=550, y=140)
    urlEntry13 = Entry(width=55)
    urlEntry13.place(x=580, y=140)

    urlLabel14 = Label(window, text="14.", font=fonts)
    urlLabel14.place(x=550, y=170)
    urlEntry14 = Entry(width=55)
    urlEntry14.place(x=580, y=170)

    urlLabel15 = Label(window, text="15.", font=fonts)
    urlLabel15.place(x=550, y=200)
    urlEntry15 = Entry(width=55)
    urlEntry15.place(x=580, y=200)

    urlLabel16 = Label(window, text="16.", font=fonts)
    urlLabel16.place(x=550, y=230)
    urlEntry16 = Entry(width=55)
    urlEntry16.place(x=580, y=230)

    urlLabel17 = Label(window, text="17.", font=fonts)
    urlLabel17.place(x=550, y=260)
    urlEntry17 = Entry(width=55)
    urlEntry17.place(x=580, y=260)

    urlLabel18 = Label(window, text="18.", font=fonts)
    urlLabel18.place(x=550, y=290)
    urlEntry18 = Entry(width=55)
    urlEntry18.place(x=580, y=290)

    urlLabel19 = Label(window, text="19.", font=fonts)
    urlLabel19.place(x=550, y=320)
    urlEntry19 = Entry(width=55)
    urlEntry19.place(x=580, y=320)

    urlLabel20 = Label(window, text="20.", font=fonts)
    urlLabel20.place(x=550, y=350)
    urlEntry20 = Entry(width=55)
    urlEntry20.place(x=580, y=350)

    runBtn = Button(window, text="실행", height=3, width=20, relief="ridge", command=validate_and_run)  # 실행 버튼
    runBtn.place(x=450, y=500)

    dirBtn = Button(window, text="폴더 선택", relief="ridge", command=ask_directory)
    dirBtn.place(x=700, y=500)

    window.mainloop()
