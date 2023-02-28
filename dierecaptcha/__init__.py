import requests
import re

class dierecaptcha:
  def __init__(this):
    this._session = requests.Session()
    this._session.headers.update({"content-type": "application/x-www-form-urlencoded"})
    this._post_data = "v={}&reason=q&c={}&k={}&co={}"
    this._base = "https://www.google.com/recaptcha/"

  def token(this, _url: str):
    matched = re.findall("([api2|enterprise]+)\/anchor\?(.*)", _url)[0]
    this._base += matched[0] + "/"
    params = matched[1]
    res = this._session.get(
      this._base + "anchor", 
      params=params
    )
    token = re.findall(r'"recaptcha-token" value="(.*?)"', res.text)[0]
    params = dict(pair.split("=") for pair in params.split("&"))
    this._post_data = this._post_data.format(
      params["v"], 
      token, 
      params["k"], 
      params["co"]
    )
    res = this._session.post(
      this._base + "reload", 
      params=f'k={params["k"]}', 
      data=this._post_data
    )
    return re.findall(r'"rresp","(.*?)"', res.text)[0]
