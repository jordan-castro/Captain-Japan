from cj.objects.novel import Novel
from cj.scraper.novels.rnf import RNF
from cj.utils.save import Save


if __name__ == "__main__":
    rnf = RNF("MUSHOKU TENSEI")
    rnf.should_scroll = False
    rnf.should_wait = True
    rnf.wait_time = 10
    # Can not change the data above.
    rnf.can_change_scroll = False
    rnf.can_change_wait = False

    result = rnf.search()
    if result:
        rnf.load_chapters(result)
        cover = rnf.cover()
        # if cover:
        #     cover_box.configure(file=cover)
        # Get a chapters text
        chapter = rnf.scrape(rnf.chapters[15])

    rnf.driver.quit()

    novel = Novel(None, rnf.title, None, cover)
    save = Save(chapter, novel)
    save.save()
    print(novel.location)