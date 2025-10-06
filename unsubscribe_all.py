#!/usr/bin/env python3
"""
YouTube 구독 채널 자동 해제 프로그램
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import sys


class YouTubeUnsubscriber:
    def __init__(self):
        """Chrome 드라이버 초기화"""
        print("Chrome 드라이버를 초기화하는 중...")
        options = webdriver.ChromeOptions()
        options.add_argument('--start-maximized')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)

        # 사용자 데이터 디렉토리 사용 (이미 로그인된 Chrome 프로필 사용)
        # options.add_argument('user-data-dir=C:/Users/admin/AppData/Local/Google/Chrome/User Data')
        # options.add_argument('profile-directory=Default')

        try:
            # Chrome 드라이버를 자동으로 찾거나 시스템에 설치된 것을 사용
            self.driver = webdriver.Chrome(options=options)
        except Exception as e:
            print(f"Chrome 드라이버 초기화 실패: {e}")
            print("\n해결 방법:")
            print("1. Chrome 브라우저가 설치되어 있는지 확인하세요")
            print("2. ChromeDriver를 수동으로 다운로드하여 PATH에 추가하세요")
            print("   다운로드: https://chromedriver.chromium.org/downloads")
            sys.exit(1)

        self.wait = WebDriverWait(self.driver, 10)

    def login_prompt(self):
        """사용자에게 수동 로그인 안내"""
        print("\n" + "="*60)
        print("YouTube에 로그인해주세요")
        print("="*60)
        print("1. 브라우저가 열리면 YouTube에 로그인하세요")
        print("2. 로그인이 완료되면 이 터미널로 돌아와서 Enter를 누르세요")
        print("="*60)

        self.driver.get("https://www.youtube.com")
        input("\n로그인 완료 후 Enter를 누르세요...")

    def go_to_subscriptions(self):
        """구독 관리 페이지로 이동"""
        print("\n구독 관리 페이지로 이동 중...")
        self.driver.get("https://www.youtube.com/feed/channels")
        time.sleep(3)

    def scroll_to_load_all(self):
        """모든 구독 채널을 로드하기 위해 스크롤"""
        print("\n모든 구독 채널을 로드하는 중...")
        last_height = self.driver.execute_script("return document.documentElement.scrollHeight")

        while True:
            # 페이지 끝까지 스크롤
            self.driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
            time.sleep(2)

            # 새로운 높이 계산
            new_height = self.driver.execute_script("return document.documentElement.scrollHeight")

            if new_height == last_height:
                break
            last_height = new_height

        print("모든 채널 로드 완료!")

    def unsubscribe_all(self):
        """모든 구독 채널 해제"""
        print("\n구독 해제를 시작합니다...")

        unsubscribed_count = 0
        failed_count = 0

        while True:
            try:
                # 구독 중 버튼 찾기
                # ytd-subscription-notification-toggle-button-renderer-next 또는
                # ytd-subscription-notification-toggle-button-renderer 내부의 button
                subscribe_buttons = self.driver.find_elements(
                    By.CSS_SELECTOR,
                    'ytd-subscription-notification-toggle-button-renderer-next button, ytd-subscription-notification-toggle-button-renderer button'
                )

                if not subscribe_buttons or len(subscribe_buttons) == 0:
                    print(f"\n더 이상 구독 채널을 찾을 수 없습니다.")
                    break

                # 첫 번째 구독 버튼 선택
                subscribe_button = subscribe_buttons[0]

                # 버튼이 보이도록 스크롤
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", subscribe_button)
                time.sleep(0.5)

                # 채널 이름 가져오기
                try:
                    channel_name = subscribe_button.find_element(
                        By.XPATH,
                        './ancestor::ytd-channel-renderer//yt-formatted-string[@id="text"]'
                    ).text
                except:
                    channel_name = "알 수 없음"

                # 구독 중 버튼 클릭하여 메뉴 열기
                print(f"처리 중: {channel_name}")
                # JavaScript로 강제 클릭 시도
                try:
                    subscribe_button.click()
                except:
                    # 클릭이 안되면 JavaScript로 강제 클릭
                    self.driver.execute_script("arguments[0].click();", subscribe_button)
                time.sleep(1.5)

                # "구독 취소" 메뉴 항목 클릭
                # ytd-menu-service-item-renderer 내부의 tp-yt-paper-item 찾기
                try:
                    # 메뉴 항목의 부모 요소(클릭 가능한 항목) 찾기
                    unsubscribe_option = self.wait.until(
                        EC.element_to_be_clickable((
                            By.XPATH,
                            '//ytd-menu-service-item-renderer[.//yt-formatted-string[contains(text(), "구독 취소")]]//tp-yt-paper-item | //ytd-menu-service-item-renderer[.//yt-formatted-string[contains(text(), "Unsubscribe")]]//tp-yt-paper-item'
                        ))
                    )
                    # JavaScript로 클릭
                    self.driver.execute_script("arguments[0].click();", unsubscribe_option)
                    time.sleep(1)

                    # 확인 대화상자에서 "구독 취소" 버튼 클릭
                    # yt-confirm-dialog-renderer 내부의 마지막 button 찾기 (구독 취소 버튼)
                    try:
                        confirm_button = self.wait.until(
                            EC.presence_of_element_located((
                                By.XPATH,
                                '//yt-confirm-dialog-renderer//yt-button-renderer[last()]//button | //yt-confirm-dialog-renderer//button[@aria-label="구독 취소"] | //yt-confirm-dialog-renderer//button[@aria-label="Unsubscribe"]'
                            ))
                        )
                        # JavaScript로 확인 버튼 클릭
                        self.driver.execute_script("arguments[0].click();", confirm_button)
                        unsubscribed_count += 1
                        print(f"✓ 구독 해제 완료: {channel_name} (총 {unsubscribed_count}개)")
                        time.sleep(2)

                        # 페이지 새로고침하여 구독 목록 업데이트
                        print("페이지 새로고침 중...")
                        self.driver.refresh()
                        time.sleep(3)

                    except TimeoutException:
                        print(f"✗ 확인 버튼을 찾을 수 없음: {channel_name}")
                        failed_count += 1
                        # ESC 키를 눌러 대화상자 닫기
                        self.driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.ESCAPE)
                        time.sleep(0.5)

                except TimeoutException:
                    print(f"✗ 구독 취소 옵션을 찾을 수 없음: {channel_name}")
                    failed_count += 1
                    # ESC 키를 눌러 메뉴 닫기
                    self.driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.ESCAPE)
                    time.sleep(0.5)

            except Exception as e:
                print(f"오류 발생: {str(e)}")
                failed_count += 1
                if failed_count > 10:
                    print("\n오류가 너무 많이 발생했습니다. 프로그램을 종료합니다.")
                    break
                # ESC 키를 눌러 열린 메뉴/대화상자 닫기
                try:
                    self.driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.ESCAPE)
                except:
                    pass
                time.sleep(1)
                continue

        print(f"\n" + "="*60)
        print(f"구독 해제 완료!")
        print(f"총 구독 해제: {unsubscribed_count}개")
        print(f"실패: {failed_count}개")
        print("="*60)

    def run(self):
        """전체 프로세스 실행"""
        try:
            self.login_prompt()
            self.go_to_subscriptions()
            self.scroll_to_load_all()

            print("\n" + "="*60)
            confirm = input("정말로 모든 구독을 해제하시겠습니까? (yes/no): ")
            print("="*60)

            if confirm.lower() in ['yes', 'y', '예']:
                self.unsubscribe_all()
            else:
                print("\n작업이 취소되었습니다.")

        except KeyboardInterrupt:
            print("\n\n프로그램이 사용자에 의해 중단되었습니다.")
        except Exception as e:
            print(f"\n오류 발생: {str(e)}")
        finally:
            print("\n5초 후 브라우저를 닫습니다...")
            time.sleep(5)
            self.driver.quit()


def main():
    print("="*60)
    print("YouTube 구독 채널 자동 해제 프로그램")
    print("="*60)

    unsubscriber = YouTubeUnsubscriber()
    unsubscriber.run()


if __name__ == "__main__":
    main()
