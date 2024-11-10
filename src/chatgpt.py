#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import requests

class ChatGPT(object):
    def __init__ (self, api_key, model="gpt-3.5-turbo", proxies=None):
        self.api_key = api_key
        self.model = model
        self.timeout = 300
        self.__verify = True

        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.api_key,
        }

        # TODO support proxy
        self.proxies = proxies

    def request(self, method, uri, headers=None, body=None):
        r = requests.request(method, uri, headers=headers, json=body,
                            timeout=self.timeout, verify=self.__verify, proxies=self.proxies)

        if r.status_code != 200:
            return sys.exit('response status is not 200: {}\nresponse body: {}'.format(r.status_code, r.text))

        response = r.json()

        choices = response.get('choices', [])
        usage = response.get('usage', {})
        total_tokens = usage.get('total_tokens', 0)

        return choices, total_tokens

    def ask_question(self, question):
        data = {
            'model': self.model,
            'messages': [
                {
                    "role": "user",
                    "content": question
                }
            ]
        }

        method = "POST"
        uri = "https://api.openai.com/v1/chat/completions"
        return self.request(method, uri, self.headers, data)
