import openpyxl
from enum import StrEnum, auto

# TODO: Cycle through excel specs
# TODO: Parse each element
# TODO: Separate pages


# Element column/entry type

    # Section -> Determines if is a visible page
        # Col H -> determines if has page number
    # Block -> Contains logic, meta values or question text. (Ignore?)
        # Col B -> Type of entry. Logic, or text.
    # Answer -> Element interaction. Text field, dropdown, radio, etc.
        # Col B -> Type of element. Text, radio, etc. 
    # XXXHeader -> Used to create "subsections". Ignore.
    # Field -> Option in a dropdown, list of radio options, etc.
    # Roster -> Meta info related to roster system. Ignore.
    # Page Break -> Denotes the start of a new page

'''
REQUIREMENTS

    - page break: current page is added to all pages, new empty page is created
    - hidden flag: if section name contains hidden, it is not a visible page set flag to true
        - if hidden flag is true, iterate to next page break.
    - full roster flag: if a new page is started, and the roster row comes after the section row than all roster members are on a single page.
        - use element value/id and instance value to find 
    - single roster flag: if a new page is started, and the roster row comes before the section row, each page is instanced for the individual answering.
        - can use element value/id only 

'''

'''
PSEUDO CODE

base_page = {eqgs_page}
all_pages = {base_page}
current_page = {}
for row in rows:
    if (row == section):
        if (row == hidden):
            continue to page break
        else:
            get section id
        if (section first):
            1 person/page
        elif (roster first):
            all persons/page
    elif (row == page break):
        start new page
    elif (row == block):
        if (row.type == question):
            get question number
    elif (row == answer):
        TODO: work out type logic
    elif (row == field):
        if (answer type == radio):
            get value/id
        elif ()
'''

def Element(StrEnum):
    SECTION = auto()
    ANSWER = auto()
    ROSTER = auto()
    FIELD = auto()
    BREAK = "pagebreak"
    END = 'endgroupheader'

def ElementType(StrEnum):
    RADIO = auto()
    RADIOTEXT = auto()
    CHECK = auto()
    DROPDOWN = auto()
    INTEGER = auto()
    TEXT = auto()


def convert(path):
    """
    Helper tool to convert EQ specs to Page model
    """

    wb = openpyxl.load_workbook(path) # Open the specs

    spec_name = "Capture Specifications"
    if spec_name not in wb.sheetnames:
        return # Throw some exception?

    specs = wb[spec_name]

    eq_page = {"elements": {
               "next": {"by": "id", "value": "__btnNext"},
               "submit": {"by": "id", "value": "__btnSubmit"}
            }
    }
    all_pages = {"eqgs": eq_page}
    cur_page = {}
    section_name = ""

    in_section = False
    hidden = False
    full_roster = False

    # Controlled by Element.END and page break
    field_type = None

    for row in specs.iter_rows(min_row=2):
        if hidden:
            continue
        else:

            row_type = row[0].value.lower()
            if row_type == Element.BREAK:
                hidden = False
                full_roster = False

                field_type = None

                if in_section:
                    in_section = False
                    # TODO: Add page to all pages, reset current page
                    
            
            if row_type == Element.SECTION:
                if row[7].value.lower().contains('hidden'):
                    hidden = True
                else:
                    section_name = row[2].value
                    in_section = True
            elif row_type == Element.ROSTER:
                if in_section:
                    full_roster = True

            elif row_type == Element.ANSWER:
                element_type = row[1].value.lower()
                match element_type:
                    case ElementType.RADIOTEXT:
                        field_type = ElementType.RADIOTEXT
                    case ElementType.RADIO:
                        field_type = ElementType.RADIO
                    case ElementType.TEXT | ElementType.INTEGER:
                        if full_roster:
                            # TODO:text field with instance
                            _e = {row[2].value:
                                f"""//input[contains(@id, 'Instance') 
                                and @value = {'{}'}]/following-sibling::*
                                /descendant::input[contains(@name, {row[2].value})]
                                """}
                            cur_page.update()

