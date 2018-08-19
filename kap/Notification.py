from bs4 import BeautifulSoup
import datetime


class Notification(object):
    """Simulates the individual notification found in the company's web page"""

    def __init__(self, source_code: str, _id: int):
        self.fetching_date = datetime.datetime.now()
        self.source_code = source_code

        self.__parse(_id)

    def __parse(self, _id: int):
        soup = BeautifulSoup(self.source_code, 'html.parser')

        try:
            self._id = int(soup.find("div")['ng-init'][-6:])
        except:
            self._id = _id

        self.company_name = soup.find(class_="type-medium type-bold bi-sky-black").contents[0].string.strip()

        try:
            self.stock = soup.find(class_="type-medium bi-dim-gray").contents[0].string.strip()
        except:
            self.stock = "-"

        # parsing the brief information
        element = soup.find(class_="w-row modal-briefsummary")
        date = element.find(class_="type-medium bi-sky-black").string
        self.publish_date = datetime.datetime.strptime(date, "%d.%m.%Y %H:%M:%S")
        self.disclosure_type = element.find_all("div", class_="type-medium bi-sky-black")[1].string.strip()

        # find related companies
        self.related_companies = []
        element = soup.find_all(class_="gwt-Label")
        try:
            if len(element) and not element[0].string is None and element[0].string.strip() == "İlgili Şirketler":
                self.related_companies.extend(element[2].string.strip()[1:-1].split(", "))
        except:
            print("!!!", self._id)
        try:
            element = soup.find_all(class_="bold font14")
            if element[1].string.strip() == "İlgili Şirketler":
                element = soup.find_all(class_="gwt-HTML control-label lineheight-32px")
                self.related_companies.extend(element[1].string.strip().split(", "))
        except:
            pass

        if len(self.related_companies) == 0:
            try:
                element = soup.find_all(class_="bold font14")
                index = -1
                for el in element:
                    if el.string.strip() == "İlgili Şirketler":
                        index = element.index(el)
                if index != -1:
                    element = soup.find_all(class_="gwt-HTML control-label lineheight-32px")
                    self.related_companies.extend(element[index].string.strip().split(", "))
            except:
                pass

        if self.stock != "-":
            self.related_companies.append(self.stock)

        # parsing the main information
        element = soup.find(class_="modal-info")
        try:
            self.header = element.find("h1").contents[0].string.strip()
        except:
            self.header = "-"
        self.source_code = str(element)

    def dump(self):
        return {
            '_id': self._id,
            'stock': self.stock,
            'company_name': self.company_name,
            'publish_date': self.publish_date,  # .strftime("%d.%m.%Y %H:%M:%S"),
            'fetching_date': self.fetching_date,  # .strftime("%d.%m.%Y %H:%M:%S"),
            'disclosure_type': self.disclosure_type,
            'header': self.header,
            'related_companies': self.related_companies,
            'source_code': self.source_code
        }
