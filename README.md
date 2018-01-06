## Image Crawler


A image crawler for [mzitu](http://www.mzitu.com/, "mzitu") 

Python 3.6

## Use
1. setup
```
git clone https://github.com/firejq/mzitu_crawler.git
```
2. Install the dependences

```powershell
pip install -r requirements.txt
```
3. Run the crawler script and then get all the images in **D:\mzitu**
```powershell
python mzitu_scraping.py
```

4. To modify the download path, you can edit the **mzitu_scraping.ini**:
```
[baseconf]
download_path=YOUR_DOWNLOAD_PATH
```

## TODO
- [ ] 优化多线程下的程序中断


## Features
- [x] Dynamic IP Proxy   
- [x] Dynamic UserAgent  
- [x] Multitasking by Multi-Process and Multi-thread
- [x] Solve synchronize I/O block by Coroutines  

## License
The mzitu_crawler is under the [MIT](https://github.com/firejq/mzitu_crawler/blob/master/LICENSE) license.




