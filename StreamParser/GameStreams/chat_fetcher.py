import json
import os

from GameStreams.analyzer import statistics
from GameStreams.controllers import save_form
from StreamParser.settings import MEDIA_ROOT, STATIC_ROOT
from selenium.common.exceptions import NoSuchWindowException, NoSuchAttributeException, \
    NoSuchElementException
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options


# from twitchstream.chat import TwitchChatStream


def save_to_json(data, folder='root', filename=''):
    if not os.path.exists(MEDIA_ROOT + '/' + folder):
        os.makedirs(MEDIA_ROOT + '/' + folder)

    with open('{}/{}/{}.json'.format(MEDIA_ROOT, folder, filename), 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)


def youtube_scraper(url):
    options = Options()
    options.add_extension('{}/extension_3_8_4_0.crx'.format(STATIC_ROOT))  # AdBlock for Chrome
    browser = Chrome(executable_path=os.path.abspath('GameStreams/chromedriver/bin/chromedriver'),
                     chrome_options=options)

    browser.get(url)
    browser.implicitly_wait(7)

    channel_name = browser.find_element_by_class_name('ytd-channel-name').text
    video_name = browser.find_element_by_css_selector('.title.ytd-video-primary-info-renderer').text
    video_folder = '{}_{}'.format(channel_name, video_name)
    print('Video: {}'.format(video_folder))

    time_current = browser.find_element_by_class_name('ytp-time-current').get_attribute('innerText')
    video_duration = browser.find_element_by_class_name('ytp-time-duration').get_attribute('innerText')
    print('Current: {}'.format(time_current))
    print('Duration: {}'.format(video_duration))

    if browser.find_element_by_class_name('ytp-play-button').get_attribute('title') == 'Смотреть (k)':
        browser.find_element_by_class_name('ytp-play-button').click()

    if browser.find_element_by_class_name('ytp-mute-button').get_attribute('title') == 'Отключение звука (m)':
        browser.find_element_by_class_name('ytp-mute-button').click()

    # fetching subtitiles
    print('Chromedriver: Fetching subtitles and chat messages...')
    browser.find_element_by_class_name('ytp-subtitles-button').click()
    sub_json = {}
    chat_json = {}
    while time_current != video_duration:
        try:
            # fetching subtitles
            browser.switch_to.default_content()
            time_current = browser.find_element_by_class_name('ytp-time-current').get_attribute('innerText')
            subtitle = browser.find_element_by_class_name('ytp-caption-segment').get_attribute('innerText')

            if time_current not in sub_json:
                sub_json[time_current] = subtitle

            # fetch chat messages once in 5 seconds
            if int(time_current.split(':')[-1]) % 5 == 0:
                browser.switch_to.frame('chatframe')
                for item in browser.find_elements_by_css_selector('yt-live-chat-text-message-renderer'):
                    # author_name = item.find_element_by_id('author-name').get_attribute('innerText')
                    timestamp = item.find_element_by_id('timestamp').get_attribute('innerText')
                    message = item.find_element_by_id('message').get_attribute('innerText')

                    if timestamp not in chat_json:
                        chat_json[timestamp] = message
        except (NoSuchWindowException, NoSuchAttributeException, NoSuchElementException) as e:
            print('Error: {}'.format(e))
            break
        except Exception as e:
            print('Error: {}'.format(e))

    browser.quit()

    # saving subtitles to file
    sub_file_name = 'subtitles'
    save_to_json(sub_json, folder=video_folder, filename=sub_file_name)

    # saving chat messages to file
    chat_file_name = 'chat'
    save_to_json(chat_json, folder=video_folder, filename=chat_file_name)

    # make word analysis
    statistics(folder=video_folder, filename=chat_file_name)
    statistics(folder=video_folder, filename=sub_file_name)

    # saving stream info to DB
    save_form(url=url, folder=video_folder, duration=video_duration, channel=channel_name, name=video_name)

# def twitch_scraper():
#     with open('{}/config.json'.format(MEDIA_ROOT), 'r', encoding='utf-8') as f:
#         config = json.load(f)  # type: dict
#
#     # Launch a verbose (!) twitch stream
#     with TwitchChatStream(username=config['username'],
#                           oauth=config['oauth'],
#                           verbose=True) as chatstream:
#
#         # Continuously check if messages are received (every ~10s)
#         # This is necessary, if not, the chat stream will close itself
#         # after a couple of minutes (due to ping messages from twitch)
#         received = []
#         while True:
#             message = chatstream.twitch_receive_messages()
#             if message:
#                 print("message:", message)
#                 received.append(message)
#             time.sleep(1)
#     return received
