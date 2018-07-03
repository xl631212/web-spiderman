from urllib.request import urlopen
from link_finder import Linkfinder
from main import *


class Spider(object):
	
	# class varible
	project_name = ''
	base_url = ''
	domain_name = ''
	queue_file = ''
	crawled_file = 'Spider.crawled'
	queue = set()
	crawled = set()

	def __init__(self, project_name, base_url, domain_name):
		Spider.project_name = project_name
		Spider.base_url = base_url
		Spider.domain_name = domain_name
		Spider.queue_file = Spider.project_name + '/queue.txt'
		Spider.crawled_file = Spider.project_name + '/crawled.txt'
		self.boot(self)
		self.crawl_page('First Spider', Spider.base_url)

	@staticmethod	
	def boot(self):
		create_project_dir(Spider.project_name)
		create_data_file(Spider.project_name,Spider.base_url)
		Spider.queue = file_to_sets(Spider.queue_file)
		Spider.crawled = file_to_sets(Spider.crawled_file)
		
		print(Spider.queue)

	@staticmethod	
	def crawl_page(thread_name, page_url):
		
		if page_url not in Spider.crawled:
			print(thread_name + 'crawling' + page_url)
			print('Queue ' + str(len(Spider.queue)) + '| Crawled ' + str(len(Spider.crawled)))
			Spider.add_links_to_queue(Spider.gather_link(page_url))
			Spider.queue.remove(page_url)
			Spider.crawled.add(page_url)
			Spider.update_files()

	@staticmethod		
	def gather_link(page_url):
		html_string = ''
		try:
			repsonse = urlopen(page_url)
			if repsonse.getheader('Content-Type') == 'text/html':
				html_bytes = repsonse.read()
				html_string = html_bytes.decode('utf-8')

			finer = Linkfinder(Spider.base_url, page_url)
			finder.feed(html_string)
		except:
			print('ERROR: can not crawl page')
			return set()
		return finder.page_links()	

	@staticmethod
	def add_links_to_queue(links):
		for url in links:
			if url in Spider.queue:
				continue
			if url in Spider.crawled:
				continue
			if Spider.domain_name not in url:
				continue
			Spider.queue.add(url)
			
	@staticmethod
	def update_files():
		set_to_file(Spider.queue, Spider.queue_file)
		set_to_file(Spider.crawled, Spider.crawled_file)								

