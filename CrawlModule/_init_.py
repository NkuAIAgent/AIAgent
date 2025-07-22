from CrawlModule.PlayWright import get_page_source
from Data.main import main
from VectorDataBase.VectorStorage import storage

def crawl():
    code="19vzb0Umx38AyTVRnZI45ksawYgWH672"
    get_page_source("https://wechatrag.zeabur.app/dash",code)
    main()
    storage()
crawl()