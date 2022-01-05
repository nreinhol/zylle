from django.contrib.auth.models import User
from datetime import timezone
import json

from .models import Post


FISH_DICT = {'Barsch': 2, 'Hecht': 1, 'Zander': 1.3}
COMPETITION_YEAR = "2022"
MONTH_MAPPING = {
    1: "Jan",
    2: "Feb",
    3: "Mär",
    4: "Apr",
    5: "Mai",
    6: "Jun",
    7: "Jul",
    8: "Aug",
    9: "Sep",
    10:"Okt",
    11: "Nov",
    12: "Dez"
}


def beautify_dates(date):
    '''Adds beginning zero to single-digit days and months'''
    if len(str(date)) == 1:
        return "0{}".format(date)
    else:
        return date


def get_all_userids_of_posts(request):
    '''Returns a list containing all distinct userids from postlist'''
    user_ids_tuple = list(Post.objects.values_list('author').distinct())
    return [ids_tuple[0] for ids_tuple in user_ids_tuple]


def get_username_of_userid(request, user_id):
    '''Returns the username of a given user id'''
    return User.objects.filter(id=user_id)[0].username


def get_all_posts(request):
    '''Returns all post objects'''
    return Post.objects


def get_all_posts_of_fish_type(request, fish_type):
    '''Returns all post objects of given fish type'''
    return Post.objects.filter(fish_type=fish_type)


def get_all_posts_of_year(request, year):
    '''Returns all post objects of a given year'''
    return Post.objects.filter(date_posted__year=year)


def get_len_of_all_posts_of_year(request, year):
    '''Returns the len of all post objects of a given year'''
    return len(get_all_posts_of_year(request, year))


def get_three_longest_fishes(request, user_id, fish_type, year):
    '''Returns the post objects of the three longest fishes of the given user id and fish type'''
    return Post.objects.filter(author=user_id).filter(fish_type=fish_type).filter(date_posted__year=year).order_by('-fish_length')[0:3]


def get_amount_all_fishes_of_user(request, user_id):
    '''Returns all post objects of user id sortet desc by fish lenght'''
    all_post_objects = Post.objects.filter(author=user_id).order_by('-fish_length')
    if all_post_objects:
        return len(all_post_objects)
    else:
        return "0"


def get_longest_fish_of_user(request, user_id):
    '''Returns the post object of the longest fish of user id'''
    all_post_objects = Post.objects.filter(author=user_id).order_by('-fish_length')
    longest_fish_dict = {"date": None, "type": None, "length": None}
    if all_post_objects:
        longest_fish = all_post_objects[0]
        longest_fish_dict["date"] = "{}.{}.{}".format(
            beautify_dates(longest_fish.date_posted.day),
            beautify_dates(longest_fish.date_posted.month),
            str(longest_fish.date_posted.year)[2:4]
        )
        longest_fish_dict["type"] = longest_fish.fish_type
        longest_fish_dict["length"] = "{}cm".format(longest_fish.fish_length)
    else:
        longest_fish_dict["date"] = "Der Tag wird kommen - Petri Heil!"
        longest_fish_dict["type"] = " - "
        longest_fish_dict["length"] = "0 cm"
    
    return longest_fish_dict


def get_all_fishes_of_fish_type(request, fish_type):
    '''Returns all post objects of the given fish type'''
    return Post.objects.filter(fish_type=fish_type)


def get_all_fishes_of_fish_type_from_user(request, user_id, fish_type):
    '''Returns all post objects of the given user id and fish type'''
    return Post.objects.filter(author=user_id).filter(fish_type=fish_type)


def get_beautified_three_longest_fishes(request, user_id, fish_type, year=COMPETITION_YEAR):
    '''Returns a beautified list of the three longest fishes of the given user id and fish type'''
    three_longest_fishes = get_three_longest_fishes(request, user_id, fish_type, year)
    fish_lengths = [fish.fish_length for fish in three_longest_fishes]
    no_entry = ['-'] * 3
    beautified_fish_lengths = fish_lengths + no_entry

    return beautified_fish_lengths[0:3]


def get_sum_of_fish_type(request, user_id, fish_type, year):
    '''Returns the sum of the three longest fishes of a given fish type'''
    three_longest_fishes = get_three_longest_fishes(request, user_id, fish_type, year)
    return sum([fish.fish_length for fish in three_longest_fishes])


def get_overall_score(request, user_id, year):
    '''Returns the sum of the sum of the three longest fishes for each fish type multiplied by his factors'''
    overall_score = sum([get_sum_of_fish_type(request, user_id, key, year) * FISH_DICT[key] for key in FISH_DICT])
    return float("{:.2f}".format(overall_score))


