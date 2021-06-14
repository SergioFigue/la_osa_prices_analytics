import pandas as pd
import scraping as scr


def acquire_current_df():
    data = pd.read_csv('./data/main_prices_list.csv')
    print(f'Current prices retrieved')
    return data


def main():
    data = acquire_current_df()
    osa_new_prices = scr.updating_osa()
    dia_new_prices = scr.updating_dia()
    eroski_new_prices = scr.updating_eroski()
    alcampo_new_prices = scr.updating_alcampo()
    navarro_new_prices = scr.updating_navarro()
    carrefour_new_prices = scr.updating_carrefour()
    up_to_date_df = data.append([osa_new_prices, dia_new_prices, eroski_new_prices, alcampo_new_prices,
                                navarro_new_prices, carrefour_new_prices])

    print(up_to_date_df)
    return up_to_date_df.to_csv('./data/main_prices_list.csv', index=False)


if __name__ == '__main__':
    main()
