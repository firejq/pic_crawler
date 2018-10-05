# Tuyimm Crawler

A image crawler for [tuyimm](http://www.tuyimm.vip/) 

Python 3.6

## Use

1. setup
    ```
    git clone https://github.com/firejq/pic_crawler.git
    ```
1. Install the dependences

    ```powershell
    pip install -r requirements.txt
    ```
1. Run the crawler script and then get all the images
    ```powershell
    python tuyimm_scraping.py [page_id]
    ```
  
    eg: For `http://www.tuyimm.vip/thread-16290-1-1.html`, page id is `16290`.

1. To modify the download path, you can edit the **tuyimm_scraping.ini**:
    ```
    [baseconf]
    download_path=YOUR_DOWNLOAD_PATH
    ```

## License

The tuyimm_crawler is under the [MIT](https://github.com/firejq/pic_crawler/blob/master/LICENSE) license.




