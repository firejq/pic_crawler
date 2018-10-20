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
1. Run the crawler script
    ```powershell
    python tuyimm_scraping.py
    ```
  	And then input the thread_id of your target theme.

    eg: 
    - For `http://www.tuyimm.vip/thread-16290-1-1.html` thread_id is `16290`, so you can run `python tuyimm_scraping.py` and then input `16290`.
    - For `http://www.tuyimm.vip/thread-7071-1-2.html` thread_id is `7071-1-2`, so you can run `python tuyimm_scraping.py` and then input `7071-1-2`.
    - To exit, input `exit`.

1. To modify the download path, you can edit the **tuyimm_scraping.ini**:
    ```
    [baseconf]
    download_path=YOUR_DOWNLOAD_PATH
    ```

## License

The tuyimm_crawler is under the [MIT](https://github.com/firejq/pic_crawler/blob/master/LICENSE) license.




