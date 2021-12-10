import scrapy
import re
import json
from scrapy.http import HtmlResponse
from urllib.parse import urlencode
from items import InstaparserItem
from copy import deepcopy


class InstagramSpider(scrapy.Spider):
    name = 'instagram'
    allowed_domains = ['instagram.com']
    start_urls = ['https://www.instagram.com/']
   
    inst_login_link = '	https://www.instagram.com/accounts/login/ajax/'
    inst_login = 'test_sergucho'
    inst_pwd = '#PWD_INSTAGRAM_BROWSER:10:1639091012:AcJQACF9RZbj8ti+j/crQrUKVadFDb4Z4LqLGM3rPituGXM8eUTTzIv05RHjS5b+HDtEM6lHLCqmZEdBJYxgfMise+071Sw6i6PKY8eIll3gD+StEpA6ajR5aX6eU0uZygeO4tjEs7pTCDSxShew'
   
    users = ['ufimskiy_anonimus_offical', 'funny_cobra_16', 'olega6848']

    def __init__(self, status):
        """
        Args:
            status ([str]): [followers or following]
        """
        super().__init__()
        self.status = status
    
    def parse(self, response: HtmlResponse):
        csrf = self.fetch_csrf_token(response.text)
        yield scrapy.FormRequest(self.inst_login_link, method='POST', callback=self.login,
                                 formdata={'username': self.inst_login,
                                           'enc_password': self.inst_pwd},
                                 headers={'X-CSRFToken': csrf})


    def login(self, response: HtmlResponse):
        j_data = response.json()
        if j_data.get('authenticated'):
            for user in self.users:
                yield response.follow(f'/{user}', callback=self.user_start,
                    cb_kwargs={'username': user})
            
    def user_start(self, response:HtmlResponse, username):
        user_id = self.fetch_user_id(response.text, username)
        url_user_followers = f'https://i.instagram.com/api/v1/friendships/{user_id}/{self.status}/?count=12&search_surface=follow_list_page'

        yield response.follow(url_user_followers, callback=self.user_parse,
                              cb_kwargs={'username': username,
                                         'user_id': user_id,},
                              headers={'User-Agent': 'Instagram 155.0.0.37.107'})
    
    
    def user_parse(self, response:HtmlResponse, username, user_id):
        j_data = response.json()
        next_max_id = j_data.get('next_max_id')
        if next_max_id:
            url_user_followers = f'https://i.instagram.com/api/v1/friendships/{user_id}/{self.status}/?count=12&max_id={next_max_id}&search_surface=follow_list_page'
            yield response.follow(url_user_followers, callback=self.user_parse,
                                  cb_kwargs={'username': username,
                                             'user_id': user_id},
                                  headers={'User-Agent': 'Instagram 155.0.0.37.107'})
       
        followers = j_data.get('users') 
   
        for follower in followers:
            item = InstaparserItem(
                user_id=follower.get('pk'),
                username=follower.get('username'),
                photo=follower.get('profile_pic_url'),
                target_id = user_id,
                target_name = username,
                status=self.status
            )
            yield item
        
        
    def fetch_csrf_token(self, text):
        ''' Get csrf-token for auth '''
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')

    def fetch_user_id(self, text, username):
        matched = re.search(
            '{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text
        ).group()
        return json.loads(matched).get('id')
    