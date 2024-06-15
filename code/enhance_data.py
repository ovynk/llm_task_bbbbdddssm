import pandas as pd


def enhance_data(excel_path, save_to):
    """
    Creates txt file with filtered and structured data.
    File must have columns as merged_data_test_task.xlsx.
    """

    df = pd.read_excel(excel_path)

    selected_columns = ['Partner', 'Brand', 'Model', 'full price of car, euro',
                        'if 1-3 days\\ euro per day', 'Locations', 'Contact person', 'link', 'Company details']

    renamed_cols_dict = {'Partner': 'Seller',
                         'full price of car, euro': 'price of car in euro',
                         'if 1-3 days\\ euro per day': 'rent price for 1-3 days'}

    # filtering, cleaning, sorting data
    processed = df[selected_columns]
    processed.rename(columns=renamed_cols_dict, inplace=True)

    processed.fillna({"price of car in euro": -1.0, "rent price for 1-3 days": -1}, inplace=True)
    processed.fillna('No data', inplace=True)

    processed['price of car in euro'] = processed['price of car in euro'].astype(int)

    processed.sort_values(['Seller', 'price of car in euro'], ascending=[True, True], inplace=True)

    # processing all data in one string with specific structure
    # so that model can better understand data (than pure pd.DataFrame)
    sting_data = ''
    last_seller = ''
    car_i = 0
    for i, r in processed.iterrows():
        if last_seller != r['Seller']:
            last_seller = r['Seller']
            car_i = 0

            link = r['link'].replace('\n', ', ').strip()
            locations = r['Locations'].replace('\n', ', ').strip()
            contacts = r['Contact person'].replace('\n', ', ').strip()
            company_details = r['Company details'].replace('\n', ', ').strip()

            sting_data += f"]\nSeller {last_seller}:[ locations where can buy cars:'{locations}', " \
                          f"seller contacts:'{contacts}', " \
                          f"links:'{link}', company details:'{company_details}', "

        car_i += 1
        brand = r['Brand']
        model = r['Model']
        price = r['price of car in euro']
        rent_price = r['rent price for 1-3 days']

        sting_data += f'car {car_i}, brand:{brand}, model:{model}, price in euro:{price}, ' \
                      f'rent price for 1-3 days:{rent_price} ; '

    # save
    with open(save_to+'enhanced_data.txt', 'w', errors='replace') as text_file:  # some chars not utf-8
        text_file.write(sting_data)
