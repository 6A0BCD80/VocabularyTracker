from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
import requests
from bs4 import BeautifulSoup
import json
from django.template import loader
from .models import Word
from django.core import serializers

# Create your views here.

display_limit = 5
def next_page(request):

	current_page_text = request.POST['current_page']
	prev_page_text = request.POST['prev_page']

	current_page = int(current_page_text)
	prev_page = int(prev_page_text)

	if	prev_page <= 0:
		current_page = 5
		prev_page = 0

	if current_page <= 5:
		current_page = 5
		prev_page = 0

	all_kanjis = Word.objects.all()[prev_page:current_page]
	all_kanjis = reversed(all_kanjis)
	displayed_kanji = []

	for kanji in all_kanjis:
		new_kanji = {}
		new_kanji['kanji'] =  kanji.kanjis
		new_kanji['meaning'] = kanji.meaning
		new_kanji['kun'] = kanji.kun
		displayed_kanji.append(new_kanji)	
	

	#data = serializers.serialize('json', Word.objects.all(), fields=('id',))
	return JsonResponse(displayed_kanji,safe=False)

def index(request):
    all_kanjis = Word.objects.all()[0:display_limit]
    template = loader.get_template("index.html")
    context = {
        'all_kanjis': all_kanjis
    }

    return HttpResponse(template.render(context,request))

def word(request, word_id):
    return render(request,'word.html',{ 'word':word_id})

def search(request):
    all_kanjis = Word.objects.all()[0:display_limit]
    all_kanjis = reversed(all_kanjis)
    template = loader.get_template("index.html")
    context = {
        'all_kanjis': all_kanjis
    }

    return render(request,'search.html', context)

def searchjisho(request):
	keys = [];
	url = "https://www.jisho.org/search/"
	url += request.POST['word']
	resp = requests.get(url)

	soup = BeautifulSoup(resp.text,'html.parser')
	main_results_tag = soup.find(id='main_results')

	results = main_results_tag.find_all(class_='concept_light clearfix')

	for result in results:
		newKanji = {}
		furigana_tag = result.find(class_='furigana')
		text_tag = result.find(class_='text')

		if furigana_tag is not  None:
			newKanji['hirigana'] = furigana_tag.get_text()

			furigana_parts = furigana_tag.find_all('span')
			if furigana_parts is not None:
				furiganas = []
				for furigana_part in furigana_parts:
					furiganas.append(furigana_part.get_text())
				newKanji['furiganas'] = furiganas

		conceptLightStatus =result.find(class_='meanings-wrapper')
		meaningmeaning = conceptLightStatus.find(class_='meaning-meaning')

		newKanji['meaning'] = meaningmeaning.getText()
		if text_tag is not None:
			newKanji['kanji'] = text_tag.get_text()

		if text_tag is not None and furigana_tag is not None:
			keys.append(newKanji)

	jsonResult = json.dumps(keys)

	return HttpResponse(jsonResult  );
 
def addkanji(request):
	wrd = Word();
	wrd.kanjis = request.POST['kanji']
	wrd.meaning = request.POST['meaning']
	wrd.kun = request.POST['hirigana']
	wrd.save()
	return HttpResponse("added Kanji!")

def delkanji(request):
	kanjiID = request.POST['kanjiId']
	Word.objects.filter(id=kanjiID).delete()
	return HttpResponse("deleted Kanji!")
