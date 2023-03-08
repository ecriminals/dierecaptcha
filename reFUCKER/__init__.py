import requests
import re


class reFUCKER:
    """
    reFUCKER: Bypass Google reCAPTCHA challenges programmatically.
    """

    def __init__(self):
        """
        Initializes the reFUCKER instance.
        """
        self.session = requests.Session()
        self.session.headers.update({"content-type": "application/x-www-form-urlencoded"})
        self.post_data = "v={v}&reason=q&c={token}&k={k}&co={co}"
        self.base_url = "https://www.google.com/recaptcha/"

    def get_token(self, url: str) -> str:
        """
        Returns the response to the reCAPTCHA challenge given the URL of the page with the reCAPTCHA.

        Args:
            url (str): The URL of the page with the reCAPTCHA.

        Returns:
            str: The response to the reCAPTCHA challenge.
        """
        try:
            match = re.findall(r"([api2|enterprise]+)/anchor\?(.*)", url)[0]
        except IndexError:
            raise ValueError("Invalid URL")

        base_url = self.base_url + match[0] + "/"
        params = dict(pair.split("=") for pair in match[1].split("&"))

        try:
            response = self.session.get(base_url + "anchor", params=params)
            token = re.findall(r'"recaptcha-token" value="(.*?)"', response.text)[0]
        except (IndexError, requests.RequestException):
            raise ValueError("Failed to get reCAPTCHA token")

        try:
            post_data = self.post_data.format(v=params["v"], token=token, k=params["k"], co=params["co"])
            response = self.session.post(base_url + "reload", params=f'k={params["k"]}', data=post_data)
            rresp = re.findall(r'"rresp","(.*?)"', response.text)[0]
        except (IndexError, requests.RequestException):
            raise ValueError("Failed to solve reCAPTCHA challenge")

        return rresp
