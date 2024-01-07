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
            response = requests.get(url)
            soup = BeautifulSoup(response.content, "html.parser")

            fstp_element = soup.find(class_="lot-dc lotto-fxl py-20")
            self.fstp_data.append(fstp_element.text)

            head_3_element = fstp_element.find_next(class_="lot-dc lotto-fxl py-20")
            texts = head_3_element.text.split('\xa0 ')
            self.head_3_data.extend(texts)

            tail_3_element = head_3_element.find_next(class_="lot-dc lotto-fxl py-20")
            texts = tail_3_element.text.split('\xa0 ')
            self.tail_3_data.extend(texts)

            tail_2_element = tail_3_element.find_next(class_="lot-dc lotto-fxl py-20")
            self.tail_2_data.append(tail_2_element.text)

            fstp_neighbor_element = soup.find(class_="lot-cw70 lotto-fx")
            text = fstp_neighbor_element.text
            texts = text.split(' \xa0 ')
            self.fstp_neighbor_data.extend(texts)

            sndp_element = soup.find(string="รางวัลที่ 2")
            for _ in range(5):
                sndp_element = sndp_element.find_next(class_='lot-dc lotto-fx lot-c20')
                self.sndp_data.append(sndp_element.text)

            trdp_element = soup.find(string="รางวัลที่ 3")
            for _ in range(10):
                trdp_element = trdp_element.find_next(class_='lot-dc lotto-fx lot-c20')
                self.trdp_data.append(trdp_element.text)

            fourthp_element = soup.find(string="รางวัลที่ 4")
            for _ in range(50):
                fourthp_element = fourthp_element.find_next(class_='lot-dc lotto-fx lot-c20')
                self.fourthp_data.append(fourthp_element.text)

            fifthp_element = soup.find(string="รางวัลที่ 5")
            for _ in range(100):
                fifthp_element = fifthp_element.find_next(class_='lot-dc lotto-fx lot-c20')
                self.fifthp_data.append(fifthp_element.text)
 
    @staticmethod
    def get_urls():
        return [
            'https://www.myhora.com/%e0%b8%ab%e0%b8%a7%e0%b8%a2/%e0%b8%87%e0%b8%a7%e0%b8%94-30-%e0%b8%98%e0%b8%b1%e0%b8%99%e0%b8%a7%e0%b8%b2%e0%b8%84%e0%b8%a1-2566.aspx?',
            'https://www.myhora.com/%e0%b8%ab%e0%b8%a7%e0%b8%a2/%e0%b8%87%e0%b8%a7%e0%b8%94-16-%e0%b8%98%e0%b8%b1%e0%b8%99%e0%b8%a7%e0%b8%b2%e0%b8%84%e0%b8%a1-2566.aspx?',
            'https://www.myhora.com/%e0%b8%ab%e0%b8%a7%e0%b8%a2/%e0%b8%87%e0%b8%a7%e0%b8%94-1-%e0%b8%98%e0%b8%b1%e0%b8%99%e0%b8%a7%e0%b8%b2%e0%b8%84%e0%b8%a1-2566.aspx?',
            'https://www.myhora.com/%e0%b8%ab%e0%b8%a7%e0%b8%a2/%e0%b8%87%e0%b8%a7%e0%b8%94-16-%e0%b8%9e%e0%b8%a4%e0%b8%a8%e0%b8%88%e0%b8%b4%e0%b8%81%e0%b8%b2%e0%b8%a2%e0%b8%99-2566.aspx?',
            'https://www.myhora.com/%E0%B8%AB%E0%B8%A7%E0%B8%A2/%e0%b8%87%e0%b8%a7%e0%b8%94-1-%e0%b8%9e%e0%b8%a4%e0%b8%a8%e0%b8%88%e0%b8%b4%e0%b8%81%e0%b8%b2%e0%b8%a2%e0%b8%99-2566.aspx',
            'https://www.myhora.com/%E0%B8%AB%E0%B8%A7%E0%B8%A2/%e0%b8%87%e0%b8%a7%e0%b8%94-16-%e0%b8%95%e0%b8%b8%e0%b8%a5%e0%b8%b2%e0%b8%84%e0%b8%a1-2566.aspx',
            'https://www.myhora.com/%E0%B8%AB%E0%B8%A7%E0%B8%A2/%e0%b8%87%e0%b8%a7%e0%b8%94-1-%e0%b8%95%e0%b8%b8%e0%b8%a5%e0%b8%b2%e0%b8%84%e0%b8%a1-2566.aspx',
            'https://www.myhora.com/%E0%B8%AB%E0%B8%A7%E0%B8%A2/%e0%b8%87%e0%b8%a7%e0%b8%94-16-%e0%b8%81%e0%b8%b1%e0%b8%99%e0%b8%a2%e0%b8%b2%e0%b8%a2%e0%b8%99-2566.aspx',
            'https://www.myhora.com/%E0%B8%AB%E0%B8%A7%E0%B8%A2/%e0%b8%87%e0%b8%a7%e0%b8%94-1-%e0%b8%81%e0%b8%b1%e0%b8%99%e0%b8%a2%e0%b8%b2%e0%b8%a2%e0%b8%99-2566.aspx',
            'https://www.myhora.com/%E0%B8%AB%E0%B8%A7%E0%B8%A2/%e0%b8%87%e0%b8%a7%e0%b8%94-16-%e0%b8%aa%e0%b8%b4%e0%b8%87%e0%b8%ab%e0%b8%b2%e0%b8%84%e0%b8%a1-2566.aspx',
            'https://www.myhora.com/%E0%B8%AB%E0%B8%A7%E0%B8%A2/%e0%b8%87%e0%b8%a7%e0%b8%94-31-%e0%b8%81%e0%b8%a3%e0%b8%81%e0%b8%8e%e0%b8%b2%e0%b8%84%e0%b8%a1-2566.aspx',
            'https://www.myhora.com/%E0%B8%AB%E0%B8%A7%E0%B8%A2/%e0%b8%87%e0%b8%a7%e0%b8%94-16-%e0%b8%81%e0%b8%a3%e0%b8%81%e0%b8%8e%e0%b8%b2%e0%b8%84%e0%b8%a1-2566.aspx',
            'https://www.myhora.com/%E0%B8%AB%E0%B8%A7%E0%B8%A2/%e0%b8%87%e0%b8%a7%e0%b8%94-1-%e0%b8%81%e0%b8%a3%e0%b8%81%e0%b8%8e%e0%b8%b2%e0%b8%84%e0%b8%a1-2566.aspx',
            'https://www.myhora.com/%E0%B8%AB%E0%B8%A7%E0%B8%A2/%e0%b8%87%e0%b8%a7%e0%b8%94-16-%e0%b8%a1%e0%b8%b4%e0%b8%96%e0%b8%b8%e0%b8%99%e0%b8%b2%e0%b8%a2%e0%b8%99-2566.aspx',
            'https://www.myhora.com/%E0%B8%AB%E0%B8%A7%E0%B8%A2/%e0%b8%87%e0%b8%a7%e0%b8%94-1-%e0%b8%a1%e0%b8%b4%e0%b8%96%e0%b8%b8%e0%b8%99%e0%b8%b2%e0%b8%a2%e0%b8%99-2566.aspx',
            'https://www.myhora.com/%E0%B8%AB%E0%B8%A7%E0%B8%A2/%e0%b8%87%e0%b8%a7%e0%b8%94-16-%e0%b8%9e%e0%b8%a4%e0%b8%a9%e0%b8%a0%e0%b8%b2%e0%b8%84%e0%b8%a1-2566.aspx',
            'https://www.myhora.com/%E0%B8%AB%E0%B8%A7%E0%B8%A2/%e0%b8%87%e0%b8%a7%e0%b8%94-2-%e0%b8%9e%e0%b8%a4%e0%b8%a9%e0%b8%a0%e0%b8%b2%e0%b8%84%e0%b8%a1-2566.aspx',
            'https://www.myhora.com/%E0%B8%AB%E0%B8%A7%E0%B8%A2/%e0%b8%87%e0%b8%a7%e0%b8%94-16-%e0%b9%80%e0%b8%a1%e0%b8%a9%e0%b8%b2%e0%b8%a2%e0%b8%99-2566.aspx',
            'https://www.myhora.com/%E0%B8%AB%E0%B8%A7%E0%B8%A2/%e0%b8%87%e0%b8%a7%e0%b8%94-1-%e0%b9%80%e0%b8%a1%e0%b8%a9%e0%b8%b2%e0%b8%a2%e0%b8%99-2566.aspx',
            'https://www.myhora.com/%E0%B8%AB%E0%B8%A7%E0%B8%A2/%e0%b8%87%e0%b8%a7%e0%b8%94-16-%e0%b8%a1%e0%b8%b5%e0%b8%99%e0%b8%b2%e0%b8%84%e0%b8%a1-2566.aspx',
            'https://www.myhora.com/%E0%B8%AB%E0%B8%A7%E0%B8%A2/%e0%b8%87%e0%b8%a7%e0%b8%94-1-%e0%b8%a1%e0%b8%b5%e0%b8%99%e0%b8%b2%e0%b8%84%e0%b8%a1-2566.aspx',
            'https://www.myhora.com/%E0%B8%AB%E0%B8%A7%E0%B8%A2/%e0%b8%87%e0%b8%a7%e0%b8%94-16-%e0%b8%81%e0%b8%b8%e0%b8%a1%e0%b8%a0%e0%b8%b2%e0%b8%9e%e0%b8%b1%e0%b8%99%e0%b8%98%e0%b9%8c-2566.aspx',
            'https://www.myhora.com/%E0%B8%AB%E0%B8%A7%E0%B8%A2/%e0%b8%87%e0%b8%a7%e0%b8%94-1-%e0%b8%81%e0%b8%b8%e0%b8%a1%e0%b8%a0%e0%b8%b2%e0%b8%9e%e0%b8%b1%e0%b8%99%e0%b8%98%e0%b9%8c-2566.aspx',
            'https://www.myhora.com/%E0%B8%AB%E0%B8%A7%E0%B8%A2/%e0%b8%87%e0%b8%a7%e0%b8%94-17-%e0%b8%a1%e0%b8%81%e0%b8%a3%e0%b8%b2%e0%b8%84%e0%b8%a1-2566.aspx',
            'https://www.myhora.com/%E0%B8%AB%E0%B8%A7%E0%B8%A2/%e0%b8%87%e0%b8%a7%e0%b8%94-30-%e0%b8%98%e0%b8%b1%e0%b8%99%e0%b8%a7%e0%b8%b2%e0%b8%84%e0%b8%a1-2565.aspx',
            'https://www.myhora.com/%E0%B8%AB%E0%B8%A7%E0%B8%A2/%e0%b8%87%e0%b8%a7%e0%b8%94-16-%e0%b8%98%e0%b8%b1%e0%b8%99%e0%b8%a7%e0%b8%b2%e0%b8%84%e0%b8%a1-2565.aspx',
            'https://www.myhora.com/%E0%B8%AB%E0%B8%A7%E0%B8%A2/%e0%b8%87%e0%b8%a7%e0%b8%94-16-%e0%b8%98%e0%b8%b1%e0%b8%99%e0%b8%a7%e0%b8%b2%e0%b8%84%e0%b8%a1-2565.aspx',
            'https://www.myhora.com/%E0%B8%AB%E0%B8%A7%E0%B8%A2/%e0%b8%87%e0%b8%a7%e0%b8%94-1-%e0%b8%98%e0%b8%b1%e0%b8%99%e0%b8%a7%e0%b8%b2%e0%b8%84%e0%b8%a1-2565.aspx',
            'https://www.myhora.com/%E0%B8%AB%E0%B8%A7%E0%B8%A2/%e0%b8%87%e0%b8%a7%e0%b8%94-16-%e0%b8%9e%e0%b8%a4%e0%b8%a8%e0%b8%88%e0%b8%b4%e0%b8%81%e0%b8%b2%e0%b8%a2%e0%b8%99-2565.aspx',
            'https://www.myhora.com/%E0%B8%AB%E0%B8%A7%E0%B8%A2/%e0%b8%87%e0%b8%a7%e0%b8%94-1-%e0%b8%9e%e0%b8%a4%e0%b8%a8%e0%b8%88%e0%b8%b4%e0%b8%81%e0%b8%b2%e0%b8%a2%e0%b8%99-2565.aspx',
            'https://www.myhora.com/%E0%B8%AB%E0%B8%A7%E0%B8%A2/%e0%b8%87%e0%b8%a7%e0%b8%94-16-%e0%b8%95%e0%b8%b8%e0%b8%a5%e0%b8%b2%e0%b8%84%e0%b8%a1-2565.aspx',
            'https://www.myhora.com/%E0%B8%AB%E0%B8%A7%E0%B8%A2/%e0%b8%87%e0%b8%a7%e0%b8%94-1-%e0%b8%95%e0%b8%b8%e0%b8%a5%e0%b8%b2%e0%b8%84%e0%b8%a1-2565.aspx',
            'https://www.myhora.com/%E0%B8%AB%E0%B8%A7%E0%B8%A2/%e0%b8%87%e0%b8%a7%e0%b8%94-16-%e0%b8%81%e0%b8%b1%e0%b8%99%e0%b8%a2%e0%b8%b2%e0%b8%a2%e0%b8%99-2565.aspx',
            'https://www.myhora.com/%E0%B8%AB%E0%B8%A7%E0%B8%A2/%e0%b8%87%e0%b8%a7%e0%b8%94-1-%e0%b8%81%e0%b8%b1%e0%b8%99%e0%b8%a2%e0%b8%b2%e0%b8%a2%e0%b8%99-2565.aspx',
            'https://www.myhora.com/%E0%B8%AB%E0%B8%A7%E0%B8%A2/%e0%b8%87%e0%b8%a7%e0%b8%94-16-%e0%b8%aa%e0%b8%b4%e0%b8%87%e0%b8%ab%e0%b8%b2%e0%b8%84%e0%b8%a1-2565.aspx',
            'https://www.myhora.com/%E0%B8%AB%E0%B8%A7%E0%B8%A2/%e0%b8%87%e0%b8%a7%e0%b8%94-1-%e0%b8%aa%e0%b8%b4%e0%b8%87%e0%b8%ab%e0%b8%b2%e0%b8%84%e0%b8%a1-2565.aspx',
            'https://www.myhora.com/%E0%B8%AB%E0%B8%A7%E0%B8%A2/%e0%b8%87%e0%b8%a7%e0%b8%94-16-%e0%b8%81%e0%b8%a3%e0%b8%81%e0%b8%8e%e0%b8%b2%e0%b8%84%e0%b8%a1-2565.aspx',
            'https://www.myhora.com/%E0%B8%AB%E0%B8%A7%E0%B8%A2/%e0%b8%87%e0%b8%a7%e0%b8%94-1-%e0%b8%81%e0%b8%a3%e0%b8%81%e0%b8%8e%e0%b8%b2%e0%b8%84%e0%b8%a1-2565.aspx',
            'https://www.myhora.com/%E0%B8%AB%E0%B8%A7%E0%B8%A2/%e0%b8%87%e0%b8%a7%e0%b8%94-16-%e0%b8%a1%e0%b8%b4%e0%b8%96%e0%b8%b8%e0%b8%99%e0%b8%b2%e0%b8%a2%e0%b8%99-2565.aspx',
            'https://www.myhora.com/%E0%B8%AB%E0%B8%A7%E0%B8%A2/%e0%b8%87%e0%b8%a7%e0%b8%94-1-%e0%b8%a1%e0%b8%b4%e0%b8%96%e0%b8%b8%e0%b8%99%e0%b8%b2%e0%b8%a2%e0%b8%99-2565.aspx',
            'https://www.myhora.com/%E0%B8%AB%E0%B8%A7%E0%B8%A2/%e0%b8%87%e0%b8%a7%e0%b8%94-16-%e0%b8%9e%e0%b8%a4%e0%b8%a9%e0%b8%a0%e0%b8%b2%e0%b8%84%e0%b8%a1-2565.aspx',
            'https://www.myhora.com/%E0%B8%AB%E0%B8%A7%E0%B8%A2/%e0%b8%87%e0%b8%a7%e0%b8%94-2-%e0%b8%9e%e0%b8%a4%e0%b8%a9%e0%b8%a0%e0%b8%b2%e0%b8%84%e0%b8%a1-2565.aspx',
            'https://www.myhora.com/%E0%B8%AB%E0%B8%A7%E0%B8%A2/%e0%b8%87%e0%b8%a7%e0%b8%94-16-%e0%b9%80%e0%b8%a1%e0%b8%a9%e0%b8%b2%e0%b8%a2%e0%b8%99-2565.aspx',
            'https://www.myhora.com/%E0%B8%AB%E0%B8%A7%E0%B8%A2/%e0%b8%87%e0%b8%a7%e0%b8%94-1-%e0%b9%80%e0%b8%a1%e0%b8%a9%e0%b8%b2%e0%b8%a2%e0%b8%99-2565.aspx',
            'https://www.myhora.com/%E0%B8%AB%E0%B8%A7%E0%B8%A2/%e0%b8%87%e0%b8%a7%e0%b8%94-16-%e0%b8%a1%e0%b8%b5%e0%b8%99%e0%b8%b2%e0%b8%84%e0%b8%a1-2565.aspx',
            'https://www.myhora.com/%E0%B8%AB%E0%B8%A7%E0%B8%A2/%e0%b8%87%e0%b8%a7%e0%b8%94-1-%e0%b8%a1%e0%b8%b5%e0%b8%99%e0%b8%b2%e0%b8%84%e0%b8%a1-2565.aspx',
            'https://www.myhora.com/%E0%B8%AB%E0%B8%A7%E0%B8%A2/%e0%b8%87%e0%b8%a7%e0%b8%94-17-%e0%b8%81%e0%b8%b8%e0%b8%a1%e0%b8%a0%e0%b8%b2%e0%b8%9e%e0%b8%b1%e0%b8%99%e0%b8%98%e0%b9%8c-2565.aspx',
            'https://www.myhora.com/%E0%B8%AB%E0%B8%A7%E0%B8%A2/%e0%b8%87%e0%b8%a7%e0%b8%94-1-%e0%b8%81%e0%b8%b8%e0%b8%a1%e0%b8%a0%e0%b8%b2%e0%b8%9e%e0%b8%b1%e0%b8%99%e0%b8%98%e0%b9%8c-2565.aspx',
            'https://www.myhora.com/%E0%B8%AB%E0%B8%A7%E0%B8%A2/%e0%b8%87%e0%b8%a7%e0%b8%94-17-%e0%b8%a1%e0%b8%81%e0%b8%a3%e0%b8%b2%e0%b8%84%e0%b8%a1-2565.aspx',
            'https://www.myhora.com/%E0%B8%AB%E0%B8%A7%E0%B8%A2/%e0%b8%87%e0%b8%a7%e0%b8%94-30-%e0%b8%98%e0%b8%b1%e0%b8%99%e0%b8%a7%e0%b8%b2%e0%b8%84%e0%b8%a1-2564.aspx',
            'https://www.myhora.com/%E0%B8%AB%E0%B8%A7%E0%B8%A2/%e0%b8%87%e0%b8%a7%e0%b8%94-16-%e0%b8%98%e0%b8%b1%e0%b8%99%e0%b8%a7%e0%b8%b2%e0%b8%84%e0%b8%a1-2564.aspx',
            'https://www.myhora.com/%E0%B8%AB%E0%B8%A7%E0%B8%A2/%e0%b8%87%e0%b8%a7%e0%b8%94-1-%e0%b8%98%e0%b8%b1%e0%b8%99%e0%b8%a7%e0%b8%b2%e0%b8%84%e0%b8%a1-2564.aspx',
            'https://www.myhora.com/%E0%B8%AB%E0%B8%A7%E0%B8%A2/%e0%b8%87%e0%b8%a7%e0%b8%94-16-%e0%b8%9e%e0%b8%a4%e0%b8%a8%e0%b8%88%e0%b8%b4%e0%b8%81%e0%b8%b2%e0%b8%a2%e0%b8%99-2564.aspx',
            'https://www.myhora.com/%E0%B8%AB%E0%B8%A7%E0%B8%A2/%e0%b8%87%e0%b8%a7%e0%b8%94-1-%e0%b8%9e%e0%b8%a4%e0%b8%a8%e0%b8%88%e0%b8%b4%e0%b8%81%e0%b8%b2%e0%b8%a2%e0%b8%99-2564.aspx',
            'https://www.myhora.com/%E0%B8%AB%E0%B8%A7%E0%B8%A2/%e0%b8%87%e0%b8%a7%e0%b8%94-16-%e0%b8%95%e0%b8%b8%e0%b8%a5%e0%b8%b2%e0%b8%84%e0%b8%a1-2564.aspx',
            'https://www.myhora.com/%E0%B8%AB%E0%B8%A7%E0%B8%A2/%e0%b8%87%e0%b8%a7%e0%b8%94-1-%e0%b8%95%e0%b8%b8%e0%b8%a5%e0%b8%b2%e0%b8%84%e0%b8%a1-2564.aspx',
            'https://www.myhora.com/%E0%B8%AB%E0%B8%A7%E0%B8%A2/%e0%b8%87%e0%b8%a7%e0%b8%94-16-%e0%b8%81%e0%b8%b1%e0%b8%99%e0%b8%a2%e0%b8%b2%e0%b8%a2%e0%b8%99-2564.aspx',
            'https://www.myhora.com/%E0%B8%AB%E0%B8%A7%E0%B8%A2/%e0%b8%87%e0%b8%a7%e0%b8%94-1-%e0%b8%81%e0%b8%b1%e0%b8%99%e0%b8%a2%e0%b8%b2%e0%b8%a2%e0%b8%99-2564.aspx',
            'https://www.myhora.com/%E0%B8%AB%E0%B8%A7%E0%B8%A2/%e0%b8%87%e0%b8%a7%e0%b8%94-16-%e0%b8%aa%e0%b8%b4%e0%b8%87%e0%b8%ab%e0%b8%b2%e0%b8%84%e0%b8%a1-2564.aspx',
            'https://www.myhora.com/%E0%B8%AB%E0%B8%A7%E0%B8%A2/%e0%b8%87%e0%b8%a7%e0%b8%94-1-%e0%b8%aa%e0%b8%b4%e0%b8%87%e0%b8%ab%e0%b8%b2%e0%b8%84%e0%b8%a1-2564.aspx',
            'https://www.myhora.com/%E0%B8%AB%E0%B8%A7%E0%B8%A2/%e0%b8%87%e0%b8%a7%e0%b8%94-16-%e0%b8%81%e0%b8%a3%e0%b8%81%e0%b8%8e%e0%b8%b2%e0%b8%84%e0%b8%a1-2564.aspx',
            'https://www.myhora.com/%E0%B8%AB%E0%B8%A7%E0%B8%A2/%e0%b8%87%e0%b8%a7%e0%b8%94-1-%e0%b8%81%e0%b8%a3%e0%b8%81%e0%b8%8e%e0%b8%b2%e0%b8%84%e0%b8%a1-2564.aspx',
            'https://www.myhora.com/%E0%B8%AB%E0%B8%A7%E0%B8%A2/%e0%b8%87%e0%b8%a7%e0%b8%94-16-%e0%b8%a1%e0%b8%b4%e0%b8%96%e0%b8%b8%e0%b8%99%e0%b8%b2%e0%b8%a2%e0%b8%99-2564.aspx',
            'https://www.myhora.com/%E0%B8%AB%E0%B8%A7%E0%B8%A2/%e0%b8%87%e0%b8%a7%e0%b8%94-16-%e0%b8%81%e0%b8%a3%e0%b8%81%e0%b8%8e%e0%b8%b2%e0%b8%84%e0%b8%a1-2564.aspx',
            'https://www.myhora.com/%E0%B8%AB%E0%B8%A7%E0%B8%A2/%e0%b8%87%e0%b8%a7%e0%b8%94-1-%e0%b8%81%e0%b8%a3%e0%b8%81%e0%b8%8e%e0%b8%b2%e0%b8%84%e0%b8%a1-2564.aspx',
            'https://www.myhora.com/%E0%B8%AB%E0%B8%A7%E0%B8%A2/%e0%b8%87%e0%b8%a7%e0%b8%94-16-%e0%b8%a1%e0%b8%b4%e0%b8%96%e0%b8%b8%e0%b8%99%e0%b8%b2%e0%b8%a2%e0%b8%99-2564.aspx',
            'https://www.myhora.com/%E0%B8%AB%E0%B8%A7%E0%B8%A2/%e0%b8%87%e0%b8%a7%e0%b8%94-1-%e0%b8%a1%e0%b8%b4%e0%b8%96%e0%b8%b8%e0%b8%99%e0%b8%b2%e0%b8%a2%e0%b8%99-2564.aspx',
            'https://www.myhora.com/%E0%B8%AB%E0%B8%A7%E0%B8%A2/%e0%b8%87%e0%b8%a7%e0%b8%94-16-%e0%b8%9e%e0%b8%a4%e0%b8%a9%e0%b8%a0%e0%b8%b2%e0%b8%84%e0%b8%a1-2564.aspx',
            'https://www.myhora.com/%E0%B8%AB%E0%B8%A7%E0%B8%A2/%e0%b8%87%e0%b8%a7%e0%b8%94-2-%e0%b8%9e%e0%b8%a4%e0%b8%a9%e0%b8%a0%e0%b8%b2%e0%b8%84%e0%b8%a1-2564.aspx',
            'https://www.myhora.com/%E0%B8%AB%E0%B8%A7%E0%B8%A2/%e0%b8%87%e0%b8%a7%e0%b8%94-16-%e0%b9%80%e0%b8%a1%e0%b8%a9%e0%b8%b2%e0%b8%a2%e0%b8%99-2564.aspx',
            'https://www.myhora.com/%E0%B8%AB%E0%B8%A7%E0%B8%A2/%e0%b8%87%e0%b8%a7%e0%b8%94-1-%e0%b9%80%e0%b8%a1%e0%b8%a9%e0%b8%b2%e0%b8%a2%e0%b8%99-2564.aspx',
            'https://www.myhora.com/%E0%B8%AB%E0%B8%A7%E0%B8%A2/%e0%b8%87%e0%b8%a7%e0%b8%94-16-%e0%b8%a1%e0%b8%b5%e0%b8%99%e0%b8%b2%e0%b8%84%e0%b8%a1-2564.aspx',
            'https://www.myhora.com/%E0%B8%AB%E0%B8%A7%E0%B8%A2/%e0%b8%87%e0%b8%a7%e0%b8%94-1-%e0%b8%a1%e0%b8%b5%e0%b8%99%e0%b8%b2%e0%b8%84%e0%b8%a1-2564.aspx',
            'https://www.myhora.com/%E0%B8%AB%E0%B8%A7%E0%B8%A2/%e0%b8%87%e0%b8%a7%e0%b8%94-16-%e0%b8%81%e0%b8%b8%e0%b8%a1%e0%b8%a0%e0%b8%b2%e0%b8%9e%e0%b8%b1%e0%b8%99%e0%b8%98%e0%b9%8c-2564.aspx',
            'https://www.myhora.com/%E0%B8%AB%E0%B8%A7%E0%B8%A2/%e0%b8%87%e0%b8%a7%e0%b8%94-1-%e0%b8%81%e0%b8%b8%e0%b8%a1%e0%b8%a0%e0%b8%b2%e0%b8%9e%e0%b8%b1%e0%b8%99%e0%b8%98%e0%b9%8c-2564.aspx',
            'https://www.myhora.com/%E0%B8%AB%E0%B8%A7%E0%B8%A2/%e0%b8%87%e0%b8%a7%e0%b8%94-17-%e0%b8%a1%e0%b8%81%e0%b8%a3%e0%b8%b2%e0%b8%84%e0%b8%a1-2564.aspx',
            'https://www.myhora.com/%E0%B8%AB%E0%B8%A7%E0%B8%A2/%e0%b8%87%e0%b8%a7%e0%b8%94-30-%e0%b8%98%e0%b8%b1%e0%b8%99%e0%b8%a7%e0%b8%b2%e0%b8%84%e0%b8%a1-2563.aspx',
            'https://www.myhora.com/%E0%B8%AB%E0%B8%A7%E0%B8%A2/%e0%b8%87%e0%b8%a7%e0%b8%94-16-%e0%b8%98%e0%b8%b1%e0%b8%99%e0%b8%a7%e0%b8%b2%e0%b8%84%e0%b8%a1-2563.aspx',
            'https://www.myhora.com/%E0%B8%AB%E0%B8%A7%E0%B8%A2/%e0%b8%87%e0%b8%a7%e0%b8%94-1-%e0%b8%98%e0%b8%b1%e0%b8%99%e0%b8%a7%e0%b8%b2%e0%b8%84%e0%b8%a1-2563.aspx',
            'https://www.myhora.com/%E0%B8%AB%E0%B8%A7%E0%B8%A2/%e0%b8%87%e0%b8%a7%e0%b8%94-16-%e0%b8%9e%e0%b8%a4%e0%b8%a8%e0%b8%88%e0%b8%b4%e0%b8%81%e0%b8%b2%e0%b8%a2%e0%b8%99-2563.aspx',
            'https://www.myhora.com/%E0%B8%AB%E0%B8%A7%E0%B8%A2/%e0%b8%87%e0%b8%a7%e0%b8%94-1-%e0%b8%9e%e0%b8%a4%e0%b8%a8%e0%b8%88%e0%b8%b4%e0%b8%81%e0%b8%b2%e0%b8%a2%e0%b8%99-2563.aspx',
            'https://www.myhora.com/%E0%B8%AB%E0%B8%A7%E0%B8%A2/%e0%b8%87%e0%b8%a7%e0%b8%94-16-%e0%b8%95%e0%b8%b8%e0%b8%a5%e0%b8%b2%e0%b8%84%e0%b8%a1-2563.aspx',
            'https://www.myhora.com/%E0%B8%AB%E0%B8%A7%E0%B8%A2/%e0%b8%87%e0%b8%a7%e0%b8%94-1-%e0%b8%81%e0%b8%b1%e0%b8%99%e0%b8%a2%e0%b8%b2%e0%b8%a2%e0%b8%99-2563.aspx',
            'https://www.myhora.com/%E0%B8%AB%E0%B8%A7%E0%B8%A2/%e0%b8%87%e0%b8%a7%e0%b8%94-16-%e0%b8%95%e0%b8%b8%e0%b8%a5%e0%b8%b2%e0%b8%84%e0%b8%a1-2563.aspx',
            'https://www.myhora.com/%E0%B8%AB%E0%B8%A7%E0%B8%A2/%e0%b8%87%e0%b8%a7%e0%b8%94-1-%e0%b8%95%e0%b8%b8%e0%b8%a5%e0%b8%b2%e0%b8%84%e0%b8%a1-2563.aspx',
            'https://www.myhora.com/%E0%B8%AB%E0%B8%A7%E0%B8%A2/%e0%b8%87%e0%b8%a7%e0%b8%94-16-%e0%b8%81%e0%b8%b1%e0%b8%99%e0%b8%a2%e0%b8%b2%e0%b8%a2%e0%b8%99-2563.aspx',
            'https://www.myhora.com/%E0%B8%AB%E0%B8%A7%E0%B8%A2/%e0%b8%87%e0%b8%a7%e0%b8%94-1-%e0%b8%81%e0%b8%b1%e0%b8%99%e0%b8%a2%e0%b8%b2%e0%b8%a2%e0%b8%99-2563.aspx',
            'https://www.myhora.com/%E0%B8%AB%E0%B8%A7%E0%B8%A2/%e0%b8%87%e0%b8%a7%e0%b8%94-16-%e0%b8%aa%e0%b8%b4%e0%b8%87%e0%b8%ab%e0%b8%b2%e0%b8%84%e0%b8%a1-2563.aspx',
            'https://www.myhora.com/%E0%B8%AB%E0%B8%A7%E0%B8%A2/%e0%b8%87%e0%b8%a7%e0%b8%94-1-%e0%b8%aa%e0%b8%b4%e0%b8%87%e0%b8%ab%e0%b8%b2%e0%b8%84%e0%b8%a1-2563.aspx',
            'https://www.myhora.com/%E0%B8%AB%E0%B8%A7%E0%B8%A2/%e0%b8%87%e0%b8%a7%e0%b8%94-16-%e0%b8%81%e0%b8%a3%e0%b8%81%e0%b8%8e%e0%b8%b2%e0%b8%84%e0%b8%a1-2563.aspx',
            'https://www.myhora.com/%E0%B8%AB%E0%B8%A7%E0%B8%A2/%e0%b8%87%e0%b8%a7%e0%b8%94-1-%e0%b8%81%e0%b8%a3%e0%b8%81%e0%b8%8e%e0%b8%b2%e0%b8%84%e0%b8%a1-2563.aspx',
            'https://www.myhora.com/%E0%B8%AB%E0%B8%A7%E0%B8%A2/%e0%b8%87%e0%b8%a7%e0%b8%94-16-%e0%b8%a1%e0%b8%b4%e0%b8%96%e0%b8%b8%e0%b8%99%e0%b8%b2%e0%b8%a2%e0%b8%99-2563.aspx',
            'https://www.myhora.com/%E0%B8%AB%E0%B8%A7%E0%B8%A2/%e0%b8%87%e0%b8%a7%e0%b8%94-1-%e0%b8%a1%e0%b8%b4%e0%b8%96%e0%b8%b8%e0%b8%99%e0%b8%b2%e0%b8%a2%e0%b8%99-2563.aspx',
            'https://www.myhora.com/%E0%B8%AB%E0%B8%A7%E0%B8%A2/%e0%b8%87%e0%b8%a7%e0%b8%94-1-%e0%b9%80%e0%b8%a1%e0%b8%a9%e0%b8%b2%e0%b8%a2%e0%b8%99-2563.aspx',
            'https://www.myhora.com/%E0%B8%AB%E0%B8%A7%E0%B8%A2/%e0%b8%87%e0%b8%a7%e0%b8%94-16-%e0%b8%a1%e0%b8%b5%e0%b8%99%e0%b8%b2%e0%b8%84%e0%b8%a1-2563.aspx',
            'https://www.myhora.com/%E0%B8%AB%E0%B8%A7%E0%B8%A2/%e0%b8%87%e0%b8%a7%e0%b8%94-1-%e0%b8%a1%e0%b8%b5%e0%b8%99%e0%b8%b2%e0%b8%84%e0%b8%a1-2563.aspx',
            'https://www.myhora.com/%E0%B8%AB%E0%B8%A7%E0%B8%A2/%e0%b8%87%e0%b8%a7%e0%b8%94-16-%e0%b8%81%e0%b8%b8%e0%b8%a1%e0%b8%a0%e0%b8%b2%e0%b8%9e%e0%b8%b1%e0%b8%99%e0%b8%98%e0%b9%8c-2563.aspx',
            'https://www.myhora.com/%E0%B8%AB%E0%B8%A7%E0%B8%A2/%e0%b8%87%e0%b8%a7%e0%b8%94-1-%e0%b8%81%e0%b8%b8%e0%b8%a1%e0%b8%a0%e0%b8%b2%e0%b8%9e%e0%b8%b1%e0%b8%99%e0%b8%98%e0%b9%8c-2563.aspx',
            'https://www.myhora.com/%E0%B8%AB%E0%B8%A7%E0%B8%A2/%e0%b8%87%e0%b8%a7%e0%b8%94-17-%e0%b8%a1%e0%b8%81%e0%b8%a3%e0%b8%b2%e0%b8%84%e0%b8%a1-2563.aspx',
        ]

if __name__ == '__main__':
    WebScraper().run()
