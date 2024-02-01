from datetime import datetime, timedelta
from postman import generate_dictionary, generate_csv
from traceback import format_exc


days_difference = (datetime.now() - datetime(1949, 11, 1)).days
start_date = datetime.strptime('11/01/1949', '%m/%d/%Y')
matches = []
for i in range(days_difference):
    current_date = start_date + timedelta(days=i)
    formatted_date = current_date.strftime('%m/%d/%Y')
    api_endpoint = f'https://core-api.nba.com/cp/api/v1.3/feeds/gamecardfeed?gamedate={formatted_date}&platform=web'
    print(formatted_date)
    try:
        matches.extend(generate_dictionary(api_endpoint))
    except:
        print(format_exc())
    generate_csv(matches)
generate_csv(matches)