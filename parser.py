import json, re
from html.parser import HTMLParser


class Parser(HTMLParser):

    Data = {}

    def handle_data(self, data):
        if data.startswith("window._sharedData"):
            self.Data = json.loads(data[data.find('{"config"'): -1])
        else:
            pass


def get_account_type(data):
    if data['is_business_account']:
        return 'Business'
    elif data['is_professional_account']:
        return 'Professional'
    else:
        return 'Individual'


def get_tags(data):
    tags = []
    for obj in data['node']['edge_media_to_tagged_user']['edges']:
        tags.append('@{}'.format(obj['node']['user']['username']))
    return ','.join(tags)


def get_hashtags(caption):
    hashtags = []
    if caption:
        for obj in re.findall(r'#(\w+)', caption):
            hashtags.append('#{}'.format(obj))
        return ','.join(hashtags)
    return ''


def get_influencer(data):
    json_data = data['entry_data']['ProfilePage'][0]['graphql']['user']
    influencer = {
        'name': json_data['full_name'] if json_data['full_name'] else json_data['username'],
        'profile_pic': json_data['profile_pic_url'],
        'bio': json_data['biography'],
        'location': json_data['business_address_json'],
        'followers': json_data['edge_followed_by']['count'],
        'total_posts': json_data['edge_owner_to_timeline_media']['count'],
        'email': json_data['business_email'],
        'website': json_data['external_url'],
        'account_type': get_account_type(json_data),
        'verified': json_data['is_verified']
    }

    posts = []
    for obj in json_data['edge_owner_to_timeline_media']['edges']:
        caption = obj['node']['accessibility_caption']
        if obj['node'].get('edge_media_to_caption'):
            if obj['node']['edge_media_to_caption'].get('edges'):
                caption = obj['node']['edge_media_to_caption']['edges'][0]['node']['text']
        post = {
            'link': 'https://instagram.com/p/{}/'.format(obj['node']['shortcode']),
            'likes': obj['node']['edge_liked_by']['count'],
            'comments': obj['node']['edge_media_to_comment']['count'],
            'hashtags': get_hashtags(caption),
            'tags': get_tags(obj),
            'caption': caption
        }
        posts.append(post)
    influencer['posts'] = posts

    return influencer
