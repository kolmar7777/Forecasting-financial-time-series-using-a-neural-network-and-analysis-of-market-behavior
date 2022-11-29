import pandas as pd

class Data:
    def __init__(
            self,
            df: pd.core.frame.DataFrame,
            key_Ticker_to_predict: str,
            window_size: int = 1,
            is_data_from_file: bool = False
    ):
        self.dates_cutted = list()
        self.is_data_from_file = is_data_from_file
        self.df = df
        self.key_Ticker_to_predict = key_Ticker_to_predict
        self.Our_First_date_which_we_wanna_start = list(df.loc[key_Ticker_to_predict].to_dict()['Adj. Close'])[1]
        self.Tickers_list = list(df.index.levels[0].array)
        self.window_size = 1#window_size
        if (is_data_from_file):
            print("Start loading data from file\n")
            self.Time_series_space = self.create_data_matrix_from_file()
        else:
            self.Time_series_space = self.create_data_matrix_from_correct_tickers()
        self.Key_ticker_values_list = self.create_key_ticker_values_list()


    r'''
            assert self.first_pred > self.window_size
            feat_idx = []
            target_idx = []
            for i in range(self.first_pred, self.series.shape[0], self.step_size):
                feat_idx.append(range(i - self.horizon - self.window_size, i - self.horizon))
                target_idx.append(i)
            self.feat_idx = feat_idx
            self.target_idx = target_idx
    '''

    
    def Find_index_of_first_date_entry(self, dates_list, start_date):#Индекс принадлежности какому-то промежутку дат в списке заданной start_date
        index = -1
        for i in range(len(dates_list) - 1):
            if (dates_list[i] < start_date and dates_list[i+1] >= start_date):
                index = i + 1
        return index

    #Индекс строгого вхождения заданной start_date в список дат
    def Hard_find_index_of_first_date_entry(self, dates_list, start_date):
        index = -1
        for i in range(len(dates_list)):
            if (dates_list[i] == start_date):
                index = i
        return index


    #Проверка идентичности двух списков
    def Check_for_equality_of_two_times_lists(self, first, second):
        if (len(first) != len(second)):
            return -1
        for i in range(len(first) - 1):
            if (first[i] != second[i]):
                return -1
        return 0

    def create_data_matrix_from_correct_tickers(self):
        number_of_ticker = 0
        Time_series_space = [] 
        for ticker in self.Tickers_list: # Идём по всем тикерам из списка
            if ticker == self.key_Ticker_to_predict: # По всем кроме ключевого
                Time_series_space.append(list())
                continue

            number_of_ticker += 1  #Счётчик тикеров
            Current_ticker = list()    #Массив для текущего временного ряда
            dict_for_ticker = self.df.loc[ticker].to_dict()['Adj. Close']  # Словарь Date:Price для текущего тикера
            dates_for_ticker = list(dict_for_ticker)                  # Список всех Dates для текущего тикера
            
            if (number_of_ticker == 1):   #Для первого тикера предыдущий он сам же. Сравниваем с предыдущими для выравнивания рядов по дате.
                dates_for_prev_ticker = dates_for_ticker.copy()
                #print ("1:\n", dates_for_ticker, "2:\n", self.Our_First_date_which_we_wanna_start)
                index_for_prev_ticker = self.Hard_find_index_of_first_date_entry(dates_for_ticker, self.Our_First_date_which_we_wanna_start)
            #print(dates_for_ticker[0])
            #print('Testing:', dates_for_ticker[0], "|", Our_First_date_which_we_wanna_start)

            if(dates_for_ticker[0] < self.Our_First_date_which_we_wanna_start): # На самом деле наша функция дальше вернула бы -1 и это условие не нужно, но для надёжности пусть будет
                index_using_our_func = self.Hard_find_index_of_first_date_entry(dates_for_ticker, self.Our_First_date_which_we_wanna_start)
                #index_using_list_func = Time_series.index(Our_First_date_which_we_wanna_start)
                #print(index_using_our_func, "or = ", index_using_list_func )
                #if(index_using_our_func != index_using_list_func):
                #print("Real start date:", Our_First_date_which_we_wanna_start)
                #print("Our_func_date:", dates_for_ticker[index_using_our_func + 1])
                #print("list_func_date:", dates_for_ticker[index_using_list_func - 1])'''
                if (index_using_our_func != -1 and self.Check_for_equality_of_two_times_lists(dates_for_prev_ticker[index_for_prev_ticker:], dates_for_ticker[index_using_our_func:]) == 0): #Проверяем совпадения по времени текущего тикера и предыдущщего
                    for date in dates_for_ticker[index_using_our_func:]:
                        Current_ticker.append(dict_for_ticker[date])
                r'''if (Current_ticker == []):
                    print(ticker)
                    for date in dates_for_ticker[index_using_our_func:]:
                        Current_ticker.append(dict_for_ticker[date])
                        print(ticker, dict_for_ticker[date], Current_ticker)'''
                Time_series_space.append(Current_ticker)
                dates_for_prev_ticker = dates_for_ticker.copy()
                self.dates_cutted = dates_for_prev_ticker
                index_for_prev_ticker = index_using_our_func
            else:
                Time_series_space.append(list())

            '''Display process'''
            if (number_of_ticker % 10 == 0):
                print(number_of_ticker, 'from', len(self.Tickers_list), 'done', len(Time_series_space))

        self.save_Time_series_space_into_file("./databases/Time_series_space.txt", Time_series_space)
            
        return Time_series_space

    def save_Time_series_space_into_file(self, filename, space):
        with open(r'./databases/Time_series_space.txt', 'w') as fp:
            fp.write("[\n")
            for i, line in enumerate(space):
                # write each item on a new line
                fp.write("%s" % str(line))
                fp.write(",\n")
                
            fp.write("]")
            print('Done')
        
        with open(r'./databases/Time_series_dates.txt', 'w') as fp:
            for item in self.dates_cutted:
                # write each item on a new line
                fp.write("%s\n" % str(item))
            print('Done')


    def create_data_matrix_from_file(self):
        Time_series_space = []
        with open(r'./databases/Time_series_space.txt', 'r') as fp:
            data_string = fp.read().split('\n')[1:-1]#.replace('\n', '')
            for line in data_string:
                if (line == '[],'):
                    Time_series_space.append(list())
                    continue
                list_of_str_line = line[1:-2].split(',')
                list_of_value_line = []
                for item in list_of_str_line:
                    #print(item)
                    #print("str:", item, "float:", float(item))
                    list_of_value_line.append(float(item))

                #print(list_of_value_line)
                Time_series_space.append(list_of_value_line)
            #print(data_string[0])
            #Time_series_space = list(data_string)
            #print(Time_series_space)

        with open(r'./databases/Time_series_dates.txt', 'r') as fp:
            self.dates_cutted = [pd.Timestamp(item) for item in fp.read().split('\n')[:-1]]

        return Time_series_space


    def create_key_ticker_values_list(self):
        Key_ticker_values_dict = self.df.loc[self.key_Ticker_to_predict].to_dict()['Open']
        Key_ticker_values_list = []
        #print(list(Key_ticker_values_dict), "|", self.dates_cutted )
        if (self.Check_for_equality_of_two_times_lists(list(Key_ticker_values_dict), self.dates_cutted) == 0):
            for date in list(Key_ticker_values_dict)[2:]:
                Key_ticker_values_list.append(Key_ticker_values_dict[date])
        print("labels for the key data with window:\n", Key_ticker_values_list)
        return Key_ticker_values_list

    r'''
    def __len__(self):
        return len(self.feat_idx)

    def __iter__(self):
        self.iter = 0
        return self

    def __next__(self):
        if self.iter < len(self.feat_idx):
            feat = self.series.iloc[self.feat_idx[self.iter]]
            target = self.series.iloc[self.target_idx[self.iter]]
            self.iter += 1
            return feat, target
        else:
            raise StopIteration
    '''
