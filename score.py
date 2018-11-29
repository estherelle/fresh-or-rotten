from bs4 import BeautifulSoup
import requests as rq 

# class that grabs Rotten Tomatoes scores and link to reviews page
class RTScore:

	# initialized to website of movie on Rotten Tomatoes
	def __init__(self, url):
		self.reviewUrl = ''
		self.set = False
		self.url = url
		self.page = rq.get(url).text
		self.soup = BeautifulSoup(self.page, 'lxml')

	# get the url for the first page of movie reviews
	def getReviewUrl(self):
		if not self.set:
			self.buildReviewUrl()
		return self.reviewUrl

	# Tomatometer score
	def criticScore(self):
		meter = "meter-value superPageFontColor"
		score = self.soup.find('span', {'class': meter})

		return score.text

	def audienceScore(self):
		audience_meter = "audience-score meter"
		audience_score = "superPageFontColor"

		meter = self.soup.find('div', {'class': audience_meter})
		score = meter.find('span', {'class': audience_score})

		return score.text

	# helper function for getting the review url
	def buildReviewUrl(self, set=False):
		if self.url[-1] != '/':
			self.url = self.url + '/'
		self.reviewUrl = self.url + "reviews/?type=user"
		return

# Audience Reviews inherits from RTScore
class AudienceReviews(RTScore):

	def __init__(self, url):
		RTScore.__init__(self, url)
		self.url = url
		self.paging = 0
		self.curSoup = self.getSoup() 
		self.nextPageUrl = url

	# to get the url of the next page
	def nextPage(self):

		paging = 'pageInfo'
		base_url = "https://www.rottentomatoes.com"
		page_section = self.curSoup.find('span', {'class': paging})
		next_page = ''
		# return page_section

		try:
			next_page = page_section.findNext('a', {'class': 'btn btn-xs btn-primary-rt'})['href']
		except:
			self.nextPageUrl = None
			return

		self.paging += 1
		self.nextPageUrl = base_url + next_page
		# print(self.nextPageUrl)
		return self.nextPageUrl

	def getReviews(self):
		reviews = self.curSoup.find('div', {'id': 'reviews'})
		cur = reviews.findNext('div', {'class': 'user_review'})

		review_list = []

		while cur:
			review_list.append(cur.text.strip())
			cur = cur.findNext('div', {'class': 'user_review'})
		return review_list

class TextReviews():

	def __init__(self, url, limit=1):
		self.page = AudienceReviews(url)
		self.limit = limit
		self.reviews = []


	# helper function to page for reviews, outputs as an array of reviews
	def getReviews(self):
		for i in range(self.limit):
			self.reviews += self.page.getReviews()
			next_page = self.page.nextPage()

			if next_page:
				self.page = AudienceReviews(next_page)
			else:
				break

		# return ''.join(self.reviews)
		return self.reviews









