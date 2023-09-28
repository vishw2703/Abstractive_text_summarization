from newspaper import Article


def get_text_article(link_of_website):
    url = link_of_website
    article = Article(url)
    article.download()
    article.parse()
    text_article = (article.text)
    
    return text_article