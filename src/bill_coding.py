"""all bills processing"""

from utils import constants, llm_utils, project_utils as utils
import article_objects


def create_bill_table():
    """returns statements to check if 'news' table exists and, if not, creates it"""
    statement = (
        "CREATE TABLE IF NOT EXISTS {}"
        "("
        "title text not null,"
        "url text not null,"
        "cap_code text,"
        "number integer primary key,"
        "committees text[],"
        "policy_area text,"
        "bill_type text,"
        "congress integer"
        ");"
    )
    table = "bill"
    return statement, table


def get_bills():
    """
    main function. creates csv, unpacks and processes JSON, writes data to csv
    """

    congress_api_key = constants.CONGRESS_API_KEY

    url = "https://api.congress.gov/v3/bill?api_key=" + congress_api_key
    content = utils.load_json(url, "bill")

    filename = utils.get_filename("bill")

    for b in content["bills"]:
        bill_number = b["number"]
        bill_title = b["title"].lower()
        bill_url = b["url"].replace("?format=json", "")
        bill_type = b["type"]
        bill_congress = b["congress"]
        bill_content = utils.load_json(
            bill_url + "?api_key=" + congress_api_key, "bill"
        )

        # policy_area
        try:
            bill_policy_area = bill_content["bill"]["policyArea"]["name"]
        except KeyError:
            bill_policy_area = None

        try:
            bill_introduced_date = bill_content["bill"]["introducedDate"]
        except KeyError:
            bill_introduced_date = None  # should never happen

        # committee
        bill_committees_url = bill_url + "/committees?api_key=" + congress_api_key
        bill_committees_content = utils.load_json(bill_committees_url, "bill")
        bill_committees = [c["name"] for c in bill_committees_content["committees"]]

        bill = article_objects.Bill(
            bill_number,
            bill_title,
            bill_url,
            bill_committees,
            bill_policy_area,
            bill_type,
            bill_congress,
            bill_introduced_date,
        )

        if not bill.in_table():
            code = cap_code(bill)
            bill.add_cap_code(code)

            bill.print_row()
            bill.write_to_csv(filename)
            bill.insert_into_sql()


def cap_code(bill: article_objects.Bill) -> str:
    """
    using policy area, committees, and title from the bill, finds the best cap code
    """
    policy_area = bill.get_policy_area()
    if policy_area is None:
        policy_area = ""
    committees = bill.get_committees()
    title = bill.get_title()

    # huggingface
    committee_string = "|".join(committees)
    bill_text = "|".join((policy_area, committee_string, title))
    return llm_utils.classify_text_with_huggingface(bill_text, "bill")
