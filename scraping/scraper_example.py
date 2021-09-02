# TODO import selenium
from bs4 import BeautifulSoup
from browser.browse import InteractiveBrowser

URL = "https://google.com/"

b = InteractiveBrowser(URL)
data = b.send_search(("name", "q"), "Python", ("class", 'LC20lb'))

for d in data:
    if "python" in d.text.lower():
        d.click()
        print(b.current_url())
        break


# opts = Options()
# opts.headless = True

# driver = webdriver.Chrome(ChromeDriverManager().install(), options=opts)
# driver.get(URL)

# search = driver.find_element_by_name("q")
# search.send_keys("Python")
# search.submit()

# results = driver.find_elements_by_class_name("LC20lb")
# results[0].click()

# soup = BeautifulSoup("page.content", "html.parser")

# names = soup.find_all(class_="gLFyf gsfi")

# window = tk.Tk()

# def find_text(text):
#     if not text:
#         return None
#     else:
#         return "Chapter" in text


# soup = BeautifulSoup(page.content, "html.parser")
# chapter_data = soup.find_all(dir="ltr")
# chapter_title = soup.find_all(
#     "h4", 
#     string=lambda text: find_text(text)
# )[0].text.strip().split(":")[-1]

# chapter_text = ""
# for data in chapter_data:
#     if data == chapter_data[-1]:
#         chapter_text += data.text
#     else:
#         chapter_text += f"{data.text}\n\n"

# generate_text_file(chapter_text, chapter_title)

# window.title(chapter_title)

# scroll = scrolledtext.ScrolledText(window, width=100, height=50, wrap=tk.WORD)
# scroll.pack()
# scroll.insert(tk.INSERT, chapter_text)

# window.mainloop()