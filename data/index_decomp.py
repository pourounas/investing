import bs4
import requests
import logging

logger = logging.getLogger(name=__name__)


def sp_500():
    """
    Return S&P500 constituents from wikipedia
    """
    constituents = []
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    response = requests.get(url)
    soup = bs4.BeautifulSoup(markup=response.content, features='html.parser')
    table = soup.find(name="table", id="constituents").tbody.findAll("tr")
    # row 0 is the header, ignore it and start from row 1
    for row in table[1:]:
        # |Symbol|Security|SEC filings|GICS Sector|GICS Sub-Industry|Headquarters Location||Date first added|CIK|Founded|
        # text has traling \n i.e. 'ABT\n' so using rstrip() to remove \n
        ticker = row.find_next("td").text.rstrip()
        # if you want to get the date the constituent was added uncomment below
        # you will get a '1976-08-09'
        # dateAdded = row.find_all("td")[6].text
        constituents.append(ticker)
    return constituents


def _ftse(index):
    """
    Return constituents given a FTSE index from www.londonstockexchange.com
    """
    constituents = []
    url = f"https://www.londonstockexchange.com/indices/{index}/constituents/table"
    flag = True
    page = 1
    # website uses a paginator to only show x number of constituents at a time
    # couldn't find a smarter way to determine how many pages there are 
    # hence the while loop TODO:find a nice way to handle this
    while flag:
        response = requests.get(url, params={"page":page})
        soup = bs4.BeautifulSoup(markup=response.content, features='html.parser')
        table = soup.find(class_="full-width ftse-index-table-table").tbody.findAll("tr")
        if not table:
            # here we are probably at a page that does't have a table
            # i.e. page goes up to 13 and we asked for 14
            flag = False
            break
        for row in table:
            # |Code|Name|Currency|Market cap (m)|Price|Change|Change %|
            # ticker (code) is in the first column, hence the find_next td
            ticker = row.find_next("td").text
            constituents.append(ticker)
        page +=1
    return constituents


def ftse_250():
    constituents = _ftse("ftse-250")
    return constituents


def ftse_100():
    constituents = _ftse("ftse-100")
    return constituents


if __name__ == "__main__":
    ftse_100()
    sp_500()