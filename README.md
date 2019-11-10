# Surfshark-spider
A spider to get surfshark available server script for openvpn.



## Requirements

You need to install `python3` environment on your system. And install the following packages through `pip3`.

- requests
- time
- selenium
- beautifulsoup4
- os

And you need to download `firefox` driver for `selenium`. Place it under the current dir.

---

## Configuration

You need to edit the following variables in `Surfshark-spider.py`

- **usr**: user name for surfshark
- **passwd**: password for surfshark
- **download_path**: Path for saving `.ovpn` files
- (Optional) **login_url**: Url to login in surfshark, default is `https://account.sharky-china.com/login?locale=en`

---

## Run

Run with the following command.

```shell
python Surfshark-spider.py
```

The whole process will last for about 10 min.

---

## Issues

If you have any problems, you can try to comment the following lines in `Surfshark-spider.py` to show the firefox broswer to debug. And if you have any questions, please put forwards an issue, and I will try to help you.