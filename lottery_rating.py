from pprint import pprint
import copy
import pandas as pd


class LotteryRater:

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

    def setup(self):
        self.fstp_data = self.read_data("FirstPrize", 6)
        self.head_3_data = self.read_data("ThreeDigitPrefix", 3)
        self.tail_3_data = self.read_data("ThreeDigitSuffix", 3)
        self.tail_2_data = self.read_data("TwoDigitSuffix", 2)
        self.fstp_neighbor_data = self.read_data("FirstPrizeNeighbors", 6)
        self.sndp_data = self.read_data("SecondPrize", 6)
        self.trdp_data = self.read_data("ThirdPrize", 6)
        self.fourthp_data = self.read_data("FourthPrize", 6)
        self.fifthp_data = self.read_data("FifthPrize", 6)

    def run(self):
        self.setup()
        stat = self.get_prize_stat()
        # pprint(stat)
        print(self.get_valuest_lottery_number(stat))
    
    @staticmethod
    def get_valuest_lottery_number(stat: dict) -> str:
        rating = stat['rating']
        lottery_number = [digit[0][0] for digit in rating]
        return "".join(lottery_number)

    @staticmethod
    def read_data(filename: str, ndigit: int) -> list:
        file_path = f"datas/{filename}.csv"
        df = pd.read_csv(file_path, dtype=str)
        df[filename] = pd.to_numeric(df[filename], errors='coerce')
        df = df.dropna()
        df[filename] = df[filename].astype(int).astype(str).str.zfill(ndigit)
        return df[filename].values.tolist()

    @staticmethod
    def count_numbers(num_strs: list) -> list:
        num_counts = [0 for _ in range(10)]
        for num_str in num_strs:
            for num_char in num_str:
                num_counts[int(num_char)] += 1
        
        return num_counts

    @staticmethod
    def rate_digits(prize_price: int, stat: list, rating=[]) -> list:
        if not rating:
            rating = copy.deepcopy(stat)

        for idx, digit_stat in enumerate(stat):
            for num_key, num_count in digit_stat.items():
                rating[idx][num_key] += prize_price * num_count

        return rating

    @staticmethod
    def get_initial_num_dict():
        return {'0': 0, '1': 0, '2': 0, '3': 0,
                '4': 0, '5': 0, '6': 0, '7': 0,
                '8': 0, '9': 0,}

    def get_initial_stat(self, ndigit: int) -> list:
        return [self.get_initial_num_dict() for _ in range(ndigit)]

    def count_ndigit_stat(self, ndigit: int, num_strs: list) -> list:
        stat = self.get_initial_stat(ndigit)
        for num_str in num_strs:
            for idx in range(ndigit):
                value = num_str[idx]
                if stat[idx].get(value, ''):
                    stat[idx][value] += 1
                else:
                    stat[idx][value] = 1

        return stat

    @staticmethod
    def sort_list_of_dict(list_of_dict: list) -> list:
        for idx, digit_stat in enumerate(list_of_dict):
            list_of_dict[idx] = sorted(digit_stat.items(), key=lambda x:x[1], reverse=True)
        
        return list_of_dict
        
    def get_prize_stat(self) -> dict:
        all_prize_data = self.fstp_data + self.head_3_data + self.tail_3_data + \
                         self.tail_2_data + self.fstp_neighbor_data + self.sndp_data + \
                         self.trdp_data + self.fourthp_data + self.fifthp_data
        count = {
            'fstp_count': self.count_numbers(self.fstp_data),
            'head_3_count': self.count_numbers(self.head_3_data),
            'tail_3_count': self.count_numbers(self.tail_3_data),
            'tail_2_count': self.count_numbers(self.tail_2_data),
            'fstp_neighbor_count': self.count_numbers(self.fstp_neighbor_data),
            'sndp_count': self.count_numbers(self.sndp_data),
            'trdp_count': self.count_numbers(self.trdp_data),
            'fourthp_count': self.count_numbers(self.fourthp_data),
            'fifthp_count': self.count_numbers(self.fifthp_data),
            'all_prize_count': self.count_numbers(all_prize_data),
        }

        fstp_stat = self.count_ndigit_stat(6, self.fstp_data)
        head_3_stat = self.count_ndigit_stat(3, self.head_3_data)
        tail_3_stat = self.count_ndigit_stat(3, self.tail_3_data)
        tail_2_stat = self.count_ndigit_stat(2, self.tail_2_data)
        fstp_neighbor_stat = self.count_ndigit_stat(6, self.fstp_neighbor_data)
        sndp_stat = self.count_ndigit_stat(6, self.sndp_data)
        trdp_stat = self.count_ndigit_stat(6, self.trdp_data)
        fourthp_stat = self.count_ndigit_stat(6, self.fourthp_data)
        fifthp_stat = self.count_ndigit_stat(6, self.fifthp_data)

        rating = self.rate_digits(6000000, fstp_stat)
        rating = self.rate_digits(4000, head_3_stat, rating)
        rating = self.rate_digits(4000, tail_3_stat, rating)
        rating = self.rate_digits(2000, tail_2_stat, rating)

        rating = self.rate_digits(100000, fstp_neighbor_stat, rating)
        rating = self.rate_digits(200000, sndp_stat, rating)
        rating = self.rate_digits(80000, trdp_stat, rating)
        rating = self.rate_digits(40000, fourthp_stat, rating)
        rating = self.rate_digits(20000, fifthp_stat, rating)

        return {
            'fstp_stat': self.sort_list_of_dict(fstp_stat),
            'head_3_stat': self.sort_list_of_dict(head_3_stat),
            'tail_3_stat': self.sort_list_of_dict(tail_3_stat),
            'tail_2_stat': self.sort_list_of_dict(tail_2_stat),
            'fstp_neighbor_stat': self.sort_list_of_dict(fstp_neighbor_stat),
            'sndp_stat': self.sort_list_of_dict(sndp_stat),
            'trdp_stat': self.sort_list_of_dict(trdp_stat),
            'fourthp_stat': self.sort_list_of_dict(fourthp_stat),
            'fifthp_stat': self.sort_list_of_dict(fifthp_stat),
            **count,
            'rating': self.sort_list_of_dict(rating)
        }

if __name__ == '__main__':
    LotteryRater().run()
