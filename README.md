# Bulk download ISPG conference videos

### 1. To extract all the videos links from the web page to a text file (using Day 2 as example)
```
python3 gen_info.py conference_websites/lobby_day2.html xxx@xxxxx.edu my_password > yt_links/day2_yt_links.txt
```

### 2. To donwload all the videos from the text file using x2converter (using Day 2 as example)
```
python3 x2convert.py yt_links/day2_yt_links.txt
```

### 3. To find the downloaded mp4 vidoes at ./my_mp4
```
ls my_mp4
```
