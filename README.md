## How to use

To create a dictionary with authors' information extracted from Google Scholar given some query labels just do something like

```
from utils import get_author_dict_from_scholar

labels = [
    'machine_learning',
    'data_mining'
]

authors_dict = get_author_dict_from_scholar(
                    labels, 
                    country_search='.cl', 
                    max_pages=30, 
                    verbose=True, 
                    check_email=True, 
                    check_email_string='.cl')
```

To add information from dblp to everyone of the previous authors, just do something like

```
from utils import add_dblp_publications

known_dblp_aka = {
    'Felipe Tobar': 'Felipe A. Tobar', 
    'Jose Antonio Garcia': 'José García 0002',
    'Carlos Aravena': 'Carlos M. Aravena',
}

add_dblp_publications(authors_dict, since=2015, upto=2020)
```

**IMPORTANT**: you need to define the dictionary `known_dblp_aka` that maps Google Scholar names to DBLP names. You can also leave the dictionary empy, but for now the dictionary has to be defined for `add_dblp_publications` to work.

Given an authors dictionary with dblp data already loaded, you can get a list of publications for every possible venue by doing

```
from utils import get_publications_by_venue

pubs_by_venue = get_publications_by_venue(authors_dict)
```

Finally after you have the publications organized by venues, you can count publications for a specific set of conferences and from a specific set of authors by doing something like the following

```
conferences = [
    'NeurIPS', 
    'AAAI', 
    'SIGIR',
]

researchers = [
    'Barbara Poblete',
    'Jorge Pérez',
    'Felipe Tobar',
    'Jorge Baier',
]

total, total_from_researchers = count_total_by_venue(
                                    pubs_by_venue, 
                                    conferences, 
                                    researchers)
```

## Chilean publications in top AI confereces

The following script presents some numbers for Chilean researchers publishing at top AI conferences. 
It considers the conferences NeurIPS, ICLR, ICML, AAAI, and IJCAI, which are the top-5 AI conferences according to [Google Scholar metrics](https://scholar.google.com/citations?view_op=top_venues&hl=en&vq=eng_artificialintelligence), and a set of researchers included in an upcoming research proposal:

```
python script.py
```

You can found some more details about this numbers and methods [here](https://github.com/jorgeperezrojas/pub_stats/blob/master/cl_ai_numbers.md)