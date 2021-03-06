from django.shortcuts import render, reverse
from posts.models import WalkthroughPost, QuestionPost
import requests
import json
# Create your views here.


def console_detail_view(request, id):
    url = 'https://api.rawg.io/api/platforms/' + str(id)
    headers={
        'User-Agent': 'Q4_Capstone',
    }
    payload={
        'key':'81ea352e06b54bb4b1218cb8d2b0e4eb',     
    }
    response = requests.get(url, headers=headers, params=payload)
    data = json.loads(response.text)
    console_name = data['name']
    console_slug = data['slug']
    console_img = data['image_background']
    console_desc = data['description'].replace('<p>', '').replace('</p>', '').replace('<br />', '').replace('&#39;', "'").replace('&quot;', '"')
    games_count = data['games_count']
    data = json.dumps(data, indent=2)
    context =  {'data': data, 'console_name':console_name, 'console_img': console_img, 'console_desc': console_desc, 'games_count':games_count, 'console_slug':console_slug ,'id':id}
    return render(request, 'console.html', context)


def console_games_view(request, console, page):
    if console == 'pc':
        id = 4
        console_name = 'PC'
    elif console == 'playstation5':
        id = 187
        console_name = 'Play Station 5'
    elif console == 'playstation4':
        id = 18
        console_name = 'Play Station 4'
    elif console == 'nintendo-switch':
        id = 7
        console_name = 'Nintendo Switch'
    elif console == 'xbox-one':
        id = 1
        console_name = 'XBOX ONE'
    elif console == 'xbox-series-x':
        id = 186
        console_name = 'XBOX SERIES S/X'
    url = 'https://api.rawg.io/api/games'
    headers={
        'User-Agent': 'Q4_Capstone',
    }
    payload={
        'key':'81ea352e06b54bb4b1218cb8d2b0e4eb',
        'platforms': id,
        'page': page
    }
    response = requests.get(url, headers=headers, params=payload)
    data = json.loads(response.text)
    game_list = []
    for game in data['results']:
        print(game['id'])
        game_obj = {
            'game_id': game['id'],
            'game_name': game['name'],
            'game_slug': game['slug'],
            'game_img': game['background_image']
        }
        game_list.append(game_obj)
    data = json.dumps(data, indent=2)
    next_page = int(page) + 1
    prev_page = int(page) - 1
    context =  {'next_page': next_page, 'prev_page': prev_page, 'data': data, 'id':id, 'game_list':game_list, 'console':console_name, 'console_slug': console}
    return render(request, 'console_all_games.html', context)

def game_detail(request, id):
    url = 'https://api.rawg.io/api/games/' + str(id)
    headers={
        'User-Agent': 'Q4_Capstone',
    }
    payload={
        'key':'81ea352e06b54bb4b1218cb8d2b0e4eb',
        'id': id      
    }
    response = requests.get(url, headers=headers, params=payload)
    data = json.loads(response.text)
    game_name = data['name']
    game_slug = data['slug']
    game_release = data['released']
    game_img = data['background_image']
    game_desc = data['description_raw'].replace('###', ' ')
    esrb_rating = ''
    if data['esrb_rating']:
        esrb_rating = data['esrb_rating']['name']
    platforms = []
    for platform in data['platforms']:
        print(platform['platform']['name'])
        platforms.append(platform['platform']['name'])
    platforms = ', '.join(platforms)
    data = json.dumps(data, indent=2)
    walkthroughs = WalkthroughPost.objects.filter(for_game=game_name)
    questions = QuestionPost.objects.filter(for_game=game_name)
    context = {'id': id, 'game_name': game_name, 'game_slug': game_slug, 'game_img': game_img, 'game_desc': game_desc, 'game_release': game_release, 'esrb_rating': esrb_rating, 'platforms': platforms, 'questions': questions, 'walkthroughs': walkthroughs}
    return render(request, 'game_detail.html', context)

def searchbar(request):  
    search = request.GET.get('search')
    print(search)
    url = 'https://api.rawg.io/api/games'
    headers={
        'User-Agent': 'Q4_Capstone',
    }
    payload={
        'key':'81ea352e06b54bb4b1218cb8d2b0e4eb',
        'search': search,
    }
    response = requests.get(url, headers=headers, params=payload)
    data = json.loads(response.text)
    count = data['count']
    game_list = []
    for game in data['results']:
        print(game['id'])
        game_obj = {
            'game_id': game['id'],
            'game_name': game['name'],
            'game_slug': game['slug'],
            'game_img': game['background_image']
        }
        game_list.append(game_obj)
    data = json.dumps(data['results'], indent=2)
    page = 1
    next_page = int(page) + 1
    prev_page = int(page) - 1
    context =  {'search': search, 'count':count, 'game_list': game_list, 'data': data, 'search':search, 'prev_page': prev_page,'next_page':next_page,}
    return render(request, 'search.html', context) 

def searchbar_page(request, search, page):
    
    url = 'https://api.rawg.io/api/games'
    headers={
    'User-Agent': 'Q4_Capstone',
}
    payload={
    'key':'81ea352e06b54bb4b1218cb8d2b0e4eb',
    'page': page, 
    'search': search,
}
    response = requests.get(url, headers=headers, params=payload)
    data = json.loads(response.text)
    count = data['count']
    game_list = []
    for game in data['results']:
        print(game['name'])
        game_obj = {
        'game_id': game['id'],
        'game_name': game['name'],
        'game_slug': game['slug'],
        'game_img': game['background_image']
    }
        game_list.append(game_obj)
    print(data['next'])
    data = json.dumps(data['results'], indent=2)
    next_page = int(page) + 1
    prev_page = int(page) - 1
    context = {'search':search,'count':count, 'game_list': game_list, 'data': data, 'search':search, 'prev_page': prev_page,'next_page':next_page,}
    return render(request, 'search.html', context) 
