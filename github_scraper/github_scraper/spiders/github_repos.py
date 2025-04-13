import scrapy

class GithubReposSpider(scrapy.Spider):
    name = "github_repos"
    allowed_domains = ["github.com"]
    start_urls = ["https://github.com/goomaralggb?tab=repositories"]

    def parse(self, response):
        repo_links = response.css('h3 a::attr(href)').getall()
        for link in repo_links:
            full_link = response.urljoin(link)
            yield scrapy.Request(full_link, callback=self.parse_repo)

    def parse_repo(self, response):
        yield {
            'url': response.url,
            'about': response.css('p.f4::text').get(default='').strip(),
            'last_updated': response.css('relative-time::attr(datetime)').get(),
            'languages': response.css('span[itemprop=programmingLanguage]::text').getall(),
            'number_of_commits': response.css('li.commits a span::text').get()
        }
