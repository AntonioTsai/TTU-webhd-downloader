from requests import get, post
from bs4 import BeautifulSoup as bs
from configparser import ConfigParser as cp
import os

#read the config file
config = cp()
config.read("local.conf")
config = config["DEFAULT"]

WEBHD = "http://webhd1.ttu.edu.tw/"
SHARE_KEY = config["SHARE_KEY"]
SHARE_PWD = config["SHARE_PWD"]

LOGIN_DATA = {'sharekey': SHARE_KEY, 'Locale': 'zh-TW', 'Submit':'進入社群'}
INPUTPWD = {'inputpwd': SHARE_PWD, 'Sent':'送出'}

res = post(WEBHD + "share/sharehd.php", data=LOGIN_DATA)
res = post(WEBHD + "share/sharehd.php", data=INPUTPWD, cookies=res.cookies)
soup = bs(res.text, 'html5lib')
sel = soup.select('.cistab a')
os.mkdir(SHARE_KEY)
for link in sel:
	res = get(WEBHD + link['href'], cookies=res.cookies, stream=True)
	filename = res.headers['Content-Disposition'].encode('latin1', 'ignore').decode('big5')[9:]
	print("Saving " + filename)
	with open(SHARE_KEY + "/" + filename, 'wb') as file:
		for chunk in res:
			file.write(chunk)
		file.close()
	print("Done!")
print("Total Download: " + str(len(sel)) + " files.")
