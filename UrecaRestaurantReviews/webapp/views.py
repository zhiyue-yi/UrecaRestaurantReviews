# 1. Note
# Used to customize QuerySet objects to cater for web services
# Another alternative to consider will be Django RESTful framework
# Django RESTful framework allows rewrite for data serialization
# 2. Note 
# Used to perform queries on the database

# libraries
import webapp.models as model
from django.db import models
from django.db.models import Avg
import json
import decimal
import math

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        return super(DecimalEncoder, self).default(o)

class QueryManager:
    def topRatedDining(self):
        with connection.cursor() as cursor:
            # Restaurant
            cursor.execute("SELECT wd.id, wd.name, wd.imgurl, ws.loc as sub_loc, AVG(wr.score) as avg_score " + \
                        "FROM webapp_diningarea as wd " + \
                        "INNER JOIN webapp_review as wr ON wd.id = wr.dining_area_id " + \
                        "INNER JOIN webapp_diningsubarea as ws ON wd.sub_loc_id = ws.id " + \
                        "WHERE wd.dining_type='Restaurant'" + \
                        "GROUP BY wd.id, wd.name, ws.loc, wd.imgurl " + \
                        "ORDER BY avg_score DESC LIMIT 3;")
            columns = [col[0] for col in cursor.description]
            restaurant = [dict(zip(columns, row)) for row in cursor.fetchall()]

            # Food Court
            cursor.execute("SELECT wd.id, wd.name, wd.imgurl, ws.loc as sub_loc, AVG(wr.score) as avg_score " + \
                        "FROM webapp_diningarea as wd " + \
                        "INNER JOIN webapp_review as wr ON wd.id = wr.dining_area_id " + \
                        "INNER JOIN webapp_diningsubarea as ws ON wd.sub_loc_id = ws.id " + \
                        "WHERE wd.dining_type='Food Court' " + \
                        "GROUP BY wd.id, wd.name, ws.loc, wd.imgurl " + \
                        "ORDER BY avg_score DESC LIMIT 3;")
            columns = [col[0] for col in cursor.description]
            food_court = [dict(zip(columns, row)) for row in cursor.fetchall()]
        response = dict()
        response["restaurant"] = restaurant
        response["food_court"] = food_court

        for i in range(len(response["restaurant"])):
            response["restaurant"][i]["avg_score"] = math.ceil(response["restaurant"][i]["avg_score"])
            response["restaurant"][i]["score"] = list(range(response["restaurant"][i]["avg_score"]))
            response["restaurant"][i]["remainder_score"] = list(range(5 - response["restaurant"][i]["avg_score"]))
            del response["restaurant"][i]["avg_score"]
        
        for i in range(len(response["food_court"])):
            response["food_court"][i]["avg_score"] = math.ceil(response["food_court"][i]["avg_score"])
            response["food_court"][i]["score"] = list(range(response["food_court"][i]["avg_score"]))
            response["food_court"][i]["remainder_score"] = list(range(response["food_court"][i]["avg_score"]))
            del response["food_court"][i]["avg_score"]

        return response
    
    def search(self, search):
        with connection.cursor() as cursor:
            # Restaurant
            cursor.execute("SELECT wd.id, wd.name, wd.imgurl, ws.loc as sub_loc, AVG(wr.score) as avg_score " + \
                        "FROM webapp_diningarea as wd " + \
                        "INNER JOIN webapp_review as wr ON wd.id = wr.dining_area_id " + \
                        "INNER JOIN webapp_diningsubarea as ws ON wd.sub_loc_id = ws.id " + \
                        "INNER JOIN webapp_tag as wt ON wd.id = wt.dining_area_id " + \
                        "WHERE wt.name LIKE " + "%s" + " OR " + \
                        "ws.loc LIKE " + "%s" + " OR " + \
                        "wd.dining_type LIKE " + "%s" + " OR " + \
                        "wd.name LIKE " + "%s" + " " + \
                        "GROUP BY wd.id, wd.name, wd.imgurl, ws.loc " + \
                        "ORDER BY avg_score DESC;", ["%" + search + "%", "%" + search + "%", "%" + search + "%", "%" + search + "%"])
            columns = [col[0] for col in cursor.description]
            restaurant = [dict(zip(columns, row)) for row in cursor.fetchall()]

            for i in range(len(restaurant)):
                restaurant[i]["avg_score"] = math.ceil(restaurant[i]["avg_score"])
                restaurant[i]["score"] = list(range(restaurant[i]["avg_score"]))
                restaurant[i]["remainder_score"] = list(range(5 - restaurant[i]["avg_score"]))
                del restaurant[i]["avg_score"]
            return (restaurant) 
    
    def diningarea(self, diningarea):
        with connection.cursor() as cursor:
            # Restaurant info
            cursor.execute("SELECT wd.id, wd.name, wd.addr, wd.phone_no, wd.operating_hour, " + \
                        "wd.capacity, ws.loc as sub_loc, AVG(wr.score) as avg_score " + \
                        "FROM webapp_diningarea as wd " + \
                        "INNER JOIN webapp_review as wr ON wd.id = wr.dining_area_id " + \
                        "INNER JOIN webapp_diningsubarea as ws ON wd.sub_loc_id = ws.id " + \
                        "WHERE wd.id = %s", [str(diningarea)])
            columns = [col[0] for col in cursor.description]
            restaurant = [dict(zip(columns, row)) for row in cursor.fetchall()]
            restaurant = restaurant[0]

            # Assets
            cursor.execute("SELECT wa.url " + \
                        "FROM webapp_diningarea as wd " + \
                        "INNER JOIN webapp_diningareaassets as wa ON wd.id = wa.dining_area_id " + \
                        "WHERE wd.id = %s " + \
                        "ORDER BY wa.id DESC;", [str(diningarea)])
            columns = [col[0] for col in cursor.description]
            assetsDict = [dict(zip(columns, row)) for row in cursor.fetchall()]
            restaurant["assets"] = assetsDict
            restaurant["imgActive"] = restaurant["assets"][0]["url"]

            if (len(restaurant["assets"]) > 1):
                restaurant["assets"] = restaurant["assets"][1:]
            else:
                restaurant["assets"] = list()

            # Menu
            cursor.execute("SELECT wm.name, wm.price " + \
                        "FROM webapp_diningarea as wd " + \
                        "INNER JOIN webapp_menu as wm ON wd.id = wm.dining_area_id " + \
                        "WHERE wd.id = %s " + \
                        "ORDER BY wm.id DESC;", [str(diningarea)])
            columns = [col[0] for col in cursor.description]
            menuDict = [dict(zip(columns, row)) for row in cursor.fetchall()]
            restaurant["menu"] = menuDict

            # Review
            cursor.execute("SELECT wr.reviewer, wr.comment, wr.score " + \
                        "FROM webapp_diningarea as wd " + \
                        "INNER JOIN webapp_review as wr ON wd.id = wr.dining_area_id " + \
                        "WHERE wd.id = %s " + \
                        "ORDER BY wr.date DESC;", [str(diningarea)])
            columns = [col[0] for col in cursor.description]
            reviewDict = [dict(zip(columns, row)) for row in cursor.fetchall()]
            restaurant["review"] = reviewDict

            scoreCounter = [0, 0, 0, 0, 0]
            for i in range(len(restaurant["review"])):
                score = math.ceil(restaurant["review"][i]["score"])
                restaurant["review"][i]["star_score"] = list(range(score))
                restaurant["review"][i]["remainder_score"] = list(range(5 - score))
                scoreCounter[score - 1] = scoreCounter[score - 1] + 1
                del restaurant["review"][i]["score"]
            
            restaurant["totalReviewer"] = sum(scoreCounter)
            restaurant["poorReview"] = scoreCounter[0]
            restaurant["poorReviewPercent"] = str(scoreCounter[0] / restaurant["totalReviewer"] * 100) + "%"
            restaurant["belowReview"] = scoreCounter[1]
            restaurant["belowReviewPercent"] = str(scoreCounter[1] / restaurant["totalReviewer"] * 100) + "%"
            restaurant["avgReview"] = scoreCounter[2]
            restaurant["avgReviewPercent"] = str(scoreCounter[2] / restaurant["totalReviewer"] * 100) + "%"
            restaurant["aboveReview"] = scoreCounter[3]
            restaurant["aboveReviewPercent"] = str(scoreCounter[3] / restaurant["totalReviewer"] * 100) + "%"
            restaurant["excellentReview"] = scoreCounter[4]
            restaurant["excellentReviewPercent"] = str(scoreCounter[4] / restaurant["totalReviewer"] * 100) + "%"

            # Tag
            cursor.execute("SELECT wt.name " + \
                        "FROM webapp_diningarea as wd " + \
                        "INNER JOIN webapp_tag as wt ON wd.id = wt.dining_area_id " + \
                        "WHERE wd.id = %s " + \
                        "ORDER BY wt.id DESC;", [str(diningarea)])
            columns = [col[0] for col in cursor.description]
            tagDict = [dict(zip(columns, row)) for row in cursor.fetchall()]
            restaurant["tag"] = tagDict

            return (restaurant)

    def comment(self, comment): 
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO webapp_review (reviewer, comment, date, score, dining_area_id) " + \
                        "VALUES (%s, %s, %s, %s, %s)", [comment['name'], comment['feedback'], \
                        datetime.datetime.now(), comment['score'], comment['id']])

