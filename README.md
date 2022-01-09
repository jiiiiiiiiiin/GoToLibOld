# GoToLibOld

仅适配于 *我去图书馆 v2* 版本。**2021年暑期，\*我去图书馆\* 已经更新版本。**

## 使用说明

- 这里只提供相关函数，定时功能自己搞。

- 抓包得到cookie

  ```python
  cookie = "" # 在这里填入抓包得到的cookie
  ```

- 每五分钟来一个心跳包，确保cookie存活

  ``````python
  ret = rob(cookies=cookie, seats_expect=[], keep_alive=True)
  if len(ret) == 2:
      is_alive, seats = ret
  else:
      # cookie失效
      is_alive = False
  ``````

- 抢座

  ```python
  # rob seats 抢常用座位
  ret = rob(cookies=cookie, seats_expect=[], my_seats_first=True)
  ```

- 这个脚本很久以前写的了。新版本感谢ws大佬，暂不上传。