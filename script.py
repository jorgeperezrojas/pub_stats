from utils import get_author_dict_from_scholar, add_dblp_publications, get_publications_by_venue, count_total_by_venue, pub_list_conf_year, get_publications_years_by_venue
from data_lists import labels, top_ai_journals, top_ai_conferences
from data_researchers import associate_researchers, young_researchers, senior_researchers

since=2015
upto=2020

authors_dict = get_author_dict_from_scholar(labels, country_search='.cl', max_pages=200, verbose=True, check_email=True, check_email_string='.cl')
add_dblp_publications(authors_dict, since=since, upto=upto)
pubs_by_venue = get_publications_by_venue(authors_dict)

print(f'Comparing publications at AI conferences for researchers')
print(f'    Conferences: {", ".join(top_ai_conferences)}')
print(f'    Associate Researchers: {", ".join(associate_researchers)}')
print(f'    Young Researchers: {", ".join(young_researchers)}')

total_conf, total_proposal_conf = count_total_by_venue(
                                    pubs_by_venue, 
                                    top_ai_conferences, 
                                    associate_researchers + young_researchers,
                                    use_as_prefix=False,
                                    verbose=False)

print(f'Top AI conference publications ({since}-{upto}) by chileans {total_conf}')
print(f'Top AI conference publications ({since}-{upto}) by researchers in proposal (Assoc.+Young) {total_proposal_conf}')
print(f'Percentage: {total_proposal_conf/total_conf*100:2.0f}%')
print()

print('Total list of publications:')
pubs_by_venue_year = get_publications_years_by_venue(authors_dict)
pub_list_ai = pub_list_conf_year(pubs_by_venue_year, top_ai_conferences)
for pub in pub_list_ai:
    print(pub[1], pub[0], pub[2], ', '.join(pub[3]))