from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.core import serializers
from django.db import connection
import datetime

# View for webpages
def index(request):
    template = loader.get_template('webapp/index.html')
    contextResponse = QueryManager().topRatedDining()
    context = {
        "restaurants" : contextResponse["restaurant"],
        "food_courts" : contextResponse["food_court"]
    }
    return HttpResponse(template.render(context, request))

def search(request):
    template = loader.get_template('webapp/search.html')
    
    if ((request.GET.__contains__('q') is False)):
        queryString = ""
    else:
        queryString = request.GET['q'].strip()

    contextResponse = QueryManager().search(queryString)
    if (len(contextResponse) >= 0):
        context = {
            "q" : queryString,
            "results" : contextResponse
        }
    else:
        context = {
            "q" : queryString
        }
    return HttpResponse(template.render(context, request))

def loc(request, diningarea_id):
    template = loader.get_template('webapp/foodplace.html')
    contextResponse = QueryManager().diningarea(diningarea_id)
    context = {
        "restaurant" : contextResponse
    }
    return HttpResponse(template.render(context, request))

# View for web services (to be shifted to another application)
def toprated(request):
    return HttpResponse(json.dumps(QueryManager().topRatedDining(), cls=DecimalEncoder), content_type="application/json")

def diningarea(request):
    return HttpResponse(json.dumps(QueryManager().diningarea(1), cls=DecimalEncoder), content_type="application/json")

def menu(request):
    # DiningSubArea
    return HttpResponse(json.dumps(QueryManager().topRatedDining(), cls=DecimalEncoder), content_type="application/json")

def comment(request):
    QueryManager().comment(json.loads(request.body))
    return HttpResponse({"response" : "200"})