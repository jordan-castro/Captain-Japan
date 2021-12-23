from cj.scraper.novels.rnf import RNF


if __name__ == "__main__":
    rnf = RNF("THE BEGINNING AFTER THE END")

    result = rnf.search()
    print(result)
    if result:
        rnf.load_chapters(result)
        print(rnf.chapters)
        cover = rnf.cover()
        # if cover:
        #     cover_box.configure(file=cover)
        print(cover)
        # Get a chapters text
        chapter = rnf.scrape(0)

    rnf.driver.quit()