import datetime
from newsdataapi import NewsDataApiClient
from django.shortcuts import get_object_or_404

from block.models import *
from core.models import User



def finance_post():
      api = NewsDataApiClient(apikey="pub_14763965a946ce477ec7b9d12746e1e0c5adf")
      query = "Finance"
      username = "pyramid"
      pk = 11
      news = api.news_api(q=query, language="en")
      block = get_object_or_404(Block, id=pk)
      author = get_object_or_404(User, username=username)
      for key, value in news.items():
         if key == 'results':
            if value[0]['content'] != None: #Create text post
               Post.objects.create(
                     title=value[0]['title'],
                     text=value[0]['content'],
                     author=author,
                     block=block,
                     post_type="text",
                  )
            if value[3]['link'] != None: #Create link post
               Post.objects.create(
                     title=value[3]['title'],
                     link=value[3]['link'],
                     author=author,
                     block=block,
                     post_type="link",
                  )                          
            if value[4]['content'] != None: #Create text post
               Post.objects.create(
                     title=value[4]['title'],
                     text=value[4]['content'],
                     author=author,
                     block=block,
                     post_type="text",
                  )                 
            if value[7]['link'] != None: #Create link post 
               Post.objects.create(
                     title=value[7]['title'],
                     link=value[7]['link'],
                     author=author,
                     block=block,
                     post_type="link",
                  )
            if value[9]['link'] != None: #Create link post       
               Post.objects.create(
                     title=value[9]['title'],
                     link=value[9]['link'],
                     author=author,
                     block=block,
                     post_type="link",
                  )
         else: 
            pass     


def crypto_post():
      api = NewsDataApiClient(apikey="pub_14763965a946ce477ec7b9d12746e1e0c5adf")
      query = "Cryptocurrency"
      username = "lesleyasah3"
      pk = 1
      news = api.news_api(q=query, language="en")
      block = get_object_or_404(Block, id=pk)
      author = get_object_or_404(User, username=username)
      for key, value in news.items():
         if key == 'results':
            if value[0]['content'] != None: #Create text post
               Post.objects.create(
                     title=value[0]['title'],
                     text=value[0]['content'],
                     author=author,
                     block=block,
                     post_type="text",
                  )
            if value[3]['link'] != None: #Create link post
               Post.objects.create(
                     title=value[3]['title'],
                     link=value[3]['link'],
                     author=author,
                     block=block,
                     post_type="link",
                  )                          
            if value[4]['content'] != None: #Create text post
               Post.objects.create(
                     title=value[4]['title'],
                     text=value[4]['content'],
                     author=author,
                     block=block,
                     post_type="text",
                  )                
            if value[7]['link'] != None: #Create link post 
               Post.objects.create(
                     title=value[7]['title'],
                     link=value[7]['link'],
                     author=author,
                     block=block,
                     post_type="link",
                  )
            if value[9]['link'] != None: #Create link post       
               Post.objects.create(
                     title=value[9]['title'],
                     link=value[9]['link'],
                     author=author,
                     block=block,
                     post_type="link",
                  )
         else: 
            pass


def stock_post():
      api = NewsDataApiClient(apikey="pub_14763965a946ce477ec7b9d12746e1e0c5adf")
      query = "Stocks"
      username = "davidandefikir1"
      pk = 7
      news = api.news_api(q=query, language="en")
      block = get_object_or_404(Block, id=pk)
      author = get_object_or_404(User, username=username)
      for key, value in news.items():
         if key == 'results':
            if value[0]['content'] != None: #Create text post
               Post.objects.create(
                     title=value[0]['title'],
                     text=value[0]['content'],
                     author=author,
                     block=block,
                     post_type="text",
                  )
            if value[3]['link'] != None: #Create link post
               Post.objects.create(
                     title=value[3]['title'],
                     link=value[3]['link'],
                     author=author,
                     block=block,
                     post_type="link",
                  )                          
            if value[4]['content'] != None: #Create text post
               Post.objects.create(
                     title=value[4]['title'],
                     text=value[4]['content'],
                     author=author,
                     block=block,
                     post_type="text",
                  )                
            if value[7]['link'] != None: #Create link post 
               Post.objects.create(
                     title=value[7]['title'],
                     link=value[7]['link'],
                     author=author,
                     block=block,
                     post_type="link",
                  )
            if value[9]['link'] != None: #Create link post       
               Post.objects.create(
                     title=value[9]['title'],
                     link=value[9]['link'],
                     author=author,
                     block=block,
                     post_type="link",
                  )
         else: 
            pass


