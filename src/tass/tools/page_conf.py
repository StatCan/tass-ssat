import openpyxl
from enum import StrEnum, auto


class Element(StrEnum):
    SECTION = auto()
    ANSWER = auto()
    ROSTER = auto()
    FIELD = auto()
    BREAK = "pagebreak"
    GROUP = "groupheader"
    ENDGROUP = 'endgroupheader'

class ElementType(StrEnum):
    RADIO = auto()
    RADIOTEXT = auto()
    CHECK = auto()
    CHECKSPECIFY = auto()
    DROPDOWN = auto()
    INTEGER = auto()
    TEXT = auto()
    PHONE = auto()
    EMAIL = auto()
    POSTALNOVAL = "postalcodenoval"
    INFO = auto()


def convert(path):
    """
    Helper tool to convert EQ specs to Page model
    """

    wb = openpyxl.load_workbook(path) # Open the specs

    spec_name = "Capture Specifications"
    if spec_name not in wb.sheetnames:
        return # Throw some exception?

    wb_out = openpyxl.Workbook()
    specs_out = wb_out.active

    specs_out.append(["Element Type", "ID", "Name", "Rostered"])
    specs_out.append(["pagebreak"])

    specs = wb[spec_name]

    elements = []

    hidden = False

    field_type = None
    radio_group = None

    for row in specs.iter_rows(min_row=2):
        row_type = row[0].value.lower()
        if row_type == Element.BREAK:
            hidden = False
            field_type = None
            radio_group = None
            if len(elements) > 0:
                for e in elements:
                    print(e)
                    specs_out.append(e)

                specs_out.append(["pagebreak"])
                elements = []
        
        elif hidden:
            print("Row is hidden:", row[0].row)
            continue
        else:
            
            if row_type == Element.SECTION:
                if "hidden" in row[7].value.lower():
                    hidden = True

            elif row_type == Element.ANSWER:
                field_type = None
                element_type = row[1].value.lower()
                print("This is an anser. It is:", element_type)
                match element_type:
                    case ElementType.RADIOTEXT:
                        print(ElementType.RADIOTEXT)
                        field_type = ElementType.RADIOTEXT
                    case ElementType.RADIO:
                        print(ElementType.RADIO)
                        field_type = ElementType.RADIO
                        radio_group = row[2].value
                    case ElementType.TEXT | ElementType.INTEGER | ElementType.PHONE | ElementType.EMAIL | ElementType.POSTALNOVAL:
                        elements.append([ElementType.TEXT, row[2].value])
                    case ElementType.DROPDOWN:
                        elements.append([ElementType.DROPDOWN, row[2].value])
                    case ElementType.CHECK | ElementType.CHECKSPECIFY:
                        elements.append([ElementType.CHECK, row[2].value])
                    case ElementType.INFO:
                        elements.append([ElementType.INFO, row[2].value])

            elif row_type == Element.FIELD:
                print("This row is a field: ", row[0].row)
                print("The field is of the type: ", field_type)
                if field_type == ElementType.RADIOTEXT:
                    elements.append([ElementType.RADIOTEXT, row[5].value])

                elif field_type == ElementType.RADIO:
                    _id = f"{radio_group},{row[5].value}"
                    _name = row[7].value.lower().replace(' ', '-')
                    elements.append([ElementType.RADIO, _id, _name])

    if len(elements)>0:
        for e in elements:
            specs_out.append(e)

    wb_out.save("pages.xlsx")
        