def get_ranking_list(request, year=COMPETITION_YEAR):
    '''Returns a dict with sorted usernames and the respective sorted scores'''
    user_ids = get_all_userids_of_posts(request)
    ranking = []
    for user_id in user_ids:
        username = get_username_of_userid(request, user_id)
        score = get_overall_score(request, user_id, year)
        ranking.append((username, score))

    # zip usernames und scores to tuples (username,score) and sort these tuples descending to score 
    sorted_ranking = sorted(ranking, key=lambda tup: tup[1], reverse=True)
    # get a list of the sorted usernames out of the tuples
    sorted_usernames = [rank[0] for rank in sorted_ranking]
    # get a list of the sorted scores out of the tuples
    sorted_scores = [rank[1] for rank in sorted_ranking]

    return {"usernames": sorted_usernames, "scores": sorted_scores}


def get_monthly_distribution_of_all_fishes_of_user(request, user_id):
    '''Returns a monthly distribution of all fish catches of a user'''
    total_monthly_distribution = {}
    for fish in FISH_DICT:
        total_monthly_distribution[fish] = get_monthly_distribution_of_fish_type_from_user(request, user_id, fish)
    
    return total_monthly_distribution


def get_monthly_distribution_of_fish_type_from_user(request, user_id, fish_type):
    '''Returns the monthly distribution of a given fish type of a user'''
    #initialize a dict with month as key and value 0
    monthly_distribution = dict.fromkeys(list(MONTH_MAPPING.values()), 0)
    for post in get_all_fishes_of_fish_type_from_user(request, user_id, fish_type):
        month = MONTH_MAPPING[post.date_posted.month]
        monthly_distribution[month] += 1
    
    return list(monthly_distribution.values())

### OVERALL STATISTICS ###

def get_longest_fishes(request):
    '''Returns a dict with the longest fish of each fish type'''
    all_posts = get_all_posts(request)
    longest_fishes = {}

    for fish in FISH_DICT:
        longest_fish = all_posts.filter(fish_type=fish).order_by('-fish_length')[0]
        longest_fish_dict = {"user": None, "date": None, "type": None, "length": None}

        longest_fish_dict["user"] = longest_fish.author.username
        longest_fish_dict["date"] = "{}.{}.{}".format(
            beautify_dates(longest_fish.date_posted.day),
            beautify_dates(longest_fish.date_posted.month),
            str(longest_fish.date_posted.year)[2:4]
        )
        longest_fish_dict["type"] = longest_fish.fish_type
        longest_fish_dict["length"] = "{}cm".format(longest_fish.fish_length)

        longest_fishes[fish] = longest_fish_dict
    
    return longest_fishes


def get_total_amount_of_fish_type(request):
    '''Returns a dict with the total amount of each fish type'''
    all_posts = get_all_posts(request)
    total_amount = {}

    for fish in FISH_DICT:
        total_amount[fish] = len(all_posts.filter(fish_type=fish))
    
    return total_amount


def get_monthly_distribution_of_all_fishes(request):
    '''Returns a monthly distribution of all fish catches'''
    total_monthly_distribution = {}
    for fish in FISH_DICT:
        total_monthly_distribution[fish] = get_monthly_distribution_of_fish_type(request, fish)
    
    return total_monthly_distribution


def get_monthly_distribution_of_fish_type(request, fish_type):
    '''Returns the monthly distribution of a given fish type'''
    #initialize a dict with month as key and value 0
    monthly_distribution = dict.fromkeys(list(MONTH_MAPPING.values()), 0)
    for post in get_all_fishes_of_fish_type(request, fish_type):
        month = MONTH_MAPPING[post.date_posted.month]
        monthly_distribution[month] += 1
    
    return list(monthly_distribution.values())


def get_date_length_of_all_fishes(request):
    '''Returns a dict with fish type as key and date length list as values'''
    date_length_dict = {}
    
    for fish in FISH_DICT:
        date_length_list = []
        all_posts = get_all_posts_of_fish_type(request, fish)
        for post in all_posts:
            post_list = []
            # transform datetime to milliseconds
            post_date = post.date_posted.replace(tzinfo=timezone.utc).timestamp() * 1000
            post_list.append(post_date)
            post_list.append(post.fish_length)
            post_list.append(get_username_of_userid(request, post.author.id))
            print(post_list)
            date_length_list.append(post_list)
        date_length_dict[fish] = date_length_list
    
    return date_length_dict
        
        
        



    



