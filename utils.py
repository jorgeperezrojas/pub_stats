import requests
import re
from bs4 import BeautifulSoup
import sys
import unidecode
from aka import known_dblp_aka

def get_after_author(soup):
    buttons = soup.find_all('button')
    if len(buttons) < 3:
        return None
    next_button = buttons[2]
    if not next_button.has_attr('onclick'):
        return None
    link_string = next_button['onclick']
    span = re.search('after_author', link_string).span()
    end = span[1]
    after_author = link_string[end+4:end+16]
    return after_author

def get_citation_count(author_div,cby_string):
    cit_class = 'gs_ai_cby'
    citation_count_div = author_div.find('div', {'class': cit_class})
    if citation_count_div == None:
        return 0
    citation_count_string = citation_count_div.text
    if citation_count_string == '':
        return 0
    else: 
        citation_count = int(citation_count_string[len(cby_string):])
        return citation_count

def get_author_info(author_div, cby_string='Citado por ', scholar_prefix='https://scholar.google.com'):
    aff_class = 'gs_ai_aff'
    topics = 'gs_ai_one_int'
    scholar_suffix = author_div.find('a')['href']
    scholar_url = scholar_prefix + scholar_suffix
    span_id = re.search('user=', scholar_suffix).span()
    end = span_id[1]
    scholar_id = scholar_suffix[end:]
    name = author_div.find('a').text
    aff = author_div.find('div', {'class': aff_class}).text
    citation_count = get_citation_count(author_div,cby_string)
    topics_div = author_div.find_all('a', {'class': topics})
    topics = [topic.text for topic in topics_div]

    info = {
        'scholar_id': scholar_id,
        'scholar_url': scholar_url,
        'name': name,
        'affiliation': aff,
        'citations': citation_count,
        'topics': topics,
    }
    return info

def check_email_authors(authors, check_email_string, verbose=True):
    len_check = len(check_email_string)
    out_authors = []
    for author in authors:
        email_info = author.find('div', {'class': 'gs_ai_eml'}).text
        if email_info[-len_check:] == check_email_string:
            out_authors.append(author)
    if verbose:
        print(f'\ndelted {len(authors)-len(out_authors)} authors not matching email {check_email_string}')
    return out_authors

def search_for_label(label='machine_learning', country_search='.cl', max_pages=2, verbose=True, check_email=True, check_email_string='.cl'):
    base_url = 'https://scholar.google.com/citations?view_op=search_authors&mauthors='
    author_class = 'gs_ai_t'
    verbose = True

    #labels_tokens = ['label:' + label for label in labels]
    labels_tokens = ['label:' + label]
    query_tokens = [country_search] + labels_tokens
    query = '+'.join(query_tokens)

    url = base_url + query
    authors = []
    pages = 0

    while pages < max_pages:
        pages += 1
        if verbose:
            out_info = f'getting page {pages} for query {query}' 
            sys.stdout.write('\r' + out_info)
        r = requests.get(url, allow_redirects=True)

        soup = BeautifulSoup(r.content, 'lxml')
        authors += soup.find_all('div', {'class': author_class})

        if verbose:
            out_info += f', authors so far:{len(authors)}'
            sys.stdout.write('\r' + out_info)

        after_author = get_after_author(soup)
        if after_author:
            after_author_query = '&after_author=' + after_author
            url = base_url + query + after_author_query
        else:
            break

    if check_email:
        authors = check_email_authors(authors, check_email_string)
    authors_info = [get_author_info(a) for a in authors]
    if verbose:
        print()
    return authors_info

def get_author_dict_from_scholar(labels, **kwargs):
    authors_dict = {}
    for label in labels:
        authors_list = search_for_label(label, **kwargs)
        for author in authors_list:
            name = author['name']
            scholar_id = author['scholar_id']
            authors_dict[name] = author
    return authors_dict

def search_dblp_by_name(name):
    base_dblp_url = 'https://dblp.uni-trier.de/search/author?q='
    search_dblp_url = base_dblp_url + name
    r = requests.get(search_dblp_url, allow_redirects=True)
    soup = BeautifulSoup(r.content, 'lxml')
    result_list = soup.find_all('ul', {'class': 'result-list'})
    if len(result_list) == 0:
        out_url = r.url
        span_search = re.search('\?q=', out_url)
        if span_search:
            span_start = span_search.span()[0]
        out_url = out_url[:span_start]
        return set([out_url])    
    else:
        # have to find the URL
        normalized_name = unidecode.unidecode(name)
        normalized_aka_name = ''
        if name in known_dblp_aka:
            normalized_aka_name = unidecode.unidecode(known_dblp_aka[name])

        urls = set()
        for r in result_list:
            pos_a_names = r.find_all('a')
            for pos_a_name in pos_a_names:
                pos_name = pos_a_name.text
                normalized_pos_name = unidecode.unidecode(pos_name)
                if normalized_pos_name == normalized_name or normalized_pos_name == normalized_aka_name:
                    urls.add(pos_a_name['href'])
        return urls

def add_dblp_urls(authors_dict, verbose=True):
    total = len(authors_dict)
    for i,name in enumerate(authors_dict):
        if verbose:
            out_info = f'\r({i+1}/{total}) getting dblp url for {name}                  ' 
            sys.stdout.write(out_info)
        dblp_urls = search_dblp_by_name(name)
        authors_dict[name]['dblp_urls'] = dblp_urls
    if verbose:
        print()

