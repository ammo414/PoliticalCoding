"""all bills processing"""
from utils import constants, llm_utils, project_utils as utils
import article_objects

def get_bills():
    """
    main function. creates csv, unpacks and processes JSON, writes data to csv
    """

    url = 'https://api.congress.gov/v3/bill?api_key=' + constants.CONGRESS_API_KEY
    content = utils.load_json(url, 'bill')

    for b in content['bills']:
        bill_number = b['number']
        bill_title = b['title'].lower()
        bill_url = b['url'].replace('?format=json', '')
        bill_type = b['type']
        bill_congress = b['congress']
        bill_content = utils.load_json(bill_url + '?api_key=' + constants.CONGRESS_API_KEY, 'bill')

        #policy_area
        try:
            bill_policy_area = bill_content['bill']['policyArea']['name']
        except KeyError:
            bill_policy_area = None

        #committee
        bill_committees_url = bill_url + '/committees?api_key=' + constants.CONGRESS_API_KEY
        bill_committees_content = utils.load_json(bill_committees_url, 'bill')

        bill_committees = [c['name'] for c in bill_committees_content['committees']]

        bill = article_objects.Bill(bill_number, bill_title, bill_url, bill_committees,
                                    bill_policy_area, bill_type, bill_congress)
        code = cap_code(bill)
        bill.add_cap_code(code)

        bill.write_to_csv(utils.get_filename('bill'))


def cap_code(bill: article_objects.Bill) -> str:
    """
    using policy area, committees, and title from the bill, finds the best cap code
    """
    policy_area = bill.get_policy_area()
    if policy_area is None:
        policy_area = ""
    committees = bill.get_committees()
    title = bill.get_title()
    print(title)

    # huggingface
    committee_string = '|'.join(committees)
    bill_text = '|'.join((policy_area, committee_string, title))
    return llm_utils.classify_text_with_huggingface(bill_text, 'bill')


def cap_code_non_llm(bill: article_objects.Bill):
    """
    using policy area, committees, and title, finds the best cap code without an llm    
    """

    policy_area = bill.get_policy_area()
    if policy_area is None:
        policy_area = ""
    committees = bill.get_committees()
    title = bill.get_title()
    print(title)


    # non-llm approach. Should AB which approach works better

    if 'abort' in title.lower():
        return 200 # abortion -- right to privacy
    if 'foreign' in title.lower():
        if 'Financial Services Committee' in committees \
            or 'Energy and Commerce Committee' in committees:
            return 1800

    match policy_area:
        case 'Agriculture and Food':
            if 'Agriculture Committee' in committees:
                return 400 # General Agriculture -- no need to go in-depth
            if 'Energy and Commerce Committee' in committees:
                return 400
            if 'Natural Resources Committee' in committees:
                return 400
            if 'Education and the Workforce Committee' in committees:
                return 300 # Health -- should be 332 specifically but, again, no need to go in-depth
            if 'Transportation and Infrastructure Committee' in committees:
                return 700 # Environment
            if 'Appropriations Committee' in committees:
                return 400

        case 'Animals':
            if 'Natural Resources Committee' in committees:
                return 700 # environment
            if 'Agriculture Committee' in committees:
                return 400

        case 'Armed Forces and National Security':
            if 'medal' in title.lower():
                return 1600
            if 'Armed Services Committee' in committees:
                return 1600 # defense
            if 'Veterans\' Affairs Committee' in committees:
                if 'hous' in title:
                    return 1400 # general housing
                else:
                    return 1600
            if 'Homeland Security Committee' in committees:
                return 1600
            if 'Intelligence Committee' in committees\
                or 'Intelligence (Permanent Select) Committee' in committees:
                return 1600

        case 'Arts, Culture, Religion':
            return 2300
        case 'Civil Rights and Liberties, Minority Issues':
            return 200
        case 'Commerce':
            return 1500
        case 'Congress':
            return 2000
        case 'Crime and Law Enforcement':
            return 1200
        case 'Economics and Public Finance':
            return 100
        case 'Education':
            return 600
        case 'Emergency Management':
            return 2000
        case 'Energy':
            return 800
        case 'Environmental Protection':
            return 700
        case 'Families':
            return 1300
        case 'Finance and Financial Sector':
            return 1500
        case 'Foreign Trade and International Finance':
            return 1800
        case 'Government Operations and Politics':
            return 2000
        case 'Health':
            return 1300
        case 'Housing and Community Development':
            return 1400
        case 'Immigration':
            return 900
        case 'International Affairs':
            return 1900
        case 'Labor and Employment':
            return 500
        case 'Law':
            return 1200
        case 'Native Americans':
            return 200
        case 'Public Lands and Natural Resources':
            return 2100
        case 'Science, Technology, Communications':
            return 1700
        case 'Social Sciences and History':
            return 600
        case 'Social Welfare':
            return 1300
        case 'Sports and Recreation':
            return 2300
        case 'Taxation':
            return 1500
        case 'Transportation and Public Works':
            return 1000
        case 'Water Resources Development':
            return 700
    return 0
