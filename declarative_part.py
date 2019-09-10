from queue import Queue
from concurrent.futures import ThreadPoolExecutor, as_completed


class Client:
    def __init__(self, name, phone_number, balance):
        self.name = name
        self.phone_number = phone_number
        self.balance = balance
        if self.balance < 0:
            self.debt = self.balance
        else:
            self.debt = 0
        self.condition = None
        self.service = True

    def __str__(self):
        s = "Имя: " + self.name + "\n"
        s += "Телефон: " + self.phone_number + "\n"
        s += "Баланс: " + str(self.balance) + "\n"
        if self.balance < 0:
            s += "Сумма задолженности: " + str(self.debt) + " руб." + "\n"
        else:
            s += "Задолженность отсутствует. " + "\n"
        return s

    def __repr__(self):
        return self.__str__()

    def check_balance(self):
        if self.balance > 0:
            return self.__str__() + self.ok()
        elif self.balance < -200:
            return self.__str__() + self.call()
        elif self.balance <= -100:
            return self.__str__() + self.message2()
        elif self.balance == 0:
            return self.__str__() + self.message1()


    def ok(self):
        self.condition = "OK"
        return "\nОповещение: \nПоложительный баланс" + "\n"

    @staticmethod
    def message1():
        message = "\nОповещение: \nУважаемый абонент! На Вашем балансе 0 руб. Пополните счет и оставайтесь на связи!"
        return message + "\n"

    def message2(self):
        self.service = False
        message = "\nОповещение: \nУважаемый абонент! На Вашем балансе меньше -100 руб. " \
                  "Временно приостановлена передача пакета услуг. Пополните баланс и оставайтесь на связи!"
        return message + "\n"

    def call(self):
        self.service = False
        woman_voice = "\nОповещение: \nЗдравствуйте! Вас приветствует Ваш сотовый оператор." \
                " В данный момент на вашем счете " + str(self.debt) + " рублей." \
                "\nВ связи с этим услуги, предоставляемые Вам временно приостановленны." \
                " Пополните счет и оставайтесь на связи!"
        return woman_voice + "\n"


class ProcessRunner:
    @staticmethod
    def read(indicator, p):
        clients_base = []
        with open("file.txt", "r") as file:
            for i in range(1000000):
                c = file.readline().strip()
                phone_number = c[:16]
                name = c[16:-4]
                balance = c[-4:]
                try:
                    balance = int(balance)
                except ValueError:
                    balance = balance[2:]
                    balance = int(balance)
                client = Client(name, phone_number, balance)
                clients_base.append(client)
            if indicator == 1:
                p.first_process(clients_base)
            elif indicator == 2:
                q = Queue()
                for c in clients_base:
                    q.put(c)

                q.put(None)
                q.put(None)
                q.put(None)

                with ThreadPoolExecutor(max_workers=3) as pool:
                    results = [pool.submit(p.second_process(q))]
            else:
                p.third_process(clients_base)

    @staticmethod
    def first_process(clients_base):
        for client in clients_base:
            client.check_balance()

    @staticmethod
    def second_process(q):
        for i in range(1000):
            if q.get() is None:
                break
            else:
                client = q.get()
                client.check_balance()

    @staticmethod
    def third_process(clients_base):
        pass