def real_estate_post():
      api = NewsDataApiClient(apikey="pub_14763965a946ce477ec7b9d12746e1e0c5adf")
      query = "Real estate"
      username = "pyramid"
      pk = 4
      news = api.news_api(q=query, language="en")
      block = get_object_or_404(Block, id=pk)
      author = get_object_or_404(User, username=username)
      for key, value in news.items():
         if key == 'results':
            if value[0]['content'] != None: #Create text post
               Post.objects.create(
                     title=value[0]['title'],
                     text=value[0]['content'],
                     author=author,
                     block=block,
                     post_type="text",
                  )
            if value[3]['link'] != None: #Create link post
               Post.objects.create(
                     title=value[3]['title'],
                     link=value[3]['link'],
                     author=author,
                     block=block,
                     post_type="link",
                  )                          
            if value[4]['content'] != None: #Create text post
               Post.objects.create(
                     title=value[4]['title'],
                     text=value[4]['content'],
                     author=author,
                     block=block,
                     post_type="text",
                  )                
            if value[7]['link'] != None: #Create link post 
               Post.objects.create(
                     title=value[7]['title'],
                     link=value[7]['link'],
                     author=author,
                     block=block,
                     post_type="link",
                  )
            if value[9]['link'] != None: #Create link post       
               Post.objects.create(
                     title=value[9]['title'],
                     link=value[9]['link'],
                     author=author,
                     block=block,
                     post_type="link",
                  )
         else: 
            pass


def forex_post():
      api = NewsDataApiClient(apikey="pub_14763965a946ce477ec7b9d12746e1e0c5adf")
      query = "Forex"
      username = "lesleyasah3"
      pk = 12
      news = api.news_api(q=query, language="en")
      block = get_object_or_404(Block, id=pk)
      author = get_object_or_404(User, username=username)
      for key, value in news.items():
         if key == 'results':
            if value[0]['content'] != None: #Create text post
               Post.objects.create(
                     title=value[0]['title'],
                     text=value[0]['content'],
                     author=author,
                     block=block,
                     post_type="text",
                  )
            if value[3]['link'] != None: #Create link post
               Post.objects.create(
                     title=value[3]['title'],
                     link=value[3]['link'],
                     author=author,
                     block=block,
                     post_type="link",
                  )                          
            if value[4]['content'] != None: #Create text post
               Post.objects.create(
                     title=value[4]['title'],
                     text=value[4]['content'],
                     author=author,
                     block=block,
                     post_type="text",
                  )                
            if value[7]['link'] != None: #Create link post 
               Post.objects.create(
                     title=value[7]['title'],
                     link=value[7]['link'],
                     author=author,
                     block=block,
                     post_type="link",
                  )
            if value[9]['link'] != None: #Create link post       
               Post.objects.create(
                     title=value[9]['title'],
                     link=value[9]['link'],
                     author=author,
                     block=block,
                     post_type="link",
                  )
         else: 
            pass


def economy_post():
      api = NewsDataApiClient(apikey="pub_14763965a946ce477ec7b9d12746e1e0c5adf")
      query = "World Economy"
      username = "pyramid"
      pk = 11
      news = api.news_api(q=query, language="en")
      block = get_object_or_404(Block, id=pk)
      author = get_object_or_404(User, username=username)
      for key, value in news.items():
         if key == 'results':
            if value[0]['content'] != None: #Create text post
               Post.objects.create(
                     title=value[0]['title'],
                     text=value[0]['content'],
                     author=author,
                     block=block,
                     post_type="text",
                  )
            if value[3]['link'] != None: #Create link post
               Post.objects.create(
                     title=value[3]['title'],
                     link=value[3]['link'],
                     author=author,
                     block=block,
                     post_type="link",
                  )                          
            if value[4]['content'] != None: #Create text post
               Post.objects.create(
                     title=value[4]['title'],
                     text=value[4]['content'],
                     author=author,
                     block=block,
                     post_type="text",
                  )                
            if value[7]['link'] != None: #Create link post 
               Post.objects.create(
                     title=value[7]['title'],
                     link=value[7]['link'],
                     author=author,
                     block=block,
                     post_type="link",
                  )
            if value[9]['link'] != None: #Create link post       
               Post.objects.create(
                     title=value[9]['title'],
                     link=value[9]['link'],
                     author=author,
                     block=block,
                     post_type="link",
                  )
         else: 
            pass