def add_dblp_publications(authors_dict, verbose=True, since=2015, upto=2020):
    add_dblp_urls(authors_dict)
    total = len(authors_dict)
    total_publications = 0
    for i,name in enumerate(authors_dict):
        if verbose:
            out_info = f'\r({i+1}/{total}) getting dblp publications for {name} (total pubs all authors: {total_publications})          ' 
            sys.stdout.write(out_info)
        dblp_urls = authors_dict[name]['dblp_urls']
        dblp_publications = []
        for url in dblp_urls:
            # ipdb.set_trace()
            r = requests.get(url, allow_redirects=True)
            soup = BeautifulSoup(r.content, 'lxml')
            pub_ul = soup.find_all('ul', {'class': 'publ-list'})
            if not pub_ul:
                continue
            pub_list = []
            for ul in pub_ul:
                pub_list += ul.find_all('li', recursive=False)
            current_year = upto
            for li in pub_list:
                if li['class'] == ['year']:
                    year = int(li.text)
                    if year < since:
                        break
                    else:
                        current_year = year
                else:
                    # item is publication ==> process it
                    pub = li.find('cite', {'class': 'data'})
                    
                    author_list = pub.find_all('span', {'itemprop':'author'})
                    author_names = [author.text for author in author_list]
                    author_urls = []
                    for author in author_list:
                        link = author.find('a')
                        if link:
                            author_urls.append(link['href'])
                        else:
                            author_urls.append(url)
                    title = pub.find('span', {'class':'title'}).text
                    try:
                        venue = pub.find('span', {'itemprop':'isPartOf'}).text
                    except:
                        venue = ''

                    data = {
                        'year': current_year,
                        'author_names': author_names,
                        'title': title,
                        'venue': venue,
                        'author_urls': author_urls
                    }
                    dblp_publications.append(data)
        authors_dict[name]['dblp_publications'] = dblp_publications
        total_publications += len(dblp_publications)
    return

def get_publications_by_venue(authors_dict):
    pubs_by_venue = {}
    for name in authors_dict:
        for pub_data in authors_dict[name]['dblp_publications']:
            venue = pub_data['venue']
            title = pub_data['title']
            if venue not in pubs_by_venue:
                pubs_by_venue[venue] = {}
            pubs_by_venue[venue][title] = pub_data['author_names']
    return pubs_by_venue

def get_publications_years_by_venue(authors_dict):
    pubs_by_venue_year = {}
    for name in authors_dict:
        for pub_data in authors_dict[name]['dblp_publications']:
            venue = pub_data['venue']
            title = pub_data['title']
            year = pub_data['year']
            authors = pub_data['author_names']
            if venue not in pubs_by_venue_year:
                pubs_by_venue_year[venue] = {}
            pubs_by_venue_year[venue][title] = (year, authors)
    return pubs_by_venue_year

def pub_list_conf_year(pubs_by_venue_year, conf_list):
    output = []
    for conf in conf_list:
        if conf in pubs_by_venue_year:
            for title in pubs_by_venue_year[conf]:
                (year, authors) = pubs_by_venue_year[conf][title]
                output.append((year, conf, title, authors))
    output = sorted(output, reverse=True)
    return output

def count_pubs_with_author(pubs_dict, author_list, verbose=False):
    if not author_list:
        return 0
    with_author = 0
    for title in pubs_dict:
        found_author = False
        authors = pubs_dict[title]
        for author in author_list:
            if author in authors:
                found_author = True
                # if verbose:
                #    print(f'found {author} in {title}')
                with_author += 1
                break
            else:
                if author in known_dblp_aka:
                    aka_author = known_dblp_aka[author]
                    if aka_author in authors:
                        found_author = True
                        # if verbose:
                        #    print(f'found {aka_author} in {title}')
                        with_author += 1
                        break
        if not found_author and verbose:
            print(f'no authors for publication {title}: {", ".join(pubs_dict[title])}')
    return with_author

def count_total_by_venue(pubs_by_venue, venue_list, author_list=None, verbose=True, use_as_prefix=True):
    total = 0
    total_authors = 0
    if not use_as_prefix:
        for venue in venue_list:
            if venue in pubs_by_venue:
                total_venue = len(pubs_by_venue[venue])
                total_authors_venue = count_pubs_with_author(pubs_by_venue[venue], author_list)
                total += total_venue
                total_authors += total_authors_venue
                if verbose:
                    print(f'counting {venue} adding {total_authors_venue}/{total_venue}')
            else:
                if verbose:
                    print(f'not data for {venue}')
    else:
        for venue in venue_list:
            data = False
            for pub_venue in pubs_by_venue:
                if pub_venue.startswith(venue):
                    data = True
                    total_venue = len(pubs_by_venue[pub_venue])
                    total_authors_venue = count_pubs_with_author(pubs_by_venue[pub_venue], author_list)
                    total += total_venue
                    total_authors += total_authors_venue
                    if verbose:
                        print(f'counting {venue} adding {total_authors_venue}/{total_venue}')
            if not data and verbose:
                print(f'not data for {venue} (not even prefixes)')
    return total, total_authors
