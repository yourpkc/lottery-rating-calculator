import csv
import requests
from bs4 import BeautifulSoup

class WebScraper:
    
    def __init__(self) -> None:
        self.fstp_data = []
        self.head_3_data = []
        self.tail_3_data = []
        self.tail_2_data = []
        self.fstp_neighbor_data = []
        self.sndp_data = []
        self.trdp_data = []
        self.fourthp_data = []
        self.fifthp_data = []
    

    def run(self):
        self.collect_data()
        self.write_data("FirstPrize", self.fstp_data)
        self.write_data("ThreeDigitPrefix", self.head_3_data)
        self.write_data("ThreeDigitSuffix", self.tail_3_data)
        self.write_data("TwoDigitSuffix", self.tail_2_data)
        self.write_data("FirstPrizeNeighbors", self.fstp_neighbor_data)
        self.write_data("SecondPrize", self.sndp_data)
        self.write_data("ThirdPrize", self.trdp_data)
        self.write_data("FourthPrize", self.fourthp_data)
        self.write_data("FifthPrize", self.fifthp_data)

    @staticmethod
    def write_data(filename: str, data: list):
        file_path = f"datas/{filename}.csv"

        with open(file_path, 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow([filename])
            csv_writer.writerows([[item] for item in data if item is not None])


    def collect_data(self):
        urls = self.get_urls()
        for url in urls:
            print("=====", url)
            response = requests.get(url)
            soup = BeautifulSoup(response.content, "html.parser")

            fstp_element = soup.find(class_="lot-dc lotto-fxl py-20")
            if fstp_element:
                self.fstp_data.append(fstp_element.text)

            head_3_element = None
            if fstp_element:
                head_3_element = fstp_element.find_next(class_="lot-dc lotto-fxl py-20")
            if head_3_element:
                texts = head_3_element.text.split('\xa0 ')
                self.head_3_data.extend(texts)

            tail_3_element = None
            if head_3_element:
                tail_3_element = head_3_element.find_next(class_="lot-dc lotto-fxl py-20")
            if tail_3_element:
                texts = tail_3_element.text.split('\xa0 ')
                self.tail_3_data.extend(texts)

            tail_2_element = None
            if tail_3_element:
                tail_2_element = tail_3_element.find_next(class_="lot-dc lotto-fxl py-20")
            if tail_2_element:
                self.tail_2_data.append(tail_2_element.text)

            fstp_neighbor_element = soup.find(class_="lot-cw70 lotto-fx")
            if fstp_neighbor_element:
                text = fstp_neighbor_element.text
                texts = text.split(' \xa0 ')
                self.fstp_neighbor_data.extend(texts)

            sndp_element = soup.find(string="รางวัลที่ 2")
            if sndp_element:
                for _ in range(5):
                    sndp_element = sndp_element.find_next(class_='lot-dc lotto-fx lot-c20')
                    if not sndp_element:
                        break
                    self.sndp_data.append(sndp_element.text)

            trdp_element = soup.find(string="รางวัลที่ 3")
            if trdp_element:
                for _ in range(10):
                    trdp_element = trdp_element.find_next(class_='lot-dc lotto-fx lot-c20')
                    if not trdp_element:
                        break
                    self.trdp_data.append(trdp_element.text)

            fourthp_element = soup.find(string="รางวัลที่ 4")
            if fourthp_element:
                for _ in range(50):
                    fourthp_element = fourthp_element.find_next(class_='lot-dc lotto-fx lot-c20')
                    if not fourthp_element:
                        break
                    self.fourthp_data.append(fourthp_element.text)

            fifthp_element = soup.find(string="รางวัลที่ 5")
            if fifthp_element:
                for _ in range(100):
                    fifthp_element = fifthp_element.find_next(class_='lot-dc lotto-fx lot-c20')
                    if not fifthp_element:
                        break
                    self.fifthp_data.append(fifthp_element.text)
 
    @staticmethod
    def get_urls():
        def check_url(url):
            try:
                response = requests.head(url)
                return response.status_code == 200
            except requests.ConnectionError as error:
                print(f"{error=}")
                return False
        
        default_dates = [16, 1]
        months = {'มกราคม': [17, 16],
                  'ธันวาคม': [30, 16, 17, 1],
                  'พฤศจิกายน': default_dates,
                  'ตุลาคม': default_dates,
                  'กันยายน': default_dates,
                  'สิงหาคม': default_dates,
                  'กรกฎาคม': [31, 16, 15, 1],
                  'มิถุนายน': [16, 2, 1],
                  'พฤษภาคม': [16, 2],
                  'เมษายน': default_dates,
                  'มีนาคม': [16, 2, 1],
                  'กุมภาพันธ์': [17, 16, 1]}

        urls = []
        for year in range(2567, 2537, -1):
            for month, dates in months.items():
                for date in dates:
                    url = f'https://www.myhora.com/หวย/งวด-{date}-{month}-{year}.aspx'
                    if check_url(url):
                        urls.append(url)

        return urls

if __name__ == '__main__':
    WebScraper().run()
