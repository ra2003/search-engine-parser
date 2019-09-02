"""@desc 
		Base class inherited by every search engine
"""

from abc import ABCMeta, abstractmethod
import requests
from bs4 import BeautifulSoup


class BaseSearch(object):
    
    __metaclass__ = ABCMeta

    """
    Search base to be extended by search parsers
    Every subclass must have two methods `search` amd `parse_single_result`
    """
    # Summary of engine
    summary = None
    # Search Engine Name
    engine = None
    # Search Engine unformatted URL
    search_url = None

    def __init__(self, query, page=None):
        """ Initialize the Search Engine 
        
        :param query: the query to search for 
        :type query: str
        """
        # Clean query before storing it
        self.query = self.parse_query(query)

        # This should be redefined in every base class implementation
        self.search_url = None


    @abstractmethod
    def search(self, query, page=1):
        """
        Master method coordinating search parsing
        """
        raise NotImplementedError("subclasses must define method <search>")

    @abstractmethod
    def parse_single_result(self, single_result):
        """
        Every div/span containing a result is passed here to retrieve
        `title`, `link` and `descr`
        """
        raise NotImplementedError("subclasses must define method <parse_results>")
    
    def parse_result(self, results):
        """
        Runs every entry on the page through parse_single_result

        :param results: Result of main search to extract individual results
        :type results: list[`bs4.element.ResultSet`]
        :returns: dictionary. Containing titles, links and descriptions.
        :rtype: dict
        """
        titles = []
        links = []
        descs = []
        for each in results:
            title = link = desc = " "
            try:
                title, link, desc = self.parse_single_result(each)
                # Append links and text to a list
                titles.append(title)
                links.append(link)
                descs.append(desc)
            except Exception as e:
                print(e)
                pass
        search_results = {'titles': titles,
                          'links': links,
                          'descriptions': descs}
        return search_results
    
    @staticmethod
    def parse_query(query):
        """
        Replace spaces in query

        :param query: query to be processed
        :type query: str
        :rtype: str
        """
        return query.replace(" ", "%20")
    
    @staticmethod
    def getSource(url):
        """
        Returns the source code of a webpage.

        :rtype: string
        :param url: URL to pull it's source code
        :return: html source code of a given URL.
        """
        # headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:20.0) Gecko/20100101 Firefox/20.0'}
        # prevent caching
        headers = {
            "Cache-Control": 'no-cache',
            "Connection": "keep-alive",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"
        }
        try:
            response = requests.get(url, headers=headers)
            html = response.text
        except Exception as e:
            raise Exception('ERROR: {}\n'.format(e))
        return str(html)

    def get_soup(self):
        """
        Get the html soup of a query

        :rtype: `bs4.element.ResultSet`
        """
        html = self.getSource(self.search_url)
        return BeautifulSoup(html, 'lxml')
